---
name: strict-agent-pipeline
description: >-
  Enforces the 9-step textbook coding pipeline globally across any project. 
  Dictates how the agent approaches context gathering, planning, code modification, 
  headless testing, documentation syncing, and knowledge graph regeneration.
---

# Strict Agent Pipeline

## Overview
This skill hardwires the "textbook 9-step pipeline" into the agent's behavior globally. No matter what project you are in, the agent will follow a strict, disciplined sequence of operations before, during, and after modifying code. 

## Dependencies
- **graphify**: Required for step 9 to sync the project architecture.

## Quick Start
"I need to add a new feature to the batch tuning script." (This workflow activates automatically upon complex requests).

## Workflow (The 9 Steps)

### 1. Read Context
- Start with context. Always read `GEMINI.md`, project root `CONTEXT.md`, and any local `CONTEXT.md` in the target folder before taking action.

### 2. Plan First
- For significant changes, create an `implementation_plan.md` artifact. Outline the proposed architecture, identify dependencies, and await explicit user approval. 80% planning, 20% execution.

### 3. Modify Code
- Write or modify the code safely. If tweaking minor things, work directly on the file. If major structural changes are needed, scaffold new pipelines alongside the old ones to avoid breaking existing functionality until merged.

### 4. Test Headless
- Write tests. Verify the engine/scripts run successfully using background terminal scripts or interactive notebooks. Do not rely on assumptions.

### 5. Iterate
- Fix any bugs identified during testing. Repeat testing until clean.

### 6. Sync Downstream Dependencies
- Double check no functionality is left behind. Update all notebooks and downstream scripts that have been impacted by the API or structural changes.

### 7. Clean Repo
- Remove redundancies, old scaffolding, and unused test files. Keep the repository modular and pristine.

### 8. Update Documentation
- Immediately update `CONTEXT.md`, README files, and any relevant markdown documentation to reflect the new state of the code.

### 9. Sync Knowledge Graph
- Finally, run `graphify update .` to lock the new project state into the structural knowledge graph.

## Common Mistakes
- **Skipping Context**: Hacking code without reading `CONTEXT.md` leads to architectural divergence. 
- **Skipping Graphify**: Forgetting to update the knowledge graph makes future agent reasoning fail.
