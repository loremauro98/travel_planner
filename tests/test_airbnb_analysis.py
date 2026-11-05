"""Tests for Airbnb URL parsing, normalization, filtering, and sorting."""

from src.services.airbnb_analysis import (
    apply_details,
    dedupe_listings,
    filter_listings,
    normalize_listing,
    parse_search_url,
    sort_listings,
)
from tests.airbnb_fixtures import (
    CLEAN_URL,
    SEARCH,
    raw_listing,
    raw_listing_without_discount,
)


def test_parse_search_url_extracts_filters_and_nights():
    search = parse_search_url(CLEAN_URL, label="Alsace New Year", currency="CHF")

    assert search["check_in"] == "2026-12-31"
    assert search["check_out"] == "2027-01-02"
    assert search["adults"] == 2
    assert search["nights"] == 2
    assert search["price_max"] == 150.0
    assert search["flexible_cancellation"] is True
    assert search["place_id"] == "ChIJv5Z326NGkUcR4CQ3mrlfCgE"
    assert search["label"] == "Alsace New Year"
    assert search["currency"] == "CHF"


def test_normalize_listing_maps_discounted_price_layout_and_cancellation():
    record = normalize_listing(raw_listing(), SEARCH)

    assert record["listing_id"] == "1152624935316030781"
    assert record["name"] == "On the edge of the forest, close to the city"
    assert record["property_type"] == "Apartment"
    assert record["location"] == "Chantraine, France"

    assert record["price_total"] == 92.0
    assert record["price_original"] == 109.0
    assert record["price_per_night"] == 46.0
    assert record["currency"] == "CHF"

    assert record["rating"] == 4.91
    assert record["reviews"] == 131
    assert record["bedrooms"] == 1
    assert record["beds"] == 1
    assert record["baths"] == 1.0
    assert record["layout"] == "1 bedroom; 1 double bed; 1 bath"
    assert record["host_type"] == "Individual host"
    assert record["badges"] == "Guest favourite"
    assert record["free_cancellation"] is True
    assert record["pay_zero_upfront"] is True

    assert record["latitude"] == 48.0599
    assert record["longitude"] == 6.3014
    assert record["image_url"] == "https://example.com/forest.jpg"
    assert record["url"].startswith("https://www.airbnb.com/rooms/1152624935316030781")
    assert "check_in=2026-12-31" in record["url"]
    assert record["amenities"] == ""


def test_normalize_listing_without_discount_uses_unit_amount():
    record = normalize_listing(raw_listing_without_discount(), SEARCH)

    assert record["price_total"] == 157.0
    assert record["price_original"] is None
    assert record["price_per_night"] == 78.5
    assert record["free_cancellation"] is False
    assert record["badges"] == ""
    assert record["host_type"] == "Business host"
    assert record["beds"] == 2
    assert record["layout"] == "1 bedroom; 2 beds; 1 bath"


def test_dedupe_listings_keeps_the_first_occurrence():
    first = normalize_listing(raw_listing(), SEARCH)
    duplicate = dict(first, name="duplicate")
    other = normalize_listing(raw_listing_without_discount(), SEARCH)

    deduped = dedupe_listings([first, duplicate, other])

    assert len(deduped) == 2
    assert deduped[0]["name"] == "On the edge of the forest, close to the city"


def test_filter_listings_reports_drop_count_per_criterion():
    records = [
        normalize_listing(raw_listing(), SEARCH),
        normalize_listing(raw_listing(room_id=2, name="Pricey"), SEARCH),
        normalize_listing(
            raw_listing(
                room_id=3,
                name="No cancellation",
                paymentMessages=[],
            ),
            SEARCH,
        ),
        normalize_listing(
            raw_listing(
                room_id=4,
                name="Low rating",
                rating={"value": 4.5, "reviewCount": "20"},
            ),
            SEARCH,
        ),
        normalize_listing(raw_listing(room_id=5, name="Another keeper"), SEARCH),
    ]
    # Make the second record too expensive without touching the first.
    records[1]["price_per_night"] = 120.0

    kept, drops = filter_listings(
        records,
        {
            "require_free_cancellation": True,
            "max_price_per_night": 100.0,
            "min_rating": 4.8,
        },
    )

    assert [record["name"] for record in kept] == [
        "On the edge of the forest, close to the city",
        "Another keeper",
    ]
    assert drops == {
        "free_cancellation": 1,
        "max_price_per_night": 1,
        "min_rating": 1,
    }


def test_filter_listings_can_exclude_non_stay_property_types():
    campsite = normalize_listing(
        raw_listing(room_id=20, title="Campsite in Schonach, Germany"),
        SEARCH,
    )
    apartment = normalize_listing(raw_listing(room_id=21), SEARCH)

    kept, drops = filter_listings(
        [campsite, apartment],
        {"exclude_property_types": ["Campsite"]},
    )

    assert [record["listing_id"] for record in kept] == ["21"]
    assert drops == {"exclude_property_types": 1}


def test_apply_details_flattens_available_amenities():
    record = normalize_listing(raw_listing(), SEARCH)
    details = {
        "amenities": [
            {
                "title": "Internet and office",
                "values": [
                    {"title": "Wifi", "available": True},
                    {"title": "Ethernet", "available": False},
                ],
            }
        ],
        "room_type": "Entire home/apt",
        "person_capacity": 2,
        "is_super_host": False,
    }

    enriched = apply_details(record, details)

    assert enriched["amenities"] == "Wifi"
    assert enriched["room_type"] == "Entire home/apt"
    assert enriched["person_capacity"] == 2
    assert enriched["is_super_host"] is False


def test_sort_listings_puts_missing_values_last():
    cheap = normalize_listing(raw_listing(room_id=10), SEARCH)
    cheap["price_per_night"] = 50.0
    expensive = normalize_listing(raw_listing(room_id=11), SEARCH)
    expensive["price_per_night"] = 100.0
    unknown = normalize_listing(raw_listing(room_id=12), SEARCH)
    unknown["price_per_night"] = None

    ordered = sort_listings([expensive, unknown, cheap], sort_by="price_per_night")

    assert [
        record["room_id"] if "room_id" in record else record["listing_id"]
        for record in ordered
    ] == [
        "10",
        "11",
        "12",
    ]
