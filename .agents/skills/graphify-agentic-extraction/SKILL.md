---
name: graphify-agentic-extraction
description: >-
  Automates background semantic knowledge graph extraction to bypass external 
  API rate limits. Spawns a subagent to read local Markdown sources and runs a 
  reusable Python script to securely stitch semantic and structural graphs together.
---

# Graphify Agentic Extraction

## Overview
When the standard `graphify` extraction fails because of free-tier API rate limits (e.g. Gemini 15 requests/minute), Graphify falls back to structural-only parsing, leaving Markdown files isolated. This skill manually orchestrates the deep semantic extraction by leveraging background AI subagents to extract the concepts, and then forcefully merges them with the document nodes, rewiring them with `contains_concept` edges.

## Dependencies
- **graphify**: Required to use standard structural components and HTML builders.
- **Python 3**: For running the `merge_graph.py` helper script.

## Quick Start
"The semantic index failed because of API rate limits. Let's run a `/graphify-agentic-extraction`."

## Workflow

### 1. Detect Files
- Read `.graphify_uncached.txt` (or `.graphify_detect.json`) in the target directory (e.g., `vault/`) to get the list of uncached Markdown files.

### 2. Dispatch Semantic Subagent
- Use `invoke_subagent` (type: `self`) to dispatch a background semantic extraction agent.
- Pass the full prompt from `C:\Users\lorem\.gemini\config\skills\graphify\references\extraction-spec.md`.
- Ensure the prompt explicitly asks the subagent to read the specific target files and output valid Graphify semantic JSON containing the `nodes` and `edges`.

### 3. Save JSON Chunk
- When the subagent completes, parse its JSON response and write it to disk as `graphify-out/.graphify_semantic_new.json` in the target directory.

### 4. Execute Merge Script
- Execute the helper Python script provided in this skill folder: `.agents/skills/graphify-agentic-extraction/scripts/merge_graph.py [TARGET_DIR]`.
- This script will read the semantic JSON, generate structural document nodes for the Markdown sources, inject `contains_concept` edges linking the sources to the semantic topics, and forcibly rebuild `graph.json` and `graph.html`.

## Common Mistakes
- **Forgetting to update the graph before extraction**: If the structural graph is out of sync, `merge_graph.py` won't have accurate baseline files.
- **Modifying the subagent JSON schema**: Do not alter the expected Graphify JSON output format when prompting the subagent, otherwise `merge_graph.py` will crash.
