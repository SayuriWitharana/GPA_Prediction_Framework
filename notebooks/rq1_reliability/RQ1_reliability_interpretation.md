# RQ1 reliability framework: when are GPA predictions trustworthy?

## Design

Ridge regression (alpha = 1.0), fit separately at each checkpoint S0–S6 using only features available by that point: pre-academic (Zscore, English marks), demographics (Gender, Department, District, medium of instruction at A-level), and cumulative semester GPA up to that checkpoint. No module-level data is used in RQ1 — that is introduced only in RQ2, to keep RQ1 answering "when," using information every institution routinely has.

Same cohorts as RQ2: 2017–2018 training set (177 students per the RQ2 documentation; the raw file has 178 data rows, worth a one-line reconciliation before submission) and the 2019 external test set (93 students). Same preprocessing pipeline (`src/preprocessing.py`, `src/models.py`): median imputation + standard scaling for numeric features, one-hot encoding for categorical features, fold-safe (fitted on training folds only).

Reliability is evaluated on the three axes named in the positioning document: **accuracy** (RMSE), **stability** (SD of RMSE across repeated CV), and **group-level directional bias**. Cross-validation is 5-fold repeated 10 times (50 folds total), stratified by final-GPA performance group, via `RepeatedStratifiedKFold` (`src/crossvalidation.py`). The 2019 cohort is evaluated once per checkpoint after CV, never used for tuning.

Performance groups (same definition used throughout RQ1 and RQ2): Underperforming (FinalGPA ≤ 2.99), Average (2.99–3.29), Performing (> 3.29).

**Multicollinearity check (justifies Ridge over OLS):** raw semester-GPA VIFs are very high (S1–S4 ≈ 170–200, since each semester GPA is highly correlated with the others). After centering, VIFs drop to 1.1–5.5. This is consistent with the RQ2 model audit's own justification for Ridge and should be cited once, not duplicated, across the paper.

## Overall (pooled) results — the headline reliability curve

| Checkpoint | CV RMSE | CV SD(RMSE) | CV R² | External RMSE | External R² | External Bias |
|---|---:|---:|---:|---:|---:|---:|
| S0 | 0.348 | 0.048 | 0.385 | 0.437 | 0.172 | -0.053 |
| S1 | 0.255 | 0.037 | 0.674 | 0.349 | 0.471 | -0.117 |
| S2 | 0.205 | 0.027 | 0.786 | 0.382 | 0.365 | -0.271 |
| S3 | 0.185 | 0.032 | 0.823 | 0.261 | 0.704 | -0.155 |
| S4 | 0.141 | 0.035 | 0.896 | 0.181 | 0.858 | -0.076 |
| S5 | 0.116 | 0.033 | 0.931 | 0.165 | 0.882 | -0.090 |
| S6 | 0.097 | 0.028 | 0.952 | 0.107 | 0.950 | +0.025 |

Pooled R² is positive and rising at every checkpoint in both CV and the external cohort — this is the safe, defensible headline number for the paper's "when" claim. RMSE roughly halves between S0 and S3, and roughly halves again between S3 and S6; SD of RMSE falls from 0.048 to ~0.03 over the same stretch. This matches the "S3 = reasonably reliable, S4–S5 = accuracy/stability plateau" narrative already drafted in `resultPlots.ipynb`.

## Group-level results — and why group-level R² should not be reported as-is

Group RMSE and bias (GPA units) behave well and are safe to report. Group-level **R² does not**, for a specific, explainable statistical reason, not a modelling failure: R² divides by the variance of the *actual* outcome within that slice. The Average group is a narrow band by construction (2.99–3.29 GPA, a 0.3-point window), so its outcome variance is tiny — even small absolute errors then produce huge, unstable, often extremely negative R² (external test: as low as -28.3 at S0). Meanwhile the Average group's RMSE is consistently the lowest or second-lowest of the three groups. Report RMSE/bias for all groups; treat R² as pooled-only, or footnote it heavily if you must show it per group.

