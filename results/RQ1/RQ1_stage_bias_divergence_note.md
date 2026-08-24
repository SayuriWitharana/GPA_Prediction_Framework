# Why Stage-1 (CV) and Stage-2 (external) bias point in different directions

Written 2026-08-10, for the journal-length RQ1 writeup. This resolves a
question raised while re-checking the ICODE camera-ready numbers: Stage-1
cross-validation bias and Stage-2 external-test bias disagree in *sign* for
two of the three performance groups. This note explains why that is an
expected consequence of the two-stage design, not an inconsistency in it,
and gives the evidence to cite.

## The observation

Bias sign convention throughout this codebase: `bias = mean(actual − predicted)`.
Positive = under-prediction (model predicts too low); negative = over-prediction
(model predicts too high) — see `src/rq1/stage2_external_bootstrap.py` and
`notebooks/RQ1/archive/RidgeRegression2017-2018.ipynb`.

| Checkpoint | Group | Stage-1 CV bias (training cohort, out-of-fold) | Stage-2 external bias (2019 cohort) |
|---|---|---:|---:|
| S0 | High-performing | +0.184 (under) | — |
| S0 | Average | −0.003 (~0) | — |
| S0 | Underperforming | −0.361 (over) | — |
| S2 | High-performing | +0.044 (under) | −0.141 (over) |
| S2 | Average | +0.010 (under) | −0.337 (over) |
| S2 | Underperforming | −0.088 (over) | −0.466 (over) |
| S4 | High-performing | +0.018 (under) | −0.014 (~0) |
| S4 | Average | +0.011 (under) | −0.071 (over) |
| S4 | Underperforming | −0.044 (over) | −0.189 (over) |
| S6 | High-performing | +0.007 (~0) | +0.050 (under) |
| S6 | Average | +0.004 (~0) | +0.043 (under) |
| S6 | Underperforming | −0.008 (~0) | −0.023 (over) |

Full checkpoint-by-checkpoint values: `cv_results.csv` (Stage-1) and
`external_bootstrap_ci.csv` (Stage-2) in this folder.

**Underperforming is directionally consistent across both stages at every
checkpoint** — over-predicted in CV, over-predicted externally, converging
toward zero by S6. This is the paper's central at-risk-group finding and it
is unaffected by anything in this note.

**High-performing and Average flip sign**: mildly under-predicted in Stage-1,
over-predicted in Stage-2 for most checkpoints, only correcting back to
under-prediction at S6.

## Why: two different, independently-explainable effects, not one bug

**Stage-1's pattern is Ridge shrinkage toward the training cohort's own mean.**
Ridge regularization pulls coefficients — and therefore predictions — toward
the fitted intercept, which is anchored to the training cohort's mean GPA
(≈3.25 for 2017–2018). Students well above that mean get pulled down
(under-predicted, positive bias); students well below it get pulled up
(over-predicted, negative bias). Because Stage-1's folds are resampled from
the *same* cohort the model was fit on, this shrinkage-toward-own-mean effect
is what CV bias measures almost by construction. It is a textbook property of
regularized regression, not a data artefact — see Hoerl & Kennard (1970),
already cited in the paper for the choice of Ridge itself.

**Stage-2 adds a second, independent effect: real distributional drift between
the 2017–2018 and 2019 cohorts' semester-GPA columns**, on top of whatever
shrinkage the model already carries. Checked directly against the raw data
(`data/raw/2017-2018 TrainSet.xlsx`, `data/raw/2019 TestSet.xlsx`):

| Column | 2017–2018 mean | 2019 mean | Difference |
|---|---:|---:|---:|
| S2 | 3.116 | 3.590 | **+0.474** |
| S6 | 3.502 | 3.057 | **−0.445** |

Overall `FinalGPA` means are nearly identical between cohorts (3.25 vs 3.27),
so this is not a simple "the 2019 cohort did worse overall" story — it is a
semester-specific grading-pattern shift. The 2019 cohort's S2 marks were
unusually inflated relative to what a 2017–2018-trained model expects from
that input, so the model — correctly applying the 2017–2018 S2→FinalGPA
relationship — predicts higher FinalGPA than these students actually achieved,
producing the sharp over-prediction spike visible at S2 in the pooled external
bias (−0.265, the single worst pooled external checkpoint; see
`RQ1_reliability_interpretation.md`, "Overall (pooled) results" table). The
S6 column shows the opposite anomaly (2019 deflated relative to training),
consistent with external bias correcting back toward — and past — zero by S6.

This is the same phenomenon this project already documents for module grades
in RQ2's limitations ("Cohort shift in module grades... 2019 cohort shows
visibly inflated module grades relative to 2017–2018") — this note extends
that same, already-accepted cohort-shift explanation to semester GPA rather
than introducing a new one.

**For Underperforming, both effects point the same way** (shrinkage already
over-predicts this group; cohort shift does not reverse that), so no sign
flip occurs and Stage-1/Stage-2 agree throughout.

## Why this does not weaken the two-stage design — it is what the design is for

The paper's own findings already establish the precedent for treating Stage-2
as confirmatory over Stage-1 candidates, for the accuracy criterion: "external
validation revealed bias exceedance at both candidate semesters, advancing the
confirmed reliability point by one semester... demonstrating that bias-based
calibration failures remain undetected under accuracy-only evaluation." The
same logic extends cleanly to bias *direction*: Stage-1 alone would report
High-performing/Average students as safely (and only mildly) under-predicted;
Stage-2 reveals that on a genuinely unseen cohort they are instead
over-predicted — the higher-stakes error direction, since over-predicting
students who look safe is what produces false security. A reviewer should
read the divergence as evidence for why external validation is necessary, not
as an inconsistency in the method — the risk would be presenting only one
stage's bias numbers, or presenting both without explaining why they differ.

## Recommendation for the journal draft

1. Do not attempt to reconcile Stage-1 and Stage-2 bias into a single number —
   they measure different things (in-cohort resampling vs. true external
   generalization) and forcing agreement would misrepresent both.
2. Add a short paragraph or table footnote in the bias/equity subsection
   citing this divergence explicitly, with the shrinkage-vs-cohort-drift
   mechanism and the S2/S6 distributional evidence above.
3. Keep the Underperforming result as the primary equity claim — it is the
   one place Stage-1 and Stage-2 fully agree, and it is already the paper's
   central finding.
4. Cross-reference: the Stage-2 "S5" checkpoint in the original camera-ready
   Table I corresponds to what this codebase now labels S6 (cumulative GPA
   through six semesters, not five) — see the "Pipeline reconciliation note"
   and "S5 external evaluation" sections of `RQ1_reliability_interpretation.md`.
   Resolve that labeling before quoting Stage-2 S5 numbers in the journal
   draft, independently of the bias-direction question this note addresses.

## Source data

- Stage-1: `results/RQ1/cv_results.csv`, generated by `src/rq1/stage1_cv.py`.
- Stage-2: `results/RQ1/external_bootstrap_ci.csv`, generated by
  `src/rq1/stage2_external_bootstrap.py` (95% bootstrap CIs; point estimates used above).
- Cohort semester-GPA comparison: computed directly from
  `data/raw/2017-2018 TrainSet.xlsx` and `data/raw/2019 TestSet.xlsx`
  (`S1`–`S6` column means), not currently persisted as a script/CSV — worth
  adding as a small reusable script if this comparison is cited in the paper,
  so it's reproducible rather than a one-off check.
