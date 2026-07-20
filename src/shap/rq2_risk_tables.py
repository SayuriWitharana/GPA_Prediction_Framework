"""Advisor-facing grade-band risk tables for early underperformance detection.

For each early feature (module grades, semester GPAs, pre-academic factors)
this reports the observed rate of eventual underperformance (final GPA <= 2.99)
per grade band on the 2017-2018 training cohort, with student counts and the
lift versus the cohort base rate.

The 2019 cohort is included only as a sanity check: its module grades are
strongly inflated relative to training (see rq2_linear_shap.py), so its low
bands are thin or empty. All rates are descriptive associations observed in
small cohorts, not causal claims, and must prompt advisor review rather than
automated designation of a student as at risk.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rq2_module_model_audit import (
    MODULES_BY_SEMESTER,
    OUT as AUDIT_OUT,
    TEST_PATH,
    TRAIN_PATH,
    clean_data,
)


OUT = AUDIT_OUT / "risk_tables"
MODULE_BAND_ORDER = ["D or F", "C- to C+", "B- to B+", "A- to A+", "Incomplete/missing"]
GPA_BAND_ORDER = ["Below 2.70", "2.70-2.99", "3.00-3.29", "3.30 or above"]


def module_band(points):
    if pd.isna(points):
        return "Incomplete/missing"
    if points >= 9:
        return "A- to A+"
    if points >= 6:
        return "B- to B+"
    if points >= 3:
        return "C- to C+"
    return "D or F"


def gpa_band(value):
    if value < 2.7:
        return "Below 2.70"
    if value < 3.0:
        return "2.70-2.99"
    if value < 3.3:
        return "3.00-3.29"
    return "3.30 or above"


def quartile_bander(train_series):
    """Quartile bands with training-cohort edges so both cohorts use the same cut-offs."""
    edges = np.nanquantile(train_series.astype(float), [0.25, 0.5, 0.75])
    order = [
        f"Q1 (lowest, <= {edges[0]:g})",
        f"Q2 ({edges[0]:g}-{edges[1]:g})",
        f"Q3 ({edges[1]:g}-{edges[2]:g})",
        f"Q4 (highest, > {edges[2]:g})",
        "Missing",
    ]

    def band(value):
        if pd.isna(value):
            return "Missing"
        if value <= edges[0]:
            return order[0]
        if value <= edges[1]:
            return order[1]
        if value <= edges[2]:
            return order[2]
        return order[3]

    return band, order


def feature_definitions(train):
    definitions = []
    english_band, english_order = quartile_bander(train["English"])
    zscore_band, zscore_order = quartile_bander(train["Zscore"])
    definitions.append(("Zscore", 0, zscore_band, zscore_order))
    definitions.append(("English", 0, english_band, english_order))
    for semester in range(1, 6):
        definitions.append((f"S{semester}", semester, gpa_band, GPA_BAND_ORDER))
    for available_from, modules in MODULES_BY_SEMESTER.items():
        for module in modules:
            definitions.append((module, available_from, module_band, MODULE_BAND_ORDER))
    return definitions


def band_rates(train, test, definitions):
    base_rate = (train["GroupLabel"] == "Underperforming").mean()
    rows = []
    for feature, available_from, band, order in definitions:
        train_bands = train[feature].map(band)
        test_bands = test[feature].map(band)
        for name in order:
            train_mask = (train_bands == name).to_numpy()
            test_mask = (test_bands == name).to_numpy()
            if train_mask.sum() == 0 and test_mask.sum() == 0:
                continue
            train_under = (train.loc[train_mask, "GroupLabel"] == "Underperforming").sum()
            train_rate = train_under / train_mask.sum() if train_mask.sum() else np.nan
            rows.append({
                "feature": feature,
                "available_from_semester": available_from,
                "band": name,
                "train_students": int(train_mask.sum()),
                "train_underperformers": int(train_under),
                "train_underperformance_rate": train_rate,
                "lift_vs_base_rate": train_rate / base_rate if train_mask.sum() else np.nan,
                "test_students": int(test_mask.sum()),
                "test_underperformance_rate": (test.loc[test_mask, "GroupLabel"] == "Underperforming").mean() if test_mask.sum() else np.nan,
            })
    return pd.DataFrame(rows), base_rate


def plot_module_risk(results, base_rate):
    modules = [module for modules in MODULES_BY_SEMESTER.values() for module in modules]
    panels = modules + ["S1"]
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    for axis, feature in zip(axes.flat, panels):
        subset = results[(results["feature"] == feature) & (results["train_students"] > 0)]
        bars = axis.bar(subset["band"], subset["train_underperformance_rate"], color="#4C78A8")
        for bar, row in zip(bars, subset.itertuples()):
            axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                      f"n={row.train_students}", ha="center", fontsize=8)
        axis.axhline(base_rate, color="#C44E52", linestyle="--", linewidth=1, label=f"Base rate {base_rate:.0%}")
        axis.set_title(feature)
        axis.set_ylabel("P(eventual underperformance)")
        axis.set_ylim(0, 1.05)
        axis.tick_params(axis="x", rotation=25, labelsize=8)
        axis.legend(fontsize=8)
    fig.suptitle("Underperformance rate by grade band (training cohort 2017-2018)", y=1.0)
    fig.tight_layout()
    fig.savefig(OUT / "risk_by_grade_band.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_report(results, base_rate, train, test):
    flagged = results[(results["train_students"] >= 10) & (results["lift_vs_base_rate"] >= 1.5)].sort_values(
        ["available_from_semester", "lift_vs_base_rate"], ascending=[True, False])
    if flagged.empty:
        highlights = "No band with at least 10 students reached 1.5x the base rate."
    else:
        highlight_lines = []
        for row in flagged.itertuples():
            highlight_lines.append(
                f"- From semester {row.available_from_semester}: **{row.feature} in band \"{row.band}\"** — "
                f"{row.train_underperformance_rate:.0%} underperformance rate "
                f"({row.train_underperformers}/{row.train_students} students; {row.lift_vs_base_rate:.1f}x the {base_rate:.0%} base rate)."
            )
        highlights = "\n".join(highlight_lines)
    text = f"""# Advisor-facing risk tables: grade bands and eventual underperformance

