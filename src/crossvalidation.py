from sklearn.model_selection import RepeatedStratifiedKFold

def get_cv():
    return RepeatedStratifiedKFold(
        n_splits=5,
        n_repeats=10,
        random_state=42
    )