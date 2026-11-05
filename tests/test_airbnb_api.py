"""Tests for the pyairbnb boundary. No live network calls are made."""

from datetime import date

from src.services import airbnb_api


def test_search_listings_caps_results_and_passes_currency(monkeypatch):
    calls = []

    def fake_search(url, currency, language, timeout):
        calls.append(
            {"url": url, "currency": currency, "language": language, "timeout": timeout}
        )
        return [{"room_id": 1}, {"room_id": 2}, {"room_id": 3}]

    monkeypatch.setattr(airbnb_api.pyairbnb, "search_all_from_url", fake_search)

    results = airbnb_api.search_listings(
        "https://www.airbnb.com/s/Alsace--France/homes",
        currency="CHF",
        language="en",
        max_results=2,
        timeout=30,
    )

    assert len(results) == 2
    assert calls[0]["currency"] == "CHF"
    assert calls[0]["language"] == "en"
    assert calls[0]["timeout"] == 30


def test_get_listing_details_converts_dates_and_returns_details(monkeypatch):
    calls = []

    def fake_details(**kwargs):
        calls.append(kwargs)
        return {"amenities": [{"title": "Internet", "values": []}]}

    monkeypatch.setattr(airbnb_api.pyairbnb, "get_details", fake_details)

    details = airbnb_api.get_listing_details(
        room_id="123",
        check_in="2026-12-31",
        check_out="2027-01-02",
        adults=2,
        currency="CHF",
        language="en",
        timeout=30,
    )

    assert details["amenities"][0]["title"] == "Internet"
    assert calls[0]["check_in"] == date(2026, 12, 31)
    assert calls[0]["check_out"] == date(2027, 1, 2)
    assert calls[0]["adults"] == 2
    assert calls[0]["currency"] == "CHF"


def test_get_listing_details_returns_empty_on_failure(monkeypatch):
    def failing_details(**kwargs):
        raise RuntimeError("blocked")

    monkeypatch.setattr(airbnb_api.pyairbnb, "get_details", failing_details)

    details = airbnb_api.get_listing_details(
        room_id="123",
        check_in="2026-12-31",
        check_out="2027-01-02",
        adults=2,
        currency="CHF",
    )

    assert details == {}
