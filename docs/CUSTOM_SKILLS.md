# Custom AI Skills Registry: Travel Planner

This document catalogues the AI-agent skills installed in this repository. `.agents/skills/` is the
**source of truth**; it is tracked in git, so skills travel with a clone.

## Where these skills live

| Path | Role | In git? | Read by |
| :--- | :--- | :--- | :--- |
| `.agents/skills/` | **Source of truth.** Edit here. | **Yes** — tracked | OpenCode, Gemini, Antigravity, generic agents |
| `.claude/skills/` | Junction / symlink onto `.agents/skills/` | No (gitignored) | Claude Code (auto-loads this path) |

Recreate the junction after a fresh clone:

- **Windows:** `cmd /c mklink /J .claude\skills .agents\skills`
- **Linux/macOS:** `ln -s ../.agents/skills .claude/skills`

## How skills are selected

`skills-orchestrator` is the mandatory session-start entry point. It consults
[`skills-route`](../.agents/skills/skills-route/SKILL.md), which classifies the task into one of
7 intent categories and returns the active skill stack. The first line of a session declares:

```text
[Intent: <Category 1-7> | Skill Stack: <skills> | Env: travel]
```

The installed profile is **42 skills: the 41-skill ICM core profile plus the repo-specific
`airbnb-search` skill**. Science-only extensions (`literature-search`, `literature-to-algorithm`,
`scientific-bullshit-detector`, `peri-event-tuning`) are not installed; Category 6 routes API/domain
research through `experts_council`, `prompter`, and `graphify` instead.

---

## Active Skills Catalog

### Orchestration & lifecycle

| Skill | Categories | Purpose |
|---|---|---|
| `skills-orchestrator` | 1–7 | Mandatory session-start routing and subagent packaging. |
| `skills-route` | 1–7 | High-level intent router and subagent bundling authority. |
| `project-checkpoint` | 7 | Wrap up a phase: tests, docs, task archive, changelog, graph, git. |
| `icm-maintenance` | 7 | ruff formatting, `docs/structure.md` sync, interpretability checks. |
| `strict-agent-pipeline` | 1, 7 | Enforces the 9-step textbook coding pipeline. |
| `verification-before-completion` | 1, 7 | Evidence-based verification before any success claim. |
| `goal` | 1 | Autonomous long-running execution with explicit completion tokens. |
| `lookback` | 7 | Distill a completed session into a reusable skill. |
| `icm-init` | 7 | Scaffold or extend the ICM architecture. |

### Engineering & quality

| Skill | Categories | Purpose |
|---|---|---|
| `be-ambitious` | 1 | Raise altitude, depth, and range of a task. |
| `brainstorming` | 1 | Explore intent, requirements, and design before creative work. |
| `writing-plans` | 1 | Dependency-ordered implementation plans. |
| `executing-plans` | 1 | Inline plan execution with verification gates. |
| `test-driven-development` | 1, 4 | Red → green → refactor, headless. |
| `systematic-debugging` | 2 | Four-phase root-cause investigation. |
| `subagent-driven-development` | 1 | Implement independent tasks through subagents. |
| `dispatching-parallel-agents` | 1 | Run independent work in parallel. |
| `requesting-code-review` | 1, 2 | Build a review package and request review. |
| `receiving-code-review` | 1, 2 | Evaluate feedback rigorously, not performatively. |
| `finishing-a-development-branch` | 1, 7 | Decide how to integrate completed work. |
| `using-git-worktrees` | 1 | Isolate feature work in a worktree. |
| `writing-skills` | 7 | Create, edit, and test new skills. |
| `robustness-audit` | 1, 4, 7 | Verify tests exist and no analytical cutoff is hidden. |
| `diagnosing-superpowers` | 2, 7 | Diagnose a failed or degraded agent session. |
| `module-migrator` | 1 | Move code into a modular folder with synchronized contexts. |

### Data & analytics

| Skill | Categories | Purpose |
|---|---|---|
| `transparent-data-masker` | 3 | Track and log exact drop counts per filter criterion. |
| `statistical-batch-orchestrator` | 4 | Scale single-route models to cohorts with valid nulls and FDR. |
| `jupyter-pickle-rescuer` | 3, 4 | Load objects pickled inside interactive notebooks. |
| `run-experiment` | 1, 4 | Run a safe one-off parameter probe and revert. |
| `datavis` | 5 | Publication-quality charts and accessible color choices. |
| `master-presenter` | 5 | Narrative PDF walkthroughs with matching markdown. |
| `flavio` | 5 | Hyper-critical, naive page-by-page peer review. |
| `scientific-pdf-dashboard` | 5 | Metrics-driven multi-page PDF dashboards. |

### Problem solving & research

| Skill | Categories | Purpose |
|---|---|---|
| `experts_council` | 1, 6 | Convene 3–4 expert subagents for debate and consensus. |
| `fable-method` | 1, 6 | Classify, define done, gather evidence, decide, verify. |
| `fable-loop` | 1, 6 | Orchestrated evidence → plan → execute → adversarial verify loop. |
| `fable-judge` | 1, 7 | Adversarial verification of a "done" claim. |
| `fable-domain` | 1, 6 | Research a domain and build a trusted skill bundle. |
| `prompter` | 6 | Build a structured research prompt from local context. |
| `graphify` | 6 | Query the structural knowledge graph before reading raw files. |
| `graphify-agentic-extraction` | 6 | Background semantic extraction to bypass API rate limits. |

### Travel data sources

| Skill | Categories | Purpose |
|---|---|---|
| `airbnb-search` | 3, 6 | Turn an Airbnb search URL into a filtered CSV + Markdown shortlist; enrich top picks; BrowserOS fallback. |

---

## Adding a new skill

1. Create `.agents/skills/<skill-name>/SKILL.md` with `name` and `description` frontmatter.
2. Add it to the catalog above.
3. Classify it in [`skills-route`](../.agents/skills/skills-route/SKILL.md) under one of the
   7 categories.
4. If it is folder-bound, add it to the Routing table in [`AGENTS.md`](../AGENTS.md).
5. Run the structure guardrail:
   `C:\Users\lorem\miniconda3\envs\travel\python.exe -m pytest tests/test_icm_structure.py -q`.

---

## Maintenance

- `docs/structure.md` is generated by `ops/sync_tree.py`; never edit it by hand.
- The registry is checked by `tests/test_icm_structure.py`, which fails if an installed skill is
  missing from this file.
- `.claude/skills/` is gitignored; recreate the junction after cloning.
