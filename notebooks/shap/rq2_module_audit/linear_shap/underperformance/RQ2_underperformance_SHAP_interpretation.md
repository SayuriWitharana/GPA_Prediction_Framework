# Early predictors of underperformance: group-stratified SHAP

## Purpose and design

This analysis uses the Ridge models already selected for RQ2. Out-of-fold SHAP values on the 2017–2018 training cohort (each student explained by a model that never saw them) are stratified by **eventual** final-GPA group. The cohort contains 46 eventual underperformers and 131 other students.

The training cohort is the explanation target because 2019 module grades are strongly inflated relative to 2017–2018, which compresses module variance and hides module signals, and because it holds almost twice as many eventual underperformers. The early-warning window covers S0–S5 (entry data through semester 5).

This design identifies which available features tend to push the model toward a lower GPA prediction for students who ultimately underperform. It does **not** train a separate underperformer model and it does **not** use the eventual group as a live prediction feature.

## Signal definition

A feature is marked as a *consistent negative early signal* only when all four conditions hold:

1. Its mean signed SHAP value is negative among eventual underperformers.
2. Its mean signed SHAP is lower for underperformers than for the other students.
3. The 95% bootstrap confidence interval for that group difference remains below zero (5,000 resamples).
4. The bootstrap p-value survives a Benjamini–Hochberg false-discovery-rate correction (q < 0.05) across all features tested at that checkpoint.

The criterion is deliberately conservative: group sizes are small and correlated semester/module features share attribution. These are model-based early-warning signals, not causal determinants.

## Academic features meeting the conservative criterion

| Semester | Feature | Family | Underperformer mean SHAP | Difference vs others | 95% CI | BH q-value |
|---:|---|---|---:|---:|---|---:|
| 0 | English | Pre-academic | -0.151 | -0.202 | [-0.270, -0.136] | 0.0022 |
| 0 | Zscore | Pre-academic | -0.022 | -0.033 | [-0.054, -0.012] | 0.0029 |
| 1 | S1 | Semester GPA | -0.389 | -0.525 | [-0.597, -0.450] | 0.0023 |
| 1 | English | Pre-academic | -0.039 | -0.054 | [-0.072, -0.036] | 0.0023 |
| 2 | S2 | Semester GPA | -0.306 | -0.415 | [-0.475, -0.353] | 0.0009 |
| 2 | S1 | Semester GPA | -0.170 | -0.228 | [-0.260, -0.195] | 0.0009 |
| 2 | English | Pre-academic | -0.044 | -0.061 | [-0.081, -0.041] | 0.0009 |
| 2 | MgtAccounting | Module grade | -0.011 | -0.014 | [-0.021, -0.009] | 0.0009 |
| 2 | Zscore | Pre-academic | -0.009 | -0.011 | [-0.019, -0.004] | 0.0059 |
| 3 | S3 | Semester GPA | -0.220 | -0.302 | [-0.342, -0.259] | 0.0008 |
| 3 | S2 | Semester GPA | -0.174 | -0.237 | [-0.272, -0.202] | 0.0008 |
| 3 | S1 | Semester GPA | -0.147 | -0.195 | [-0.224, -0.165] | 0.0008 |
| 3 | Zscore | Pre-academic | -0.010 | -0.012 | [-0.020, -0.005] | 0.0008 |
| 3 | MgtAccounting | Module grade | -0.006 | -0.009 | [-0.013, -0.004] | 0.0008 |
| 4 | S4 | Semester GPA | -0.227 | -0.307 | [-0.367, -0.254] | 0.0011 |
| 4 | S3 | Semester GPA | -0.139 | -0.191 | [-0.217, -0.164] | 0.0011 |
| 4 | S1 | Semester GPA | -0.133 | -0.177 | [-0.204, -0.150] | 0.0011 |
| 4 | S2 | Semester GPA | -0.069 | -0.092 | [-0.106, -0.078] | 0.0011 |
| 4 | Zscore | Pre-academic | -0.007 | -0.010 | [-0.017, -0.004] | 0.0019 |
| 5 | S5 | Semester GPA | -0.147 | -0.198 | [-0.242, -0.160] | 0.0006 |
| 5 | S3 | Semester GPA | -0.143 | -0.194 | [-0.221, -0.167] | 0.0006 |
| 5 | S4 | Semester GPA | -0.125 | -0.169 | [-0.200, -0.140] | 0.0006 |
| 5 | S1 | Semester GPA | -0.086 | -0.116 | [-0.132, -0.099] | 0.0006 |
| 5 | S2 | Semester GPA | -0.084 | -0.114 | [-0.130, -0.098] | 0.0006 |
| 5 | English | Pre-academic | -0.014 | -0.019 | [-0.026, -0.012] | 0.0006 |
| 5 | Maths 2 | Module grade | -0.007 | -0.010 | [-0.013, -0.007] | 0.0006 |
| 5 | Zscore | Pre-academic | -0.005 | -0.007 | [-0.012, -0.003] | 0.0023 |

## Use in the study

Use S1–S5 as the early-warning window, with S1–S3 as the primary window for timely intervention. Present the charted signals as prompts for advisor review or additional evidence, never as an automated designation of a student as at risk. The full ranked CSV retains exploratory signals that do not meet the conservative threshold. Pair these signals with the grade-band risk tables (`risk_tables/`) for advisor-facing thresholds.

## Files

- `underperformance_feature_shap_summary.csv`: all feature-level group comparisons, bootstrap intervals, and FDR-adjusted q-values.
- `underperformance_consistent_negative_signals.csv`: all features meeting the conservative criterion, including demographics for fairness auditing.
- `underperformance_early_academic_signals.csv`: only actionable academic features meeting the criterion.
- `underperformance_early_signals_s0.png` to `..._s5.png`: academic signed early-signal charts (red = meets criterion; grey = exploratory negative signal).
