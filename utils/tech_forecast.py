import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def tech_saturation_forecast(
    df,
    latency_threshold=20.0
):
    """
    Forecast the date when average ingestion latency
    crosses the saturation threshold using linear regression.
    """

    df = df.copy()

    # Convert date to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Create day index (0,1,2,...)
    df["day_index"] = (df["date"] - df["date"].min()).dt.days

    # Prepare regression variables
    X = df[["day_index"]]
    y = df["avg_ingestion_latency_min"]

    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)

    intercept = model.intercept_
    slope = model.coef_[0]

    # Solve for saturation day:
    # latency_threshold = intercept + slope * day_index
    if slope <= 0:
        return None  # No saturation trend

    saturation_day_index = (
        latency_threshold - intercept
    ) / slope

    saturation_day_index = int(np.ceil(saturation_day_index))

    saturation_date = (
        df["date"].min()
        + pd.Timedelta(days=saturation_day_index)
    )

    return {
        "slope": slope,
        "intercept": intercept,
        "saturation_day_index": saturation_day_index,
        "saturation_date": saturation_date
    }
