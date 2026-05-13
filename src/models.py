from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

def get_ridge_pipeline(preprocessor, alpha=1.0):
    return Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', Ridge(alpha=alpha))
    ])

# How to decide alpha?

# Ridge regression was used to address multicollinearity among semester GPAs. 
# The regularization parameter α was fixed at 1.0, which corresponds to the default value in scikit-learn and provides moderate regularization. 
# A fixed α was used across all semester models to ensure comparability of coefficients and prediction performance over time, to ensure that the semesters can be compared,
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