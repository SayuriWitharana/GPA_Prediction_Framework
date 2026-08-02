"""Generates the EDA summary chart for the ICODE presentation.

Standalone script (not a notebook), reads the canonical 2017-2018 training
set and produces ICODE_EDA_Summary.png: FinalGPA distribution (left) +
FinalGPA by performance group with the paper's group thresholds annotated
(right). Saved alongside the other ICODE_*.png presentation assets.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "2017-2018 TrainSet.xlsx"
OUT_PATH = Path(__file__).resolve().parent / "ICODE_EDA_Summary.png"

df = pd.read_excel(DATA_PATH)


def perf_group(gpa):
    if gpa <= 2.99:
        return "Underperforming"
    elif gpa <= 3.29:
        return "Average"
    return "Performing"


df["PerfGroup"] = df["FinalGPA"].apply(perf_group)
group_order = ["Underperforming", "Average", "Performing"]
palette = {"Underperforming": "#d62728", "Average": "#ff7f0e", "Performing": "#2ca02c"}

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# Panel (a): FinalGPA distribution
ax = axes[0]
sns.histplot(df["FinalGPA"], kde=True, bins=20, ax=ax, color="#4c72b0")
ax.set_title("(a) FinalGPA Distribution (n=178)", fontsize=13, loc="left")
ax.set_xlabel("Final GPA", fontsize=12)
ax.set_ylabel("Number of Students", fontsize=12)
ax.tick_params(labelsize=10)

# Panel (b): FinalGPA by performance group with thresholds
ax = axes[1]
sns.boxplot(data=df, x="PerfGroup", y="FinalGPA", order=group_order, palette=palette, ax=ax)
ax.axhline(2.99, color="gray", linestyle="--", linewidth=1.2)
ax.axhline(3.29, color="gray", linestyle="--", linewidth=1.2)
ax.text(2.05, 2.99, " 2.99", va="center", fontsize=10, color="gray")
ax.text(2.05, 3.29, " 3.29", va="center", fontsize=10, color="gray")
ax.set_title("(b) FinalGPA by Performance Group", fontsize=13, loc="left")
ax.set_xlabel("")
ax.set_ylabel("Final GPA", fontsize=12)
ax.tick_params(labelsize=10)

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300)
print("Saved:", OUT_PATH)
print(df["PerfGroup"].value_counts())
