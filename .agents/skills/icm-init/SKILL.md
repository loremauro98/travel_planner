---
name: icm-init
description: >-
  Initializes a new project with the Interpretable Context Methodology (ICM) architecture, including layer 1 routing map (GEMINI.md), layer 2 room contracts (CONTEXT.md), and a robust 9-step code pipeline with Graphify, Serena, and testing integration.
---

# Interpretable Context Methodology (ICM) Project Scaffolder

## Overview
This skill acts as an intelligent project initializer. When the user asks to create a new project or scaffold the folder structure for a project, use this skill to generate a customized ICM folder structure. The setup includes creating a `GEMINI.md` routing map, a strict `CODE_PIPELINE.md` 9-step workflow, and specific workspace directories with `CONTEXT.md` room contracts.

## Workflow

### 1. Clarification
Before creating any files, ask the user clarifying questions:
- What is the specific purpose and scope of the project?
- What are the key stages or workspaces (e.g., planning, src, ops, docs, frontend, backend) needed for this project?
- What tech stack or languages will be used?

Wait for the user's response. If the initial description is already detailed enough to derive workspaces and tech stack, you can skip this step or ask for final confirmation.

### 2. Edge Case Check
If the project directory is not empty, ask the user if they want to merge the ICM structure into the existing files or abort. Wait for their response before proceeding.

### 3. Layer 1 Creation (`GEMINI.md`)
Generate a `GEMINI.md` file at the root of the project. It MUST contain:
- **Identity & Context:** The project identity, goal, and the AI's role/personality traits.
- **Workspaces:** A list of the defined workspaces (e.g., `/planning`, `/src`, `/docs`, etc.).
- **Naming Conventions:** Specific naming conventions for the tech stack (e.g., snake_case for Python, PascalCase for classes).
- **Tooling & Code Navigation:** Explicit instructions demanding the use of `Serena` for semantic indexing, `Graphify` for structural knowledge graphs (including running `graphify update .`), and writing Unit Tests for code.
- **Routing Table:** A markdown table defining Tasks, "Go to" paths, and "Read" files (`CONTEXT.md`).

### 4. Pipeline Creation (`CODE_PIPELINE.md`)
Generate a `CODE_PIPELINE.md` file at the root of the project outlining a strict 9-step textbook coding pipeline:
1. Start with Context
2. Plan and Track
3. Modify Code
4. Test (Headless/Unit Tests)
5. Iterate
6. Consolidate & Double Check
7. Integration
8. Clean the Repo
9. Documentation & State Sync (including `graphify update .`)

### 5. Layer 2 Creation (`CONTEXT.md` files)
For each workspace defined in step 1/3 (e.g., `/planning`, `/src`, `/ops`, `/docs`), create the directory and generate a `CONTEXT.md` file inside it.
Each `CONTEXT.md` MUST strictly follow this format:
- **Inputs**: (e.g., `Layer 1 (map): ../GEMINI.md`, or working inputs from other folders).
- **Process**: The specific concrete steps for what to do in this workspace.
- **Outputs**: Where the files should go.
- **Notes / constraints**: Any stage-specific constraints.
- A general note at the top linking to the `../CODE_PIPELINE.md` for general workflow rules.

### 6. Tool Initialization & Testing (Serena & Graphify)
After generating the files, actively initialize the knowledge tools to ensure the environment is ready for coding:
- **Graphify Setup**: Create a `.graphifyignore` file to ignore raw data and large media assets (e.g., `*.ipynb`, `*.pdf`, `*.csv`, `*.png`, etc.), but allow `.md` and `.py` files so documentation and code are semantically linked. Then, run the initialization command (e.g., `graphify update .`) to map the structure locally.
- **Serena Setup**: Run the initialization command for Serena (e.g., `serena init` or `serena update`) to build the semantic index.
- **Verification**: Run a quick test query on both tools to guarantee they are correctly indexing the new project and report the success to the user.

## Common Mistakes
- **Skipping clarification**: Do not invent workspaces blindly if the project scope is vague. Ask first.
- **Forgetting tools**: Do not forget to integrate `Graphify` and `Serena` rules into `GEMINI.md`.
- **Incomplete Contexts**: Ensure every created workspace folder actually has a `CONTEXT.md` file with the correct formatting (Inputs, Process, Outputs).

## Theoretical Foundation
The full theoretical background and academic rationale for the Interpretable Context Methodology (ICM) is located in the attached paper. When the user asks questions about the paper, methodology, or underlying principles of ICM, you MUST read the paper located at `references/InterpretableContextMethodology.pdf` to ground your answers.

Additionally, the official GitHub repository for ICM (https://github.com/RinDig/Interpreted-Context-Methdology) has been archived locally at `references/github_repo.md`. Refer to this document for code examples, implementation specifics, and repository documentation.
