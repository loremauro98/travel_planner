"""CSV and Markdown output for the Airbnb shortlist."""

import csv
from datetime import UTC, datetime
from pathlib import Path

CSV_COLUMNS = [
    "listing_id",
    "name",
    "property_type",
    "location",
    "price_total",
    "price_original",
    "price_per_night",
    "currency",
    "nights",
    "rating",
    "reviews",
    "bedrooms",
    "beds",
    "baths",
    "layout",
    "host_type",
    "badges",
    "free_cancellation",
    "pay_zero_upfront",
    "latitude",
    "longitude",
    "image_url",
    "amenities",
    "room_type",
    "person_capacity",
    "is_super_host",
    "url",
    "check_in",
    "check_out",
    "adults",
    "scraped_at",
    "search_label",
]


def format_money(amount, currency="CHF"):
    if amount is None:
        return "—"
    return f"{currency} {amount:,.2f}"


def _cell(value):
    if value is None:
        return ""
    return str(value).replace("|", "\\|")


def _type_location(record):
    property_type = record.get("property_type") or ""
    location = record.get("location") or ""
    if property_type and location:
        return f"{property_type} · {location}"
    return property_type or location or "—"


def _rating_text(record):
    if record.get("rating") is None:
        return "—"
    text = f"{record['rating']:.2f}"
    if record.get("reviews") is not None:
        text += f" ({record['reviews']})"
    return text


def _drop_line(drop_report):
    if not drop_report:
        return "- **Dropped:** none"
    parts = [f"{name}={count}" for name, count in drop_report.items()]
    return "- **Dropped:** " + ", ".join(parts)


def write_csv(records, path):
    """Write the normalized records to a UTF-8 CSV with a fixed schema."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({column: record.get(column, "") for column in CSV_COLUMNS})


def write_markdown(
    records, path, search, drop_report=None, total_raw=0, after_filters=None
):
    """Write a human-readable shortlist with parameters, table, and drop report."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    currency = search.get("currency", "CHF")
    label = search.get("label") or "Airbnb search"
    after_filters = len(records) if after_filters is None else after_filters

    lines = [
        f"# Airbnb shortlist — {label}",
        "",
        f"- **Search:** {search.get('url', '')}",
        (
            f"- **Dates:** {search.get('check_in') or '—'} → {search.get('check_out') or '—'}"
            f" ({search.get('nights') or '—'} nights)"
        ),
        f"- **Guests:** {search.get('adults') or '—'} adults",
        f"- **Currency:** {currency}",
        f"- **Generated:** {datetime.now(UTC).isoformat(timespec='seconds')}",
        "",
        "## Summary",
        "",
        f"- **Listings retrieved:** {total_raw}",
        f"- **Listings after filters:** {after_filters}",
        f"- **Shortlist shown:** {len(records)}",
        _drop_line(drop_report),
        "",
        "## Shortlist",
        "",
    ]

    if not records:
        lines.append("No listings matched the filters.")
    else:
        lines.append(
            "| # | Property | Type & location | Price/night | Total | Rating | Layout | Badges |"
        )
        lines.append("|---|---|---|---|---|---|---|---|")
        for index, record in enumerate(records, start=1):
            total = format_money(record.get("price_total"), currency)
            if record.get("price_original") is not None:
                total += f" (was {format_money(record['price_original'], currency)})"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(index),
                        f"[{_cell(record.get('name'))}]({record.get('url', '')})",
                        _cell(_type_location(record)),
                        format_money(record.get("price_per_night"), currency),
                        _cell(total),
                        _rating_text(record),
                        _cell(record.get("layout")),
                        _cell(record.get("badges")),
                    ]
                )
                + " |"
            )

    enriched = [
        record
        for record in records
        if record.get("amenities") or record.get("room_type")
    ]
    if enriched:
        lines.extend(["", "## Top picks — details", ""])
        for index, record in enumerate(enriched, start=1):
            lines.append(
                f"### {index}. [{record.get('name')}]({record.get('url', '')})"
            )
            lines.append("")
            room_type = record.get("room_type") or record.get("property_type") or "—"
            capacity = record.get("person_capacity") or "—"
            lines.append(f"- **Type:** {room_type} · {capacity} guests")
            price_line = (
                f"- **Price:** {format_money(record.get('price_per_night'), currency)}/night"
                f" · {format_money(record.get('price_total'), currency)} total"
            )
            if record.get("price_original") is not None:
                price_line += (
                    f" (was {format_money(record['price_original'], currency)})"
                )
            lines.append(price_line)
            lines.append(f"- **Rating:** {_rating_text(record)}")
            lines.append(f"- **Layout:** {record.get('layout') or '—'}")
            if record.get("amenities"):
                lines.append(f"- **Amenities:** {record['amenities']}")
            lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- Prices are the Airbnb total for the stay; per-night is derived from the search card breakdown.",
            "- `Free cancellation` is taken from Airbnb's payment message, not assumed from the filter.",
            "- Verify availability and the final price on Airbnb before booking.",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
