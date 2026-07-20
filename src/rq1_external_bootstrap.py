"""Bootstrap confidence intervals for RQ1's Stage-2 external-cohort evaluation.

Stage 2 (see notebooks/rq1_reliability/RQ1_reliability_interpretation.md) trains
on the full 2017-2018 cohort and evaluates once on the 2019 cohort. A single
evaluation is one draw from a small, group-split external set (19-50 students
per group), so point-estimate RMSE/bias alone cannot assess whether the observed performance 
is sufficiently stable to support conclusions about reliability. 
Because each performance group contains only 19–50 students, the resulting RMSE and bias are point estimates 
from a single external evaluation and do not quantify the sampling uncertainty associated with these metrics. 
This script keeps the trained model fixed and resamples students within each performance group (with replacement) 
to estimate 95% bootstrap confidence intervals for the external RMSE and bias values reported in Table III.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import root_mean_squared_error

from src.preprocessing import clean_categoricals, get_preprocessor
from src.models import get_ridge_pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "notebooks" / "rq1_reliability" / "external_bootstrap_ci.csv"

CATEGORICAL = ["Gender", "Department", "District", "MediumAL"]
FEATURE_SETS = {
    "S2": ["Zscore", "EnglishMarks", "S1", "S2"],
    "S3": ["Zscore", "EnglishMarks", "S1", "S2", "S3"],
    "S4": ["Zscore", "EnglishMarks", "S1", "S2", "S3", "S4"],
    "S5": ["Zscore", "EnglishMarks", "S1", "S2", "S3", "S4", "S5"],
    "S6": ["Zscore", "EnglishMarks", "S1", "S2", "S3", "S4", "S5", "S6"],
}
GROUPS = ["High-performing", "Average", "Underperforming"]
N_BOOT = 5000
SEED = 42


def assign_perf_group(gpa: float) -> str:
    if gpa <= 2.99:
        return "Underperforming"
    if gpa <= 3.29:
        return "Average"
    return "High-performing"


def bootstrap_group(actual, pred, rng, n_boot=N_BOOT):
    n = len(actual)
    idx = np.arange(n)
    resid = actual - pred
    boot_rmse = np.empty(n_boot)
    boot_bias = np.empty(n_boot)
    for b in range(n_boot):
        sample = rng.choice(idx, size=n, replace=True)
        boot_rmse[b] = np.sqrt(np.mean((actual[sample] - pred[sample]) ** 2))
        boot_bias[b] = resid[sample].mean()
    return {
        "rmse": root_mean_squared_error(actual, pred),
        "rmse_lo": np.percentile(boot_rmse, 2.5),
        "rmse_hi": np.percentile(boot_rmse, 97.5),
        "bias": resid.mean(),
        "bias_lo": np.percentile(boot_bias, 2.5),
        "bias_hi": np.percentile(boot_bias, 97.5),
    }


def main():
    train = pd.read_excel(DATA / "2017-2018 TrainSet.xlsx")
    train = clean_categoricals(train, CATEGORICAL)
    train["GroupLabel"] = train["FinalGPA"].apply(assign_perf_group)
    test = pd.read_excel(DATA / "2019 TestSet.xlsx")
    test = clean_categoricals(test, CATEGORICAL)
    test["GroupLabel"] = test["FinalGPA"].apply(assign_perf_group)

    rng = np.random.default_rng(SEED)
    rows = []
    for semester, numeric_features in FEATURE_SETS.items():
        preprocessor = get_preprocessor(numeric_features=numeric_features, categorical_features=CATEGORICAL)
        model = get_ridge_pipeline(preprocessor=preprocessor, alpha=1.0)
        model.fit(train[numeric_features + CATEGORICAL], train["FinalGPA"])
        y_pred = model.predict(test[numeric_features + CATEGORICAL])
        y_true = test["FinalGPA"].to_numpy()
        grp = test["GroupLabel"].to_numpy()

        for g in GROUPS:
            mask = grp == g
            stats = bootstrap_group(y_true[mask], y_pred[mask], rng)
            rows.append({"semester": semester, "group": g, "n": int(mask.sum()), **stats})

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    pd.set_option("display.width", 160)
    print(out.round(3).to_string(index=False))
    print(f"\nSaved: {OUT}")


if __name__ == "__main__":
    main()
