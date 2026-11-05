import logging
from unittest.mock import patch

import pandas as pd

from ops.scripts.price_scraper import run_pipeline


@patch("ops.scripts.price_scraper.fetch_flights")
@patch("ops.scripts.price_scraper.insert_flight_prices")
@patch("ops.scripts.price_scraper.get_historical_prices")
@patch("ops.scripts.price_scraper.setup_database")
def test_run_pipeline_detects_dip(
    mock_setup, mock_get_historical, mock_insert, mock_fetch
):
    # Mock routing expansion: just 1 route for simplicity
    with (
        patch(
            "ops.scripts.price_scraper.generate_routes", return_value=[("BSL", "OSL")]
        ),
        patch("ops.scripts.price_scraper.time.sleep"),
    ):
        # Mock fetched flight
        mock_fetch.return_value = [
            {
                "origin": "BSL",
                "destination": "OSL",
                "departure_date": "2026-12-15",
                "price": 100.0,
                "currency": "USD",
                "stops": 0,
                "travel_time_minutes": 150,
            }
        ]

        # Mock historical data: previous prices were 200, 200, current is 100
        data = {
            "scraped_at": pd.date_range(start="2026-06-01", periods=3),
            "price": [200.0, 200.0, 100.0],
        }
        mock_get_historical.return_value = pd.DataFrame(data)

        # Run pipeline
        alerts = run_pipeline(
            "Switzerland", "Norway", "2026-12-15", dip_threshold=0.20, ma_window=3
        )

        # The MA is (200+200+100)/3 = 166.66
        # A 20% dip threshold is 166.66 * 0.8 = 133.32
        # Since 100 < 133.32, it should trigger an alert.
        assert len(alerts) == 1
        assert "PRICE DIP ALERT: BSL->OSL" in alerts[0]

        mock_insert.assert_called_once()
        mock_fetch.assert_called_once_with("BSL", "OSL", "2026-12-15")


def test_run_pipeline_logs_filter_drops(caplog):
    with (
        patch("ops.scripts.price_scraper.fetch_flights") as mock_fetch,
        patch("ops.scripts.price_scraper.insert_flight_prices"),
        patch("ops.scripts.price_scraper.get_historical_prices") as mock_get_historical,
        patch("ops.scripts.price_scraper.setup_database"),
        patch(
            "ops.scripts.price_scraper.generate_routes", return_value=[("BSL", "OSL")]
        ),
        patch("ops.scripts.price_scraper.time.sleep"),
    ):
        mock_fetch.return_value = [
            {
                "origin": "BSL",
                "destination": "OSL",
                "departure_date": "2026-12-15",
                "price": 100.0,
                "currency": "USD",
                "stops": 0,
                "travel_time_minutes": 100,
            },
            {
                "origin": "BSL",
                "destination": "OSL",
                "departure_date": "2026-12-15",
                "price": 120.0,
                "currency": "USD",
                "stops": 2,
                "travel_time_minutes": 200,
            },
        ]
        mock_get_historical.return_value = pd.DataFrame()

        with caplog.at_level(logging.INFO, logger="ops.scripts.price_scraper"):
            run_pipeline(
                "Switzerland",
                "Norway",
                "2026-12-15",
                max_stops=1,
                max_travel_time=150,
                api_pause_seconds=0,
            )

        messages = " ".join(record.message for record in caplog.records)
        assert "max_stops" in messages
        assert "max_travel_time" in messages
        assert "dropped" in messages.lower()
