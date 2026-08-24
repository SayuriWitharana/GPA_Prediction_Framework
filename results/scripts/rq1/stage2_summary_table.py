import pandas as pd

from src.rq1.config import GROUPS, RESULTS_DIR

IN_PATH = RESULTS_DIR / "external_bootstrap_ci.csv"
OUT_PATH = RESULTS_DIR / "external_summary_table.md"


def format_ci(lo, hi):
    return f"[{lo:.3f}, {hi:.3f}]"


def section_to_markdown(group, rows):
    lines = [
        f"## {group}",
        "",
        "| Semester | n | RMSE | RMSE 95% CI | Bias | Bias 95% CI |",
        "|---|---:|---:|---|---:|---|",
    ]
    for _, row in rows.iterrows():
        lines.append(
            f"| {row['semester']} | {int(row['n'])} | {row['rmse']:.3f} | "
            f"{format_ci(row['rmse_lo'], row['rmse_hi'])} | {row['bias']:+.3f} | "
            f"{format_ci(row['bias_lo'], row['bias_hi'])} |"
        )
    return "\n".join(lines)


def main():
    df = pd.read_csv(IN_PATH)
    sections_markdown = [section_to_markdown(group, df[df["group"] == group]) for group in GROUPS]

    content = (
        "# RQ1 Stage-2 external bootstrap summary table\n\n"
        "Auto-generated from `external_bootstrap_ci.csv` by "
        "`results/scripts/rq1/stage2_summary_table.py` — do not hand-edit; "
        "re-run `python -m results.scripts.rq1.stage2_summary_table` after "
        "any `src/rq1/stage2_external_bootstrap.py` re-run. No Pooled section: "
        "`stage2_external_bootstrap.py` only ever bootstraps per performance "
        "group, not a pooled external CI.\n\n" + "\n\n".join(sections_markdown) + "\n"
    )
    OUT_PATH.write_text(content, encoding="utf-8")
    print(content)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
