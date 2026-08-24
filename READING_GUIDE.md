# Reading guide: understanding the RQ1/RQ2 workflow and the TALE paper

This is the order to read things in, going from "why this exists" down to the
actual code, so nothing later is a mystery. Written 2026-07-20.

## Quickstart: reproducing RQ1's results

For someone who just wants to run the pipeline, not read about it first.

**0. Data isn't in git.** `data/` is gitignored (student records). A fresh
clone has no `.xlsx` files — get `2017-2018 TrainSet.xlsx` and
`2019 TestSet.xlsx` separately and place them in `data/raw/`. Then
`pip install -r requirements.txt`, and run `nbstripout --install` once —
this wires up the git filter that strips notebook outputs on commit
(`.gitattributes` declares it; the local git config it needs is per-clone,
so every fresh clone has to run this once).

**1. Run these five commands, from the repo root, in this order:**

| # | Command | Needs | Produces |
|---|---|---|---|
| 1 | `python -m src.rq1.stage1_cv` | TrainSet.xlsx | `results/RQ1/cv_results.csv` |
| 2 | `python -m src.rq1.stage2_external_bootstrap` | TrainSet.xlsx + TestSet.xlsx | `results/RQ1/external_bootstrap_ci.csv` |
| 3 | `python -m results.scripts.rq1.stage1_summary_table` | output of #1 | `results/RQ1/cv_summary_table.md` |
| 4 | `python -m results.scripts.rq1.stage2_summary_table` | output of #2 | `results/RQ1/external_summary_table.md` |
| 5 | `python -m results.scripts.rq1.eda_plot` | TrainSet.xlsx | `results/RQ1/ICODE_EDA_Summary.png` |

Two real dependencies: #3 needs #1, #4 needs #2, both already run. #2 and
#5 are independent of everything else. All five run in seconds.

**2. One notebook still needs manual execution:**
`results/scripts/rq1/plots_for_ICODE.ipynb` — open in Jupyter, run all
cells. Produces `ICODE_RMSE_Trend.png`, `ICODE_Stability_Trend.png`,
`ICODE_Bias_Trend.png`, `ICODE_Convergence_3Panel.png`,
`ICODE_Convergence_Grid.png` in `results/RQ1/`. It plots **hand-transcribed
values from the paper's Table I**, not a live read of `cv_results.csv` — if
step 1 ever produces different numbers, this notebook needs manual
resyncing, it will not pick up the change automatically. (Checked 2026-08-23:
51/63 of its hardcoded cells are within 0.01 of the current pipeline —
expected drift from the preprocessing-unification documented below — but
two aren't: S2 Average Bias is off by 0.096, and S3 High-performing Bias
has flipped sign, +0.027 now vs. −0.028 hardcoded. Worth checking before
presenting that chart.)

**3. Then read, don't run:** `results/RQ1/RQ1_reliability_interpretation.md`
and `RQ1_stage_bias_divergence_note.md` (the narrative conclusions),
`results/RQ1/cv_summary_table.md` (the clean per-group tables from step 3).
`notebooks/RQ1/model_comparison/{baselineModels,randomForest}.ipynb`
**cannot be re-run** — they read `TotalDataSet.xlsx`, which no longer
exists in `data/raw/` — they're read-only evidence for the "why Ridge, not
Random Forest" decision.

**Known gap:** `RQ1_RMSE_Stability.png`, `RQ1_R2_Trend.png`,
`RQ1_Bias_Trend.png`, and `ICODE_Pooled_Convergence_3Panel.png` in
`results/RQ1/` have **no script that regenerates them** — static leftovers
from an earlier one-off plotting session. Rebuilding from scratch won't
bring these back without new plotting code.

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

RQ1 lives under `src/rq1/` as a package. `src/rq1/config.py` (checkpoint
feature sets, categorical columns, group cutoffs) and `src/rq1/groups.py`
(`assign_perf_group`) are the shared building blocks every RQ1 script below
imports from — read those two first.

- `src/rq1/stage1_cv.py` — Stage-1: repeated stratified 5-fold CV (50 splits) at
  each checkpoint S0-S6, computing pooled and per-group RMSE/R²/bias. Run it
  yourself (`python -m src.rq1.stage1_cv`). Output:
  `results/RQ1/cv_results.csv`.
- `src/rq1/stage2_external_bootstrap.py` — Stage-2: trains on the full 2017-2018
  cohort, evaluates once on the 2019 cohort, and bootstraps 95% confidence
  intervals for the external RMSE/bias per group per semester, S0-S6 (originally
  scoped to S2-S6 to match the paper's Table III, extended 2026-08-24 — there
  was no technical reason to exclude S0/S1, the paper just never reported
  them). Run it yourself (`python -m src.rq1.stage2_external_bootstrap`) to
  see it reproduce the paper's Table III live. Output:
  `results/RQ1/external_bootstrap_ci.csv`.
- `results/scripts/rq1/eda_plot.py` — generates the FinalGPA distribution /
  by-group chart used in the ICODE presentation. Draws from already-loaded
  raw data rather than computing pipeline results, so it lives alongside the
  other reporting scripts rather than in `src/rq1/`. Run with
  `python -m results.scripts.rq1.eda_plot`. Output:
  `results/RQ1/ICODE_EDA_Summary.png`.
