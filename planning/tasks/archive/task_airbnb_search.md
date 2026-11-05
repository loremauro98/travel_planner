# Task: Automated Airbnb Search & Shortlist

**Status:** Active
**Started:** 2026-11-05
**Env:** `C:\Users\lorem\miniconda3\envs\travel\python.exe`

## Question

Can we replace the manual Airbnb loop — set filters, scroll, zoom, click every property — with a
repeatable command that takes the search URL (or parameters), returns the listings that satisfy the
filters, and writes a CSV + Markdown shortlist?

## Plan

- [x] Spike `pyairbnb==2.2.2` against the real Alsace search URL.
- [x] Compare the API output with the visible BrowserOS page.
- [x] Resolve the full URL vs cleaned URL difference.
- [x] Verify details enrichment (amenities, room type, capacity).
- [x] Write the spec and failing tests.
- [x] Implement the API wrapper, normalization, filters, and report.
- [x] Add the CLI and config.
- [x] Run the live search and inspect the CSV + Markdown.
- [x] Package the `airbnb-search` skill and route it.
- [x] Checkpoint: tests, ruff, changelog, commit.

## Spike findings (2026-11-05)

- `pyairbnb.search_all_from_url` returned **280 listings in ~7 seconds** for the Alsace URL, in CHF.
- The full URL from BrowserOS includes session/tracking and date-picker state
  (`acp_id`, `ref_fsid`, `ref_search_session_id`, `selected_filter_order`, `monthly_*`,
  `flexible_trip_lengths=one_week`). It returns a **different result set** from the cleaned URL.
- The cleaned core URL reproduces the visible page’s top listings:
  1. Trognon's tiny house (CHF 146)
  2. On the edge of the forest (CHF 92, originally 109)
  3. Small apartment on the vineyard (CHF 111)
  4. Studio* the Turckheim lookout (CHF 157)
  5. Gite "Au chant du coq" (CHF 127)
- Price fields are misleading: `price.unit.amount` is the **original total**, `price.unit.discount`
  is the **discounted total**, and the per-night price is in `price.break_down`
  (`"2 nights x Fr. 51.85"`). Use `unit.discount` when present, then `unit.amount`.
- `paymentMessages` carries `FREE_CANCELLATION_HIGHLIGHT`; use it for the free-cancellation flag.
- `structuredContent.primaryLine` carries bedroom/bed/bath labels; `secondaryLine` carries host type.
- `pyairbnb.get_details` works with `datetime.date` objects (strings fail). It returns amenities,
  room type, capacity, rating breakdown, images, and coordinates. Host details are flaky; do not
  depend on them. Use the search-result price, not the detail price, because they can differ.
- The API returns 280 listings while the page says “Over 1,000 homes”; 280 is the API’s practical
  cap for this search. A capped shortlist is the right output, not an exhaustive crawl.

## Decisions

- Source of truth: the cleaned search URL (`place_id`, dates, guests, price, cancellation,
  refinement path, price-filter nights). Strip tracking/date-picker state.
- One-off for now: CSV + Markdown in `current_output/`; no SQLite until a watchlist is requested.
- Enrich only the top N listings, not all 280.
- Document `pyairbnb==2.2.2` and `curl_cffi==0.17.0` as validated dependencies.
- BrowserOS remains the verification and fallback layer.

## Verification (2026-11-05)

- `pytest -q`: **37 passed** (existing 19 + Airbnb 18).
- `ruff check src ops tests`: **clean**.
- Live Alsace run: 280 retrieved, 205 after local filters, 40-row shortlist.
- Filters reported: `free_cancellation=17`, `max_price_per_night=9`, `exclude_hotels=0`,
  `exclude_property_types=1`.
- Top results matched the visible BrowserOS page (names and CHF totals).
- Outputs:
  - `current_output/airbnb_alsace_new_year_2026-12-31_2027-01-02.csv`
  - `current_output/airbnb_alsace_new_year_2026-12-31_2027-01-02.md`
- The sample still includes private rooms because the URL does not constrain room type. Add
  `exclude_property_types: ["Room", "Campsite"]` or a future `room_types` filter to focus on entire
  homes.

### Room-type follow-up (2026-11-05)

- Added `room_types[]=Entire home/apt` to the search URL and `Room` to `exclude_property_types`.
- Rerun: 280 retrieved, 204 after local filters, 40-row shortlist.
- All 40 rows are entire places; the enriched top five all report `room_type=Entire home/apt`.
- Property-type mix: 31 apartments, 3 homes, plus one each of condo, townhouse, guest suite, tiny
  home, camper/RV, and shepherd’s hut.
