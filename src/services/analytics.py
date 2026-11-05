"""
analytics.py - Statistical analysis and moving averages for flight prices.
"""

import pandas as pd


def calculate_moving_average(df, window_size, min_periods=1):
    """
    Calculates the moving average for the price column over a given window.
    Sorts by scraped_at to ensure chronological order. Both the window and the
    minimum number of observations are explicit parameters.
    """
    if df.empty or "price" not in df.columns or "scraped_at" not in df.columns:
        return df

    # Ensure chronological order
    df = df.sort_values(by="scraped_at").copy()

    # Calculate rolling mean
    ma_col = f"ma_{window_size}"
    df[ma_col] = df["price"].rolling(window=window_size, min_periods=min_periods).mean()

    return df


def detect_price_dips(df, ma_column, threshold_percentage):
    """
    Detects if the current price is significantly below the moving average.
    threshold_percentage: float (e.g., 0.10 for 10% below MA)
    Returns a DataFrame containing only the rows where a dip was detected.
    """
    if df.empty or ma_column not in df.columns:
        return pd.DataFrame()

    # A dip occurs if price <= MA * (1 - threshold)
    threshold_value = df[ma_column] * (1.0 - threshold_percentage)
    is_dip = df["price"] <= threshold_value

    return df[is_dip]
