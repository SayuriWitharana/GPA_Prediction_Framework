# RQ1 reliability framework: when are GPA predictions trustworthy?

## Design

Ridge regression (alpha = 1.0), fit separately at each checkpoint S0–S6 using only features available by that point: pre-academic (Zscore, English marks), demographics (Gender, Department, District, medium of instruction at A-level), and cumulative semester GPA up to that checkpoint. No module-level data is used in RQ1 — that is introduced only in RQ2, to keep RQ1 answering "when," using information every institution routinely has.

Same cohorts as RQ2: 2017–2018 training set (177 students) and the 2019 external test set (93 students). **Resolved 2026-08-23:** the raw `2017-2018 TrainSet.xlsx` has 178 rows because student `176001R` appears twice as an exact byte-for-byte duplicate (confirmed via `df.duplicated()`); RQ2's own training file never had this row duplicated, which is why RQ2's documentation always said 177. `src/rq1/cv.py` and `src/rq1/external_bootstrap.py` now call `.drop_duplicates()` immediately after loading this file, so RQ1 uses the same 177 unique students RQ2 does. Same preprocessing pipeline (`src/preprocessing.py`, `src/models.py`), and as of 2026-07-20 this is now literally the same shared `get_preprocessor()` function RQ2 imports too (see Pipeline reconciliation note below): median imputation with a missingness indicator, standard scaling for numeric features, most-frequent imputation plus one-hot encoding (rare categories grouped, `min_frequency=5`) for categorical features, district spelling/whitespace harmonised via `clean_categoricals()`, all fold-safe (fitted on training folds only).

Reliability is evaluated on the three axes named in the positioning document: **accuracy** (RMSE), **stability** (SD of RMSE across repeated CV), and **group-level directional bias**. Cross-validation is 5-fold repeated 10 times (50 folds total), stratified by final-GPA performance group, via `RepeatedStratifiedKFold` (`src/crossvalidation.py`). The 2019 cohort is evaluated once per checkpoint after CV, never used for tuning.

Performance groups (same definition used throughout RQ1 and RQ2): Underperforming (FinalGPA ≤ 2.99), Average (2.99–3.29), Performing (> 3.29).

**Multicollinearity check (justifies Ridge over OLS):** raw semester-GPA VIFs are very high (S1–S4 ≈ 170–200, since each semester GPA is highly correlated with the others). After centering, VIFs drop to 1.1–5.5. This is consistent with the RQ2 model audit's own justification for Ridge and should be cited once, not duplicated, across the paper.

## Overall (pooled) results — the headline reliability curve

Regenerated 2026-07-20 under the shared, unified `src/preprocessing.py`: CV columns from `src/rq1/cv.py`, pooled external columns computed directly (see script snippet referenced in the reconciliation note), per-group external columns from `src/rq1/external_bootstrap.py`.

**Full numbers (CV RMSE/RMSE SD/R²/bias, pooled and per group, every checkpoint):
see `results/RQ1/cv_summary_table.md`** — auto-generated from `cv_results.csv`
by `results/scripts/rq1/summary_table.py`, so it can't drift out of date the
way a hand-typed table here would. Re-run
`python -m results.scripts.rq1.summary_table` after any `cv.py` re-run.

The external (Stage-2) pooled figures now match RQ2's model-audit script almost exactly at every checkpoint (e.g. S0 0.434 here vs 0.434 in `model_comparison.csv`, S6 0.107 vs 0.102) — the residual RQ1-vs-RQ2 gap that remains is entirely attributable to RQ2 including module-grade features from S2 onward, not to any preprocessing difference. That confirms the unification worked.

Pooled R² is positive and rising at every checkpoint in both CV and the external cohort — this is the safe, defensible headline number for the paper's "when" claim. RMSE roughly halves between S0 and S3, and roughly halves again between S3 and S6. Pooled RMSE SD (fold-to-fold stability) does **not** fall as cleanly as RMSE itself — 0.063 at S0, dipping to 0.032 by S2, then bouncing between 0.035–0.040 through S3–S6 rather than continuing to shrink; the same non-monotonic pattern shows up in the Average group's stability discussed below, and is worth reading as one instance of the same phenomenon rather than two.

## Group-level results — and why group-level R² should not be reported as-is

Group RMSE and bias (GPA units) behave well and are safe to report. Group-level **R² does not**, for a specific, explainable statistical reason, not a modelling failure: R² divides by the variance of the *actual* outcome within that slice. The Average group is a narrow band by construction (2.99–3.29 GPA, a 0.3-point window), so its outcome variance is tiny — even small absolute errors then produce huge, unstable, often extremely negative R² (external test: as low as -28.3 at S0). Meanwhile the Average group's RMSE is consistently the lowest or second-lowest of the three groups. Report RMSE/bias for all groups; treat R² as pooled-only, or footnote it heavily if you must show it per group.

