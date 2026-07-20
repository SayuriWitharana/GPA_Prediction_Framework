from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# District spelling variants observed across the 2017-2018 and 2019 raw
# files (e.g. "Kegalla" vs "Kegalle", "Kilinochi" vs "Kilinochchi"), plus
# incidental leading/trailing whitespace ("Badulla ", "Kandy ") that would
# otherwise be encoded as distinct categories from their trimmed form.
DISTRICT_SPELLING_FIXES = {
    "Kegalla": "Kegalle",
    "Kilinochi": "Kilinochchi",
}


def clean_categoricals(df, categorical_features):
    """Strip whitespace and harmonise known spelling variants in-place.

    Shared by both RQ1 and RQ2 pipelines so the same student is encoded
    identically regardless of which analysis is reading the data.
    """
    df = df.copy()
    for column in categorical_features:
        df[column] = df[column].astype("string").str.strip()
    if "District" in df.columns:
        df["District"] = df["District"].replace(DISTRICT_SPELLING_FIXES)
    return df


def get_preprocessor(numeric_features, categorical_features):
    numeric_transformer = Pipeline(steps=[
        ('medianImputer', SimpleImputer(strategy='median', add_indicator=True)),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('mostFrequentImputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore', min_frequency=5, sparse_output=False)) #we have nominal data
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            # Named 'numeric'/'categorical' (not the sklearn-default 'num'/'cat')
            # because the RQ2 SHAP scripts' feature-name cleanup
            # (src/shap/rq2_linear_shap.py: tidy_feature_name) strips exactly
            # these prefixes from ColumnTransformer's generated output names.
            ('numeric', numeric_transformer, numeric_features),
            ('categorical', categorical_transformer, categorical_features)
        ]
    )

    return preprocessor

# Notes:
# The English marks variable exhibited a wide distribution with potential skewness and extreme values,
# as shown in the histogram. Since mean imputation is sensitive to outliers and may distort the distribution,
#  missing values (n = 7) were imputed using the median to preserve robustness and minimize bias in subsequent predictive modeling.
#
# add_indicator=True on the numeric imputer and min_frequency=5 on the
# categorical encoder match RQ2's model-audit pipeline (src/shap/rq2_module_model_audit.py),
# so the "no-module baseline" is computed identically whether it's run from
# the RQ1 notebook/scripts or the RQ2 audit script. See
# notebooks/rq1_reliability/RQ1_reliability_interpretation.md for the
# reconciliation note this resolves.
#
# RobustScaler compresses tails. Your zeros (failures) are meaningful. If you use RobustScaler: extreme low GPA values shrink
# ,underperformance signal weakens, early risk detection weaker. But your research wants:, detect underperformance early
# So we should NOT suppress tails. StandardScaler keeps them visible.
