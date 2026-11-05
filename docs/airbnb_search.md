# Airbnb Search & Shortlist

A repeatable replacement for the manual Airbnb loop: set filters once, run one command, get a CSV
and a Markdown shortlist.

## Quickstart

1. Set the filters in Airbnb and copy the search URL.
2. Put the cleaned URL in a config (copy `ops/configs/airbnb_alsace.json`).
3. Run:

```powershell
& "C:\Users\lorem\miniconda3\envs\travel\python.exe" `
    ops\scripts\airbnb_search.py --config ops\configs\airbnb_alsace.json
```

4. Open the outputs:

```text
current_output/airbnb_alsace_new_year_2026-12-31_2027-01-02.csv
current_output/airbnb_alsace_new_year_2026-12-31_2027-01-02.md
```

## What the URL controls

The cleaned search URL is the source of truth:

- `place_id`, `checkin`, `checkout`, `adults`
- `price_max`, `price_filter_input_type`, `price_filter_num_nights`
- `flexible_cancellation`
- `refinement_paths[]=/homes`
- `room_types[]=Entire home/apt` (whole house/flat only)

Strip tracking and date-picker state (`acp_id`, `ref_fsid`, `ref_search_session_id`,
`selected_filter_order`, `monthly_*`, `flexible_trip_lengths`, `date_picker_type`). In the Alsace
spike, the cleaned URL reproduced the visible page’s top listings; the full URL did not.

## Config

```json
{
  "label": "Alsace New Year",
  "url": "https://www.airbnb.com/s/Alsace--France/homes?...",
  "currency": "CHF",
  "language": "en",
  "max_results": 40,
  "enrich_top": 5,
  "sort_by": "price_per_night",
  "descending": false,
  "filters": {
    "require_free_cancellation": true,
    "max_price_per_night": 150,
    "min_rating": null,
    "min_reviews": null,
    "exclude_hotels": true,
    "exclude_property_types": ["Room", "Campsite", "Parking space"]
  }
}
```

- `max_results` applies after filtering and sorting, before enrichment.
- `enrich_top` fetches amenities, room type, and capacity for the top N.
- Local filters are a safety net; the URL remains the primary filter definition.

## Output columns

`listing_id, name, property_type, location, price_total, price_original, price_per_night, currency,
nights, rating, reviews, bedrooms, beds, baths, layout, host_type, badges, free_cancellation,
pay_zero_upfront, latitude, longitude, image_url, amenities, room_type, person_capacity,
is_super_host, url, check_in, check_out, adults, scraped_at, search_label`

Price rules:

- `price_total` uses the discounted card total when Airbnb shows one.
- `price_original` preserves the pre-discount total.
- `price_per_night` is derived from the stay total and the date range.
- The currency label comes from the config (`CHF`), not the display symbol.

## What it does not do

- It does not book, message hosts, or pay.
- It does not crawl every result; Airbnb’s API returns a practical cap (280 in the Alsace sample)
  while the page counts “over 1,000 homes.”
- It does not persist a watchlist yet. Outputs are one-off files in `current_output/` (gitignored).

## Verification

- `pytest tests/test_airbnb_*.py` — unit tests with mocked API calls.
- Compare the top five names and totals against the visible Airbnb page before trusting a run.
- The sample run returned 280 listings, 204 after local filters, and a 40-row shortlist; all 40 rows
  were entire places.

## BrowserOS fallback

If the API is blocked, open the same cleaned URL in BrowserOS, wait for
`[data-testid="card-container"]`, read the page, and extract the cards. Do not click every listing.

## Safety

Airbnb has no public search API and its terms prohibit automated scraping. Keep runs to one search
at a time, cap results, and verify prices before booking.
