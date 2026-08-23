# RQ2 module-data model audit (pre-SHAP)

## Design decision

This is **not a second RQ1**. The TALE positioning document states that RQ1 uses routinely available pre-academic, demographic, and semester-GPA data to establish reliability. Here, module grades are included only in RQ2 to explain why the predictive signal changes over time. The existing RQ1 reliability conclusions therefore remain the primary institutional benchmark.

The training cohort contains 177 students (2017–2018) and the held-out external cohort contains 93 students (2019). All models use only features that would have been available by each semester; no future semester GPA or future module result is included.

## Preprocessing and feature engineering

- Identifier and cohort-year columns are excluded from prediction.
- District spelling variants are harmonised before one-hot encoding. Rare categories are grouped by the encoder (`min_frequency=5`), and unseen 2019 categories are safely ignored.
- Module letter grades are converted to an ordinal grade-point scale (A+ = 11 through F = 0; D/S = 2). Administrative/incomplete outcomes (`I-we`, `I-ca` — did not sit the exam or did not complete the continuous-assessment component) are coded as a fail-equivalent grade point of 1, one step above outright F, not imputed as missing.
- Numeric values are median-imputed and standardised within each fold. This makes Ridge coefficients/linear SHAP comparable while avoiding validation or test leakage.

## Model audit

Ridge (alpha=1) is compared with a conservative Random Forest (100 trees, depth 3). Model comparison uses 5-fold CV repeated 10 times in the training cohorts, stratified by the pre-defined final-GPA groups, followed by one untouched 2019 external evaluation. The test cohort is not used to tune models.

### Model-selection result

**Selected explanation model: Ridge.** Ridge is considered practically competitive whenever its repeated-CV RMSE is within 0.01 GPA points of Random Forest; this tolerance favours the transparent linear model only when predictive performance is essentially indistinguishable. Ridge met that criterion at 7 of 7 temporal checkpoints.

### Observed temporal pattern

- In repeated CV, Ridge is comparable to or better than Random Forest at every checkpoint under the pre-specified 0.01-RMSE practical-equivalence rule. Its RMSE falls from 0.346 at baseline to 0.248 after S1, 0.181 after S3, and 0.087 after S6. Its CV variability also narrows from 0.063 to 0.036.
- The 2019 external cohort supports the later-semester pattern: Ridge has RMSE 0.236 (R² 0.757) at S3, 0.164 (R² 0.883) at S4, and 0.102 (R² 0.955) at S6. Ridge outperforms Random Forest externally at S4–S6 by 0.029, 0.034, and 0.043 RMSE points respectively.
- S2 is a caution point, not evidence that modules harm attainment: external Ridge RMSE rises from 0.346 at S1 to 0.371 at S2 despite improving CV. This is likely cohort/distribution shift and the limited sample, so RQ2 should explain model behaviour rather than claim a module-driven performance gain.
- Underperforming students remain least precise on the 2019 cohort (Ridge RMSE 0.383 at S3, 0.271 at S4, and 0.167 at S6), echoing RQ1. This group-wise result is descriptive support for the explanation phase; it does not redefine RQ1’s module-free reliability thresholds.

The final SHAP stage should use the selected model at each checkpoint. If Ridge is selected, use `shap.LinearExplainer` with a training-background sample and report both signed and mean-absolute SHAP values. If Random Forest is selected, use `shap.TreeExplainer`; do not use a linear explainer for a non-linear model.

## Interpretation boundaries

Module features can be correlated with semester GPA, so SHAP attribution is an explanation of the fitted model under the chosen background distribution, not a causal claim about a module. For the paper, report grouped SHAP importance (pre-academic, demographics, semester GPA, modules) alongside individual features; show a temporal heatmap of mean |SHAP| by feature family and a small number of dependence plots for the strongest early module signals. Avoid individual student force plots in the paper unless explicitly de-identified and ethically approved.

## Files

- `model_comparison.csv`: CV and external-test metrics for Ridge and Random Forest.
- `eda_cohort_summary.csv` and `eda_training_correlations_with_final_gpa.csv`: EDA outputs.
- `external_test_rmse_by_semester.png`, `cv_rmse_by_semester.png`, and `external_test_r2_by_semester.png`: model-audit plots.