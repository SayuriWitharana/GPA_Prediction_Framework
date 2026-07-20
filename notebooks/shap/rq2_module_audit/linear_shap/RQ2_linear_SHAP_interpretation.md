# RQ2 temporal linear-SHAP analysis

## Method

Ridge was selected in the pre-SHAP model audit. For each checkpoint S0–S6, the model is trained on all 2017–2018 module-data records and explained on the untouched 2019 cohort with `shap.LinearExplainer`. The SHAP background is a capped (n ≤ 100) training-cohort sample. This explains external predictions rather than in-sample fits.

All preprocessing is fitted on the training cohort only. Therefore, SHAP values are in final-GPA points after the same leakage-safe imputation, scaling, and encoding used during model evaluation.

## How to read the outputs

- `mean_abs_shap` measures a feature’s average contribution magnitude; use it for importance.
- `mean_shap` is directional only for this 2019 cohort; it should not be interpreted as a causal effect.
- The family heatmap compares pre-academic, demographic, semester-GPA, and module-grade contribution over time. It is the primary RQ2 temporal figure.
- Beeswarm plots show whether higher/lower values tend to increase or decrease a prediction. Module dependence plots are descriptive checks of the strongest available module at each early checkpoint.

## Early module signals

At S2, the leading module-grade features are: Maths 2 (mean |SHAP| = 0.041); MgtAccounting (mean |SHAP| = 0.011).

At S3, the leading module-grade features are: Missing: StatsII (mean |SHAP| = 0.030); Maths 2 (mean |SHAP| = 0.028); StatsII (mean |SHAP| = 0.025).

## Interpretation guardrails

Semester GPA and module grades are correlated. SHAP distributes model attribution among correlated predictors according to the chosen training-background distribution; it does not establish that a module causes a later GPA outcome. The findings should be framed as early academic signals that help explain model behaviour and support advisor review, not automated intervention decisions.

## Generated artefacts

- `linear_shap_feature_importance.csv`: feature-level signed and absolute SHAP values by checkpoint.
- `linear_shap_family_importance.csv`: grouped temporal importance for the paper’s main heatmap.
- `linear_shap_family_heatmap.png`, `linear_shap_top_features_by_semester.png`, and checkpoint beeswarms.
- Early-module dependence plots for: S2: Maths 2, S3: Maths 2, S4: Maths 2.