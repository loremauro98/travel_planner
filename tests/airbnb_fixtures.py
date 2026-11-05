"""Shared fixtures for the Airbnb search tests.

These are test-only helpers. Production code lives in ``src/services``.
"""

SEARCH = {
    "label": "Alsace New Year",
    "check_in": "2026-12-31",
    "check_out": "2027-01-02",
    "adults": 2,
    "nights": 2,
    "currency": "CHF",
}

CLEAN_URL = (
    "https://www.airbnb.com/s/Alsace--France/homes?"
    "adults=2"
    "&checkin=2026-12-31"
    "&checkout=2027-01-02"
    "&place_id=ChIJv5Z326NGkUcR4CQ3mrlfCgE"
    "&refinement_paths%5B%5D=%2Fhomes"
    "&flexible_cancellation=true"
    "&price_max=150"
    "&price_filter_input_type=2"
    "&price_filter_num_nights=2"
)


def raw_listing(**overrides):
    """A discounted listing with free cancellation (On the edge of the forest)."""
    raw = {
        "room_id": 1152624935316030781,
        "name": "On the edge of the forest, close to the city",
        "title": "Apartment in Chantraine, France",
        "price": {
            "unit": {
                "qualifier": "total",
                "curency_symbol": "Fr.\u00a0",
                "amount": 109.0,
                "discount": 92.0,
            },
            "total": {"currency_symbol": "", "amount": 0},
            "break_down": [
                {
                    "description": "2 nights x Fr.\u00a051.85",
                    "amount": 103.65,
                    "currency": "Fr.\u00a0",
                },
                {
                    "description": "Early booking discount",
                    "amount": -14.3,
                    "currency": "Fr.\u00a0",
                },
                {
                    "description": "Discount from Airbnb",
                    "amount": -2.25,
                    "currency": "Fr.\u00a0",
                },
                {"description": "Taxes", "amount": 4.45, "currency": "Fr.\u00a0"},
                {"description": "Total", "amount": 91.55, "currency": "Fr.\u00a0"},
            ],
        },
        "rating": {"value": 4.91, "reviewCount": "131"},
        "badges": ["GUEST_FAVORITE"],
        "paymentMessages": [
            {
                "text": "Pay Fr.\u00a00 today",
                "type": "PAY_ZERO_UPFRONT_HIGHLIGHT",
            },
            {
                "text": "Free cancellation",
                "type": "FREE_CANCELLATION_HIGHLIGHT",
            },
        ],
        "structuredContent": {
            "primaryLine": [
                {"body": "1 bedroom", "type": "BEDINFO"},
                {"body": "1 double bed", "type": "BEDINFO"},
                {"body": "1 bath", "type": "BATHROOMINFO"},
            ],
            "secondaryLine": [{"body": "Individual host", "type": "HOSTINFO"}],
        },
        "coordinates": {"latitude": 48.0599, "longitud": 6.3014},
        "images": [{"url": "https://example.com/forest.jpg"}],
    }
    raw.update(overrides)
    return raw


def raw_listing_without_discount(**overrides):
    """A non-discounted listing without free cancellation (Studio Turckheim)."""
    raw = {
        "room_id": 844852770866183803,
        "name": "Studio* the Turckheim lookout vineyards* forests*",
        "title": "Apartment in Turckheim, France",
        "price": {
            "unit": {
                "qualifier": "total",
                "curency_symbol": "Fr.\u00a0",
                "amount": 157.0,
            },
            "total": {"currency_symbol": "", "amount": 0},
            "break_down": [
                {
                    "description": "2 nights x Fr.\u00a074.30",
                    "amount": 148.6,
                    "currency": "Fr.\u00a0",
                },
                {"description": "Taxes", "amount": 7.6, "currency": "Fr.\u00a0"},
                {"description": "Total", "amount": 156.2, "currency": "Fr.\u00a0"},
            ],
        },
        "rating": {"value": 4.63, "reviewCount": "181"},
        "badges": [],
        "paymentMessages": [],
        "structuredContent": {
            "primaryLine": [
                {"body": "1 bedroom", "type": "BEDINFO"},
                {"body": "2 beds", "type": "BEDINFO"},
                {"body": "1 bath", "type": "BATHROOMINFO"},
            ],
            "secondaryLine": [{"body": "Business host", "type": "HOSTINFO"}],
        },
        "coordinates": {"latitude": 48.09776, "longitud": 7.22904},
        "images": [{"url": "https://example.com/turckheim.jpg"}],
    }
    raw.update(overrides)
    return raw


def normalized_record(**overrides):
    """A flat record matching the output schema, for report tests."""
    record = {
        "listing_id": "1152624935316030781",
        "name": "On the edge of the forest, close to the city",
        "property_type": "Apartment",
        "location": "Chantraine, France",
        "price_total": 92.0,
        "price_original": 109.0,
        "price_per_night": 46.0,
        "currency": "CHF",
        "nights": 2,
        "rating": 4.91,
        "reviews": 131,
        "bedrooms": 1,
        "beds": 1,
        "baths": 1.0,
        "layout": "1 bedroom; 1 double bed; 1 bath",
        "host_type": "Individual host",
        "badges": "Guest favourite",
        "free_cancellation": True,
        "pay_zero_upfront": True,
        "latitude": 48.0599,
        "longitude": 6.3014,
        "image_url": "https://example.com/forest.jpg",
        "amenities": "Wifi; Kitchen",
        "room_type": "Entire home/apt",
        "person_capacity": 2,
        "is_super_host": False,
        "url": "https://www.airbnb.com/rooms/1152624935316030781?adults=2&check_in=2026-12-31&check_out=2027-01-02",
        "check_in": "2026-12-31",
        "check_out": "2027-01-02",
        "adults": 2,
        "scraped_at": "2026-11-05T12:00:00+00:00",
        "search_label": "Alsace New Year",
    }
    record.update(overrides)
    return record
