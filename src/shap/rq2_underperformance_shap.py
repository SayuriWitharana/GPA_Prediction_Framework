"""Identify early underperformance signals by stratifying external-cohort SHAP values.

Performance groups are used only after prediction/explanation, for retrospective
evaluation. They are never model inputs and cannot be used for live triage.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rq2_linear_shap import feature_family, run_checkpoint, tidy_feature_name
from rq2_module_model_audit import OUT as AUDIT_OUT, TEST_PATH, TRAIN_PATH, clean_data


OUT = AUDIT_OUT / "linear_shap" / "underperformance"
EARLY_SEMESTERS = range(0, 4)
RNG = np.random.default_rng(42)


def bootstrap_difference(underperforming, other, n_bootstrap=5000):
    """Bootstrap the difference in mean signed SHAP: underperforming - other."""
    differences = np.empty(n_bootstrap)
    for index in range(n_bootstrap):
        under_sample = RNG.choice(underperforming, size=len(underperforming), replace=True)
        other_sample = RNG.choice(other, size=len(other), replace=True)
        differences[index] = under_sample.mean() - other_sample.mean()
    return np.quantile(differences, [0.025, 0.975])


def checkpoint_summary(values, names, test, semester):
    under_mask = (test["GroupLabel"] == "Underperforming").to_numpy()
    rows = []
    for position, raw_name in enumerate(names):
        under_values = values.values[under_mask, position]
        other_values = values.values[~under_mask, position]
        lower, upper = bootstrap_difference(under_values, other_values)
        rows.append({
            "semester": semester,
            "feature": tidy_feature_name(raw_name),
            "raw_feature": raw_name,
            "family": feature_family(raw_name),
            "underperforming_mean_shap": under_values.mean(),
            "underperforming_mean_abs_shap": np.abs(under_values).mean(),
            "other_students_mean_shap": other_values.mean(),
            "difference_under_minus_other": under_values.mean() - other_values.mean(),
            "difference_ci_lower": lower,
            "difference_ci_upper": upper,
        })
    result = pd.DataFrame(rows)
    result["consistent_negative_signal"] = (
        (result["underperforming_mean_shap"] < 0)
        & (result["difference_under_minus_other"] < 0)
        & (result["difference_ci_upper"] < 0)
    )
    return result


def plot_signals(results, semester):
    academic = results[(results["semester"] == semester) & (results["family"] != "Demographic")]
    signals = academic[academic["consistent_negative_signal"]]
    if signals.empty:
        signals = academic[academic["underperforming_mean_shap"] < 0]
    signals = signals.nsmallest(10, "underperforming_mean_shap").sort_values("underperforming_mean_shap")
    if signals.empty:
        return
    fig, ax = plt.subplots(figsize=(9, max(4, len(signals) * 0.45)))
    colours = signals["consistent_negative_signal"].map({True: "#C44E52", False: "#999999"})
    ax.barh(signals["feature"], signals["underperforming_mean_shap"], color=colours)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set(
        title=f"Early signals associated with lower predicted GPA: through semester {semester}",
        xlabel="Mean signed SHAP among actual underperformers (GPA points)",
    )
    fig.tight_layout()
    fig.savefig(OUT / f"underperformance_early_signals_s{semester}.png", dpi=300)
    plt.close(fig)


def write_report(results, test):
    signal_rows = results[(results["consistent_negative_signal"]) & (results["family"] != "Demographic")].sort_values(["semester", "underperforming_mean_shap"])
    if signal_rows.empty:
        table = "No individual feature met the conservative bootstrap criterion; use the ranked negative SHAP table as exploratory evidence."
    else:
        selected = signal_rows.groupby("semester", group_keys=False).head(8)
        table_lines = ["| Semester | Feature | Family | Underperformer mean SHAP | Difference vs others | 95% CI |", "|---:|---|---|---:|---:|---|"]
        for row in selected.itertuples():
            table_lines.append(
                f"| {row.semester} | {row.feature} | {row.family} | {row.underperforming_mean_shap:.3f} | "
                f"{row.difference_under_minus_other:.3f} | [{row.difference_ci_lower:.3f}, {row.difference_ci_upper:.3f}] |"
            )
        table = "\n".join(table_lines)
    text = f"""# Early predictors of underperformance: group-stratified SHAP

## Purpose and design

This analysis uses the Ridge models already selected for RQ2. Each model is trained on the full 2017–2018 cohort, then SHAP values for the external 2019 cohort are stratified by **eventual** final-GPA group. The 2019 cohort includes {(test['GroupLabel'] == 'Underperforming').sum()} underperforming and {(test['GroupLabel'] != 'Underperforming').sum()} other students.

This design identifies which available features tend to push the model toward a lower GPA prediction for students who ultimately underperform. It does **not** train a separate underperformer model and it does **not** use the eventual group as a live prediction feature.

## Signal definition

A feature is marked as a *consistent negative early signal* only when all three conditions hold:

1. Its mean signed SHAP value is negative among actual underperformers.
2. Its mean signed SHAP is lower for underperformers than for the other students.
3. The 95% bootstrap confidence interval for that group difference remains below zero (5,000 resamples).

The criterion is deliberately conservative: group sizes are small and correlated semester/module features share attribution. These are model-based early-warning signals, not causal determinants.

## Academic features meeting the conservative criterion

{table}

## Use in the study

Use S1–S3 as the primary early-warning window. Present the charted signals as prompts for advisor review or additional evidence, never as an automated designation of a student as at risk. The full ranked CSV retains exploratory signals that do not meet the bootstrap threshold.

## Files

- `underperformance_feature_shap_summary.csv`: all feature-level group comparisons and bootstrap intervals.
- `underperformance_consistent_negative_signals.csv`: all features meeting the conservative criterion, including demographics for fairness auditing.
- `underperformance_early_academic_signals.csv`: only actionable academic features meeting the criterion.
- `underperformance_early_signals_s0.png` to `..._s3.png`: academic signed early-signal charts (red = meets criterion; grey = exploratory negative signal).
"""
    (OUT / "RQ2_underperformance_SHAP_interpretation.md").write_text(text, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = clean_data(TRAIN_PATH), clean_data(TEST_PATH)
    summaries = []
    for semester in EARLY_SEMESTERS:
        _, _, values, _, names = run_checkpoint(train, test, semester)
        summaries.append(checkpoint_summary(values, names, test, semester))
    results = pd.concat(summaries, ignore_index=True)
    results.to_csv(OUT / "underperformance_feature_shap_summary.csv", index=False)
    results[results["consistent_negative_signal"]].to_csv(OUT / "underperformance_consistent_negative_signals.csv", index=False)
    results[(results["consistent_negative_signal"]) & (results["family"] != "Demographic")].to_csv(OUT / "underperformance_early_academic_signals.csv", index=False)
    for semester in EARLY_SEMESTERS:
        plot_signals(results, semester)
    write_report(results, test)
    print("Completed group-stratified early-underperformance SHAP analysis.")


if __name__ == "__main__":
    main()
