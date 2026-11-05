# Context: data

> Room contract for `/data`. Governs what is allowed and expected in this folder.
> Consult [`../AGENTS.md`](../AGENTS.md) for project-wide routing and rules.

## 1. Role & Purpose

Empirical flight-price recordings and the append-only SQLite store. This room is the historical
memory of the project: what was observed, when it was observed, and at what price.

---

## 2. Allowed Inputs

- Append-only writes from the ingestion pipeline through `src.database.db_manager.insert_flight_prices`.
- Schema migrations applied through `src.database.db_manager.setup_database`.
- Stable exports produced from the database for analysis.

---

## 3. Core Process & Execution

1. The ingestion runner observes live fares.
2. Accepted rows are appended with a `scraped_at` timestamp.
3. Analytics read history through `get_historical_prices`; they never mutate it.
4. Exports for reports go to `current_output/`, not back into `/data`.
5. Schema changes are versioned through the database module, never by hand.

---

## 4. Expected Outputs

- `flight_data.db` — the local SQLite price store (gitignored).
- Stable exported tables or CSV/Parquet artifacts when explicitly requested (gitignored).
- No ad-hoc edits, scratch files, or notebooks in this folder.

---

## 5. Local Invariants & NEVER Rules

- **Never edit or delete existing rows by hand.** The store is append-only.
- **Never drop or recreate tables** outside a reviewed migration in `db_manager.py`.
- **Never commit the database.** `*.db`, `*.sqlite`, and the WAL/SHM files are gitignored.
- **Never put secrets or API keys here.**
- **Never let analytics write back to this folder.** Read-only for analysis.
- **Never treat a derived export as raw data.** Label provenance and keep the original.

---

## 6. General Guidelines

All changes here follow the 9-step pipeline in [`../CODE_PIPELINE.md`](../CODE_PIPELINE.md).
The schema, path, and connection helpers are owned by
[`../src/database/db_manager.py`](../src/database/db_manager.py). Read it before touching the store.
