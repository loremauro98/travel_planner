"""Run an Airbnb search and write a CSV + Markdown shortlist.

Example:
    C:\\Users\\lorem\\miniconda3\\envs\\travel\\python.exe ops\\scripts\\airbnb_search.py ^
        --config ops\\configs\\airbnb_alsace.json
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

# Ensure src modules can be imported when running ops/scripts
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.services.airbnb_analysis import (
    apply_details,
    dedupe_listings,
    filter_listings,
    normalize_listing,
    parse_search_url,
    sort_listings,
)
from src.services.airbnb_api import get_listing_details, search_listings
from src.services.airbnb_report import write_csv, write_markdown

logger = logging.getLogger(__name__)


def load_config(path):
    """Load a JSON search configuration."""
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if not config.get("url"):
        raise ValueError(f"Config {path} must contain a 'url' field.")
    return config


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return slug or "airbnb"


def build_output_paths(search, out_dir="current_output", label=None):
    """Return (csv_path, markdown_path) for a search."""
    out_dir = Path(out_dir)
    stem = (
        f"airbnb_{slugify(label or search.get('label') or 'search')}"
        f"_{search.get('check_in') or 'undated'}"
        f"_{search.get('check_out') or 'undated'}"
    )
    return out_dir / f"{stem}.csv", out_dir / f"{stem}.md"


def enrich_records(records, top_n, search):
    """Enrich the first top_n records with listing details."""
    if top_n <= 0:
        return records

    enriched = []
    for index, record in enumerate(records):
        if index < top_n:
            details = get_listing_details(
                room_id=record["listing_id"],
                check_in=search.get("check_in"),
                check_out=search.get("check_out"),
                adults=search.get("adults", 1),
                currency=search.get("currency", "CHF"),
            )
            record = apply_details(record, details)
        enriched.append(record)
    return enriched


def run_search(config, out_dir="current_output"):
    """Execute one search and write the CSV/Markdown outputs."""
    search = parse_search_url(
        config["url"],
        label=config.get("label"),
        currency=config.get("currency", "CHF"),
    )

    raw = search_listings(
        config["url"],
        currency=search["currency"],
        language=config.get("language", "en"),
        timeout=config.get("timeout", 90),
    )

    records = [normalize_listing(item, search) for item in raw]
    records = dedupe_listings(records)

    filters = dict(config.get("filters") or {})
    if "require_free_cancellation" not in filters:
        filters["require_free_cancellation"] = search["flexible_cancellation"]
    if "max_price_per_night" not in filters and search.get("price_max") is not None:
        filters["max_price_per_night"] = search["price_max"]

    records, drops = filter_listings(records, filters)
    records = sort_listings(
        records,
        sort_by=config.get("sort_by", "price_per_night"),
        descending=config.get("descending", False),
    )
    after_filters = len(records)
    if config.get("max_results") is not None:
        records = records[: int(config["max_results"])]
    records = enrich_records(records, int(config.get("enrich_top", 0)), search)

    csv_path, md_path = build_output_paths(search, out_dir, config.get("label"))
    write_csv(records, csv_path)
    write_markdown(
        records,
        md_path,
        search=search,
        drop_report=drops,
        total_raw=len(raw),
        after_filters=after_filters,
    )

    return {
        "search": search,
        "records": records,
        "drops": drops,
        "total_raw": len(raw),
        "after_filters": after_filters,
        "csv_path": csv_path,
        "md_path": md_path,
    }


def _print_summary(result):
    records = result["records"]
    print(
        f"Retrieved {result['total_raw']} listings; "
        f"{result.get('after_filters', len(records))} after filters; "
        f"showing {len(records)}."
    )
    for name, count in result["drops"].items():
        print(f"  filter {name}: dropped {count}")
    print()
    for index, record in enumerate(records[:10], start=1):
        price = record.get("price_per_night")
        price_text = f"{record['currency']} {price:.2f}" if price is not None else "—"
        rating = record.get("rating")
        rating_text = f"{rating:.2f}" if rating is not None else "—"
        print(
            f"{index:>2}. {record['name'][:70]:<70} "
            f"{price_text:>12}  {rating_text:>4}  {record['url']}"
        )
    print()
    print(f"CSV:      {result['csv_path']}")
    print(f"Markdown: {result['md_path']}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Airbnb search to CSV + Markdown shortlist"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--config", help="Path to a JSON search config")
    source.add_argument("--url", help="Airbnb search URL")
    parser.add_argument("--label", help="Short label used in the report and filenames")
    parser.add_argument("--currency", default=None, help="Currency code, e.g. CHF")
    parser.add_argument("--language", default=None, help="Locale, e.g. en")
    parser.add_argument("--max-results", type=int, default=None)
    parser.add_argument("--enrich-top", type=int, default=None)
    parser.add_argument("--sort-by", default=None)
    parser.add_argument("--descending", action="store_true")
    parser.add_argument("--out-dir", default="current_output")
    return parser


def main(argv=None):
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stdout
    )
    args = build_parser().parse_args(argv)

    config = load_config(args.config) if args.config else {"url": args.url}
    for key, value in (
        ("label", args.label),
        ("currency", args.currency),
        ("language", args.language),
        ("max_results", args.max_results),
        ("enrich_top", args.enrich_top),
        ("sort_by", args.sort_by),
    ):
        if value is not None:
            config[key] = value
    if args.descending:
        config["descending"] = True

    result = run_search(config, out_dir=args.out_dir)
    _print_summary(result)


if __name__ == "__main__":
    main()
