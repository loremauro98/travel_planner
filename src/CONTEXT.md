# Context: src

> Room contract for `/src`. Governs what is allowed and expected in this folder.
> Consult [`../AGENTS.md`](../AGENTS.md) for project-wide routing and rules.

## 1. Role & Purpose

Pure computational engines and core business logic for the Travel Planner. This folder owns the
routing engine, the analytics engine, the SerpApi boundary, and SQLite access. Code here must be
stateless where possible and deterministic given its inputs.

---

## 2. Allowed Inputs

- Feature specs and decisions from [`../planning/specs/`](../planning/specs/) and
  [`../planning/decisions/`](../planning/decisions/).
- Explicit function arguments: regions, airport codes, dates, windows, thresholds, and filters.
- Environment configuration loaded at the API boundary (`SERPAPI_KEY`).
- Price history read through `src/database/db_manager.py`.

---

## 3. Core Process & Execution

1. Read the relevant spec and the local tests before changing anything.
2. Write or update a failing headless test in [`../tests/`](../tests/).
3. Implement the smallest pure function or typed class that makes the test pass.
4. Keep all analytical parameters in signatures or config; no hidden defaults.
5. Refactor until each quantity and region map has exactly one authority file.
6. Run the full suite:
   `C:\Users\lorem\miniconda3\envs\travel\python.exe -m pytest -q`.

---

## 4. Expected Outputs

- `services/routing.py` — regional airport expansion and route generation.
- `services/analytics.py` — moving averages and price-dip detection.
- `services/flight_api.py` — the SerpApi network boundary; fetch and parse.
- `services/airbnb_api.py` — the Airbnb network boundary; pyairbnb search and detail calls.
- `services/airbnb_analysis.py` — price/layout normalization, dedupe, local filters, sorting.
- `services/airbnb_report.py` — CSV and Markdown shortlist output.
- `database/db_manager.py` — schema, connection, insert, and historical query helpers.
- `[snake_case.py]` -> `services/`, `database/`, or `utils/`.

---

## 5. Local Invariants & NEVER Rules

- **Never import from `/ops`.** The dependency is strictly one-way: `/ops` → `/src`.
- **Never hardcode a threshold, window, seed, or cutoff.** Expose it in the signature or a config.
- **Never duplicate the region map.** `get_airports_for_region` in `routing.py` is the authority.
- **Never duplicate the moving-average or dip formula.** `analytics.py` is the authority.
- **Never open SQLite outside `db_manager.py`.** The database path and schema live there.
- **Never call the network from a test.** Mock `fetch_flights`, `pyairbnb.search_all_from_url`, and
  `pyairbnb.get_details`.
- **Never call Airbnb outside `airbnb_api.py`.** The rest of the code works with plain dictionaries.
- **Never use the detail-page price as the search price.** The search card total is the source of
  truth; details are for amenities, room type, and capacity.
- **Never merge untested math.** A headless test must pass before the change lands.
- **Never store secrets.** Read `SERPAPI_KEY` from the environment; never print it.

---

## 6. General Guidelines

All changes here follow the 9-step pipeline in [`../CODE_PIPELINE.md`](../CODE_PIPELINE.md).
Tests governing this folder belong in [`../tests/`](../tests/). Use `snake_case` for modules,
functions, and variables; `PascalCase` for classes. Keep functions small, typed, and docstringed.
