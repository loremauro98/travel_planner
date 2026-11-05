---
name: airbnb-search
description: Use when the user wants an Airbnb shortlist from filters or a search URL. Runs the pyairbnb CLI, applies local filters, enriches the top picks, writes CSV + Markdown, and uses BrowserOS for verification and fallback.
---

# Airbnb Search & Shortlist

## When to use

- The user wants a list of Airbnb properties that satisfy dates, guests, price, cancellation, room
  type, rating, or amenity filters.
- The user has a search URL from the Airbnb UI and wants it turned into a structured shortlist.
- The user wants to avoid manually scrolling, zooming, and opening every card.

Do **not** use this skill for booking, messaging hosts, payments, or exhaustive crawling.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `url` | required | Cleaned Airbnb search URL. The URL is the filter source of truth. |
| `currency` | `CHF` | Must match the currency in the user's Airbnb session. |
| `language` | `en` | Locale for names and labels. |
| `max_results` | `40` | Final shortlist size after filtering and sorting. |
| `enrich_top` | `5` | Details calls for the top N (amenities, room type, capacity). |
| `sort_by` | `price_per_night` | `price_per_night`, `price_total`, `rating`, or `reviews`. |
| `filters` | see below | Local safety net and optional preferences. |

### Cleaning the URL

Keep the real filters: `place_id`, `checkin`, `checkout`, `adults`, `price_max`,
`flexible_cancellation`, `refinement_paths[]`, `price_filter_input_type`,
`price_filter_num_nights`.

Strip tracking and date-picker state: `acp_id`, `ref_fsid`, `ref_search_session_id`,
`selected_filter_order`, `search_type`, `search_mode`, `channel`, `monthly_*`,
`flexible_trip_lengths`, `date_picker_type`. In the Alsace spike, the full URL returned a different
result set from the visible page; the cleaned URL reproduced the visible top listings.

## Workflow

1. Set the filters once in Airbnb (BrowserOS or the user's browser).
2. Copy the search URL and clean it using the rules above.
3. Save a config under `ops/configs/` (copy `airbnb_alsace.json` as the template).
4. Run the CLI with the explicit `travel` interpreter:

```powershell
& "C:\Users\lorem\miniconda3\envs\travel\python.exe" `
    ops\scripts\airbnb_search.py --config ops\configs\airbnb_alsace.json
```

5. Inspect `current_output/airbnb_<label>_<checkin>_<checkout>.csv` and `.md`.
6. Verify the top results against the visible Airbnb page before reporting them as a shortlist.

## Output

- CSV: one row per listing, 32 columns, including price/night, total, original price, rating,
  reviews, layout, badges, free cancellation, coordinates, amenities, and the listing URL.
- Markdown: search parameters, summary counts, per-filter drop counts, compact shortlist table, and a
  details section for the enriched top N.

## Local filters

- `require_free_cancellation` — keep only `FREE_CANCELLATION_HIGHLIGHT` listings.
- `max_price_per_night`, `min_price_per_night`
- `min_rating`, `min_reviews`
- `min_bedrooms`, `min_beds`, `min_baths`
- `exclude_hotels`
- `exclude_property_types` — e.g. `["Campsite", "Parking space"]`

Every active filter reports the exact number of listings it dropped.

## BrowserOS fallback

If `pyairbnb` is blocked (403, captcha, empty response):

1. Open the same cleaned URL in BrowserOS.
2. Wait for `[data-testid="card-container"]`.
3. Read the page with `page.read()` or `page.snapshot()`.
4. Extract the cards; do not click every listing.
5. For details, open only the shortlisted listings.

Logged-in browsing reduces the chance of blocks; it does not eliminate them.

## Failure modes

| Failure | Response |
|---|---|
| Airbnb 403 / captcha | Stop, report the block, use the BrowserOS fallback. |
| Zero listings | Check the URL, currency, and dates; do not fabricate. |
| Missing price breakdown | Use `price.unit.amount`; leave per-night empty if nights are unknown. |
| Details call fails | Keep the search record; log a warning; skip enrichment for that listing. |

## Safety

Airbnb has no public search API and its terms prohibit automated scraping. This is for personal,
low-volume shortlist generation. Run one search at a time, cap results, do not loop, and verify
prices before booking. `pyairbnb==2.2.2` and `curl_cffi==0.17.0` are the validated dependency pair.