- `results/scripts/rq1/plots_for_ICODE.ipynb` — the notebook that draws the
  remaining `ICODE_*.png` conference figures from hardcoded paper-table
  values (not from `cv_results.csv` directly — see the note at the top of
  its first cell). Outputs land in `results/RQ1/`.
- `results/scripts/rq1/stage1_summary_table.py` — regenerates
  `results/RQ1/cv_summary_table.md`, one clean table with every Stage-1
  metric (RMSE, RMSE SD, R², bias) for the pooled model and all three
  performance groups, one block per checkpoint S0-S6. Run with
  `python -m results.scripts.rq1.stage1_summary_table` any time `cv_results.csv`
  changes — this is the up-to-date source for "all metrics per semester,"
  not the hand-typed tables that used to live in the interpretation doc.
- `results/scripts/rq1/stage2_summary_table.py` — the Stage-2 counterpart:
  regenerates `results/RQ1/external_summary_table.md`, one table per
  performance group (no Pooled section — Stage 2 never bootstraps a pooled
  CI) with RMSE, its 95% CI, bias, and its 95% CI, S0-S6. Run with
  `python -m results.scripts.rq1.stage2_summary_table` any time
  `external_bootstrap_ci.csv` changes.
- `results/RQ1/RQ1_reliability_interpretation.md` — the write-up
  synthesizing those two scripts' numbers, including the corrected R²
  framing and the pipeline-reconciliation note (why these numbers differ
  slightly from RQ2's audit script). Points at `cv_summary_table.md` and
  `external_summary_table.md` for the full numbers rather than repeating
  them inline.
- `notebooks/RQ1/EDA/` — the exploratory notebooks on RQ1's own raw
  datasets (`eda 2017-2018.ipynb`, `eda 2019.ipynb`); `eda 2019.ipynb` is
  where the performance-group GPA thresholds were originally worked out.
- `notebooks/RQ1/model_comparison/` — `baselineModels.ipynb` and
  `randomForest.ipynb`, the Ridge-vs-Random-Forest baseline comparison that
  justified choosing Ridge for the rest of RQ1 (Random Forest underperformed
  Ridge, especially in early semesters — see `randomForest.ipynb`'s closing
  cell for the explicit conclusion). Not part of the live pipeline (no
  script re-runs this comparison), but kept active rather than archived
  since it's part of the RQ1 methodology, not dead code.
- `notebooks/RQ1/archive/` — superseded RQ1 notebooks kept for provenance
  only, not maintained and not where current numbers come from:
  `RidgeRegression2017-2018.ipynb` (the original notebook `stage1_cv.py`
  and `stage2_external_bootstrap.py` were extracted from — per-semester code was
  copy-pasted seven times), `featureEngineering.ipynb`, `resultPlots.ipynb`,
  and an earlier snapshot `eda 2019 - Copy.ipynb`.

**Note:** the *specific* three-criterion framework in the paper
(RMSE ≤ 0.25/0.35, |bias| ≤ 0.10, stability convergence) comes from
`conferences/Final_Submission_Extended_Abstract.docx` — the other paper
under review — not from a script in this repo. Read that docx too; it's
short (2 pages) and it's the actual source of the per-group threshold
logic.

## 4. RQ2: the SHAP pipeline

RQ2 lives under `src/rq2/` as a package (each script keeps its historical
`rq2_` filename prefix for clarity). Same invocation convention as RQ1 now:
run each with `python -m src.rq2.<script name>` from the repo root — e.g.
`python -m src.rq2.rq2_module_model_audit`. They chain-import each other via
proper package imports (`from src.rq2.rq2_module_model_audit import ...`),
not bare module names, so this is the only way to run them; running a
script by direct path (`python src/rq2/rq2_linear_shap.py`) will fail with
an import error. Read these five scripts in this exact order — they import
from each other:

1. `src/rq2/rq2_module_model_audit.py` — loads data, defines the module
   grade-point scale (**this is where the F=0/I-we=1 recoding lives**, in
   `GRADE_POINTS`), picks Ridge vs Random Forest, writes
   `RQ2_pre_SHAP_interpretation.md`. Run first — the other four import
   constants and helper functions from it.
2. `src/rq2/rq2_linear_shap.py` — imports from #1; computes out-of-fold
   SHAP per semester, writes the linear-SHAP doc and family heatmap.
3. `src/rq2/rq2_group_shap.py` — imports from #2; splits SHAP by the
   three performance groups.
4. `src/rq2/rq2_underperformance_shap.py` — imports from #2; the
   bootstrap+FDR early-warning signal test.
5. `src/rq2/rq2_risk_tables.py` — imports from #1; the grade-band advisor
   tables (StatsII 91% finding lives here).

For each script, its matching `.md` doc sits next to its outputs in
`results/RQ2/...` — read the script, then immediately read the doc it
produces, rather than reading all five scripts and then all five docs.
`notebooks/RQ2/EDA/edaWithModules.ipynb` is the exploratory notebook on the
module dataset; `notebooks/RQ2/archive/randomForest_WithModules.ipynb` is
RQ2's superseded RF-vs-Ridge baseline (kept for provenance, not maintained).

**Note:** `results/RQ2/group_shap/RQ2_group_SHAP_interpretation.md` carries
a hand-written "Fairness note" section that `rq2_group_shap.py` does not
generate — the file itself flags this. Re-add that section manually after
re-running the script, or it will be lost.

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
