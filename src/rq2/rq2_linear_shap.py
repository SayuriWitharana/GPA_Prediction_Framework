"""Temporal linear-SHAP analysis for the selected RQ2 Ridge models.

Primary explanations are leakage-safe out-of-fold SHAP values on the
2017-2018 training cohort: each student is explained by a model that never
saw them. The 2019 cohort is kept only as an external robustness check
because its module grades are strongly inflated relative to 2017-2018
(e.g. 70% of Maths 2 grades are A/A+ in 2019 versus 16% in training).
That shift compresses module-grade variance and mechanically understates
module importance whenever SHAP is computed on the 2019 cohort alone.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.linear_model import Ridge
from sklearn.model_selection import StratifiedKFold

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
EXTERNAL_OUT = OUT / "external_check"
GROUPS = ["Underperforming", "Average", "Performing"]
GRADE_LABELS = {1: "F", 2: "D/S", 3: "C-", 4: "C", 5: "C+", 6: "B-", 7: "B", 8: "B+", 9: "A-", 10: "A", 11: "A+"}
FAMILY_ORDER = ["Pre-academic", "Demographic", "Semester GPA", "Module grade", "Other"]
FAMILY_COLOURS = {"Pre-academic": "#4C78A8", "Demographic": "#72B7B2", "Semester GPA": "#F58518", "Module grade": "#E45756", "Other": "#999999"}


def feature_family(feature_name):
    name = feature_name.split("__", 1)[-1]
    # Strip the prefix instead of rsplit so module names containing spaces or
    # digits (e.g. "missingindicator_Maths 2") keep their family.
    name = name.removeprefix("missingindicator_")
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
    name = name.replace("_infrequent_sklearn", " (rare categories)")
    return name.replace("missingindicator_", "Missing: ")


def linear_shap_frame(pipeline, background, explain, features):
    """SHAP values for `explain` rows using `background` as the reference distribution."""
    preprocessor = pipeline.named_steps["preprocessor"]
    transformed_background = preprocessor.transform(background[features])
    transformed_explain = preprocessor.transform(explain[features])
    names = list(preprocessor.get_feature_names_out())
    masker = shap.maskers.Independent(transformed_background, max_samples=len(background))
    explainer = shap.LinearExplainer(pipeline.named_steps["model"], masker)
    values = explainer(transformed_explain)
    return (
        pd.DataFrame(values.values, index=explain.index, columns=names),
        pd.DataFrame(transformed_explain, index=explain.index, columns=names),
    )


def oof_shap(train, semester):
    """Out-of-fold SHAP on the training cohort: every student is explained by a model that never saw them."""
    numeric = numeric_features(semester)
    features = numeric + CATEGORICAL
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    value_parts, data_parts = [], []
    for fit_index, explain_index in folds.split(train, train["GroupLabel"]):
        fold_train = train.iloc[fit_index]
        pipeline = make_pipeline(Ridge(alpha=1.0), numeric)
        pipeline.fit(fold_train[features], fold_train["FinalGPA"])
        values, data = linear_shap_frame(pipeline, fold_train, train.iloc[explain_index], features)
        value_parts.append(values)
        data_parts.append(data)
    # Fold encoders can emit slightly different one-hot/indicator columns; align on
    # the union, where an absent column simply contributed nothing for that fold.
    values = pd.concat(value_parts).loc[train.index].fillna(0.0)
    data = pd.concat(data_parts).loc[train.index]
    return values, data[values.columns]


def external_shap(train, test, semester):
    """SHAP for the 2019 cohort under the model trained on the full training cohort."""
    numeric = numeric_features(semester)
    features = numeric + CATEGORICAL
    pipeline = make_pipeline(Ridge(alpha=1.0), numeric)
    pipeline.fit(train[features], train["FinalGPA"])
    return linear_shap_frame(pipeline, train, test, features)


def summarise(values, semester):
    importance = pd.DataFrame({
        "feature": [tidy_feature_name(name) for name in values.columns],
        "raw_feature": list(values.columns),
        "mean_abs_shap": np.abs(values.to_numpy()).mean(axis=0),
        "mean_shap": values.to_numpy().mean(axis=0),
    })
    importance["semester"] = semester
    importance["family"] = importance["raw_feature"].map(feature_family)
    family_rows = []
    for family in importance["family"].unique():
        members = importance.loc[importance["family"] == family, "raw_feature"]
        combined = values[list(members)].sum(axis=1)
        family_rows.append({
            "semester": semester,
            "family": family,
            "mean_abs_shap": combined.abs().mean(),
            "mean_shap": combined.mean(),
        })
    return importance, pd.DataFrame(family_rows)


def to_explanation(values, data):
    return shap.Explanation(
        values=values.to_numpy(),
        data=data.to_numpy(),
        feature_names=[tidy_feature_name(name) for name in values.columns],
    )


def plot_beeswarm(values, data, semester, cohort_label, path):
    plt.figure()
    shap.plots.beeswarm(to_explanation(values, data), max_display=15, show=False)
    plt.title(f"Linear SHAP ({cohort_label}): through semester {semester}")
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_family_heatmap(family_results, path, title):
    matrix = family_results.pivot(index="family", columns="semester", values="mean_abs_shap")
    matrix = matrix.reindex([name for name in FAMILY_ORDER if name in matrix.index])
    masked = np.ma.masked_invalid(matrix.to_numpy(dtype=float))
    cmap = plt.get_cmap("YlOrRd").copy()
    cmap.set_bad("#f2f2f2")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    image = ax.imshow(masked, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(matrix.columns)), matrix.columns)
    ax.set_yticks(range(len(matrix.index)), matrix.index)
    ax.set(xlabel="Information available through semester", ylabel="Feature family", title=title)
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            value = matrix.iloc[row, column]
            # Blank cell = family not yet available at that checkpoint, not zero importance.
            if pd.notna(value):
                ax.text(column, row, f"{value:.3f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, label="Mean |SHAP value| (GPA points)")
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def plot_top_features(feature_results, path, cohort_label):
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    for axis, semester in zip(axes.flat, range(7)):
        subset = feature_results[feature_results["semester"] == semester].nlargest(10, "mean_abs_shap").sort_values("mean_abs_shap")
        colours = subset["family"].map(FAMILY_COLOURS)
        axis.barh(subset["feature"], subset["mean_abs_shap"], color=colours)
        axis.set_title(f"Through semester {semester}")
        axis.set_xlabel("Mean |SHAP| (GPA points)")
    axes.flat[-1].set_axis_off()
    fig.suptitle(f"Top feature contributions by temporal model ({cohort_label})", y=1.02)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def module_dependence_plot(importance, values, train, semester):
    candidates = importance[
        (importance["family"] == "Module grade")
        & ~importance["feature"].str.startswith("Missing:")
    ]
    if candidates.empty:
        return None
    selected = candidates.nlargest(1, "mean_abs_shap").iloc[0]
    module = selected["feature"]
    grades = train[module]
    contributions = values[selected["raw_feature"]]
    keep = grades.notna()
    jitter = np.random.default_rng(42).uniform(-0.15, 0.15, int(keep.sum()))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(grades[keep] + jitter, contributions[keep], alpha=0.6)
    ax.axhline(0, color="black", linewidth=0.8)
    # Only mark a "low grade pushes the prediction down" threshold when the
    # conditional attribution really is positively related to the grade. With
    # semester GPAs in the model, multicollinearity can flip or destabilise a
    # module's coefficient across folds, and a threshold would mislead.
    correlation = np.corrcoef(grades[keep], contributions[keep])[0, 1]
    if correlation >= 0.6:
        by_grade = contributions[keep].groupby(grades[keep]).mean()
        negative = by_grade[by_grade < 0]
        if not negative.empty:
            threshold = int(negative.index.max())
            ax.axvline(threshold + 0.5, color="#C44E52", linestyle="--", linewidth=1)
            ax.text(threshold + 0.6, ax.get_ylim()[1] * 0.9, f"pushes GPA prediction down at ≤ {GRADE_LABELS[threshold]}",
                    color="#C44E52", fontsize=8, va="top")
    else:
        ax.text(0.02, 0.02, "Conditional attribution (semester GPAs controlled) is weak/unstable here;\nuse the grade-band risk tables for advisor-facing cut-offs.",
                transform=ax.transAxes, fontsize=8, color="#C44E52", va="bottom")
    ax.set_xticks(sorted(GRADE_LABELS), [GRADE_LABELS[points] for points in sorted(GRADE_LABELS)])
    ax.set(
        xlabel=f"{module} grade",
        ylabel=f"SHAP contribution of {module} (GPA points)",
        title=f"Module signal at semester {semester} (training cohort, out-of-fold)",
    )
    fig.tight_layout()
    safe_name = "".join(character if character.isalnum() else "_" for character in module)
    fig.savefig(OUT / f"linear_shap_module_dependence_s{semester}_{safe_name}.png", dpi=300)
    plt.close(fig)
    return module


def write_report(feature_results, family_results, dependence_features):
    module_start = feature_results[(feature_results["semester"] == 2) & (feature_results["family"] == "Module grade")].nlargest(3, "mean_abs_shap")
    sem3_modules = feature_results[(feature_results["semester"] == 3) & (feature_results["family"] == "Module grade")].nlargest(3, "mean_abs_shap")
    lines = [
        "# RQ2 temporal linear-SHAP analysis",
        "",
        "## Method",
        "",
        "Ridge was selected in the pre-SHAP model audit. For each checkpoint S0–S6, SHAP values on the 2017–2018 training cohort are computed **out-of-fold**: a 5-fold split (stratified by final-GPA group) is used so that every student is explained by a Ridge model that never saw them, with the fold's own training portion as SHAP background. This avoids in-sample explanation while keeping realistic module-grade variance.",
        "",
        "The 2019 cohort is reported only as an external robustness check (`external_check/`). Its module grades are strongly inflated relative to 2017–2018 (e.g. 70% of Maths 2 grades are A/A+ in 2019 versus 16% in training), which compresses module variance and mechanically understates module importance in external SHAP. This cohort shift is why the training cohort is the primary explanation target.",
        "",
        "All preprocessing is fitted on each fold's training portion only, so SHAP values are in final-GPA points after the same leakage-safe imputation, scaling, and encoding used during model evaluation.",
        "",
        "## How to read the outputs",
        "",
        "- `mean_abs_shap` measures a feature's average contribution magnitude; use it for importance.",
        "- `mean_shap` is directional only for the explained cohort; it should not be interpreted as a causal effect.",
        "- The family heatmap compares pre-academic, demographic, semester-GPA, and module-grade contribution over time. It is the primary RQ2 temporal figure. Blank cells mean the family is not yet available at that checkpoint.",
        "- Beeswarm plots show whether higher/lower values tend to increase or decrease a prediction. Module dependence plots are shown in original grade units with the highest grade that still pushes the prediction down marked.",
        "",
        "## Early module signals",
        "",
        "At S2, the leading module-grade features are: " + "; ".join(f"{row.feature} (mean |SHAP| = {row.mean_abs_shap:.3f})" for row in module_start.itertuples()) + ".",
        "",
        "At S3, the leading module-grade features are: " + "; ".join(f"{row.feature} (mean |SHAP| = {row.mean_abs_shap:.3f})" for row in sem3_modules.itertuples()) + ".",
        "",
        "## Interpretation guardrails",
        "",
        "Semester GPA and module grades are correlated. SHAP distributes model attribution among correlated predictors according to the chosen background distribution; it does not establish that a module causes a later GPA outcome. The findings should be framed as early academic signals that help explain model behaviour and support advisor review, not automated intervention decisions.",
        "",
        "Individual signed module SHAP must be read as **conditional** attribution: once semester GPAs are in the model, a correlated module can receive a negative Ridge coefficient through multicollinearity suppression (e.g. StatsII at S3), which inverts the marginal 'low grade → low predicted GPA' association in beeswarm plots. Use the family-level views for the temporal story and the grade-band risk tables (`risk_tables/`) for advisor-facing direction; the marginal association between low module grades and eventual underperformance remains strongly positive there.",
        "",
        "## Generated artefacts",
        "",
        "- `linear_shap_feature_importance.csv` / `linear_shap_family_importance.csv`: training-cohort out-of-fold SHAP by checkpoint.",
        "- `linear_shap_family_heatmap.png`, `linear_shap_top_features_by_semester.png`, and checkpoint beeswarms (training cohort).",
        "- Early-module dependence plots (original grade units) for: " + ", ".join(dependence_features) + ".",
        "- `external_check/`: the same feature/family summaries and heatmap computed on the 2019 cohort for robustness, subject to the cohort-shift caveat above.",
    ]
    (OUT / "RQ2_linear_SHAP_interpretation.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    EXTERNAL_OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("linear_shap_module_dependence_*.png"):
        stale.unlink()
    train, test = clean_data(TRAIN_PATH), clean_data(TEST_PATH)
    feature_frames, family_frames, dependence_features = [], [], []
    external_feature_frames, external_family_frames = [], []
    for semester in range(7):
        values, data = oof_shap(train, semester)
        importance, family_importance = summarise(values, semester)
        feature_frames.append(importance)
        family_frames.append(family_importance)
        plot_beeswarm(values, data, semester, "training cohort, out-of-fold", OUT / f"linear_shap_beeswarm_s{semester}.png")
        if semester in (2, 3, 4):
            selected = module_dependence_plot(importance, values, train, semester)
            if selected:
                dependence_features.append(f"S{semester}: {selected}")
        external_values, _ = external_shap(train, test, semester)
        external_importance, external_family = summarise(external_values, semester)
        external_feature_frames.append(external_importance)
        external_family_frames.append(external_family)
    feature_results = pd.concat(feature_frames, ignore_index=True)
    family_results = pd.concat(family_frames, ignore_index=True)
    feature_results.to_csv(OUT / "linear_shap_feature_importance.csv", index=False)
    family_results.to_csv(OUT / "linear_shap_family_importance.csv", index=False)
    plot_family_heatmap(family_results, OUT / "linear_shap_family_heatmap.png", "Training cohort (out-of-fold SHAP)")
    plot_top_features(feature_results, OUT / "linear_shap_top_features_by_semester.png", "training cohort, out-of-fold")
    external_features = pd.concat(external_feature_frames, ignore_index=True)
    external_families = pd.concat(external_family_frames, ignore_index=True)
    external_features.to_csv(EXTERNAL_OUT / "linear_shap_feature_importance.csv", index=False)
    external_families.to_csv(EXTERNAL_OUT / "linear_shap_family_importance.csv", index=False)
    plot_family_heatmap(external_families, EXTERNAL_OUT / "linear_shap_family_heatmap.png", "External 2019 cohort (robustness check; module grades inflated vs training)")
    write_report(feature_results, family_results, dependence_features)
    print("Completed temporal linear-SHAP analysis (training-cohort primary).")


if __name__ == "__main__":
    main()
