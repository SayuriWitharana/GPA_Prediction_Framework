# Reading guide: understanding the RQ1/RQ2 workflow and the TALE paper

This is the order to read things in, going from "why this exists" down to the
actual code, so nothing later is a mystery. Written 2026-07-20.

## 1. Orientation (10 min) — read, don't run

- `conferences/TALE_Research_Positioning_Updated.md` — the whole project's
  thesis: why "when/why/how trustworthy" instead of "best accuracy," how RQ1
  and RQ2 relate, plus the Limitations section.
- `conferences/Literature_Review_Trustworthy_Learning_Analytics.md` — skip
  the 24 paper summaries, read only Section 2 (Thematic Synthesis) and
  Section 4 (Gaps). That's where "nobody combines reliability +
  explainability + fairness" comes from — it's now directly in the paper's
  Related Work.

## 2. Shared building blocks (10 min) — small, reused everywhere

- `src/preprocessing.py` — the imputation/scaling/encoding pipeline every
  model uses.
- `src/models.py` — Ridge and Random Forest pipeline definitions (note the
  comment block explaining why alpha=1.0 is fixed).
- `src/crossvalidation.py` — the 5-fold × 10-repeat stratified CV setup used
  everywhere "50 splits" is mentioned.

These three files are tiny but everything downstream imports them — read
them first so nothing later is a mystery function.

## 3. RQ1: the reliability framework

- `notebooks/RidgeRegression2017-2018.ipynb` — the canonical notebook. This
  is where the actual per-semester models get fit and the raw
  RMSE/R²/bias numbers come from (both cross-validation and the 2019
  external test). It's long; skim the code, read the markdown
  interpretation cells between sections.
- `notebooks/rq1_reliability/RQ1_reliability_interpretation.md` — the
  write-up synthesizing that notebook's numbers, including the corrected
  R² framing and the pipeline-reconciliation note (why this notebook's
  numbers differ slightly from RQ2's audit script).
- `src/rq1_external_bootstrap.py` — bootstraps 95% confidence intervals for
  the Stage-2 external-cohort RMSE/bias per group per semester. Run it
  yourself (`python -m src.rq1_external_bootstrap`) to see it reproduce
  the paper's Table III live. Output: `notebooks/rq1_reliability/external_bootstrap_ci.csv`.

**Note:** the *specific* three-criterion framework in the paper
(RMSE ≤ 0.25/0.35, |bias| ≤ 0.10, stability convergence) comes from
`conferences/Final_Submission_Extended_Abstract.docx` — the other paper
under review — not from a script in this repo. Read that docx too; it's
short (2 pages) and it's the actual source of the per-group threshold
logic.

## 4. RQ2: the SHAP pipeline

Read these five scripts in this exact order — they import from each other:

1. `src/shap/rq2_module_model_audit.py` — loads data, defines the module
   grade-point scale (**this is where the F=0/I-we=1 recoding lives**, in
   `GRADE_POINTS`), picks Ridge vs Random Forest, writes
   `RQ2_pre_SHAP_interpretation.md`.
2. `src/shap/rq2_linear_shap.py` — imports from #1; computes out-of-fold
   SHAP per semester, writes the linear-SHAP doc and family heatmap.
3. `src/shap/rq2_group_shap.py` — imports from #2; splits SHAP by the
   three performance groups.
4. `src/shap/rq2_underperformance_shap.py` — imports from #2; the
   bootstrap+FDR early-warning signal test.
5. `src/shap/rq2_risk_tables.py` — imports from #1; the grade-band advisor
   tables (StatsII 91% finding lives here).

For each script, its matching `.md` doc sits next to its outputs in
`notebooks/shap/rq2_module_audit/...` — read the script, then immediately
read the doc it produces, rather than reading all five scripts and then
all five docs.

## 5. The paper itself

- `conferences/TALE2026_Paper_Draft.docx` — read this last. Everything
  above is the evidence; this is the argument built from it. Reading it
  last means every number in it will already make sense.

## What's not written down anywhere except the chat history

Two decisions only existed in conversation, not in any doc, as of when
this guide was written: (a) why I-we/I-ca became fail-equivalent rather
than missing (reasoning: a re-attempt next year doesn't erase what the
record showed at prediction time), and (b) the S5-vs-S6 labeling
reconciliation between this paper and the other one. Both are already
written into the paper's own text and the RQ1 doc's notes, so the chat
history isn't needed to understand the *current* files — but if a
standalone decisions-log doc would help, ask for one.
