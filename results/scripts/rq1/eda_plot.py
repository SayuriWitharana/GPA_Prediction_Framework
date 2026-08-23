"""Generates the EDA summary chart for the ICODE presentation.

Reads the canonical 2017-2018 training set and produces
ICODE_EDA_Summary.png: FinalGPA distribution (left) + FinalGPA by
performance group with the paper's group thresholds annotated (right).
Saved alongside the other ICODE_*.png presentation assets. Uses the same
shared src/rq1/groups.py labelling as the rest of the RQ1 pipeline (this
used to be a standalone script with its own, differently-labelled copy of
the group assignment).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.rq1.config import AVERAGE_MAX_GPA, DATA, UNDERPERFORMING_MAX_GPA
from src.rq1.groups import add_group_label

OUT_PATH = Path(__file__).resolve().parents[3] / "results" / "RQ1" / "ICODE_EDA_Summary.png"

# Ascending performance order, left-to-right on the boxplot (independent of
# config.GROUPS, whose order only matters for CSV column ordering elsewhere).
PLOT_ORDER = ["Underperforming", "Average", "High-performing"]
PALETTE = {
    "Underperforming": "#d62728",
    "Average": "#ff7f0e",
    "High-performing": "#2ca02c",
}


def main():
    df = pd.read_excel(DATA / "2017-2018 TrainSet.xlsx")
    df = add_group_label(df, label_column="PerfGroup")

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # Panel (a): FinalGPA distribution
    ax = axes[0]
    sns.histplot(df["FinalGPA"], kde=True, bins=20, ax=ax, color="#4c72b0")
    ax.set_title(f"(a) FinalGPA Distribution (n={len(df)})", fontsize=13, loc="left")
    ax.set_xlabel("Final GPA", fontsize=12)
    ax.set_ylabel("Number of Students", fontsize=12)
    ax.tick_params(labelsize=10)

    # Panel (b): FinalGPA by performance group with thresholds
    ax = axes[1]
    sns.boxplot(data=df, x="PerfGroup", y="FinalGPA", order=PLOT_ORDER, palette=PALETTE, ax=ax)
    ax.axhline(UNDERPERFORMING_MAX_GPA, color="gray", linestyle="--", linewidth=1.2)
    ax.axhline(AVERAGE_MAX_GPA, color="gray", linestyle="--", linewidth=1.2)
    ax.text(2.05, UNDERPERFORMING_MAX_GPA, f" {UNDERPERFORMING_MAX_GPA}", va="center", fontsize=10, color="gray")
    ax.text(2.05, AVERAGE_MAX_GPA, f" {AVERAGE_MAX_GPA}", va="center", fontsize=10, color="gray")
    ax.set_title("(b) FinalGPA by Performance Group", fontsize=13, loc="left")
    ax.set_xlabel("")
    ax.set_ylabel("Final GPA", fontsize=12)
    ax.tick_params(labelsize=10)

    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=300)
    print("Saved:", OUT_PATH)
    print(df["PerfGroup"].value_counts())


if __name__ == "__main__":
    main()
