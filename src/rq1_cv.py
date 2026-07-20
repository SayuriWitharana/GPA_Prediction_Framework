"""RQ1 Stage-1 cross-validation under the unified preprocessing pipeline.

Repeated stratified 5-fold CV (10 repeats, 50 splits total) at each of the
seven checkpoints S0-S6, computing pooled and per-performance-group RMSE,
R^2, and directional bias for Ridge regression. This is the CV counterpart
to src/rq1_external_bootstrap.py (Stage 2, external test); together they
are the full RQ1 reliability pipeline, both now using the same shared
src/preprocessing.py functions RQ2 uses. See
notebooks/rq1_reliability/RQ1_reliability_interpretation.md for the
narrative this feeds into.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, root_mean_squared_error

from src.crossvalidation import get_cv
from src.models import get_ridge_pipeline
from src.preprocessing import clean_categoricals, get_preprocessor

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "notebooks" / "rq1_reliability" / "cv_results.csv"

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


def assign_perf_group(gpa: float) -> str:
    if gpa <= 2.99:
        return "Underperforming"
    if gpa <= 3.29:
        return "Average"
    return "High-performing"


def main():
    df = pd.read_excel(DATA / "2017-2018 TrainSet.xlsx")
    df = clean_categoricals(df, CATEGORICAL)
    df["GroupLabel"] = df["FinalGPA"].apply(assign_perf_group)
    y = df["FinalGPA"]
    strata = df["GroupLabel"]

    rows = []
    for semester, numeric_features in FEATURE_SETS.items():
        X = df[numeric_features + CATEGORICAL]
        cv = get_cv()

        pooled_rmse, pooled_r2 = [], []
        group_rmse = {g: [] for g in GROUPS}
        group_r2 = {g: [] for g in GROUPS}
        group_bias = {g: [] for g in GROUPS}

        for train_idx, val_idx in cv.split(X, strata):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            g_val = strata.iloc[val_idx]

            preprocessor = get_preprocessor(numeric_features=numeric_features, categorical_features=CATEGORICAL)
            model = get_ridge_pipeline(preprocessor=preprocessor, alpha=1.0)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)

            pooled_rmse.append(root_mean_squared_error(y_val, y_pred))
            pooled_r2.append(r2_score(y_val, y_pred))

            for g in GROUPS:
                mask = (g_val == g).to_numpy()
                if mask.sum() == 0:
                    continue
                actual = y_val.to_numpy()[mask]
                pred = y_pred[mask]
                group_rmse[g].append(root_mean_squared_error(actual, pred))
                group_r2[g].append(r2_score(actual, pred))
                group_bias[g].append(np.mean(actual - pred))

        row = {
            "semester": semester,
            "cv_rmse_mean": np.mean(pooled_rmse),
            "cv_rmse_sd": np.std(pooled_rmse),
            "cv_r2_mean": np.mean(pooled_r2),
        }
        for g in GROUPS:
            row[f"{g}_rmse"] = np.mean(group_rmse[g])
            row[f"{g}_rmse_sd"] = np.std(group_rmse[g])
            row[f"{g}_r2"] = np.mean(group_r2[g])
            row[f"{g}_bias"] = np.mean(group_bias[g])
        rows.append(row)

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    pd.set_option("display.width", 200)
    print(out.round(3).to_string(index=False))
    print(f"\nSaved: {OUT}")


if __name__ == "__main__":
    main()