### Cross-validation (training cohort, out-of-fold) — re-verified 2026-07-20 under the unified preprocessor

Regenerated by `src/rq1/cv.py`. RMSE SD (fold-to-fold stability) is now included per group, since it is the criterion that actually determines each group's Stage-1 pass point in the three-criterion framework (`Final_Submission_Extended_Abstract.docx`), not just RMSE/bias.

**Full per-group CV table: see `results/RQ1/cv_summary_table.md`** (same
auto-generated file as the pooled table above — one unified table with
every checkpoint, every group, every metric). Two values worth flagging
inline since the paragraph below discusses them directly: Underperforming's
CV R² turns positive at S4 (**+0.292**), and Average's CV R² only turns
positive at S6 (**+0.334**), staying negative at every earlier checkpoint.

**Important nuance found during this re-run, relevant to the paper's Table II:** under the unified pipeline, the Average group's accuracy (RMSE well under 0.25 by S0) and bias (within ±0.10 from S0 onward) both look acceptable almost immediately — much earlier than "Semester 3," which is what the paper's Table II currently states as Average's Stage-1 CV pass point (sourced from `Final_Submission_Extended_Abstract.docx`'s narrative). The only criterion that could delay it is stability: Average's RMSE SD does not decline cleanly (0.032 → 0.035 → 0.025 → 0.023 → 0.032 → 0.022 → 0.019), bouncing at S1 and again at S4 before settling at S5–S6. Whether that counts as "not yet convergent" through S3 is a judgment call the three-criterion framework leaves subjective, not something this re-run can resolve definitively. This does not change the paper's confirmed reliability semester for Average (S4), which comes from the external Stage-2 bootstrap and is independent of this ambiguity — but if a reviewer asks about the Stage-1/S3 figure specifically, this is the honest answer.

### External test (2019 cohort) — updated 2026-07-20 after the preprocessing unification below

RMSE/bias regenerated by `src/rq1/external_bootstrap.py` (which now uses the shared, unified preprocessor) with 95% bootstrap confidence intervals; see `results/RQ1/external_bootstrap_ci.csv` for the full CI values used in the paper's Table III. **R² has not been recomputed** in this refresh — the R² column below is retained from the pre-unification run for reference only and should be treated as approximate; recompute before quoting R² externally again.

| Checkpoint | Group | RMSE | R² (pre-unification, approximate) | Bias |
|---|---|---:|---:|---:|
| S2 | High-performing | 0.202 | +0.010 | -0.141 |
| S2 | Underperforming | 0.593 | -2.563 | -0.466 |
| S2 | Average | 0.383 | -22.327 | -0.337 |
| S3 | High-performing | 0.134 | +0.538 | -0.074 |
| S3 | Underperforming | 0.411 | -0.777 | -0.278 |
| S3 | Average | 0.221 | -7.445 | -0.159 |
| S4 | High-performing | 0.091 | +0.809 | -0.014 |
| S4 | Underperforming | 0.295 | **+0.091** | -0.189 |
| S4 | Average | 0.143 | -2.383 | -0.071 |
| S5 | High-performing | 0.079 | +0.844 | -0.037 |
| S5 | Underperforming | 0.266 | +0.240 | -0.183 |
| S5 | Average | 0.128 | -1.843 | -0.083 |
| S6 | High-performing | 0.075 | +0.880 | +0.050 |
| S6 | Underperforming | 0.160 | +0.738 | -0.023 |
| S6 | Average | 0.095 | -0.444 | +0.043 |

S0/S1 rows are omitted here because they are unaffected by this refresh (see reconciliation note) — the pre-unification S0/S1 values already in this document's history remain valid; re-run `src/rq1/external_bootstrap.py` with those checkpoints added if you need them refreshed too.

**On the "R² starts negative, turns positive by the semesters we selected" claim:** true for the pooled model (positive from S0 onward — this framing doesn't even apply there); true for High-performing (positive from S2 CV / S3 external); **only true for Underperforming from S4 onward**, not S3 (CV -0.116 and external -0.777 at S3, per the pre-unification external run — see caveat above); **not true for Average**, whose R² is negative everywhere in CV except S6, and negative at every external checkpoint including S6. If the paper makes an "R² turns positive" claim, anchor it at **S4 for the at-risk group**, which is a more precise and arguably more useful claim for the paper's actual thesis (reliability differs by group, and knowing *when* it differs is the point of RQ1).

## S5 external evaluation (now filled in)

The notebook (`notebooks/RQ1/archive/RidgeRegression2017-2018.ipynb`) jumped from the S4 external-test cell straight to S6, skipping S5. Re-run using the identical `evaluate_on_test` logic already in that notebook: pooled 2019 RMSE = 0.165, R² = 0.882, bias = -0.090 (n=93). Group breakdown: Performing RMSE 0.082 / R² 0.844 (n=50); Underperforming RMSE 0.278 / R² 0.240 (n=24); Average RMSE 0.132 / R² -1.843 (n=19, restricted-range caveat applies as above). This confirms the S3→S5 narrative has external-cohort support at both semesters, and that Underperforming R² is positive by S4 and stays positive at S5 externally too, consistent with the CV pattern. Consider adding this cell back into the notebook itself so the source stays reproducible.

## Pipeline reconciliation note — resolved 2026-07-20

The RQ2 model-audit script (`src/rq2/rq2_module_model_audit.py`, output `model_comparison.csv`) and RQ1 used to define their preprocessing separately, and their numbers for the same conceptual "no-module baseline" were close but not identical (e.g. S0 external RMSE 0.434 vs 0.437). **This is now fixed at the source**, not just documented: both pipelines call the same `get_preprocessor()` / `clean_categoricals()` functions in `src/preprocessing.py`. RQ2's script was updated to import them instead of defining its own local `ColumnTransformer` (see `src/rq2/rq2_module_model_audit.py`), and RQ1's reproducible script (`src/rq1/external_bootstrap.py`) already used the shared module. The two remaining differences are structural, not accidental: RQ2 reads `DatasetWithModules_Training/Test.xlsx` (needed for module columns) while RQ1 reads `2017-2018 TrainSet.xlsx`/`2019 TestSet.xlsx`, and RQ2's feature set includes module grades from S2 onward while RQ1's never does — both by design, not by preprocessing drift. One incidental fix came out of the unification: both raw files contained un-stripped whitespace in District values ("Badulla ", "Kandy ") that neither pipeline had been stripping; `clean_categoricals()` now fixes this everywhere. Re-running RQ1's external evaluation under the unified pipeline changed numbers by roughly 0.005–0.015 GPA points per cell and did **not** change any pass/fail conclusion in the paper's Table II — the Underperforming group's Semester 6 confirmation is, if anything, more robust than before (its bootstrap CI no longer sits at the edge of the ±0.10 boundary). **The CV-side (Stage 1) numbers above have not yet been re-run under the unified pipeline** — see the flag on the CV table.

**2026-07-20 update:** RQ2's `I-we`/`I-ca` module outcomes were recoded from "missing/imputed" to fail-equivalent (grade point 1, one step above F=0) — see the RQ2 docs for the corrected module-grade findings this produced (a new StatsII "D or F" risk-table band at 91% underperformance rate, strengthened MgtAccounting/Maths 2/MIS/DataV SHAP signals). This recoding only touches module columns and does not affect any RQ1 number in this document, since RQ1 never uses module grades.

## Limitations

See the shared limitations section in `conferences/TALE_Research_Positioning_Updated.md` (sample size, single institution, cohort-shift, subgroup uncertainty) — apply it to RQ1 as well as RQ2; both share the same 177/93-student cohorts.

## Source notes

- `src/rq1/cv.py` and `src/rq1/external_bootstrap.py` are now the reproducible, unified-preprocessing source of truth for every number in this document (run with `python -m src.rq1.cv` / `python -m src.rq1.external_bootstrap`). Outputs: `cv_results.csv` and `external_bootstrap_ci.csv` in this folder.
- `notebooks/RQ1/archive/RidgeRegression2017-2018.ipynb` is the original canonical RQ1 notebook this document was first based on; it predates the preprocessing unification and its cell outputs are now superseded by the two scripts above.
- `notebooks/RQ1/model_comparison/baselineModels.ipynb` and `randomForest.ipynb` document the Ridge-vs-Random-Forest comparison that justified this document's choice of Ridge — different dataset (`TotalDataSet.xlsx`), fewer features (no English marks), not re-runnable against current data. Cite them for the model-selection methodology; do not cite them as the source of any number in this document.
- `RQ1_RMSE_Stability.png`, `RQ1_R2_Trend.png`, `RQ1_Bias_Trend.png` (this folder): group-level CV plots, regenerated 2026-07-20 directly from `cv_results.csv` (unified pipeline). `RQ1_R2_Trend.png` marks the Average group's line as a restricted-range caution rather than presenting it at face value. `notebooks/resultPlots.ipynb` contains an older, pre-unification version of these plots and can be treated as superseded.
