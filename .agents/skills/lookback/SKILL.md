---
name: lookback
description: Distill knowledge, steps, and edge-case fixes from a completed chat session into a reusable Agent Skill following the agentskills.io standard. Use when asked to look back, summarize session workflows, or create a skill from what was just done.
---

# Lookback & Skill Distillation

Distills the knowledge, procedural steps, and bugfixes from a completed session into a structured, reusable Agent Skill.

## Structure of Generated Skills

When distilling a session into a new skill under `.agents/skills/<skill-name>/`:

1. **YAML Frontmatter**: Include `name` and a detailed `description` explaining the task and trigger conditions.
2. **Overview**: A concise 2-sentence summary of the task.
3. **Prerequisites & Environment**: Required libraries, environments (e.g., conda envs), and file paths.
4. **Step-by-Step Procedure**: The exact commands and code logic that solved the problem.
5. **Gotchas & Error Recovery**: Errors encountered during the session and how to prevent or fix them.
6. **Helper Scripts**: If reusable helper scripts were developed, save them under `.agents/skills/<skill-name>/scripts/`.