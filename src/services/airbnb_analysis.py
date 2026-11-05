"""Normalization, filtering, and sorting for Airbnb search results.

Pure functions only. The network boundary lives in ``airbnb_api.py``.
"""

import re
from datetime import UTC, date, datetime
from urllib.parse import parse_qs, urlencode, urlparse

BADGE_LABELS = {
    "GUEST_FAVORITE": "Guest favourite",
    "TOP_X_GUEST_FAVORITE": "Top guest favourite",
    "FEATURED_HOTEL": "Featured hotel",
}

_BEDROOMS_RE = re.compile(r"([\d.]+)\s+bedroom", re.IGNORECASE)
_BEDS_RE = re.compile(r"([\d.]+)\s+.*?\bbeds?\b", re.IGNORECASE)
_BATHS_RE = re.compile(r"([\d.]+)\s+baths?", re.IGNORECASE)
_TITLE_IN_RE = re.compile(r"^(.*?)\s+in\s+(.+)$", re.IGNORECASE)


def _first(query, key, default=None):
    values = query.get(key)
    if not values:
        return default
    return values[0]


def _number(value):
    number = float(value)
    return int(number) if number.is_integer() else number


def parse_search_url(url, label=None, currency="CHF"):
    """Extract the filters and stay details that matter from an Airbnb search URL."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    check_in = _first(query, "checkin")
    check_out = _first(query, "checkout")
    nights = None
    if check_in and check_out:
        nights = (date.fromisoformat(check_out) - date.fromisoformat(check_in)).days
    if nights is None:
        nights_raw = _first(query, "price_filter_num_nights")
        nights = int(nights_raw) if nights_raw else None

    price_max_raw = _first(query, "price_max")
    price_max = float(price_max_raw) if price_max_raw not in (None, "") else None

    if label is None:
        marker = "/s/"
        if marker in parsed.path:
            slug = parsed.path.split(marker, 1)[1].split("/", 1)[0]
            label = slug.replace("--", ", ").replace("-", " ")
        else:
            label = "Airbnb search"

    return {
        "url": url,
        "label": label,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "adults": int(_first(query, "adults", "1")),
        "price_max": price_max,
        "flexible_cancellation": str(
            _first(query, "flexible_cancellation", "false")
        ).lower()
        in {"true", "1", "yes"},
        "place_id": _first(query, "place_id"),
        "currency": currency,
    }


def _split_title(title):
    title = (title or "").strip()
    match = _TITLE_IN_RE.match(title)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return title, ""


def _parse_price(price, nights):
    unit = (price or {}).get("unit") or {}
    amount = unit.get("amount")
    discount = unit.get("discount")

    price_total = None
    price_original = None
    if discount is not None and discount > 0:
        price_total = float(discount)
        price_original = float(amount) if amount is not None else None
    elif amount is not None:
        price_total = float(amount)

    if price_total is None:
        for item in (price or {}).get("break_down", []):
            if (item.get("description") or "").strip().lower() == "total":
                if item.get("amount") is not None:
                    price_total = float(item["amount"])
                break

    price_per_night = None
    if price_total is not None and nights:
        price_per_night = round(price_total / nights, 2)
    return price_total, price_original, price_per_night


def _parse_layout(structured):
    parts = []
    bedrooms = None
    beds = None
    baths = None

    for message in (structured or {}).get("primaryLine") or []:
        body = (message.get("body") or "").strip()
        if not body:
            continue
        parts.append(body)
        lower = body.lower()

        if "bedroom" in lower:
            match = _BEDROOMS_RE.search(body)
            if match:
                bedrooms = _number(match.group(1))
        elif re.search(r"\bbeds?\b", lower):
            match = _BEDS_RE.search(body)
            if match:
                beds = _number(match.group(1))
        if "bath" in lower:
            match = _BATHS_RE.search(body)
            if match:
                baths = float(match.group(1))

    return "; ".join(parts), bedrooms, beds, baths


def _parse_host_type(structured):
    for message in (structured or {}).get("secondaryLine") or []:
        if message.get("type") == "HOSTINFO" and message.get("body"):
            return message["body"].strip()
    return ""


def _badges(raw):
    labels = []
    for code in raw.get("badges") or []:
        labels.append(BADGE_LABELS.get(code, code.replace("_", " ").title()))
    return "; ".join(labels)


def _has_payment_flag(messages, flag_type, text=None):
    for message in messages or []:
        if message.get("type") == flag_type:
            return True
        if text and text in (message.get("text") or "").lower():
            return True
    return False


def _listing_url(listing_id, search):
    params = {}
    if search.get("adults"):
        params["adults"] = search["adults"]
    if search.get("check_in"):
        params["check_in"] = search["check_in"]
    if search.get("check_out"):
        params["check_out"] = search["check_out"]
    query = urlencode(params)
    return f"https://www.airbnb.com/rooms/{listing_id}" + (f"?{query}" if query else "")


def normalize_listing(raw, search):
    """Turn one raw pyairbnb search result into a flat shortlist record."""
    listing_id = str(raw.get("room_id"))
    property_type, location = _split_title(raw.get("title"))
    price_total, price_original, price_per_night = _parse_price(
        raw.get("price"), search.get("nights")
    )
    layout, bedrooms, beds, baths = _parse_layout(raw.get("structuredContent"))
    messages = raw.get("paymentMessages") or []

    rating_raw = (raw.get("rating") or {}).get("value")
    rating = float(rating_raw) if rating_raw else None
    reviews_raw = (raw.get("rating") or {}).get("reviewCount")
    try:
        reviews = int(reviews_raw) if reviews_raw is not None else None
    except (TypeError, ValueError):
        reviews = None

    coordinates = raw.get("coordinates") or {}
    latitude = coordinates.get("latitude")
    longitude = coordinates.get("longitud", coordinates.get("longitude"))
    images = raw.get("images") or []

    return {
        "listing_id": listing_id,
        "name": (raw.get("name") or "").strip(),
        "property_type": property_type,
        "location": location,
        "price_total": price_total,
        "price_original": price_original,
        "price_per_night": price_per_night,
        "currency": search.get("currency", "CHF"),
        "nights": search.get("nights"),
        "rating": rating,
        "reviews": reviews,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "layout": layout,
        "host_type": _parse_host_type(raw.get("structuredContent")),
        "badges": _badges(raw),
        "free_cancellation": _has_payment_flag(
            messages, "FREE_CANCELLATION_HIGHLIGHT", "free cancellation"
        ),
        "pay_zero_upfront": _has_payment_flag(messages, "PAY_ZERO_UPFRONT_HIGHLIGHT"),
        "latitude": float(latitude) if latitude is not None else None,
        "longitude": float(longitude) if longitude is not None else None,
        "image_url": images[0].get("url", "") if images else "",
        "amenities": "",
        "room_type": "",
        "person_capacity": None,
        "is_super_host": None,
        "url": _listing_url(listing_id, search),
        "check_in": search.get("check_in"),
        "check_out": search.get("check_out"),
        "adults": search.get("adults"),
        "scraped_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "search_label": search.get("label", ""),
    }


def dedupe_listings(records):
    """Keep the first occurrence of each listing ID."""
    seen = set()
    deduped = []
    for record in records:
        listing_id = record["listing_id"]
        if listing_id in seen:
            continue
        seen.add(listing_id)
        deduped.append(record)
    return deduped


def filter_listings(records, filters):
    """Apply local filters sequentially and return (kept, drop_counts).

    Each active criterion gets its own drop count, even when it is zero.
    """
    filters = filters or {}
    kept = list(records)
    drops = {}

    def apply(name, predicate):
        nonlocal kept
        before = len(kept)
        kept = [record for record in kept if predicate(record)]
        drops[name] = before - len(kept)

    if filters.get("require_free_cancellation"):
        apply("free_cancellation", lambda record: bool(record.get("free_cancellation")))

    if filters.get("max_price_per_night") is not None:
        limit = float(filters["max_price_per_night"])
        apply(
            "max_price_per_night",
            lambda record: (
                record.get("price_per_night") is not None
                and record["price_per_night"] <= limit
            ),
        )

    if filters.get("min_price_per_night") is not None:
        limit = float(filters["min_price_per_night"])
        apply(
            "min_price_per_night",
            lambda record: (
                record.get("price_per_night") is not None
                and record["price_per_night"] >= limit
            ),
        )

    if filters.get("min_rating") is not None:
        limit = float(filters["min_rating"])
        apply(
            "min_rating",
            lambda record: (
                record.get("rating") is not None and record["rating"] >= limit
            ),
        )

    if filters.get("min_reviews") is not None:
        limit = int(filters["min_reviews"])
        apply(
            "min_reviews",
            lambda record: (
                record.get("reviews") is not None and record["reviews"] >= limit
            ),
        )

    if filters.get("min_bedrooms") is not None:
        limit = float(filters["min_bedrooms"])
        apply(
            "min_bedrooms",
            lambda record: (
                record.get("bedrooms") is not None and record["bedrooms"] >= limit
            ),
        )

    if filters.get("min_beds") is not None:
        limit = float(filters["min_beds"])
        apply(
            "min_beds",
            lambda record: record.get("beds") is not None and record["beds"] >= limit,
        )

    if filters.get("min_baths") is not None:
        limit = float(filters["min_baths"])
        apply(
            "min_baths",
            lambda record: record.get("baths") is not None and record["baths"] >= limit,
        )

    if filters.get("exclude_hotels"):
        apply(
            "exclude_hotels",
            lambda record: (
                "hotel" not in (record.get("property_type") or "").lower()
                and "hotel" not in (record.get("badges") or "").lower()
            ),
        )

    excluded_types = {
        value.lower() for value in filters.get("exclude_property_types") or []
    }
    if excluded_types:
        apply(
            "exclude_property_types",
            lambda record: (
                (record.get("property_type") or "").lower() not in excluded_types
            ),
        )

    return kept, drops


def sort_listings(records, sort_by="price_per_night", descending=False):
    """Sort by a numeric field, always putting missing values last."""

    def key(record):
        value = record.get(sort_by)
        if value is None:
            return (1, 0)
        return (0, -value if descending else value)

    return sorted(records, key=key)


def apply_details(record, details):
    """Flatten the useful pyairbnb detail fields into a normalized record."""
    if not details:
        return record

    amenities = []
    for group in details.get("amenities") or []:
        for value in group.get("values") or []:
            if value.get("available", True) and value.get("title"):
                amenities.append(value["title"])
    record["amenities"] = "; ".join(amenities)
    record["room_type"] = details.get("room_type") or ""
    record["person_capacity"] = details.get("person_capacity")
    record["is_super_host"] = details.get("is_super_host")
    return record
