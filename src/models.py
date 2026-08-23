from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline


def get_ridge_pipeline(preprocessor, alpha=1.0):
    return Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', Ridge(alpha=alpha))
    ])


# Ridge regression was used to address multicollinearity among semester GPAs. 
# A fixed α was used across all semester models to ensure comparability of coefficients 
# and prediction performance over time, to ensure that the semesters can be compared,
# since the objective of the study is to analyze temporal stability rather than optimize individual model performance.

from sklearn.ensemble import RandomForestRegressor


def get_rf_pipeline(preprocessor, n_estimators=100, max_depth=None):
    return Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(
            n_estimators=n_estimators, 
            max_depth=max_depth, 
            random_state=42,
            n_jobs=-1 # Uses all CPU cores for faster training
        ))
    ])