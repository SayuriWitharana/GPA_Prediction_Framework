import pandas as pd

from src.rq1.groups import add_group_label, assign_perf_group


def test_underperforming_boundary():
    assert assign_perf_group(2.99) == "Underperforming"
    assert assign_perf_group(0.0) == "Underperforming"


def test_average_boundary():
    assert assign_perf_group(3.0) == "Average"
    assert assign_perf_group(3.29) == "Average"


def test_high_performing_boundary():
    assert assign_perf_group(3.30) == "High-performing"
    assert assign_perf_group(4.0) == "High-performing"


def test_add_group_label_uses_final_gpa_by_default():
    df = pd.DataFrame({"FinalGPA": [2.5, 3.1, 3.8]})
    out = add_group_label(df)
    assert out["GroupLabel"].tolist() == ["Underperforming", "Average", "High-performing"]
