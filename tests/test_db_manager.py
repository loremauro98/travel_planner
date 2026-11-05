"""Tests for the SQLite storage layer."""

import pandas as pd
import pytest

from src.database import db_manager


def test_database_path_lives_under_data():
    assert db_manager.DB_PATH.parent.name == "data"
    assert db_manager.DB_PATH.name == "flight_data.db"


def test_setup_insert_and_query(tmp_path, monkeypatch):
    db_path = tmp_path / "nested" / "test.db"
    monkeypatch.setattr(db_manager, "DB_PATH", db_path)

    db_manager.setup_database()
    assert db_path.exists(), (
        "setup_database must create the parent directory and the file"
    )

    db_manager.insert_flight_prices(
        [
            {
                "origin": "BSL",
                "destination": "OSL",
                "departure_date": "2026-12-15",
                "return_date": None,
                "price": 100.0,
                "currency": "USD",
                "stops": 0,
                "travel_time_minutes": 150,
            }
        ]
    )

    df = db_manager.get_historical_prices("BSL", "OSL", "2026-12-15")
    assert len(df) == 1
    assert df["price"].iloc[0] == pytest.approx(100.0)
    assert pd.api.types.is_datetime64_any_dtype(df["scraped_at"])
