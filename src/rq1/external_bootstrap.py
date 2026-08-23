"""Bootstrap confidence intervals for RQ1's Stage-2 external-cohort evaluation.

Stage 2 (see results/RQ1/RQ1_reliability_interpretation.md) trains
on the full 2017-2018 cohort and evaluates once on the 2019 cohort. A single
evaluation is one draw from a small, group-split external set (19-50 students
per group), so point-estimate RMSE/bias alone cannot assess whether the observed performance
is sufficiently stable to support conclusions about reliability.
Because each performance group contains only 19–50 students, the resulting RMSE and bias are point estimates
from a single external evaluation and do not quantify the sampling uncertainty associated with these metrics.
This script keeps the trained model fixed and resamples students within each performance group (with replacement)
to estimate 95% bootstrap confidence intervals for the external RMSE and bias values reported in Table III.
This is the Stage-2 counterpart to src/rq1/cv.py (Stage 1, cross-validation).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import root_mean_squared_error

from src.models import get_ridge_pipeline
from src.preprocessing import clean_categoricals, get_preprocessor
from src.rq1.config import CATEGORICAL, DATA, FEATURE_SETS, GROUPS, RESULTS_DIR
from src.rq1.groups import add_group_label

OUT = RESULTS_DIR / "external_bootstrap_ci.csv"
N_BOOT = 5000
SEED = 42

# Stage 2 starts evaluation at S2 (the earliest checkpoint the external test
# is reported for); S0/S1 are Stage-1-only.
EXTERNAL_FEATURE_SETS = {k: v for k, v in FEATURE_SETS.items() if k not in ("S0", "S1")}


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
    train = add_group_label(train)
    test = pd.read_excel(DATA / "2019 TestSet.xlsx")
    test = clean_categoricals(test, CATEGORICAL)
    test = add_group_label(test)

    rng = np.random.default_rng(SEED)
    rows = []
    for semester, numeric_features in EXTERNAL_FEATURE_SETS.items():
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
