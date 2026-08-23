"""Shared constants for the RQ1 reliability pipeline (Stage-1 CV, Stage-2
external bootstrap, and the EDA summary chart) so the checkpoint feature
sets and performance-group cutoffs are defined in exactly one place.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw"
RESULTS_DIR = ROOT / "results" / "RQ1"

CATEGORICAL = ["Gender", "Department", "District", "MediumAL"]

FEATURE_SETS = {
    "S0": ["Zscore", "EnglishMarks"],
    "S1": ["Zscore", "EnglishMarks", "S1"],
    "S2": ["Zscore", "EnglishMarks", "S1", "S2"],
    "S3": ["Zscore", "EnglishMarks", "S1", "S2", "S3"],
    "S4": ["Zscore", "EnglishMarks", "S1", "S2", "S3", "S4"],
    "S5": ["Zscore", "EnglishMarks", "S1", "S2", "S3", "S4", "S5"],
    "S6": ["Zscore", "EnglishMarks", "S1", "S2", "S3", "S4", "S5", "S6"],
}

GROUPS = ["High-performing", "Average", "Underperforming"]

UNDERPERFORMING_MAX_GPA = 2.99
AVERAGE_MAX_GPA = 3.29
