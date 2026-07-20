# Early predictors of underperformance: group-stratified SHAP

## Purpose and design

This analysis uses the Ridge models already selected for RQ2. Each model is trained on the full 2017–2018 cohort, then SHAP values for the external 2019 cohort are stratified by **eventual** final-GPA group. The 2019 cohort includes 24 underperforming and 69 other students.

This design identifies which available features tend to push the model toward a lower GPA prediction for students who ultimately underperform. It does **not** train a separate underperformer model and it does **not** use the eventual group as a live prediction feature.

## Signal definition

A feature is marked as a *consistent negative early signal* only when all three conditions hold:

1. Its mean signed SHAP value is negative among actual underperformers.
2. Its mean signed SHAP is lower for underperformers than for the other students.
3. The 95% bootstrap confidence interval for that group difference remains below zero (5,000 resamples).

The criterion is deliberately conservative: group sizes are small and correlated semester/module features share attribution. These are model-based early-warning signals, not causal determinants.

## Academic features meeting the conservative criterion

| Semester | Feature | Family | Underperformer mean SHAP | Difference vs others | 95% CI |
|---:|---|---|---:|---:|---|
| 0 | English | Pre-academic | -0.190 | -0.266 | [-0.348, -0.181] |
| 0 | Zscore | Pre-academic | -0.035 | -0.080 | [-0.126, -0.039] |
| 1 | S1 | Semester GPA | -0.226 | -0.514 | [-0.614, -0.413] |
| 1 | English | Pre-academic | -0.052 | -0.074 | [-0.096, -0.049] |
| 1 | Zscore | Pre-academic | -0.005 | -0.012 | [-0.019, -0.006] |
| 2 | S1 | Semester GPA | -0.098 | -0.223 | [-0.267, -0.178] |
| 2 | English | Pre-academic | -0.058 | -0.082 | [-0.107, -0.055] |
| 2 | Zscore | Pre-academic | -0.006 | -0.014 | [-0.021, -0.007] |
| 3 | S3 | Semester GPA | -0.225 | -0.318 | [-0.372, -0.267] |
| 3 | S1 | Semester GPA | -0.085 | -0.194 | [-0.232, -0.154] |
| 3 | Missing: StatsII | Module grade | -0.050 | -0.060 | [-0.100, -0.021] |
| 3 | MIS | Module grade | -0.009 | -0.009 | [-0.011, -0.007] |
| 3 | Zscore | Pre-academic | -0.006 | -0.014 | [-0.022, -0.007] |

## Use in the study

Use S1–S3 as the primary early-warning window. Present the charted signals as prompts for advisor review or additional evidence, never as an automated designation of a student as at risk. The full ranked CSV retains exploratory signals that do not meet the bootstrap threshold.

## Files

- `underperformance_feature_shap_summary.csv`: all feature-level group comparisons and bootstrap intervals.
- `underperformance_consistent_negative_signals.csv`: all features meeting the conservative criterion, including demographics for fairness auditing.
- `underperformance_early_academic_signals.csv`: only actionable academic features meeting the criterion.
- `underperformance_early_signals_s0.png` to `..._s3.png`: academic signed early-signal charts (red = meets criterion; grey = exploratory negative signal).
