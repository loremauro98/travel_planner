"""Tests for the Airbnb CLI helpers. No live network calls are made."""

import json

import ops.scripts.airbnb_search as airbnb_cli
from tests.airbnb_fixtures import CLEAN_URL, SEARCH, normalized_record, raw_listing


def test_load_config_reads_json(tmp_path):
    path = tmp_path / "search.json"
    path.write_text(
        json.dumps({"url": "https://example.com", "label": "Test"}), encoding="utf-8"
    )

    config = airbnb_cli.load_config(path)

    assert config["url"] == "https://example.com"
    assert config["label"] == "Test"


def test_build_output_paths_uses_label_and_dates(tmp_path):
    csv_path, md_path = airbnb_cli.build_output_paths(SEARCH, tmp_path)

    assert csv_path.name == "airbnb_alsace_new_year_2026-12-31_2027-01-02.csv"
    assert md_path.name == "airbnb_alsace_new_year_2026-12-31_2027-01-02.md"
    assert csv_path.parent == tmp_path


def test_enrich_records_only_enriches_the_top_n(monkeypatch):
    records = [
        normalized_record(listing_id="1", name="Alpha"),
        normalized_record(listing_id="2", name="Beta"),
        normalized_record(listing_id="3", name="Gamma"),
    ]
    calls = []

    def fake_details(**kwargs):
        calls.append(kwargs["room_id"])
        return {
            "amenities": [
                {"title": "Internet", "values": [{"title": "Wifi", "available": True}]}
            ],
            "room_type": "Entire home/apt",
            "person_capacity": 2,
            "is_super_host": False,
        }

    monkeypatch.setattr(airbnb_cli, "get_listing_details", fake_details)

    enriched = airbnb_cli.enrich_records(records, top_n=2, search=SEARCH)

    assert calls == ["1", "2"]
    assert enriched[0]["amenities"] == "Wifi"
    assert enriched[1]["amenities"] == "Wifi"
    assert enriched[2]["amenities"] == "Wifi; Kitchen"


def test_run_search_filters_then_caps_and_writes_outputs(monkeypatch, tmp_path):
    raws = []
    for room_id, amount, discount in [
        (101, 200.0, 100.0),  # CHF 50/night
        (102, 300.0, None),  # CHF 150/night, dropped by the local price cap
        (103, 120.0, None),  # CHF 60/night
        (104, 80.0, None),  # CHF 40/night
    ]:
        raw = raw_listing(room_id=room_id, name=f"Listing {room_id}")
        raw["price"]["unit"]["amount"] = amount
        if discount is None:
            raw["price"]["unit"].pop("discount", None)
        else:
            raw["price"]["unit"]["discount"] = discount
        raws.append(raw)

    monkeypatch.setattr(airbnb_cli, "search_listings", lambda *args, **kwargs: raws)
    monkeypatch.setattr(airbnb_cli, "get_listing_details", lambda **kwargs: {})

    config = {
        "url": CLEAN_URL,
        "label": "Cap Test",
        "currency": "CHF",
        "max_results": 2,
        "enrich_top": 0,
        "filters": {
            "require_free_cancellation": True,
            "max_price_per_night": 100,
        },
    }

    result = airbnb_cli.run_search(config, out_dir=tmp_path)

    assert result["total_raw"] == 4
    assert result["after_filters"] == 3
    assert [record["listing_id"] for record in result["records"]] == ["104", "101"]
    assert result["csv_path"].exists()
    assert result["md_path"].exists()
