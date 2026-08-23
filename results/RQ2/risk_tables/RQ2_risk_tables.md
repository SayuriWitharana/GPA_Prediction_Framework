# Advisor-facing risk tables: grade bands and eventual underperformance

## Purpose and design

For every early feature available by semester 5, this table reports the observed share of students who ultimately finished with final GPA <= 2.99 (Underperforming), per grade band, on the 2017-2018 training cohort (177 students; base rate 26%). Lift is the band's rate divided by the base rate.

The 2019 cohort (93 students) is shown only as a sanity check. Its module grades are strongly inflated relative to 2017-2018 (e.g. 70% of Maths 2 grades are A/A+ versus 16% in training), so its low-grade bands are thin or empty and its rates are not comparable band-by-band.

These are descriptive associations in small cohorts — several bands hold fewer than 10 students (counts are always shown). They indicate which students an advisor should look at more closely; they are not causal claims and must never trigger automated designation of a student as at risk.

## Bands that stand out (>= 10 students and >= 1.5x base rate)

- From semester 0: **English in band "Q1 (lowest, <= 41)"** — 52% underperformance rate (24/46 students; 2.0x the 26% base rate).
- From semester 0: **Zscore in band "Q1 (lowest, <= 1.5216)"** — 42% underperformance rate (19/45 students; 1.6x the 26% base rate).
- From semester 1: **S1 in band "Below 2.70"** — 88% underperformance rate (30/34 students; 3.4x the 26% base rate).
- From semester 2: **S2 in band "Below 2.70"** — 86% underperformance rate (37/43 students; 3.3x the 26% base rate).
- From semester 2: **MgtAccounting in band "C- to C+"** — 62% underperformance rate (33/53 students; 2.4x the 26% base rate).
- From semester 2: **Maths 2 in band "C- to C+"** — 47% underperformance rate (36/77 students; 1.8x the 26% base rate).
- From semester 3: **StatsII in band "D or F"** — 91% underperformance rate (10/11 students; 3.5x the 26% base rate).
- From semester 3: **S3 in band "Below 2.70"** — 88% underperformance rate (37/42 students; 3.4x the 26% base rate).
- From semester 3: **StatsII in band "C- to C+"** — 49% underperformance rate (27/55 students; 1.9x the 26% base rate).
- From semester 3: **MIS in band "C- to C+"** — 43% underperformance rate (6/14 students; 1.6x the 26% base rate).
- From semester 3: **MIS in band "B- to B+"** — 40% underperformance rate (21/52 students; 1.6x the 26% base rate).
- From semester 4: **S4 in band "Below 2.70"** — 96% underperformance rate (22/23 students; 3.7x the 26% base rate).
- From semester 4: **S4 in band "2.70-2.99"** — 67% underperformance rate (16/24 students; 2.6x the 26% base rate).
- From semester 5: **S5 in band "Below 2.70"** — 75% underperformance rate (30/40 students; 2.9x the 26% base rate).
- From semester 5: **S5 in band "2.70-2.99"** — 48% underperformance rate (12/25 students; 1.8x the 26% base rate).

## How advisors can use this

- Pre-entry (S0): Zscore and English bands flag students for light-touch monitoring from day one.
- After each semester, check newly available bands: semester GPA bands plus the modules completed that semester (S2: Maths 2, MgtAccounting; S3: StatsII, MIS; S4: DataV).
- "I-we"/"I-ca" outcomes (did not sit the exam or did not complete the continuous-assessment component) are coded as fail-equivalent and appear inside the "D or F" band above, not as a separate category.
- Combine with the SHAP early-warning signals (`linear_shap/underperformance/`): a student in a high-lift band whose profile also carries negative SHAP signals is a priority for advisor review.

## Files

- `risk_tables.csv`: full band-level table (training rates, lift, 2019 sanity-check columns).
- `risk_by_grade_band.png`: training-cohort underperformance rate per band for the five modules and S1 GPA.
