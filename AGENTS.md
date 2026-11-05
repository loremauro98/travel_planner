# AGENTS.md — Layer 1 Map: Travel Planner

> The root routing map for this repository. Every workspace has a local `CONTEXT.md` that governs
> that space. **Read the local `CONTEXT.md` first; come back here only when it does not answer you.**

## Project Overview

**Travel Planner**: a smart flight-tracking tool with live fare ingestion, historical price
analysis, moving-average dip detection, and multi-airport regional routing.

- **Language:** Python 3.11
- **Database:** SQLite (local, append-only price history)
- **Analytics:** pandas / numpy
- **Flight API:** SerpApi (Google Flights)
- **Environment:** `C:\Users\lorem\miniconda3\envs\travel\python.exe`

---

## Workspaces

| Folder | Holds | Core Constraint |
|---|---|---|
| `/planning` | Specs, architecture decisions, task logs | Active task logs live in `/planning/tasks/`; completed ones move to `/planning/tasks/archive/`. Never write task notes to the repo root. |
| `/src` | Pure computational engines and core logic | Stateless services and database access only. Must never import from `/ops`. |
| `/data` | Empirical price recordings and the SQLite store | Append-only. Never edit or delete existing rows by hand. The database is gitignored. |
| `/docs` | Documentation, skill registry, changelog, reference notes | Keep `CUSTOM_SKILLS.md`, `structure.md`, and `CHANGELOG.md` synchronized. |
| `/ops` | Ingestion pipelines, runners, notebooks, maintenance scripts | Strict one-way dependency: `/ops` → `/src`. Never re-implement core math here. |
| `/tests` | Headless pytest suites | Tests never call live APIs and never touch the production database. |

**Output style.** Answers are written BLUF — answer first, plain words, no preamble. The rules live
in `.claude/output-styles/bluf.md` and are activated for Claude Code by `"outputStyle": "BLUF"` in
`.claude/settings.json`. Agents that do not load output styles should read that file and follow it
anyway.

---

## Routing

| Task / Domain | Target Folder | Read First | Skills |
|---|---|---|---|
| **[ORCHESTRATOR & LIFECYCLE] Proactive skill routing & subagent bundling** — mandatory session-start entry point; classifies task context, enforces process/domain skill priority, and injects skill constraints into subagents | Global / Root | [.agents/skills/skills-orchestrator/SKILL.md](.agents/skills/skills-orchestrator/SKILL.md) | `skills-orchestrator` |
| **[WORKFLOWS & QUALITY GATE] Ambition, brainstorming, TDD, debugging, subagents & autonomous goal** — plan-first engineering, ambition-raising, test-driven implementation, root-cause investigation, subagent review, autonomous goal execution | Global / Root | [docs/CUSTOM_SKILLS.md](docs/CUSTOM_SKILLS.md) | `be-ambitious`, `brainstorming`, `writing-plans`, `test-driven-development`, `systematic-debugging`, `executing-plans`, `subagent-driven-development`, `verification-before-completion`, `goal` |
| **[EXPERT COUNCIL & MULTI-AGENT DEBATE] Multidisciplinary debate & consensus** — spawns 3–4 expert subagents to debate complex architectural, statistical, or product questions | Global / Root | [.agents/skills/experts_council/SKILL.md](.agents/skills/experts_council/SKILL.md) | `experts_council`, `skills-orchestrator` |
| **[CORE LOGIC & ENGINES] Pure algorithmic implementation** — routing, analytics, moving averages, dip detection, database access | `/src` | [src/CONTEXT.md](src/CONTEXT.md) | `test-driven-development`, `statistical-batch-orchestrator`, `transparent-data-masker` |
| **[INGESTION & RUNNERS] Scraping, pipeline execution & batch reporting** — price ingestion, rate-limited runners, notebooks, maintenance scripts | `/ops` | [ops/CONTEXT.md](ops/CONTEXT.md) | `statistical-batch-orchestrator`, `transparent-data-masker`, `datavis` |
| **[DATA GOVERNANCE] Raw fares & price history** — append-only SQLite recordings and stable exports | `/data` | [data/CONTEXT.md](data/CONTEXT.md) | `transparent-data-masker` |
| **[TRAVEL DATA SOURCES] Airbnb search & shortlist** — authenticated search URL, local filters, CSV + Markdown shortlist | `/ops` + `/src` | [ops/CONTEXT.md](ops/CONTEXT.md) | `airbnb-search`, `transparent-data-masker`, `verification-before-completion` |
| **[PLANNING & SPECS] Feature specifications & task tracking** — formal specs, ADRs, task logs | `/planning` | [planning/CONTEXT.md](planning/CONTEXT.md) | `writing-plans`, `strict-agent-pipeline` |
| **[TESTING] Headless verification** — unit and integration tests for `/src` and `/ops` | `/tests` | [tests/CONTEXT.md](tests/CONTEXT.md) | `test-driven-development`, `verification-before-completion` |
| **[MAINTENANCE, DISTILLATION & CHECKPOINT] Codebase maintenance, skill distillation & phase wrap-up** — formatting, tree sync, graph update, test verification, session distillation | Root / `/ops` | [docs/CHANGELOG.md](docs/CHANGELOG.md) | `icm-maintenance`, `project-checkpoint`, `verification-before-completion`, `lookback` |

