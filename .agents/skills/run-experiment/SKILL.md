---
name: run-experiment
description: Safely run one-off experimental logic modifications by temporarily modifying code, executing the pipeline, collecting results, and explicitly reverting changes via git to ensure codebase integrity.
---

# `run-experiment`

This skill defines the strict protocol for testing "what-if" scenarios (like changing grid sizes, testing a new parameter outside the spec, or modifying a core equation) without polluting the canonical codebase.

## The Protocol

When instructed to run an experiment that requires modifying frozen or canonical logic:

1. **Write Temporary Scripts to Scratch:** Do not manually edit the tracked files with sed/echo directly. Write a dedicated Python monkey-patch script to your `scratch` directory (`<appDataDir>/brain/<conversation-id>/scratch/`). This script should parse and replace the specific strings/logic in the target `.py` files.
2. **Execute Modifications:** Run the scratch script to apply the changes to the codebase.
3. **Run the Pipeline:** Execute the standard pipeline commands (e.g. `ops/sub_behaviours/run_all.py`) to generate the data. The pipelines are designed to output to isolated, digest-stamped folders in `current_output/`. Do not redirect outputs; let the engine put them where they belong.
4. **Extract Findings:** Read the metrics from the automatically generated `REPORT.md` or `.json` files in the new output directories.
5. **Revert and Clean Up (CRITICAL):**
   - Run `git restore <modified_files>` immediately after you have extracted the data. 
   - Delete your temporary modification scripts from the scratch directory.
   - Run `git status` to verify the working tree is clean.

## Principles
- **No Leftover Logic:** The project codebase must NEVER retain experimental hacks.
- **Traceable Outputs:** The generated outputs stay in `current_output/` because their digest hashes make them unique. They are safe to leave behind as they serve as the permanent empirical record of the experiment.
