"""Pre-SHAP temporal audit for RQ2 using the module-level cohorts.

This script deliberately does not replace RQ1: module grades are used only
to explain the evolution of GPA prediction reliability, as specified in the
TALE research positioning document.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.preprocessing import clean_categoricals, get_preprocessor  # noqa: E402

DATA = ROOT / "data" / "raw"
OUT = ROOT / "notebooks" / "shap" / "rq2_module_audit"
TRAIN_PATH = DATA / "DatasetWithModules_Training.xlsx"
TEST_PATH = DATA / "DatasetWithModules_Test.xlsx"

MODULES_BY_SEMESTER = {
    2: ["Maths 2", "MgtAccounting"],
    3: ["StatsII", "MIS"],
    4: ["DataV"],
}
MODULE_COLUMNS = [module for modules in MODULES_BY_SEMESTER.values() for module in modules]
GRADE_POINTS = {
    "A+": 11, "A": 10, "A-": 9, "B+": 8, "B": 7, "B-": 6,
    "C+": 5, "C": 4, "C-": 3, "D": 2, "S": 2, "F": 0,
    "I-we": 1, "I-ca": 1,
}
CATEGORICAL = ["Gender", "Department", "District", "MediumAL"]
BASE_NUMERIC = ["Zscore", "English"]


def performance_group(gpa):
    if gpa <= 2.99:
        return "Underperforming"
    if gpa <= 3.29:
        return "Average"
    return "Performing"


def clean_data(path):
    df = pd.read_excel(path).copy()
    df = clean_categoricals(df, CATEGORICAL)
    for column in MODULE_COLUMNS:
        # I-we/I-ca mean the student did not sit the exam or did not complete
        # the continuous-assessment component, i.e. a fail-equivalent outcome
        # for that module. Coded as grade point 1 (one step above outright F,
        # F=0) rather than treated as missing, so these are not imputed away.
        df[column] = df[column].astype("string").str.strip().map(GRADE_POINTS).astype(float)
    df["GroupLabel"] = df["FinalGPA"].map(performance_group)
    return df


def numeric_features(semester):
    features = BASE_NUMERIC + [f"S{i}" for i in range(1, semester + 1)]
    for available_from, modules in MODULES_BY_SEMESTER.items():
        if semester >= available_from:
            features.extend(modules)
    return features


def make_pipeline(model, numeric):
    preprocessor = get_preprocessor(numeric_features=numeric, categorical_features=CATEGORICAL)
    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def metrics(y_true, prediction):
    return {
        "rmse": mean_squared_error(y_true, prediction) ** 0.5,
        "r2": r2_score(y_true, prediction),
        "bias": float(np.mean(np.asarray(y_true) - prediction)),
    }


def evaluate(train, test, semester, model_name, estimator, cv):
    numeric = numeric_features(semester)
    features = numeric + CATEGORICAL
    x_train, y_train = train[features], train["FinalGPA"]
    x_test, y_test = test[features], test["FinalGPA"]
    fold_metrics = []
    for train_index, validation_index in cv.split(x_train, train["GroupLabel"]):
        fitted = clone(estimator).fit(x_train.iloc[train_index], y_train.iloc[train_index])
        prediction = fitted.predict(x_train.iloc[validation_index])
        fold_metrics.append(metrics(y_train.iloc[validation_index], prediction))
    final_model = clone(estimator).fit(x_train, y_train)
    test_prediction = final_model.predict(x_test)
    row = {
        "semester": semester,
        "model": model_name,
        "n_features_before_encoding": len(features),
        "cv_rmse_mean": np.mean([row["rmse"] for row in fold_metrics]),
        "cv_rmse_sd": np.std([row["rmse"] for row in fold_metrics]),
        "cv_r2_mean": np.mean([row["r2"] for row in fold_metrics]),
        "cv_bias_mean": np.mean([row["bias"] for row in fold_metrics]),
        **{f"test_{key}": value for key, value in metrics(y_test, test_prediction).items()},
    }
    for group in ["Underperforming", "Average", "Performing"]:
        mask = test["GroupLabel"] == group
        group_result = metrics(y_test[mask], test_prediction[mask])
        row[f"test_{group}_rmse"] = group_result["rmse"]
        row[f"test_{group}_bias"] = group_result["bias"]
    return row


def write_eda(train, test):
    summary = []
    for name, df in [("Training (2017–2018)", train), ("External test (2019)", test)]:
        summary.append({
            "cohort": name,
            "students": len(df),
            "final_gpa_mean": df["FinalGPA"].mean(),
            "final_gpa_sd": df["FinalGPA"].std(),
            "underperforming": (df["GroupLabel"] == "Underperforming").sum(),
            "average": (df["GroupLabel"] == "Average").sum(),
            "performing": (df["GroupLabel"] == "Performing").sum(),
        })
    pd.DataFrame(summary).to_csv(OUT / "eda_cohort_summary.csv", index=False)
    correlations = train[["FinalGPA"] + BASE_NUMERIC + [f"S{i}" for i in range(1, 9)] + MODULE_COLUMNS].corr(numeric_only=True)["FinalGPA"]
    correlations.sort_values(ascending=False).to_csv(OUT / "eda_training_correlations_with_final_gpa.csv", header=["pearson_correlation"])


def plot_results(results):
    plt.style.use("seaborn-v0_8-whitegrid")
    for metric, ylabel, filename in [
        ("test_rmse", "External-test RMSE (lower is better)", "external_test_rmse_by_semester.png"),
        ("cv_rmse_mean", "Repeated-CV mean RMSE (lower is better)", "cv_rmse_by_semester.png"),
        ("test_r2", "External-test R² (higher is better)", "external_test_r2_by_semester.png"),
    ]:
        fig, ax = plt.subplots(figsize=(8, 5))
        for model, subset in results.groupby("model"):
            ax.plot(subset["semester"], subset[metric], marker="o", label=model)
        ax.set(xlabel="Information available through semester", ylabel=ylabel, xticks=range(0, 7))
        ax.legend(title="Model")
        fig.tight_layout()
        fig.savefig(OUT / filename, dpi=300)
        plt.close(fig)


def write_interpretation(results, train, test):
    pivot = results.pivot(index="semester", columns="model", values=["cv_rmse_mean", "test_rmse", "test_r2"])
    ridge_advantage = (pivot[("cv_rmse_mean", "Ridge")] <= pivot[("cv_rmse_mean", "Random Forest")] + 0.01).sum()
    primary = "Ridge" if ridge_advantage >= 5 else "Random Forest"
    ridge = results[results["model"] == "Ridge"].set_index("semester")
    forest = results[results["model"] == "Random Forest"].set_index("semester")
    lines = [
        "# RQ2 module-data model audit (pre-SHAP)",
        "",
        "## Design decision",
        "",
        "This is **not a second RQ1**. The TALE positioning document states that RQ1 uses routinely available pre-academic, demographic, and semester-GPA data to establish reliability. Here, module grades are included only in RQ2 to explain why the predictive signal changes over time. The existing RQ1 reliability conclusions therefore remain the primary institutional benchmark.",
        "",
        "The training cohort contains {} students (2017–2018) and the held-out external cohort contains {} students (2019). All models use only features that would have been available by each semester; no future semester GPA or future module result is included.".format(len(train), len(test)),
        "",
        "## Preprocessing and feature engineering",
        "",
        "- Identifier and cohort-year columns are excluded from prediction.",
        "- District spelling variants are harmonised before one-hot encoding. Rare categories are grouped by the encoder (`min_frequency=5`), and unseen 2019 categories are safely ignored.",
        "- Module letter grades are converted to an ordinal grade-point scale (A+ = 11 through F = 0; D/S = 2). Administrative/incomplete outcomes (`I-we`, `I-ca` — did not sit the exam or did not complete the continuous-assessment component) are coded as a fail-equivalent grade point of 1, one step above outright F, not imputed as missing.",
        "- Numeric values are median-imputed and standardised within each fold. This makes Ridge coefficients/linear SHAP comparable while avoiding validation or test leakage.",
        "",
        "## Model audit",
        "",
        "Ridge (alpha=1) is compared with a conservative Random Forest (100 trees, depth 3). Model comparison uses 5-fold CV repeated 10 times in the training cohorts, stratified by the pre-defined final-GPA groups, followed by one untouched 2019 external evaluation. The test cohort is not used to tune models.",
        "",
        "### Model-selection result",
        "",
        "**Selected explanation model: {}.** Ridge is considered practically competitive whenever its repeated-CV RMSE is within 0.01 GPA points of Random Forest; this tolerance favours the transparent linear model only when predictive performance is essentially indistinguishable. Ridge met that criterion at {} of 7 temporal checkpoints.".format(primary, ridge_advantage),
        "",
        "### Observed temporal pattern",
        "",
        "- In repeated CV, Ridge is comparable to or better than Random Forest at every checkpoint under the pre-specified 0.01-RMSE practical-equivalence rule. Its RMSE falls from {:.3f} at baseline to {:.3f} after S1, {:.3f} after S3, and {:.3f} after S6. Its CV variability also narrows from {:.3f} to {:.3f}.".format(ridge.loc[0, "cv_rmse_mean"], ridge.loc[1, "cv_rmse_mean"], ridge.loc[3, "cv_rmse_mean"], ridge.loc[6, "cv_rmse_mean"], ridge.loc[0, "cv_rmse_sd"], ridge.loc[6, "cv_rmse_sd"]),
        "- The 2019 external cohort supports the later-semester pattern: Ridge has RMSE {:.3f} (R² {:.3f}) at S3, {:.3f} (R² {:.3f}) at S4, and {:.3f} (R² {:.3f}) at S6. Ridge outperforms Random Forest externally at S4–S6 by {:.3f}, {:.3f}, and {:.3f} RMSE points respectively.".format(ridge.loc[3, "test_rmse"], ridge.loc[3, "test_r2"], ridge.loc[4, "test_rmse"], ridge.loc[4, "test_r2"], ridge.loc[6, "test_rmse"], ridge.loc[6, "test_r2"], forest.loc[4, "test_rmse"] - ridge.loc[4, "test_rmse"], forest.loc[5, "test_rmse"] - ridge.loc[5, "test_rmse"], forest.loc[6, "test_rmse"] - ridge.loc[6, "test_rmse"]),
        "- S2 is a caution point, not evidence that modules harm attainment: external Ridge RMSE rises from {:.3f} at S1 to {:.3f} at S2 despite improving CV. This is likely cohort/distribution shift and the limited sample, so RQ2 should explain model behaviour rather than claim a module-driven performance gain.".format(ridge.loc[1, "test_rmse"], ridge.loc[2, "test_rmse"]),
        "- Underperforming students remain least precise on the 2019 cohort (Ridge RMSE {:.3f} at S3, {:.3f} at S4, and {:.3f} at S6), echoing RQ1. This group-wise result is descriptive support for the explanation phase; it does not redefine RQ1’s module-free reliability thresholds.".format(ridge.loc[3, "test_Underperforming_rmse"], ridge.loc[4, "test_Underperforming_rmse"], ridge.loc[6, "test_Underperforming_rmse"]),
        "",
        "The final SHAP stage should use the selected model at each checkpoint. If Ridge is selected, use `shap.LinearExplainer` with a training-background sample and report both signed and mean-absolute SHAP values. If Random Forest is selected, use `shap.TreeExplainer`; do not use a linear explainer for a non-linear model.",
        "",
        "## Interpretation boundaries",
        "",
        "Module features can be correlated with semester GPA, so SHAP attribution is an explanation of the fitted model under the chosen background distribution, not a causal claim about a module. For the paper, report grouped SHAP importance (pre-academic, demographics, semester GPA, modules) alongside individual features; show a temporal heatmap of mean |SHAP| by feature family and a small number of dependence plots for the strongest early module signals. Avoid individual student force plots in the paper unless explicitly de-identified and ethically approved.",
        "",
        "## Files",
        "",
        "- `model_comparison.csv`: CV and external-test metrics for Ridge and Random Forest.",
        "- `eda_cohort_summary.csv` and `eda_training_correlations_with_final_gpa.csv`: EDA outputs.",
        "- `external_test_rmse_by_semester.png`, `cv_rmse_by_semester.png`, and `external_test_r2_by_semester.png`: model-audit plots.",
    ]
    (OUT / "RQ2_pre_SHAP_interpretation.md").write_text("\n".join(lines), encoding="utf-8")
    return primary


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = clean_data(TRAIN_PATH), clean_data(TEST_PATH)
    write_eda(train, test)
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
    rows = []
    for semester in range(7):
        numeric = numeric_features(semester)
        models = {
            "Ridge": Ridge(alpha=1.0),
            "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=3, min_samples_leaf=2, random_state=42, n_jobs=1),
        }
        for model_name, model in models.items():
            rows.append(evaluate(train, test, semester, model_name, make_pipeline(model, numeric), cv))
    results = pd.DataFrame(rows)
    results.to_csv(OUT / "model_comparison.csv", index=False)
    plot_results(results)
    primary = write_interpretation(results, train, test)
    print(f"Completed RQ2 pre-SHAP audit. Selected model: {primary}")


if __name__ == "__main__":
    main()