Skills are catalogued in [`docs/CUSTOM_SKILLS.md`](docs/CUSTOM_SKILLS.md) and live in
`.agents/skills/`, which is tracked, so they travel with a clone. `.claude/skills/` is a junction
onto that folder — Claude Code only auto-loads that path. **After a fresh clone, recreate it:**
- **Windows:** `cmd /c mklink /J .claude\skills .agents\skills`
- **Linux/macOS:** `ln -s ../.agents/skills .claude/skills`

> [!IMPORTANT]
> **Skills Orchestration & Selection Authority (`skills-route`):** How skills are selected based on
> high-level intent and bundled for subagents is defined in
> [`.agents/skills/skills-route/SKILL.md`](.agents/skills/skills-route/SKILL.md). The travel-specific
> classification (ingestion, time-series analytics, visualization, API research) is in that file.

---

## NEVER

Hard constraints. Violating one is a defect, not a style choice.

1. **Never hide an analytical parameter.** Every seed, moving-average window, dip threshold, stop
   limit, and travel-time cutoff is exposed in a function signature or config — never buried in a
   utility.
2. **Never assume.** Ask. If you are unsure, say so. Be unbiased by what is claimed — go to the
   foundations and report errors.
3. **Never modify raw data.** Read from `/data` only. The price database is append-only; schema
   changes go through `/src/database/`.
4. **Never skip the 9-step pipeline** in [`CODE_PIPELINE.md`](CODE_PIPELINE.md) for any modification.
5. **Never integrate untested math.** Core data-processing, statistical, and routing logic requires a
   passing headless unit test before it goes in.
6. **Never introduce an undocumented third-party library** without explicit validation.
7. **Never define a quantity twice — point at the authority instead.** A threshold, region map, or
   constant is declared in exactly one place, and every other file imports or references that place.
8. **Never state a configurable choice as a fact.** If how a dip is decided, which window is primary,
   or which data source runs is set by a config constant, name the constant and its default.
9. **Never take ad-hoc, un-orchestrated actions or write code without consulting skills.** Always
   invoke the relevant skill via `skills-orchestrator` before any response, plan, or implementation
   action.
10. **Never run `git add .`, `git add -A`, or `git add -u`.** Always stage files explicitly by path
    (`git add path/to/file`). Run `git status` prior to commit to confirm zero data arrays, caches,
    secrets, or untracked outputs are staged.
11. **Never bypass Serena.** It is mandatory to use Serena to locate functions, logic, variables, and
    code symbols. If it is unavailable, say so in one line and fall back to a scoped pattern search —
    do not spend turns installing or restarting it.
12. **Never commit secrets or the price database.** `.env` and `data/*.db` stay out of git.

---

## DEFAULTS

How to work unless told otherwise.

- **Start every session with `skills-orchestrator`:** Immediately after reading `AGENTS.md` on turn 1,
  invoke `skills-orchestrator` to evaluate task context and declare the 1-line pre-flight tag:
  `[Intent: <Category 1-7> | Skill Stack: <skills> | Env: travel]`
  before taking action or responding.
- **Explicit environment execution:** Run Python scripts, tests, and pipeline runners with the
  explicit interpreter:
  `C:\Users\lorem\miniconda3\envs\travel\python.exe`.
  Do not rely on a global `python` (it is not on PATH).
