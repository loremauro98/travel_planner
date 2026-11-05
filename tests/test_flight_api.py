"""Tests for the SerpApi boundary. No live network calls are made."""

from unittest.mock import patch

from src.services import flight_api


class _FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"best_flights": [], "other_flights": []}


def test_fetch_flights_uses_round_trip_type_with_return_date(monkeypatch):
    monkeypatch.setattr(flight_api, "SERPAPI_KEY", "test-key")

    with patch(
        "src.services.flight_api.requests.get", return_value=_FakeResponse()
    ) as mock_get:
        flight_api.fetch_flights("BSL", "OSL", "2026-12-15", return_date="2026-12-22")

    params = mock_get.call_args.kwargs["params"]
    assert params["type"] == "1"
    assert params["return_date"] == "2026-12-22"


def test_fetch_flights_uses_one_way_type_without_return_date(monkeypatch):
    monkeypatch.setattr(flight_api, "SERPAPI_KEY", "test-key")

    with patch(
        "src.services.flight_api.requests.get", return_value=_FakeResponse()
    ) as mock_get:
        flight_api.fetch_flights("BSL", "OSL", "2026-12-15")

    params = mock_get.call_args.kwargs["params"]
    assert params["type"] == "2"
    assert "return_date" not in params
