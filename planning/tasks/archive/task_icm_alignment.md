# Task: ICM Alignment, Skills Suite & Routing

**Status:** Active
**Started:** 2026-11-05
**Env:** `C:\Users\lorem\miniconda3\envs\travel\python.exe`

## Question

The `icm-core` blueprint (https://github.com/loremauro98/icm-core) defines the organization for every
repo: a Layer 1 `AGENTS.md` map, Layer 2 `CONTEXT.md` room contracts, a `.agents/skills/` suite with
`skills-route`, a 9-step pipeline, and a checkpoint discipline. The Travel Planner already has a
partial version of the architecture. What is still missing, and what has drifted?

## Plan

- [x] Audit the local repo against the `icm-core` template.
- [x] Install the ICM core skill suite into `.agents/skills/` (41 skills).
- [x] Copy the rules bundle and create the `.claude/skills` junction.
- [x] Write a travel-specific `AGENTS.md` Layer 1 map.
- [x] Rewrite every workspace `CONTEXT.md` to the 6-part room contract.
- [x] Write a travel-specific `skills-route` classification and a complete skill registry.
- [x] Add `CODE_PIPELINE.md`, `README.md`, BLUF output style, ignore files, and pytest config.
- [x] Move the SQLite store to `data/` and tests to root `tests/`.
- [x] Add guardrail tests for the ICM layout and skill registry.
- [x] Add per-criterion filter drop logging and expose `min_periods` / `api_pause_seconds`.
- [x] Run the full test suite and record evidence.
- [x] Generate `docs/structure.md` and update the changelog.
- [x] Checkpoint: archive this task, stage explicitly, commit.
- [x] GitHub remote: created and pushed to `loremauro98/travel_planner`.

## Work log

### 2026-11-05 — Audit

- No `.git` directory; no remote; no `travel_planner` repo on GitHub (only `icm-core`, `datavista`, `nav18`).
- Python is not on PATH; the project env is `C:\Users\lorem\miniconda3\envs\travel`.
- Existing `GEMINI.md` had a partial Layer 1 map; `CONTEXT.md` files had 4 sections, not the 6-part standard.
- No `.agents/skills/`, no `CODE_PIPELINE.md`, no skill registry, no BLUF style.
- `SKOOL.md` (course notes) sat at the repo root; the database sat at the root; tests lived in `src/tests/`.

### 2026-11-05 — Implementation

- Installed 41 core skills and the 3-file rules bundle.
- Created `.claude/skills` junction and BLUF output style.
- Relocated the database to `data/flight_data.db`, tests to `tests/`, and course notes to
  `docs/reference/icm_course_notes.md`.
- Added `ops/sync_tree.py` to satisfy the `icm-maintenance` dependency.
- Exposed `min_periods` in the moving average, replaced the hardcoded region map with
  `REGION_AIRPORTS`, and added per-criterion drop logging in the scraper.

## Verification

- `pytest -q`: **19 passed** (analytics, routing, scraper, API boundary, database, ICM structure).
- `ruff format` / `ruff check src ops tests`: clean.
- `ops/sync_tree.py`: wrote `docs/structure.md`.
- `graphify update .`: rebuilt the code graph (1327 nodes, 1335 edges).
- `serena project create --language python --index`: indexed 15 Python files.
- `git status`: audited before the initial commit; no `.env`, database, cache, or graph artifacts staged.

## Resolution

- The workspace had no `.git` directory and no `travel_planner` repository on GitHub. The repository
  was initialized on `main` and pushed to `https://github.com/loremauro98/travel_planner` on
  2026-11-05.
