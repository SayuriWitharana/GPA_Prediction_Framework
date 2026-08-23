import pandas as pd

from src.preprocessing import clean_categoricals


def test_strips_whitespace():
    df = pd.DataFrame({"District": [" Kandy ", "Colombo"], "Gender": ["Male", "Female "]})
    out = clean_categoricals(df, ["District", "Gender"])
    assert out["District"].tolist() == ["Kandy", "Colombo"]
    assert out["Gender"].tolist() == ["Male", "Female"]


def test_fixes_known_district_spelling_variants():
    df = pd.DataFrame({"District": ["Kegalla", "Kilinochi", "Kandy"]})
    out = clean_categoricals(df, ["District"])
    assert out["District"].tolist() == ["Kegalle", "Kilinochchi", "Kandy"]


def test_does_not_mutate_input_frame():
    df = pd.DataFrame({"District": [" Kandy "]})
    clean_categoricals(df, ["District"])
    assert df["District"].iloc[0] == " Kandy "
