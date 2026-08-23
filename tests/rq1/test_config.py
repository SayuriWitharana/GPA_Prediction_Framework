from src.rq1.config import CATEGORICAL, FEATURE_SETS, GROUPS

SEMESTERS = ["S0", "S1", "S2", "S3", "S4", "S5", "S6"]
BASE_FEATURES = ["Zscore", "EnglishMarks"]


def test_feature_sets_cover_all_checkpoints():
    assert list(FEATURE_SETS.keys()) == SEMESTERS


def test_feature_sets_are_cumulative():
    previous = FEATURE_SETS["S0"]
    assert previous == BASE_FEATURES
    for semester in SEMESTERS[1:]:
        current = FEATURE_SETS[semester]
        assert current[:-1] == previous
        assert current[-1] == semester
        previous = current


def test_categorical_and_groups_are_non_empty_and_disjoint():
    assert CATEGORICAL
    assert GROUPS
    assert set(CATEGORICAL).isdisjoint(GROUPS)
