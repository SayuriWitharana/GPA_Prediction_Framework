from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def get_preprocessor(numeric_features, categorical_features):
    numeric_transformer = Pipeline(steps=[
        ('medianImputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False)) #we have nominal data
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    return preprocessor

# Notes:
# The English marks variable exhibited a wide distribution with potential skewness and extreme values, 
# as shown in the histogram. Since mean imputation is sensitive to outliers and may distort the distribution,
#  missing values (n = 7) were imputed using the median to preserve robustness and minimize bias in subsequent predictive modeling.

# RobustScaler compresses tails. Your zeros (failures) are meaningful. If you use RobustScaler: extreme low GPA values shrink
# ,underperformance signal weakens, early risk detection weaker. But your research wants:, detect underperformance early
# So we should NOT suppress tails. StandardScaler keeps them visible.