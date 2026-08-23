from src.rq1.config import AVERAGE_MAX_GPA, UNDERPERFORMING_MAX_GPA


def assign_perf_group(gpa: float) -> str:
    if gpa <= UNDERPERFORMING_MAX_GPA:
        return "Underperforming"
    if gpa <= AVERAGE_MAX_GPA:
        return "Average"
    return "High-performing"


def add_group_label(df, gpa_column="FinalGPA", label_column="GroupLabel"):
    df[label_column] = df[gpa_column].apply(assign_perf_group)
    return df
