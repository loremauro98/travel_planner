---
name: prompter
description: Spawns a subagent that gathers context via Serena, Graphify, and local CONTEXT.md files to generate a structured prompt for outsourcing complex planning or scientific problems to external LLMs or human experts.
---

# `prompter` - Planning Outsourcing Prompt Generator

When this skill is invoked (via `/prompter`, "use prompter", "outsource planning for...", "generate external prompt", or when asked to prepare a prompt for an external LLM/colleague), execute the following workflow to construct a comprehensive, self-contained prompt.

---

## Workflow Instructions

### 1. Receive & Clarify Problem
Identify the problem or analytical feature specified by the user. If the problem statement lacks essential detail, ask brief clarifying questions before gathering context.

### 2. Define & Invoke Context-Gathering Subagent
Spawn a context-gathering subagent using `define_subagent` (or invoke a `research` / `self` subagent) named `prompter_context_gatherer`.

**Subagent Configuration:**
- **name**: `prompter_context_gatherer`
- **description**: `Context researcher that maps code structures, graphify relationships, and CONTEXT.md files for outsourcing prompts`
- **system_prompt**:
```text
You are a context extraction specialist for the active avoidance neuroscience pipeline.
Your task is to gather complete, precise context for a given analytical or coding problem so it can be cleanly outsourced to an external LLM or human expert.

INSPECTION PROTOCOL:
1. Serena & Code Search: Locate exact functions, data structures, variables, and module boundaries related to the problem.
2. Graphify Knowledge Graph: Run `graphify query "<problem keywords>"`, `graphify path`, and `graphify explain` to map architectural dependencies and affected modules.
3. Local Context Files: Read `CONTEXT.md` files in relevant directories (`/src`, `/planning`, `/data`, `/ops`), along with `AGENTS.md` and any relevant `math_spec.md` or `REFERENCES.md`.
4. Domain Constraints: Extract key parameters (e.g. frame rates, sampling rates, normalization rules, cell count constraints, shuffle numbers).

Return a clear, structured summary of your findings covering code references, equations, input/output schemas, and project rules.
```

Instruct the subagent with the user's target problem statement.

### 3. Synthesize the Outsourcing Prompt
Using the research findings returned by the subagent, draft a standalone, copy-pasteable Markdown prompt containing the following **4 mandatory sections**:

#### Section 1: Persona / Role (`Who the LLM/Expert is`)
Define a precise expert persona tailored to the domain.
- *Examples*:
  - `"You are an expert computational neuroscientist and statistician with deep experience in 1P calcium imaging, hippocampal CA3 spatial representations, and non-parametric bootstrap resampling."`
  - `"You are a senior python software architect specializing in vectorized numpy/scipy operations and high-throughput analytical pipelines."`

#### Section 2: Problem Statement (`What the problem is`)
A clear, unambiguous statement of the problem to solve, including goals, edge cases, and known failure modes.

#### Section 3: Technical & Scientific Context (`The Context`)
Complete background context assembled from the codebase:
- Relevant source files, functions, and data structures (with links/paths)
- Mathematical rules, equations, normalization methods, and sampling rates
- Project rules from `AGENTS.md` (e.g., percentages over raw counts, speed vs rigor, transparent data masking)

#### Section 4: Expected Output (`The Expected Output`)
Specify exactly what the external LLM or human expert must produce:
- A step-by-step implementation plan or mathematical specification
- Recommended function signatures, data structures, and null-distribution definitions
- Strategy for edge-case handling and computational optimization
- Designed so Lorenzo or an agent can directly re-ingest the response back into the active pipeline context.

### 4. Output the Prompt Artifact
Save the formatted prompt to an artifact file (e.g., `outsourced_prompt.md` or `prompter_<problem_slug>.md`) in the artifacts directory and present it cleanly to the user.
