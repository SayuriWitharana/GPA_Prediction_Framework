# RQ2 temporal linear-SHAP analysis

## Method

Ridge was selected in the pre-SHAP model audit. For each checkpoint S0–S6, SHAP values on the 2017–2018 training cohort are computed **out-of-fold**: a 5-fold split (stratified by final-GPA group) is used so that every student is explained by a Ridge model that never saw them, with the fold's own training portion as SHAP background. This avoids in-sample explanation while keeping realistic module-grade variance.

The 2019 cohort is reported only as an external robustness check (`external_check/`). Its module grades are strongly inflated relative to 2017–2018 (e.g. 70% of Maths 2 grades are A/A+ in 2019 versus 16% in training), which compresses module variance and mechanically understates module importance in external SHAP. This cohort shift is why the training cohort is the primary explanation target.

All preprocessing is fitted on each fold's training portion only, so SHAP values are in final-GPA points after the same leakage-safe imputation, scaling, and encoding used during model evaluation.

## How to read the outputs

- `mean_abs_shap` measures a feature's average contribution magnitude; use it for importance.
- `mean_shap` is directional only for the explained cohort; it should not be interpreted as a causal effect.
- The family heatmap compares pre-academic, demographic, semester-GPA, and module-grade contribution over time. It is the primary RQ2 temporal figure. Blank cells mean the family is not yet available at that checkpoint.
- Beeswarm plots show whether higher/lower values tend to increase or decrease a prediction. Module dependence plots are shown in original grade units with the highest grade that still pushes the prediction down marked.

## Early module signals

At S2, the leading module-grade features are: Maths 2 (mean |SHAP| = 0.025); MgtAccounting (mean |SHAP| = 0.015).

At S3, the leading module-grade features are: Maths 2 (mean |SHAP| = 0.025); StatsII (mean |SHAP| = 0.023); MIS (mean |SHAP| = 0.012).

## Interpretation guardrails

Semester GPA and module grades are correlated. SHAP distributes model attribution among correlated predictors according to the chosen background distribution; it does not establish that a module causes a later GPA outcome. The findings should be framed as early academic signals that help explain model behaviour and support advisor review, not automated intervention decisions.

Individual signed module SHAP must be read as **conditional** attribution: once semester GPAs are in the model, a correlated module can receive a negative Ridge coefficient through multicollinearity suppression (e.g. StatsII at S3), which inverts the marginal 'low grade → low predicted GPA' association in beeswarm plots. Use the family-level views for the temporal story and the grade-band risk tables (`risk_tables/`) for advisor-facing direction; the marginal association between low module grades and eventual underperformance remains strongly positive there.

## Generated artefacts

- `linear_shap_feature_importance.csv` / `linear_shap_family_importance.csv`: training-cohort out-of-fold SHAP by checkpoint.
- `linear_shap_family_heatmap.png`, `linear_shap_top_features_by_semester.png`, and checkpoint beeswarms (training cohort).
- Early-module dependence plots (original grade units) for: S2: Maths 2, S3: Maths 2, S4: Maths 2.
- `external_check/`: the same feature/family summaries and heatmap computed on the 2019 cohort for robustness, subject to the cohort-shift caveat above.