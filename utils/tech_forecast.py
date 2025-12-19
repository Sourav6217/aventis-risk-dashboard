import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def tech_saturation_forecast(df, latency_threshold=20.0):
    """
    Forecast the date when average ingestion latency
    crosses the saturation threshold using linear regression.
    """

    df = df.copy()

    # --- Robust date parsing ---
    df["date"] = pd.to_datetime(
        df["date"].astype(str).str.strip(),
        format="%Y-%m-%d",
        errors="coerce"
    )

    # Drop rows with invalid dates
    df = df.dropna(subset=["date"])

    # Safety check
    if df.empty:
        return None

    # --- Create day index (0,1,2,...) ---
    df["day_index"] = (df["date"] - df["date"].min()).dt.days

    # Regression variables
    X = df[["day_index"]]
    y = df["avg_ingestion_latency_min"]

    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)

    intercept = model.intercept_
    slope = model.coef_[0]

    # If no upward trend, no saturation
    if slope <= 0:
        return None

    # Solve for saturation day
    saturation_day_index = (latency_threshold - intercept) / slope
    saturation_day_index = int(np.ceil(saturation_day_index))

    saturation_date = df["date"].min() + pd.Timedelta(days=saturation_day_index)

    return {
        "slope": slope,
        "intercept": intercept,
        "saturation_day_index": saturation_day_index,
        "saturation_date": saturation_date
    }
