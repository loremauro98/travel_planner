# Context: tests

> Room contract for `/tests`. Governs what is allowed and expected in this folder.
> Consult [`../AGENTS.md`](../AGENTS.md) for project-wide routing and rules.

## 1. Role & Purpose

Headless verification for `/src` and `/ops`. Tests are the executable specification: they prove the
routing engine, analytics engine, database layer, and ingestion pipeline behave as documented.

---

## 2. Allowed Inputs

- Modules from [`../src/`](../src/) and [`../ops/`](../ops/).
- Temporary databases created with `tmp_path` or `monkeypatch`.
- Mocked API responses and fixtures built inside the test.

---

## 3. Core Process & Execution

1. Write the failing test first (RED).
2. Run it with the explicit interpreter:
   `C:\Users\lorem\miniconda3\envs\travel\python.exe -m pytest tests/test_<module>.py -q`.
3. Implement the minimal change in `/src` or `/ops` (GREEN).
4. Refactor and re-run the full suite:
   `C:\Users\lorem\miniconda3\envs\travel\python.exe -m pytest -q`.

---

## 4. Expected Outputs

- `test_routing.py` — region expansion and route generation.
- `test_analytics.py` — moving averages and dip detection.
- `test_scraper.py` — ingestion pipeline with a mocked API boundary.
- `test_flight_api.py` — SerpApi request construction, including round-trip vs one-way.
- `test_db_manager.py` — schema, insert, and historical query behavior.
- `test_icm_structure.py` — guardrail for the ICM layout and skill registry.

---

## 5. Local Invariants & NEVER Rules

- **Never call a live API.** Mock `fetch_flights` and any other network boundary.
- **Never touch `data/flight_data.db`.** Use `tmp_path` or a monkeypatched `DB_PATH`.
- **Never hardcode credentials or environment-specific paths** in a test.
- **Never weaken a test to make it pass.** Fix the code or the test's premise.
- **Never skip the RED step.** A test that never failed has not been proven.

---

## 6. General Guidelines

All changes here follow the 9-step pipeline in [`../CODE_PIPELINE.md`](../CODE_PIPELINE.md).
Use `test-driven-development` and `verification-before-completion`. Keep tests deterministic,
fast, and independent of the network and the production database.