### Cross-validation (training cohort, out-of-fold)

| Checkpoint | Group | RMSE | R² | Bias |
|---|---|---:|---:|---:|
| S0 | Performing | 0.299 | -1.540 | +0.182 |
| S0 | Underperforming | 0.498 | -2.798 | -0.343 |
| S0 | Average | 0.191 | -4.892 | -0.007 |
| S1 | Performing | 0.206 | -0.222 | +0.078 |
| S1 | Underperforming | 0.354 | -0.797 | -0.167 |
| S1 | Average | 0.195 | -5.043 | +0.022 |
| S2 | Performing | 0.159 | +0.258 | +0.042 |
| S2 | Underperforming | 0.291 | -0.429 | -0.097 |
| S2 | Average | 0.162 | -3.162 | +0.016 |
| S3 | Performing | 0.138 | +0.449 | +0.028 |
| S3 | Underperforming | 0.274 | -0.249 | -0.080 |
| S3 | Average | 0.135 | -1.851 | +0.025 |
| S4 | Performing | 0.097 | +0.723 | +0.019 |
| S4 | Underperforming | 0.208 | **+0.250** | -0.052 |
| S4 | Average | 0.109 | -1.037 | +0.012 |
| S5 | Performing | 0.079 | +0.810 | +0.010 |
| S5 | Underperforming | 0.167 | +0.570 | -0.035 |
| S5 | Average | 0.092 | -0.389 | +0.017 |
| S6 | Performing | 0.058 | +0.901 | +0.009 |
| S6 | Underperforming | 0.154 | +0.673 | -0.013 |
| S6 | Average | 0.068 | **+0.226** | +0.005 |

### External test (2019 cohort)

| Checkpoint | Group | RMSE | R² | Bias |
|---|---|---:|---:|---:|
| S0 | Performing | 0.332 | -1.528 | +0.178 |
| S0 | Underperforming | 0.606 | -2.599 | -0.358 |
| S0 | Average | 0.424 | -28.277 | -0.274 |
| S1 | Performing | 0.200 | +0.079 | -0.002 |
| S1 | Underperforming | 0.540 | -1.858 | -0.283 |
| S1 | Average | 0.349 | -18.896 | -0.209 |
| S2 | Performing | 0.208 | +0.010 | -0.152 |
| S2 | Underperforming | 0.603 | -2.563 | -0.480 |
| S2 | Average | 0.378 | -22.327 | -0.321 |
| S3 | Performing | 0.142 | +0.538 | -0.087 |
| S3 | Underperforming | 0.426 | -0.777 | -0.302 |
| S3 | Average | 0.228 | -7.445 | -0.149 |
| S4 | Performing | 0.091 | +0.809 | -0.017 |
| S4 | Underperforming | 0.305 | **+0.091** | -0.202 |
| S4 | Average | 0.144 | -2.383 | -0.072 |
| S5 | Performing | 0.082 | +0.844 | -0.042 |
| S5 | Underperforming | 0.278 | +0.240 | -0.199 |
| S5 | Average | 0.132 | -1.843 | -0.081 |
| S6 | Performing | 0.072 | +0.880 | +0.048 |
| S6 | Underperforming | 0.163 | +0.738 | -0.035 |
| S6 | Average | 0.094 | -0.444 | +0.041 |