- **Package skills for subagents:** When dispatching subagents, the parent agent MUST bundle the
  required role instructions and constraints into the subagent's prompt per
  [`.agents/skills/skills-route/SKILL.md`](.agents/skills/skills-route/SKILL.md).
- **Use simple language. Keep output short.** Explain in plain words, step by step, and write as
  little as possible to make the point. No stream of consciousness. Give output strictly when a
  decision is needed or there is a problem that requires deviation from the plan.
- **80% planning, 20% execution.** Plan, then execute.
- **Search for elegance, do not over-engineer.** The simplest well-reasoned solution in few lines
  wins. Code must stay easy to modify.
- **Log the session in a task-description `.md` under [`planning/tasks/`](planning/tasks/)** —
  question → plan → task list, extended as work continues. Name it `task_<name>.md`.
  **Never write one to the repository root.**
- **Close a phase with `project-checkpoint`**, which archives the task log into
  `docs/CHANGELOG.md` and moves the completed task markdown from `planning/tasks/` into
  `planning/tasks/archive/`.

### Need for speed

The cost of a task is the number of calls it takes, not the size of the work. Every extra call is
another round trip, so spend a few and make each one count.

- **One command per job.** A single invocation must carry the whole job — locate the thing, check
  the imports, run it, print a summary. Never issue one command per question, and never chain
  exploratory one-liners.
- **Never wait out loud.** Do not answer "I am waiting for the process to complete". If a command
  was backgrounded, do independent work in the same turn instead of yielding.
- **Call the interpreter by path.** Use the explicit interpreter binary, not indirect runners that
  wrap commands in slow harness wrappers.
- **Read through the fastest Serena tool.** `get_symbols_overview` → `find_symbol` → `read_file`;
  use `search_for_pattern` in place of grep. Treat `find_referencing_symbols` as a deliberate
  choice, never a first look.
- **Never stall on tooling.** If Serena is unavailable, say so in one line and fall back to a
  scoped pattern search. Do not spend turns installing, indexing, or restarting it.
- **Write once.** Once a script runs and produces the artefact, stop rewriting it. Re-create it
  only when the output is actually wrong, or the request changes.

---

## Tooling

- **Serena** — the project is semantically indexed. Mandatory to use it to locate functions, logic,
  variables, and code symbols. Work fastest-first (`get_symbols_overview` → `find_symbol` →
  `read_file`), and use `search_for_pattern` in place of grep; see [Need for speed](#need-for-speed).
  If Serena is unavailable, say so in one line and fall back to a scoped pattern search — do not
  spend turns installing or restarting it. **Run `serena project index` strictly during
  `project-checkpoint` milestones or when creating new packages. Never run it during iterative code
  edits or quick bugfixes.**
- **Graphify** — structural knowledge graph in `graphify-out/`. Use `graphify query|path|explain`
  to understand architecture before editing. **Run `graphify update .` strictly during
  `project-checkpoint` milestones or when creating new packages. Never run it during iterative code
  edits or quick bugfixes.**
- **pytest** — `C:\Users\lorem\miniconda3\envs\travel\python.exe -m pytest -q` from the repo root.
- **ruff** — `uvx ruff format .` and `uvx ruff check . --fix` (ruff is not installed in the `travel`
  env by default; `uvx` is available).
- **Airbnb search** — `pyairbnb==2.2.2` (validated). Run
  `C:\Users\lorem\miniconda3\envs\travel\python.exe ops\scripts\airbnb_search.py --config ops\configs\airbnb_alsace.json`.
  Outputs go to `current_output/` (gitignored). One search at a time; use BrowserOS as the
  verification and fallback layer.

---

## Conventions

- `snake_case` for modules, functions, variables. `PascalCase` for classes.
- **Specs:** `planning/specs/<feature_name>_spec.md`.
- **Task logs:** `planning/tasks/task_<name>.md`; archive to `planning/tasks/archive/`.
- **Decisions:** `planning/decisions/YYYY-MM-DD-<decision>.md`.
- **Tests:** `tests/test_<module>.py`.
- **New skill** → write it in `.agents/skills/`, register it in
  [`docs/CUSTOM_SKILLS.md`](docs/CUSTOM_SKILLS.md), classify it in
  [`skills-route`](.agents/skills/skills-route/SKILL.md), and add it to the Routing table above if
  folder-bound.
