---
name: robustness-audit
description: >-
  A fast, code-level check run automatically during /project-checkpoint to verify 
  headless tests exist and no hardcoded statistical parameters are hidden in utility functions.
---

# Robustness Audit

## Overview
This skill acts as an automated quality gate for statistical code. It is designed to be run as Phase A of the `/project-checkpoint` workflow, ensuring that no technical debt or hidden assumptions sneak into the codebase before documentation is synced.

## Workflow

### 1. Hardcoded Variable Scan
- Scan the `src/` directory (or the specific folder being audited).
- Look for statistical functions. Verify that parameters like `p-values`, `alpha`, `n_shuffles`, or `cutoffs` are NOT hardcoded deep inside utility functions.
- Ensure all such thresholds are exposed as parameters and bubbled up to the highest level (e.g., the batch script).

### 2. Headless Test Verification
- Verify that every new statistical function or core data processing logic has a corresponding headless test or unit test.
- If a function lacks a test, flag it immediately.

### 3. Output Folder Naming Check
- Verify that any newly created output directories use explanatory, specific names (e.g., `apa_spatial_tuning/speed_tuning_outputs` instead of just generic names).

### 4. Reporting
- If any checks fail, pause the checkpoint and ask the user if they want to fix the issues before proceeding.
- If all checks pass, report success and allow the checkpoint to continue to the documentation synchronization phase.
