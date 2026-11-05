# Spec: Automated Airbnb Search & Shortlist

**Status:** Approved for MVP
**Date:** 2026-11-05
**Owner:** Travel Planner

## 1. Goal

Given an Airbnb search URL (filters configured in the UI), retrieve the matching listings, apply
optional local filters, and write a CSV plus a Markdown shortlist. Replace the manual loop of
scrolling, zooming, and opening every property.

## 2. Non-goals

- Booking, messaging hosts, or making payments.
- Exhaustive crawling of every result (the API caps around 280 for this search).
- A persistent watchlist / price-history database (deferred).
- Bypassing Airbnb login, captchas, or account restrictions.

## 3. Inputs

### 3.1 Search URL

The cleaned Airbnb URL is the source of truth. It must contain the location and the filters the user
wants. Example:

```text
https://www.airbnb.com/s/Alsace--France/homes
  ?adults=2
  &checkin=2026-12-31
  &checkout=2027-01-02
  &place_id=ChIJv5Z326NGkUcR4CQ3mrlfCgE
  &refinement_paths%5B%5D=%2Fhomes
  &room_types%5B%5D=Entire%20home%2Fapt
  &flexible_cancellation=true
  &price_max=150
  &price_filter_input_type=2
  &price_filter_num_nights=2
```

Strip tracking/session/date-picker parameters: `acp_id`, `ref_fsid`, `ref_search_session_id`,
`selected_filter_order`, `search_type`, `search_mode`, `channel`, `monthly_*`,
`flexible_trip_lengths`, `date_picker_type`. They can change the result set without changing the
user’s intent.

### 3.2 Runtime parameters

| Parameter | Default | Meaning |
|---|---|---|
| `currency` | `CHF` | Currency passed to Airbnb. Must match the visible page. |
| `language` | `en` | Locale for names and labels. |
| `max_results` | `40` | Cap the final shortlist after filtering and sorting, before enrichment. |
| `enrich_top` | `5` | Number of top listings to enrich with details (0 disables). |
| `sort_by` | `price_per_night` | `price_per_night`, `price_total`, `rating`, or `reviews`. |
| `descending` | `false` | Sort direction. |

### 3.3 Local filters (optional)

| Filter | Meaning |
|---|---|
| `require_free_cancellation` | Keep only listings with `FREE_CANCELLATION_HIGHLIGHT`. |
| `max_price_per_night` | Local safety net for the URL’s price filter. |
| `min_price_per_night` | Lower bound. |
| `min_rating` | Minimum average rating. |
| `min_reviews` | Minimum review count. |
| `min_bedrooms`, `min_beds`, `min_baths` | Layout constraints. |
| `exclude_hotels` | Drop `FEATURED_HOTEL` / title containing “hotel”. |
| `exclude_property_types` | Drop non-stay property types such as `Room`, `Campsite`, or `Parking space`. The URL’s `room_types[]=Entire home/apt` is the primary filter; this is the local safety net. |

Every active filter must report the exact number of listings it dropped (transparent-data-masker).

## 4. Pipeline

1. Parse the search URL: dates, guests, nights, price cap, cancellation, place ID.
2. Call `pyairbnb.search_all_from_url(url, currency, language)`.
3. Normalize each raw listing into the flat record in §5.
4. Deduplicate by `listing_id`.
5. Apply local filters sequentially, recording drop counts per criterion.
6. Sort by the configured key; `None` values go last.
7. Cap the final shortlist at `max_results`.
8. Optionally enrich the top N with `pyairbnb.get_details` (amenities, room type, capacity).
9. Write CSV and Markdown to `current_output/`.
10. Print the output paths, counts, and drop report.

## 5. Output schema

CSV columns:

`listing_id, name, property_type, location, price_total, price_original, price_per_night, currency,
nights, rating, reviews, bedrooms, beds, baths, layout, host_type, badges, free_cancellation,
pay_zero_upfront, latitude, longitude, image_url, amenities, room_type, person_capacity,
is_super_host, url, check_in, check_out, adults, scraped_at, search_label`

Price rules:

- `price_total = price.unit.discount` when present, else `price.unit.amount`.
- `price_original = price.unit.amount` when a discount exists, else empty.
- `price_per_night = price_total / nights`.
- Label the currency from the requested currency (e.g. `CHF`), not the display symbol.

## 6. Acceptance criteria

- The CLI runs from the repo root with the explicit `travel` interpreter.
- The Alsace sample produces a CSV and Markdown file in `current_output/`.
- The top five normalized listings match the visible BrowserOS page (names and CHF totals).
- The Markdown contains the search parameters, the shortlist table, and the per-filter drop report.
- Unit tests cover URL parsing, price normalization, layout parsing, dedupe, filters, sorting,
  CSV writing, and Markdown writing. No test calls the live API.
- `pytest` and `ruff check` pass.
- `pyairbnb` is documented as a validated third-party dependency.

## 7. Failure modes

| Failure | Response |
|---|---|
| Airbnb returns 403 / captcha | Stop, report the block, fall back to BrowserOS on the same URL. |
| API returns zero listings | Report zero; do not fabricate. Check the URL and currency. |
| Missing price breakdown | Use `price.unit.amount`; leave per-night empty if nights unknown. |
| Missing layout info | Leave bedrooms/beds/baths empty; keep the listing. |
| Details call fails | Keep the search record; log a warning; skip enrichment for that listing. |
| Slow request | Timeout at 90s per search; the current search takes ~7s. |

## 8. Dependencies

- `pyairbnb==2.2.2` (MIT) — Airbnb StaysSearch client.
- `curl_cffi==0.17.0` — validated TLS-impersonation version.
- Existing: `pandas`, `requests`, `python-dotenv`, `pytest`, `ruff`.

## 9. Safety

Airbnb has no public search API and its terms prohibit automated scraping. This tool is for personal,
low-volume shortlist generation. Keep runs to one search at a time, cap results, do not run it in a
loop, and verify prices before booking. BrowserOS is the human-like fallback when the API is blocked.
