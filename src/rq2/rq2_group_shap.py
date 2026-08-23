"""Three-group temporal SHAP profiles for RQ2.

For each checkpoint S0-S6, out-of-fold SHAP values on the 2017-2018 training
cohort are stratified by eventual final-GPA group (Underperforming / Average /
Performing) to show which features drive predictions for each group of
students, and how that changes over the degree.

The 2019 cohort is summarised only as an external check: its module grades are
strongly inflated relative to training (see rq2_linear_shap.py), which
compresses module variance and understates module importance externally.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from rq2_linear_shap import (
    GROUPS,
    external_shap,
    feature_family,
    oof_shap,
    plot_family_heatmap,
    plot_top_features,
    tidy_feature_name,
)
from rq2_module_model_audit import OUT as AUDIT_OUT, TEST_PATH, TRAIN_PATH, clean_data


OUT = AUDIT_OUT / "group_shap"


def group_summaries(values, labels, semester):
    """Per-group feature and family SHAP summaries for one checkpoint."""
    families = {name: feature_family(name) for name in values.columns}
    feature_rows, family_rows = [], []
    for group in GROUPS:
        subset = values[(labels == group).to_numpy()]
        for raw_name in values.columns:
            column = subset[raw_name]
            feature_rows.append({
                "semester": semester,
                "group": group,
                "n_students": len(subset),
                "feature": tidy_feature_name(raw_name),
                "raw_feature": raw_name,
                "family": families[raw_name],
                "mean_abs_shap": column.abs().mean(),
                "mean_shap": column.mean(),
            })
        for family in dict.fromkeys(families.values()):
            members = [name for name in values.columns if families[name] == family]
            combined = subset[members].sum(axis=1)
            family_rows.append({
                "semester": semester,
                "group": group,
                "family": family,
                "mean_abs_shap": combined.abs().mean(),
                "mean_shap": combined.mean(),
            })
    return pd.DataFrame(feature_rows), pd.DataFrame(family_rows)


def advisor_matrix(feature_results):
    """Semester x group table of the strongest prediction drivers per group."""
    lines = [
        "| Semester | " + " | ".join(GROUPS) + " |",
        "|---:|" + "---|" * len(GROUPS),
    ]
    for semester in sorted(feature_results["semester"].unique()):
        cells = []
        for group in GROUPS:
            subset = feature_results[(feature_results["semester"] == semester) & (feature_results["group"] == group)]
            top = subset.nlargest(3, "mean_abs_shap")
            cells.append("; ".join(
                f"{row.feature} {'↓' if row.mean_shap < 0 else '↑'}" for row in top.itertuples()
            ))
        lines.append(f"| {semester} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_report(feature_results, family_results, train):
    counts = train["GroupLabel"].value_counts()
    text = f"""# RQ2 three-group temporal SHAP profiles

## Purpose and design

Out-of-fold SHAP values on the 2017–2018 training cohort ({counts.get('Underperforming', 0)} Underperforming, {counts.get('Average', 0)} Average, {counts.get('Performing', 0)} Performing students) are stratified by **eventual** final-GPA group at each checkpoint S0–S6. This shows which features drive the model's predictions for each group of students and how those drivers evolve, supporting group-specific advisor guidance.

Groups are retrospective labels used only to stratify explanations; they are never model inputs. The training cohort is the explanation target because 2019 module grades are strongly inflated relative to 2017–2018 (compressed module variance would understate module signals); `external_check_family_importance.csv` retains the 2019 view for robustness.

## How to read the outputs

- `mean_abs_shap` within a group = how strongly a feature moves predictions for those students.
- `mean_shap` within a group = the typical direction (negative pushes predicted GPA down).
- ↓/↑ in the matrix below shows that typical direction for that group.
- Because groups are defined by eventual GPA, low grades mechanically push underperformers' predictions down; the value of the table is *which* features carry that signal at each checkpoint, i.e. what an advisor should look at first.
- Signed module SHAP is **conditional** attribution: with semester GPAs in the model, a correlated module can take a negative Ridge coefficient (multicollinearity suppression, e.g. StatsII at S3) and its arrow can invert the marginal association. For advisor-facing direction on individual modules, use the grade-band risk tables (`risk_tables/`).

## Advisor monitoring matrix (top-3 drivers per group)

{advisor_matrix(feature_results)}

## Files

- `group_shap_feature_importance.csv` / `group_shap_family_importance.csv`: per-group, per-checkpoint SHAP summaries (training, out-of-fold).
- `group_family_heatmap_<group>.png`: temporal family importance per group.
- `group_top_features_<group>.png`: top-10 feature evolution per group.
- `external_check_family_importance.csv`: 2019-cohort per-group family summary (robustness only; see cohort-shift caveat).
"""
    (OUT / "RQ2_group_SHAP_interpretation.md").write_text(text, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = clean_data(TRAIN_PATH), clean_data(TEST_PATH)
    feature_frames, family_frames, external_family_frames = [], [], []
    for semester in range(7):
        values, _ = oof_shap(train, semester)
        features, families = group_summaries(values, train["GroupLabel"], semester)
        feature_frames.append(features)
        family_frames.append(families)
        external_values, _ = external_shap(train, test, semester)
        _, external_families = group_summaries(external_values, test["GroupLabel"], semester)
        external_family_frames.append(external_families)
    feature_results = pd.concat(feature_frames, ignore_index=True)
    family_results = pd.concat(family_frames, ignore_index=True)
    feature_results.to_csv(OUT / "group_shap_feature_importance.csv", index=False)
    family_results.to_csv(OUT / "group_shap_family_importance.csv", index=False)
    pd.concat(external_family_frames, ignore_index=True).to_csv(OUT / "external_check_family_importance.csv", index=False)
    for group in GROUPS:
        plot_family_heatmap(
            family_results[family_results["group"] == group],
            OUT / f"group_family_heatmap_{group}.png",
            f"{group} students (training cohort, out-of-fold SHAP)",
        )
        plot_top_features(
            feature_results[feature_results["group"] == group],
            OUT / f"group_top_features_{group}.png",
            f"{group} students, training cohort",
        )
    write_report(feature_results, family_results, train)
    print("Completed three-group temporal SHAP profiles.")


if __name__ == "__main__":
    main()
