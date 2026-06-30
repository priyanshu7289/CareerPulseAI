"""
forecasting/hiring_trend_forecast.py

Hiring Trend Forecast Module
CareerPulse AI

Forecast hiring demand using Linear Regression.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# DATA PREPARATION
# ============================================================

def prepare_monthly_series(
    jobs_df: pd.DataFrame,
    date_col: str = "posted_date",
) -> pd.DataFrame:
    """
    Convert raw job postings into monthly counts.
    """

    if date_col not in jobs_df.columns:
        raise ValueError(
            f"Column '{date_col}' not found."
        )

    df = jobs_df.copy()

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce",
    )

    df = df.dropna(subset=[date_col])

    monthly = (
        df.set_index(date_col)
        .resample("MS")
        .size()
        .reset_index(name="y")
    )

    monthly.rename(
        columns={date_col: "ds"},
        inplace=True,
    )

    return monthly


# ============================================================
# FORECAST
# ============================================================

def forecast_hiring_trend(
    jobs_df: pd.DataFrame,
    periods: int = 6,
) -> pd.DataFrame:
    """
    Forecast future hiring demand.

    Parameters
    ----------
    jobs_df : DataFrame
        Raw jobs dataframe.

    periods : int
        Number of future months.

    Returns
    -------
    DataFrame
    """

    monthly = prepare_monthly_series(jobs_df)

    if len(monthly) < 2:
        raise ValueError(
            "At least two months of data required."
        )

    y = monthly["y"].to_numpy(dtype=float)

    X = np.arange(
        len(y),
        dtype=float,
    ).reshape(-1, 1)

    model = LinearRegression()

    model.fit(X, y)

    future_X = np.arange(
        len(y),
        len(y) + periods,
        dtype=float,
    ).reshape(-1, 1)

    predictions = model.predict(future_X)

    predictions = np.maximum(
        predictions,
        0,
    )

    residuals = y - model.predict(X)

    std = float(np.std(residuals))

    future_dates = pd.date_range(
        start=monthly["ds"].iloc[-1]
        + pd.offsets.MonthBegin(1),
        periods=periods,
        freq="MS",
    )

    forecast = pd.DataFrame(
        {
            "ds": future_dates,
            "yhat": predictions.round(0),
            "yhat_lower": np.maximum(
                predictions - std,
                0,
            ).round(0),
            "yhat_upper": (
                predictions + std
            ).round(0),
        }
    )

    return forecast


# ============================================================
# SYNTHETIC DATA
# ============================================================

def generate_synthetic_postings(
    n_months: int = 24,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Create demo dataset.
    """

    rng = np.random.default_rng(seed)

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=n_months,
        freq="MS",
    )

    trend = np.linspace(
        500,
        1500,
        n_months,
    )

    seasonal = (
        150
        * np.sin(
            np.linspace(
                0,
                4 * np.pi,
                n_months,
            )
        )
    )

    noise = rng.normal(
        0,
        80,
        n_months,
    )

    counts = np.maximum(
        trend + seasonal + noise,
        50,
    ).astype(int)

    rows = []

    for d, c in zip(dates, counts):

        rows.extend(
            [
                {"posted_date": d}
                for _ in range(c)
            ]
        )

    return pd.DataFrame(rows)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    jobs = generate_synthetic_postings()

    forecast = forecast_hiring_trend(
        jobs,
        periods=6,
    )

    print(forecast)