# RQ2 three-group temporal SHAP profiles

## Purpose and design

Out-of-fold SHAP values on the 2017–2018 training cohort (46 Underperforming, 43 Average, 88 Performing students) are stratified by **eventual** final-GPA group at each checkpoint S0–S6. This shows which features drive the model's predictions for each group of students and how those drivers evolve, supporting group-specific advisor guidance.

Groups are retrospective labels used only to stratify explanations; they are never model inputs. The training cohort is the explanation target because 2019 module grades are strongly inflated relative to 2017–2018 (compressed module variance would understate module signals); `external_check_family_importance.csv` retains the 2019 view for robustness.

## How to read the outputs

- `mean_abs_shap` within a group = how strongly a feature moves predictions for those students.
- `mean_shap` within a group = the typical direction (negative pushes predicted GPA down).
- ↓/↑ in the matrix below shows that typical direction for that group.
- Because groups are defined by eventual GPA, low grades mechanically push underperformers' predictions down; the value of the table is *which* features carry that signal at each checkpoint, i.e. what an advisor should look at first.
- Signed module SHAP is **conditional** attribution: with semester GPAs in the model, a correlated module can take a negative Ridge coefficient (multicollinearity suppression, e.g. StatsII at S3) and its arrow can invert the marginal association. For advisor-facing direction on individual modules, use the grade-band risk tables (`risk_tables/`).

## Advisor monitoring matrix (top-3 drivers per group)

| Semester | Underperforming | Average | Performing |
|---:|---|---|---|
| 0 | English ↓; Gender_M ↓; Department_BPM ↓ | Gender_M ↓; Department_BPM ↓; English ↓ | English ↑; Department_BPM ↑; Gender_M ↑ |
| 1 | S1 ↓; English ↓; Department_BPM ↓ | S1 ↓; English ↓; Department_BPM ↓ | S1 ↑; English ↑; Department_BPM ↑ |
| 2 | S2 ↓; S1 ↓; English ↓ | S2 ↓; S1 ↓; English ↓ | S2 ↑; S1 ↑; English ↑ |
| 3 | S3 ↓; S2 ↓; S1 ↓ | S1 ↓; S3 ↓; S2 ↓ | S3 ↑; S2 ↑; S1 ↑ |
| 4 | S4 ↓; S3 ↓; S1 ↓ | S4 ↓; S1 ↓; S3 ↓ | S4 ↑; S3 ↑; S1 ↑ |
| 5 | S5 ↓; S3 ↓; S4 ↓ | S5 ↓; S3 ↓; S1 ↓ | S3 ↑; S5 ↑; S4 ↑ |
| 6 | S3 ↓; S4 ↓; S6 ↓ | S3 ↓; S1 ↓; S4 ↓ | S3 ↑; S4 ↑; S1 ↑ |

## Files

- `group_shap_feature_importance.csv` / `group_shap_family_importance.csv`: per-group, per-checkpoint SHAP summaries (training, out-of-fold).
- `group_family_heatmap_<group>.png`: temporal family importance per group.
- `group_top_features_<group>.png`: top-10 feature evolution per group.
- `external_check_family_importance.csv`: 2019-cohort per-group family summary (robustness only; see cohort-shift caveat).
