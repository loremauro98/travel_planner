import pandas as pd

from src.services.analytics import calculate_moving_average, detect_price_dips


def test_calculate_moving_average():
    # Setup dummy time-series data
    data = {
        "scraped_at": pd.date_range(start="2026-06-01", periods=5),
        "price": [100.0, 120.0, 80.0, 90.0, 110.0],
    }
    df = pd.DataFrame(data)

    # Calculate 3-period moving average
    result = calculate_moving_average(df, window_size=3)

    assert "ma_3" in result.columns
    # Check manual calculations
    assert result["ma_3"].iloc[0] == 100.0  # Just 100
    assert result["ma_3"].iloc[1] == 110.0  # (100+120)/2
    assert result["ma_3"].iloc[2] == 100.0  # (100+120+80)/3
    assert result["ma_3"].iloc[4] == 93.33333333333333  # (80+90+110)/3


def test_calculate_moving_average_respects_min_periods():
    data = {
        "scraped_at": pd.date_range(start="2026-06-01", periods=3),
        "price": [100.0, 120.0, 80.0],
    }
    df = pd.DataFrame(data)

    result = calculate_moving_average(df, window_size=3, min_periods=3)

    assert pd.isna(result["ma_3"].iloc[0])
    assert pd.isna(result["ma_3"].iloc[1])
    assert result["ma_3"].iloc[2] == 100.0


def test_detect_price_dips():
    # Setup dummy data with a calculated MA
    data = {
        "scraped_at": pd.date_range(start="2026-06-01", periods=3),
        "price": [100.0, 100.0, 80.0],
        "ma_3": [100.0, 100.0, 93.33],
    }
    df = pd.DataFrame(data)

    # We want to detect a 10% dip
    # 93.33 * 0.9 = 83.99, so 80.0 is indeed a dip!
    dips = detect_price_dips(df, "ma_3", 0.10)

    assert len(dips) == 1
    assert dips["price"].iloc[0] == 80.0
