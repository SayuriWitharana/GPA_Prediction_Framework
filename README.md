# GPA Prediction Framework

[![Tests](https://github.com/SayuriWitharana/GPA_Prediction_Framework/actions/workflows/tests.yml/badge.svg)](https://github.com/SayuriWitharana/GPA_Prediction_Framework/actions/workflows/tests.yml)

Predicting undergraduate final GPA from academic records, with two research
questions:

- **RQ1 — Reliability**: at each checkpoint from pre-university entry data
  through Semester 6, how accurate and unbiased is a GPA prediction, and
  does that reliability hold for underperforming students specifically —
  not just on average?
- **RQ2 — Explainability & fairness**: using SHAP, which features actually
  drive those predictions, how does that change by performance group and
  over time, and are there fairness concerns (e.g. demographic features
  showing up as early drivers)?

Full context on why this project exists and how RQ1/RQ2 relate:
[`READING_GUIDE.md`](READING_GUIDE.md).

## Setup

```bash
pip install -r requirements.txt
nbstripout --install   # one-time, strips notebook outputs on commit
```

`data/` is gitignored (student records) — place the raw `.xlsx` files in
`data/raw/` separately; they aren't in this repository.

## Quickstart — reproducing RQ1

```bash
python -m src.rq1.cv                        # Stage 1: 50-fold CV, S0-S6
python -m src.rq1.external_bootstrap         # Stage 2: 2019 external cohort, bootstrap CIs
python -m results.scripts.rq1.summary_table  # clean per-group metrics tables
python -m results.scripts.rq1.eda_plot       # FinalGPA distribution chart
```

Outputs land in `results/RQ1/`. See the
[Quickstart section of READING_GUIDE.md](READING_GUIDE.md#quickstart-reproducing-rq1s-results)
for the full runbook, including the one notebook that still needs manual
execution and known reproducibility gaps.

## Running RQ2 - In-Progress

```bash
python -m src.rq2.rq2_module_model_audit
python -m src.rq2.rq2_linear_shap
python -m src.rq2.rq2_group_shap
python -m src.rq2.rq2_underperformance_shap
python -m src.rq2.rq2_risk_tables
```

Run in this order — each later script imports from an earlier one. Outputs
land in `results/RQ2/`.

## Tests

```bash
python -m pytest tests/
```

Runs automatically on every pull request into `main`
(`.github/workflows/tests.yml`).

## Layout

```
src/            importable pipeline code — preprocessing, models, CV
                shared by both RQs; src/rq1/ and src/rq2/ hold each RQ's
                own scripts
notebooks/      exploration notebooks, grouped by RQ into EDA/,
                model_comparison/, and archive/ (superseded, kept for
                provenance)
results/        generated artifacts — csv/png/md outputs under RQ1/ and
                RQ2/, plus scripts/ for the reporting code that draws
                charts from them
data/raw/       not in git — see Setup
tests/          pytest suite for the pure-logic pieces
```

## Documentation

- [`READING_GUIDE.md`](READING_GUIDE.md) — full onboarding: what to read
  first, the RQ1/RQ2 workflow end to end, and a Quickstart runbook.
- `results/RQ1/RQ1_reliability_interpretation.md` — the RQ1 findings,
  synthesized from `cv_results.csv` and `external_bootstrap_ci.csv`.
- `results/RQ2/**/RQ2_*_interpretation.md` — one write-up per RQ2 script,
  sitting next to the outputs it explains.