## Purpose and design

For every early feature available by semester 5, this table reports the observed share of students who ultimately finished with final GPA <= 2.99 (Underperforming), per grade band, on the 2017-2018 training cohort ({len(train)} students; base rate {base_rate:.0%}). Lift is the band's rate divided by the base rate.

The 2019 cohort ({len(test)} students) is shown only as a sanity check. Its module grades are strongly inflated relative to 2017-2018 (e.g. 70% of Maths 2 grades are A/A+ versus 16% in training), so its low-grade bands are thin or empty and its rates are not comparable band-by-band.

These are descriptive associations in small cohorts — several bands hold fewer than 10 students (counts are always shown). They indicate which students an advisor should look at more closely; they are not causal claims and must never trigger automated designation of a student as at risk.

## Bands that stand out (>= 10 students and >= 1.5x base rate)

{highlights}

## How advisors can use this

- Pre-entry (S0): Zscore and English bands flag students for light-touch monitoring from day one.
- After each semester, check newly available bands: semester GPA bands plus the modules completed that semester (S2: Maths 2, MgtAccounting; S3: StatsII, MIS; S4: DataV).
- "I-we"/"I-ca" outcomes (did not sit the exam or did not complete the continuous-assessment component) are coded as fail-equivalent and appear inside the "D or F" band above, not as a separate category.
- Combine with the SHAP early-warning signals (`linear_shap/underperformance/`): a student in a high-lift band whose profile also carries negative SHAP signals is a priority for advisor review.

## Files

- `risk_tables.csv`: full band-level table (training rates, lift, 2019 sanity-check columns).
- `risk_by_grade_band.png`: training-cohort underperformance rate per band for the five modules and S1 GPA.
"""
    (OUT / "RQ2_risk_tables.md").write_text(text, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = clean_data(TRAIN_PATH), clean_data(TEST_PATH)
    definitions = feature_definitions(train)
    results, base_rate = band_rates(train, test, definitions)
    results.to_csv(OUT / "risk_tables.csv", index=False)
    plot_module_risk(results, base_rate)
    write_report(results, base_rate, train, test)
    print(f"Completed risk tables. Training base rate: {base_rate:.1%}.")


if __name__ == "__main__":
    main()
