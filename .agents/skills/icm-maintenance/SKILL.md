---
name: icm-maintenance
description: >-
  Runs the standard repository maintenance checks. Enforces python formatting via ruff, synchronizes the directory tree in docs/structure.md, and ensures codebase interpretability.
---

# ICM Repo Maintenance

## Overview
This skill orchestrates the routine maintenance steps required to keep the project clean, perfectly formatted, and well documented for the AI workforce. It should be invoked during Step 9 of the `CODE_PIPELINE.md`.

## Dependencies
- **ruff**: Required for code formatting and linting.
- **Python 3.x**: Required to run the tree sync script.

## Workflow

### Phase A: Code Formatting
1. Run `ruff format .` from the root directory to automatically format all Python code according to the global `pyproject.toml`.
2. Run `ruff check . --fix` to auto-fix any linting or import issues.

### Phase B: Architecture Synchronization
1. Execute the `python ops/sync_tree.py` script.
2. This script will automatically traverse the project hierarchy and inject a freshly mapped directory tree directly into `docs/structure.md`.

### Phase C: Review & Report
1. Summarize any modified files (e.g., if `ruff` changed formatting or if `structure.md` was updated).
2. Ensure you have not introduced syntax errors.
3. If new libraries or significant logic changes were made during your work, gently remind the user to trigger `/project-checkpoint` to run `graphify update .`.

## Common Mistakes
- **Forgetting to format**: AI agents might introduce subtle stylistic deviations. Running this skill ensures the codebase always looks like it was written by a single expert.
