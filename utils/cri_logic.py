import pandas as pd

def compute_cri(df):
    """
    Compute Client Reliability Index (CRI) per client per week.
    CRI range: 0 to 100
    """

    df = df.copy()

    # Derived rates
    df["late_submission_rate"] = (
        df["files_received_late"] / df["files_expected"]
    )

    df["schema_error_rate"] = (
        df["records_invalid"] / df["records_total"]
    )

    # CRI calculation
    df["CRI"] = (
        100
        - (df["late_submission_rate"] * 60)
        - (df["schema_error_rate"] * 40)
    )

    # Clip CRI between 0 and 100
    df["CRI"] = df["CRI"].clip(0, 100)

    # Risk categorization
    def risk_bucket(cri):
        if cri >= 80:
            return "Low Risk"
        elif cri >= 50:
            return "Medium Risk"
        else:
            return "High Risk"

    df["Risk_Category"] = df["CRI"].apply(risk_bucket)

    return df
