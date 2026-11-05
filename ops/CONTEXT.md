# Context: ops

> Room contract for `/ops`. Governs what is allowed and expected in this folder.
> Consult [`../AGENTS.md`](../AGENTS.md) for project-wide routing and rules.

## 1. Role & Purpose

Pipeline orchestration, ingestion runners, exploration notebooks, and repository maintenance
scripts. Code here wires the `/src` engines together; it does not own the math.

---

## 2. Allowed Inputs

- Engines and helpers from [`../src/`](../src/).
- The append-only price store in [`../data/`](../data/).
- Runtime configuration from `.env` (`SERPAPI_KEY`).
- CLI arguments and filter parameters: `dip_threshold`, `ma_window`, `max_stops`,
  `max_travel_time`.

---

## 3. Core Process & Execution

1. Expand the requested regions into routes via `src.services.routing.generate_routes`.
2. Fetch fares through `src.services.flight_api.fetch_flights`.
3. Filter by `max_stops` and `max_travel_time`; record how many flights each filter drops.
4. Insert accepted flights through `src.database.db_manager.insert_flight_prices`.
5. Read history through `get_historical_prices` and analyze with `analytics.py`.
6. Emit alerts or reports; rate-limit live API calls (`time.sleep`).
7. Run maintenance scripts only at checkpoints.

---

## 4. Expected Outputs

- `scripts/price_scraper.py` — the main ingestion and alert runner.
- `scripts/generate_graphify_chunk.py` — manual semantic chunk builder for the knowledge graph.
- `scripts/merge_graph.py` — manual incremental graph merge helper.
- `notebooks/explore_flights.ipynb` — interactive exploration and plotting.
- Run artifacts and reports in `current_output/` (gitignored).

---

## 5. Local Invariants & NEVER Rules

- **Never re-implement core math here.** Call `/src` engines instead.
- **Never import `/ops` from `/src`.** The dependency is one-way.
- **Never bypass `db_manager.py`** with ad-hoc SQL or a second database path.
- **Never log or commit secrets.** API keys come from `.env`.
- **Never drop flights silently.** Every filter must log the count it removed per criterion.
- **Never call a live API in a test.** Mock the boundary.
- **Never write task notes or scratch outputs to the repo root.**

---

## 6. General Guidelines

All changes here follow the 9-step pipeline in [`../CODE_PIPELINE.md`](../CODE_PIPELINE.md).
Use Python's `logging` module, not bare `print`, for operational scripts. Tests for runners belong
in [`../tests/`](../tests/) and must use a temporary database. Graphify scripts are maintenance
helpers and may be run only during `project-checkpoint`.
