"""Temporal linear-SHAP analysis for the selected RQ2 Ridge models."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.linear_model import Ridge

from rq2_module_model_audit import (
    BASE_NUMERIC,
    CATEGORICAL,
    MODULE_COLUMNS,
    OUT as AUDIT_OUT,
    TEST_PATH,
    TRAIN_PATH,
    clean_data,
    make_pipeline,
    numeric_features,
)


OUT = AUDIT_OUT / "linear_shap"


def feature_family(feature_name):
    name = feature_name.split("__", 1)[-1]
    if "missingindicator" in name:
        name = name.rsplit("_", 1)[-1]
    if name in BASE_NUMERIC:
        return "Pre-academic"
    if name in MODULE_COLUMNS:
        return "Module grade"
    if name.startswith("S") and name[1:].isdigit():
        return "Semester GPA"
    if any(name == column or name.startswith(f"{column}_") for column in CATEGORICAL):
        return "Demographic"
    return "Other"


def tidy_feature_name(feature_name):
    name = feature_name.replace("numeric__", "").replace("categorical__", "")
    return name.replace("missingindicator_", "Missing: ")


def plot_family_heatmap(family_results):
    matrix = family_results.pivot(index="family", columns="semester", values="mean_abs_shap")
    order = ["Pre-academic", "Demographic", "Semester GPA", "Module grade", "Other"]
    matrix = matrix.reindex([name for name in order if name in matrix.index])
    fig, ax = plt.subplots(figsize=(9, 4.5))
    image = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(matrix.columns)), matrix.columns)
    ax.set_yticks(range(len(matrix.index)), matrix.index)
    ax.set(xlabel="Information available through semester", ylabel="Feature family")
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            ax.text(column, row, f"{matrix.iloc[row, column]:.3f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, label="Mean |SHAP value| (GPA points)")
    fig.tight_layout()
    fig.savefig(OUT / "linear_shap_family_heatmap.png", dpi=300)
    plt.close(fig)


def plot_top_features(feature_results):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for axis, semester in zip(axes.flat, range(1, 7)):
        subset = feature_results[feature_results["semester"] == semester].nlargest(10, "mean_abs_shap").sort_values("mean_abs_shap")
        colours = subset["family"].map({"Pre-academic": "#4C78A8", "Demographic": "#72B7B2", "Semester GPA": "#F58518", "Module grade": "#E45756", "Other": "#999999"})
        axis.barh(subset["feature"], subset["mean_abs_shap"], color=colours)
        axis.set_title(f"Through semester {semester}")
        axis.set_xlabel("Mean |SHAP| (GPA points)")
    fig.suptitle("Top external-cohort feature contributions by temporal model", y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / "linear_shap_top_features_by_semester.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def run_checkpoint(train, test, semester):
    numeric = numeric_features(semester)
    features = numeric + CATEGORICAL
    pipeline = make_pipeline(Ridge(alpha=1.0), numeric)
    pipeline.fit(train[features], train["FinalGPA"])
    transformed_train = pipeline.named_steps["preprocessor"].transform(train[features])
    transformed_test = pipeline.named_steps["preprocessor"].transform(test[features])
    names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    background = shap.maskers.Independent(transformed_train, max_samples=min(100, len(train)))
    explainer = shap.LinearExplainer(pipeline.named_steps["model"], background)
    values = explainer(transformed_test)
    values.feature_names = list(names)
    importance = pd.DataFrame({
        "feature": [tidy_feature_name(name) for name in names],
        "raw_feature": names,
        "mean_abs_shap": np.abs(values.values).mean(axis=0),
        "mean_shap": values.values.mean(axis=0),
    })
    importance["semester"] = semester
    importance["family"] = importance["raw_feature"].map(feature_family)
    family_rows = []
    for family in importance["family"].unique():
        positions = np.flatnonzero(importance["family"].to_numpy() == family)
        combined_contribution = values.values[:, positions].sum(axis=1)
        family_rows.append({
            "semester": semester,
            "family": family,
            "mean_abs_shap": np.abs(combined_contribution).mean(),
            "mean_shap": combined_contribution.mean(),
        })
    # Two complementary plots: ranking (magnitude) and beeswarm (direction).
    plt.figure()
    shap.plots.beeswarm(values, max_display=15, show=False)
    plt.title(f"Linear SHAP on the external 2019 cohort: through semester {semester}")
    plt.tight_layout()
    plt.savefig(OUT / f"linear_shap_beeswarm_s{semester}.png", dpi=300, bbox_inches="tight")
    plt.close()
    return importance, pd.DataFrame(family_rows), values, transformed_test, names


def module_dependence_plot(importance, values, transformed_test, names, semester):
    candidates = importance[
        (importance["family"] == "Module grade")
        & (importance["semester"] == semester)
        & ~importance["feature"].str.startswith("Missing:")
    ]
    if candidates.empty:
        return None
    selected = candidates.nlargest(1, "mean_abs_shap").iloc[0]
    position = list(names).index(selected["raw_feature"])
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.scatter(transformed_test[:, position], values.values[:, position], alpha=0.75)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set(
        xlabel=f"Standardised {selected['feature']}",
        ylabel=f"SHAP contribution of {selected['feature']} (GPA points)",
        title=f"Module signal at semester {semester}",
    )
    fig.tight_layout()
    safe_name = "".join(character if character.isalnum() else "_" for character in selected["feature"])
    filename = f"linear_shap_module_dependence_s{semester}_{safe_name}.png"
    fig.savefig(OUT / filename, dpi=300)
    plt.close(fig)
    return selected["feature"]


def write_report(feature_results, family_results, dependence_features):
    module_start = feature_results[(feature_results["semester"] == 2) & (feature_results["family"] == "Module grade")].nlargest(3, "mean_abs_shap")
    sem3_modules = feature_results[(feature_results["semester"] == 3) & (feature_results["family"] == "Module grade")].nlargest(3, "mean_abs_shap")
    lines = [
        "# RQ2 temporal linear-SHAP analysis",
        "",
        "## Method",
        "",
        "Ridge was selected in the pre-SHAP model audit. For each checkpoint S0–S6, the model is trained on all 2017–2018 module-data records and explained on the untouched 2019 cohort with `shap.LinearExplainer`. The SHAP background is a capped (n ≤ 100) training-cohort sample. This explains external predictions rather than in-sample fits.",
        "",
        "All preprocessing is fitted on the training cohort only. Therefore, SHAP values are in final-GPA points after the same leakage-safe imputation, scaling, and encoding used during model evaluation.",
        "",
        "## How to read the outputs",
        "",
        "- `mean_abs_shap` measures a feature’s average contribution magnitude; use it for importance.",
        "- `mean_shap` is directional only for this 2019 cohort; it should not be interpreted as a causal effect.",
        "- The family heatmap compares pre-academic, demographic, semester-GPA, and module-grade contribution over time. It is the primary RQ2 temporal figure.",
        "- Beeswarm plots show whether higher/lower values tend to increase or decrease a prediction. Module dependence plots are descriptive checks of the strongest available module at each early checkpoint.",
        "",
        "## Early module signals",
        "",
        "At S2, the leading module-grade features are: " + "; ".join(f"{row.feature} (mean |SHAP| = {row.mean_abs_shap:.3f})" for row in module_start.itertuples()) + ".",
        "",
        "At S3, the leading module-grade features are: " + "; ".join(f"{row.feature} (mean |SHAP| = {row.mean_abs_shap:.3f})" for row in sem3_modules.itertuples()) + ".",
        "",
        "## Interpretation guardrails",
        "",
        "Semester GPA and module grades are correlated. SHAP distributes model attribution among correlated predictors according to the chosen training-background distribution; it does not establish that a module causes a later GPA outcome. The findings should be framed as early academic signals that help explain model behaviour and support advisor review, not automated intervention decisions.",
        "",
        "## Generated artefacts",
        "",
        "- `linear_shap_feature_importance.csv`: feature-level signed and absolute SHAP values by checkpoint.",
        "- `linear_shap_family_importance.csv`: grouped temporal importance for the paper’s main heatmap.",
        "- `linear_shap_family_heatmap.png`, `linear_shap_top_features_by_semester.png`, and checkpoint beeswarms.",
        "- Early-module dependence plots for: " + ", ".join(dependence_features) + ".",
    ]
    (OUT / "RQ2_linear_SHAP_interpretation.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = clean_data(TRAIN_PATH), clean_data(TEST_PATH)
    feature_frames, family_frames, dependence_features = [], [], []
    for semester in range(7):
        importance, family_importance, values, transformed_test, names = run_checkpoint(train, test, semester)
        feature_frames.append(importance)
        family_frames.append(family_importance)
        if semester in (2, 3, 4):
            selected = module_dependence_plot(importance, values, transformed_test, names, semester)
            if selected:
                dependence_features.append(f"S{semester}: {selected}")
    feature_results = pd.concat(feature_frames, ignore_index=True)
    family_results = pd.concat(family_frames, ignore_index=True)
    feature_results.to_csv(OUT / "linear_shap_feature_importance.csv", index=False)
    family_results.to_csv(OUT / "linear_shap_family_importance.csv", index=False)
    plot_family_heatmap(family_results)
    plot_top_features(feature_results)
    write_report(feature_results, family_results, dependence_features)
    print("Completed temporal linear-SHAP analysis.")


if __name__ == "__main__":
    main()
