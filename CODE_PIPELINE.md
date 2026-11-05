# The 9-Step Textbook Coding Pipeline

> The strict standard operating procedure for implementing features, modifying algorithms,
> and refactoring code in this repository. **Never skip these steps.**

```mermaid
flowchart TD
    S1["1. Start with Context\n(Read local CONTEXT.md & AGENTS.md)"] --> S2["2. Plan & Track\n(Create planning/tasks/task_*.md)"]
    S2 --> S3["3. Test-First (TDD)\n(Write failing headless test in tests/)"]
    S3 --> S4["4. Minimal Implementation\n(Pass the test & calibrate null)"]
    S4 --> S5["5. Refactor & De-duplicate\n(Single-authority declarations)"]
    S5 --> S6["6. Consolidate & Audit\n(Check NEVER rules & hardcoded cutoffs)"]
    S6 --> S7["7. Integration & Smoke\n(Verify end-to-end runners)"]
    S8 --> S9["9. Documentation & Sync\n(Sync CONTEXT.md recursively & graph)"]
    S7 --> S8["8. Clean Workspace\n(Remove caches, check git status)"]
```

---

## 1. Start with Context
- Read the local `CONTEXT.md` in the target directory before writing code.
- Consult `AGENTS.md` for project-level constraints and routing.
- If modifying an existing module, inspect existing tests and inputs.

## 2. Plan and Track
- Create or update a task tracking file under `planning/tasks/task_<name>.md`.
- Break down the goal into verifiable subtasks with binary completion checkboxes (`[ ]` $\rightarrow$ `[x]`).
- Identify potential failure modes and trade-offs before touching code.
- Clarify ambiguities early; never assume.

## 3. Test-First (TDD RED Phase)
- Write a headless unit test in `tests/` capturing the desired behavior.
- Run the test to confirm it fails for the expected reason (`RED`).
- Never integrate untested math, statistics, or data transformations.

Recommended command:
```powershell
& "C:\Users\lorem\miniconda3\envs\travel\python.exe" -m pytest tests/test_<module>.py -q
```

## 4. Minimal Implementation & Calibrated Null (TDD GREEN Phase)
- Write the minimal, elegant implementation to make the test pass.
- Keep functions pure, typed, and modular.
- Expose all parameters in function signatures or configs.
- **A passing test suite is not a calibrated null:** if the change adds or touches a statistical
  reference — a shuffle, a percentile, a chance level — one of the tests must measure its
  false-positive rate on data built to contain no effect, and assert that rate against the nominal
  alpha. A null must be constructed by the exact same procedure as the observation, including every
  fitting step, or it measures a different quantity.

## 5. Refactor & De-duplicate (TDD REFACTOR Phase)
- Ensure quantities, region maps, and constants are defined in exactly ONE authority file.
  - Regional airport expansion: `src/services/routing.py`
  - Moving-average and dip logic: `src/services/analytics.py`
  - Database path and schema: `src/database/db_manager.py`
- Clean up intermediate variables, add docstrings, and ensure readability.
- Point at the authority; never declare duplicates across module boundaries.

## 6. Consolidate & Audit
- Check against the `NEVER` rules in `AGENTS.md`.
- Confirm zero hardcoded analytical cutoffs, seeds, windows, or thresholds.
- Verify error handling and edge cases (empty flights, missing prices, zero division, NaNs).
- If filtering flights or rows, verify that drop counts per criterion are tracked and logged
  (per `transparent-data-masker`).

## 7. Integration & Verification
- Run the full test suite on touched modules:
  `& "C:\Users\lorem\miniconda3\envs\travel\python.exe" -m pytest -q`
- Smoke-test upstream and downstream dependencies.
- Verify end-to-end runners exit with code 0.
- Do not call live SerpApi from tests; mock the API boundary.

## 8. Clean the Workspace
- Remove all temporary scratch files, debug prints, and test outputs.
- Run `git status` to ensure zero untracked data arrays, caches, `.env` files, or unapproved
  temporary files exist.

## 9. Documentation & State Sync
- **Update Documentation (Recursive):** Modify all relevant `CONTEXT.md` files to accurately reflect
  changes. This must be done **recursively**: if a change occurs deep in a subproject, screen and
  update all parent `CONTEXT.md` routing files up to root.
- **Technical Context Standard:** All leaf-level analytical folders must possess a detailed
  `CONTEXT.md` following the standardized 6-part structural template:
  1. **Core Philosophy** — the approach, briefly.
  2. **Script Architecture & Dependency Map** — tree of scripts and their imports.
  3. **Execution Command Sequence** — the exact commands in execution order.
  4. **Architectural Principles** — null construction, significance rules, masking, corrections, exclusions.
  5. **Step-by-Step Analysis Pipeline Breakdown** — flowchart of data flow.
  6. **Detailed Steps** — numbered prose matching the flowchart.
- **Point at the authority; never restate it:** When documenting a quantity, threshold, geometry, or
  rule, name the defining symbol/file instead of copying numbers.
- **Document configurable choices as a switch, not a fact:** Name the constant and its current
  default, rather than declaring one of its values as the immutable method.
- **Numbers quoted must cite provenance:** Any number in documentation must name the run and rule
  that produced it.
- **Maintenance & Indexing:** Run `icm-maintenance` to check formatting and sync `docs/structure.md`.
  Re-index structural and semantic graphs (`graphify update .`, `serena project index`) when
  concluding milestone checkpoints.
