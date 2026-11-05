# Travel Planner

A smart flight-tracking tool: live fare ingestion from SerpApi (Google Flights), historical SQLite
storage, moving-average price-dip detection, and multi-airport regional routing.

## Architecture

This repo uses the **Interpretable Context Methodology (ICM)**.

- **Layer 1 map:** [`AGENTS.md`](AGENTS.md) — root routing, NEVER rules, and defaults.
- **Layer 2 contracts:** `CONTEXT.md` in every workspace — what belongs there and what does not.
- **Layer 3 skills:** `.agents/skills/` — 41 reusable skills, routed by intent in
  [`skills-route`](.agents/skills/skills-route/SKILL.md).
- **Engineering pipeline:** [`CODE_PIPELINE.md`](CODE_PIPELINE.md) — the mandatory 9-step workflow.
- **Skill registry:** [`docs/CUSTOM_SKILLS.md`](docs/CUSTOM_SKILLS.md).

## Repository map

| Path | Purpose |
|---|---|
| `planning/` | Specs, decisions, active task logs, archive |
| `src/` | Pure services and database access |
| `data/` | Append-only SQLite price store (gitignored) |
| `ops/` | Ingestion runners, notebooks, maintenance scripts |
| `tests/` | Headless pytest suites |
| `docs/` | Documentation, skill registry, changelog, reference notes |
| `.agents/skills/` | Skill source of truth |
| `.claude/skills/` | Junction onto `.agents/skills/` (gitignored) |

## Quickstart

```powershell
# Use the project environment explicitly
$py = "C:\Users\lorem\miniconda3\envs\travel\python.exe"

# Install dependencies
& $py -m pip install -r requirements.txt

# Configure the SerpApi key
Copy-Item .env.example .env
# then edit .env and set SERPAPI_KEY

# Create/refresh the database schema
& $py -m src.database.db_manager

# Run the ingestion pipeline
& $py ops\scripts\price_scraper.py

# Run the full test suite
& $py -m pytest -q
```

## Data

The SQLite database lives at `data/flight_data.db`. It is append-only and gitignored. The schema and
path are owned by `src/database/db_manager.py`; never edit or delete rows by hand.

## Skills

Start a session by reading `AGENTS.md`. The mandatory entry point is `skills-orchestrator`, which
classifies the task with `skills-route` and declares:

```text
[Intent: <Category 1-7> | Skill Stack: <skills> | Env: travel]
```

After a fresh clone, recreate the Claude Code junction:

```powershell
cmd /c mklink /J .claude\skills .agents\skills
```