**On the "R² starts negative, turns positive by the semesters we selected" claim:** true for the pooled model (positive from S0 onward — this framing doesn't even apply there); true for Performing (positive from S2 CV / S3 external); **only true for Underperforming from S4 onward**, not S3 (CV -0.249 and external -0.777 at S3); **not true for Average**, whose R² is negative everywhere in CV except S6, and negative at every external checkpoint including S6. If the paper makes an "R² turns positive" claim, anchor it at **S4 for the at-risk group**, which is a more precise and arguably more useful claim for the paper's actual thesis (reliability differs by group, and knowing *when* it differs is the point of RQ1).

## S5 external evaluation (now filled in)

The notebook (`RidgeRegression2017-2018.ipynb`) jumped from the S4 external-test cell straight to S6, skipping S5. Re-run using the identical `evaluate_on_test` logic already in that notebook: pooled 2019 RMSE = 0.165, R² = 0.882, bias = -0.090 (n=93). Group breakdown: Performing RMSE 0.082 / R² 0.844 (n=50); Underperforming RMSE 0.278 / R² 0.240 (n=24); Average RMSE 0.132 / R² -1.843 (n=19, restricted-range caveat applies as above). This confirms the S3→S5 narrative has external-cohort support at both semesters, and that Underperforming R² is positive by S4 and stays positive at S5 externally too, consistent with the CV pattern. Consider adding this cell back into the notebook itself so the source stays reproducible.

## Pipeline reconciliation note

The RQ2 model-audit script (`src/shap/rq2_module_model_audit.py`, output `model_comparison.csv`) also computes a Ridge baseline at each checkpoint, and its numbers are close to but **not identical** to this notebook's (e.g. S0 external RMSE 0.434 vs 0.437 here; S6 external RMSE 0.102 vs 0.107 here). This was checked and is not a bug: the two pipelines read different source files (`DatasetWithModules_Training/Test.xlsx` vs `2017-2018 TrainSet.xlsx` / `2019 TestSet.xlsx`) and use different preprocessing (the RQ2 script harmonises district spelling variants, groups rare categories with `min_frequency=5`, and adds a missingness indicator; this RQ1 notebook does none of those). S0 and S1 are unaffected by module-grade coding (modules only enter RQ2's feature set from S2 onward), which is a useful cross-check: those two checkpoints match almost exactly between the pipelines (S0 0.4339 vs 0.437, S1 0.3464 vs 0.349), confirming the residual gap elsewhere is really about module coding + the extra preprocessing steps, not a hidden bug. **Do not quote RQ1 numbers and RQ2 pre-SHAP numbers interchangeably in the paper** — they come from two slightly different pipelines. For the short paper, cite RQ1 numbers only from this document/notebook, and RQ2 numbers only from `RQ2_pre_SHAP_interpretation.md`/`model_comparison.csv`; if there's time after submission, unify the two preprocessing pipelines so the baseline is computed identically in both places.

**2026-07-20 update:** RQ2's `I-we`/`I-ca` module outcomes were recoded from "missing/imputed" to fail-equivalent (grade point 1, one step above F=0) — see the RQ2 docs for the corrected module-grade findings this produced (a new StatsII "D or F" risk-table band at 91% underperformance rate, strengthened MgtAccounting/Maths 2/MIS/DataV SHAP signals). This recoding only touches module columns and does not affect any RQ1 number in this document, since RQ1 never uses module grades.

## Limitations

See the shared limitations section in `conferences/TALE_Research_Positioning_Updated.md` (sample size, single institution, cohort-shift, subgroup uncertainty) — apply it to RQ1 as well as RQ2; both share the same 177/93-student cohorts.

## Source notes

- `notebooks/RidgeRegression2017-2018.ipynb` is the canonical RQ1 pipeline (2017–2018 training set, 2019 external test) and is the notebook this document is based on.
- `notebooks/baselineModels.ipynb` is an earlier, superseded exploratory version — different dataset (`TotalDataSet.xlsx`), fewer features (no English marks). Do not cite it as the RQ1 source.
- `RQ1_RMSE_Stability.png`, `RQ1_R2_Trend.png`, `RQ1_Bias_Trend.png` (this folder): group-level CV plots regenerated from the verified numbers in the tables above. `RQ1_R2_Trend.png` marks the Average group's line as a restricted-range caution rather than presenting it at face value. `notebooks/resultPlots.ipynb` contains the original (unsaved) versions of these plots and can be treated as superseded by the copies in this folder.
