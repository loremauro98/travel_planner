---
name: module-migrator
description: >-
  Safely migrates an existing set of code files into a modular sub-project folder 
  with strict structural organization. Updates relative imports, document context, 
  and syncs the semantic knowledge graph.
---

# Module Migrator

## Overview
Safely moves flat codebases or sets of files into structured sub-modules (e.g., separating `scripts/`, `notebooks/`, and `current_output/`). It orchestrates file relocation, automatically parses and updates relative `sys.path` injections, manages documentation context, and ensures the semantic graph remains synced.

## Dependencies
- **graphify**: Required to rebuild the knowledge graph after structural changes.

## Quick Start
"Extract the visualization scripts into a new module called `plot_engine`."
"Move the folders notebook, scripts, along with these other notebook in a subfolder called `data_processing`."

## Workflow

### 1. Plan & Scaffold
- Identify exactly which files need to be moved.
- Create the target module folder and standard subdirectories (`scripts/`, `notebooks/`, `current_output/` or whatever structure the user requested).

### 2. Migrate Files
- Use standard terminal commands (`Move-Item` / `mv`) to relocate the specified Python scripts, Jupyter Notebooks, and output files to their new specific subdirectories.
- Do NOT delete the original folders yet if they are still in use (e.g., locked by a background Jupyter Kernel).

### 3. Rewrite Imports
- Systematically search for and edit relative path injections (like `sys.path.append('..')` or `sys.path.insert(0, parent_dir)`) in Python scripts and Notebooks to account for their new nested depth so that shared utilities can still be imported.
- **IMPORTANT**: If the import logic is highly complex or non-standard, STOP and ask the user for guidance. Do not guess.

### 4. Contextualize New Module
- Create a `CONTEXT.md` file inside the new module describing its purpose, architecture, and where shared resources (like a root `utils.py`) are located.

### 5. Contextualize Parent Folder
- Update the `CONTEXT.md` (and any other relevant documentation) in the original parent folder to reflect the newly extracted module and the new architectural split.

### 6. Sync Graph
- Run `graphify update .` to ensure the semantic knowledge graph matches the new file topology.

### 7. Walkthrough
- Present a final summary to the user highlighting what was moved, how imports were updated, and the new structure.
- **IMPORTANT**: If any files or folders were locked and could not be moved or deleted, you MUST clearly report them in this final summary.

## Common Mistakes
- **Failing to update Jupyter Notebooks**: `sys.path` logic in `.ipynb` files is notoriously brittle when moved. You must edit the raw JSON of the notebook or use your editing tools to update the code cells.
- **Ignoring locked files**: Background kernels often lock directories. Skip destructive deletes on locked files and clearly report them rather than crashing the workflow.
- **Skipping Graphify**: Forgetting to run `graphify update .` will leave the semantic graph broken and future reasoning tasks will fail.
