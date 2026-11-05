"""Tests for the CSV and Markdown shortlist output."""

from src.services.airbnb_report import (
    CSV_COLUMNS,
    format_money,
    write_csv,
    write_markdown,
)
from tests.airbnb_fixtures import SEARCH, normalized_record


def test_format_money_uses_the_currency_code():
    assert format_money(50, "CHF") == "CHF 50.00"
    assert format_money(92.5, "EUR") == "EUR 92.50"
    assert format_money(None, "CHF") == "—"


def test_write_csv_writes_the_schema_and_rows(tmp_path):
    records = [
        normalized_record(listing_id="1", name="Alpha"),
        normalized_record(listing_id="2", name="Beta", price_total=150.0),
    ]
    path = tmp_path / "shortlist.csv"

    write_csv(records, path)

    text = path.read_text(encoding="utf-8")
    header = text.splitlines()[0]
    assert header == ",".join(CSV_COLUMNS)
    assert "Alpha" in text
    assert "Beta" in text
    assert "1" in text
    assert "2" in text


def test_write_markdown_contains_parameters_links_and_drop_report(tmp_path):
    records = [
        normalized_record(listing_id="1", name="Alpha"),
        normalized_record(listing_id="2", name="Beta", price_total=150.0),
    ]
    path = tmp_path / "shortlist.md"

    write_markdown(
        records,
        path,
        search=SEARCH,
        drop_report={"free_cancellation": 1, "max_price_per_night": 2},
        total_raw=5,
    )

    text = path.read_text(encoding="utf-8")
    assert "# Airbnb shortlist — Alsace New Year" in text
    assert "2026-12-31" in text
    assert "2027-01-02" in text
    assert "CHF 46.00" in text
    assert "Alpha" in text
    assert "Beta" in text
    assert "https://www.airbnb.com/rooms/1" in text
    assert "free_cancellation" in text
    assert "max_price_per_night" in text
    assert "5" in text
