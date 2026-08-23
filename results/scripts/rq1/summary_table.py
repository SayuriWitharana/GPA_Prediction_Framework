"""Regenerates the RQ1 Stage-1 CV all-metrics summary table.

Reshapes results/RQ1/cv_results.csv (one row per semester, pooled and
per-group columns side by side) into one markdown table per group (Pooled,
High-performing, Average, Underperforming), each with every metric across
all seven checkpoints, so there's one clean, regeneratable place to look
for "all metrics per semester" instead of hand-typing numbers into
RQ1_reliability_interpretation.md.
"""

import pandas as pd

from src.rq1.config import GROUPS, RESULTS_DIR

IN_PATH = RESULTS_DIR / "cv_results.csv"
OUT_PATH = RESULTS_DIR / "cv_summary_table.md"

SECTIONS = [("Pooled", None)] + [(g, g) for g in GROUPS]


def build_section(df, column_prefix):
    if column_prefix is None:
        cols = {"RMSE": "cv_rmse_mean", "RMSE SD": "cv_rmse_sd", "R2": "cv_r2_mean", "Bias": "cv_bias_mean"}
    else:
        cols = {
            "RMSE": f"{column_prefix}_rmse",
            "RMSE SD": f"{column_prefix}_rmse_sd",
            "R2": f"{column_prefix}_r2",
            "Bias": f"{column_prefix}_bias",
        }
    section = pd.DataFrame({"Semester": df["semester"]})
    for label, col in cols.items():
        section[label] = df[col]
    return section


def section_to_markdown(title, section):
    lines = [f"## {title}", "", "| Semester | RMSE | RMSE SD | R² | Bias |", "|---|---:|---:|---:|---:|"]
    for _, row in section.iterrows():
        lines.append(
            f"| {row['Semester']} | {row['RMSE']:.3f} | {row['RMSE SD']:.3f} | "
            f"{row['R2']:+.3f} | {row['Bias']:+.3f} |"
        )
    if title == "Average":
        lines.append("")
        lines.append(
            "*R² is unreliable for this group — its 2.99–3.29 GPA range is a "
            "narrow band by construction, so small absolute errors produce "
            "large, unstable R² swings. RMSE and bias are the metrics to "
            "trust here.*"
        )
    return "\n".join(lines)


def main():
    df = pd.read_csv(IN_PATH)
    sections_markdown = [section_to_markdown(title, build_section(df, col)) for title, col in SECTIONS]

    content = (
        "# RQ1 Stage-1 CV summary table\n\n"
        "Auto-generated from `cv_results.csv` by "
        "`results/scripts/rq1/summary_table.py` — do not hand-edit; "
        "re-run `python -m results.scripts.rq1.summary_table` after any "
        "`src/rq1/cv.py` re-run.\n\n" + "\n\n".join(sections_markdown) + "\n"
    )
    OUT_PATH.write_text(content, encoding="utf-8")
    print(content)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
