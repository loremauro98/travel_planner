# 2026-11-05

## [ICM Architecture, Skills Suite & Routing Alignment]

### Tasks
- **Layer 1 map:** Replaced the partial `GEMINI.md` routing with a full `AGENTS.md` map (workspaces,
  routing, NEVER rules, defaults, tooling, conventions); `CLAUDE.md` and `GEMINI.md` are now pointers
  to the single authority.
- **Layer 2 contracts:** Rewrote every workspace `CONTEXT.md` to the 6-part ICM room contract and
  added a contract for `data/` and `tests/`.
- **Skills suite:** Installed the 41-skill ICM core profile in `.agents/skills/`, copied the rules
  bundle to `.agents/rules/`, and created the `.claude/skills` junction.
- **Skills routing:** Replaced the generic router with a travel-specific 7-category `skills-route`
  and catalogued every installed skill in `docs/CUSTOM_SKILLS.md`.
- **Pipeline & style:** Added `CODE_PIPELINE.md`, the BLUF output style and settings, `.gitignore`,
  `.graphifyignore`, `pytest.ini`, `.env.example`, and a human-facing `README.md`.
- **Organization:** Moved the SQLite store to `data/flight_data.db`, tests to root `tests/`, and
  course notes to `docs/reference/icm_course_notes.md`; removed `__pycache__` artifacts.
- **Code alignment:** Exposed `min_periods` in the moving average, made `REGION_AIRPORTS` a module
  authority, added per-criterion filter drop logging, exposed `api_pause_seconds`, fixed the
  round-trip/one-way SerpApi request type, and replaced broad exception handling with specific
  catches plus logging.
- **Maintenance:** Added `ops/sync_tree.py` (generates `docs/structure.md`) and
  `tests/test_icm_structure.py` (guards the layout and skill registry).
- **Git:** Initialized the repository; no GitHub remote exists yet.

### Verification
- `pytest -q`: **19 passed**.
- `ruff check src ops tests`: **clean**.
- `graphify update .`: rebuilt the code graph (1327 nodes, 1335 edges).
- `serena project index`: indexed 15 Python files.

---

# 2026-07-03

## [Flight Tracker Foundation & Live SerpApi Ingestion]

### Tasks
- **Database Schema**: Created SQLite-based time-series price storage tracking `origin`, `destination`, `price`, `stops`, `travel_time_minutes`, and `scraped_at` timestamp.
- **Flight Data API**: Built a modular API interface featuring both a mock generator (for offline testing) and a live **SerpApi Google Flights** integration.
- **Analytics Engine**: Developed a `pandas` service implementing `calculate_moving_average` and `detect_price_dips` (alerting when prices drop below a threshold).
- **Multi-Airport Routing**: Created a routing utility to expand regional queries (e.g. "Switzerland" to "Norway") into all `N * M` possible airport combinations.
- **Ingestion Pipeline**: Built `price_scraper.py` which automates routing, fetching, storage, and analytics run with rate-limiting pauses.
- **Unit Tests**: Implemented comprehensive `pytest` suites covering routing, analytics, and mock scraper runs.
- **Exploration Notebook**: Created a Jupyter Notebook (`explore_flights.ipynb`) configured with autoreload so the user can easily query parameters, filter by stops/time, and plot the price history.
