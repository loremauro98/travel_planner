---
name: project-checkpoint
description: >-
  Standardizes the process of wrapping up a phase of work. Automates the 
  synchronization of all local and global documentation, cleans the repository 
  of temporary scaffolding, regenerates the structural knowledge graph, and commits/pushes session work.
---

# Project Checkpoint

## Overview
When a major milestone or phase of work is completed, the codebase is often left with outdated documentation, scratch files, or desynchronized knowledge graphs. This skill orchestrates a rigorous wrap-up sequence to officially establish a stable "checkpoint" in the project.

## Dependencies
- **graphify**: Required to rebuild the knowledge graph at the end of the checkpoint.

## Quick Start
"We're done with the spatial tuning engine. Let's run a project checkpoint."

## Workflow

### Phase A: Audit & Verification

#### 1. Robustness Audit
- Invoke the `/robustness-audit` skill to verify that headless tests exist, no statistical parameters are hardcoded, and output folders have explanatory names.
- Flag and prompt the user to archive or delete orphaned outputs from deprecated pipelines.

### Phase B: Documentation Synchronization
**Crucial:** This phase is extremely dense and prone to failure if rushed. To ensure strict compliance, you MUST spawn a dedicated subagent to handle this phase.

#### 2. Spawn the Documentation Subagent
- Use `invoke_subagent` to spawn a `self` subagent with the role `Documentation Synchronizer`.
- Prompt the subagent with the list of files/pipelines modified during your current session (referencing your `task.md`), and explicitly instruct it to perform the following two tasks:

  **Task A: Standardised Technical Context (Leaf Nodes)**
  - Locate all leaf-level analytical folders that were modified (e.g., `src/action_tuning/scripts/glm_based`).
  - Read their code to understand the architecture, then rewrite their `CONTEXT.md` to strictly follow this 6-part standardized structural template:
    1. **Core Philosophy:** Brief explanation of the statistical approach.
    2. **Script Architecture & Dependency Map:** Tree representation of scripts and imports.
    3. **Execution Command Sequence:** Exact CLI commands to run it.
    4. **Architectural Principles:** Numbered list of core theoretical choices (e.g., Null sampling rules, Spatial masking, FDR).
    5. **Step-by-Step Analysis Pipeline Breakdown:** ASCII flowchart of the data flow.
    6. **Detailed Steps:** Numbered prose breakdown matching the flowchart.

  **Task B: Recursive Context Updates & Lineage**
  - For every local `CONTEXT.md` updated in Task A, the subagent MUST recursively evaluate and update all parent `CONTEXT.md` routing files up to the repository root.
  - Screen each parent directory level. If an entirely new pipeline or major architectural logic was added, the change must bubble up completely through all routing tables. If only a minor local parameter changed, upper-level updates might be minimal. 
  - Ensure proper local citations are injected (do not use global `REFERENCES.md`) and methodology lineage is clear.
  - Trace horizontal dependencies (e.g. if `/src` changes impact `/data` or `/ops`, update those contexts too).
  - Explicitly review and update `CODE_PIPELINE.md` and `docs/visualisations/` if the core workflow or plot aesthetics changed.

- **Wait** for the `Documentation Synchronizer` subagent to complete its task and report back before proceeding to Phase C.

### Phase C: Finalization

#### 5. Task Archival & Changelog Update
- Read the current `task_<arm>.md` artifact under `planning/tasks/`.
- Generate a concise bullet-point summary of what was achieved, the files touched, and the design decisions made.
- Append this summary to `docs/CHANGELOG.md` following the strict `# YYYY-MM-DD` / `## [Title]` / `### Tasks` hierarchy.
- **Archive Task Log:** Move the completed `task_<arm>.md` file from `planning/tasks/` into `planning/tasks/archive/` so `planning/tasks/` remains clean for active work.

#### 6. Knowledge Graph & Semantic Index Regeneration (Milestone Authorized)
- Run `graphify update .` from the root of the project to index the final structural state of the codebase.
- Run `serena project index` from the root of the project to update Serena's semantic symbol cache.
- These commands are authorized strictly at milestone checkpoints.

#### 7. Commit and Push Session Work
- Inspect `git status` and stage **strictly only** the files modified during the current session (referencing the task log and touched files). **NEVER run `git add .`, `git add -A`, or `git add -u` (AGENTS.md NEVER #10).** Always name files explicitly by path (`git add path/to/file`).
- Commit with a clear, descriptive message summarizing the session milestone.
- Push the commit to the active tracking branch (`git push origin <branch>`).

#### 8. Checkpoint Walkthrough
- Generate a final summary detailing exactly what was established in this checkpoint, including the specific files committed and pushed, and remind the user to run `/graphify --update` if deep semantic parsing of new documentation is required.

## Common Mistakes
- **Forgetting `graphify`**: If you skip updating the graph, the agent will enter the next phase of work operating on stale architectural knowledge.
- **Ignoring Local Contexts**: Updating the root `CONTEXT.md` but leaving local folder contexts outdated leads to conflicting instructions for future subagents.
- **Blanket Staging**: Running `git add .` or committing files unrelated to the session's specific task. Always stage session files selectively.
