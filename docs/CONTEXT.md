# Context: docs

> Room contract for `/docs`. Governs what is allowed and expected in this folder.
> Consult [`../AGENTS.md`](../AGENTS.md) for project-wide routing and rules.

## 1. Role & Purpose

Permanent documentation: the skill registry, the changelog, the generated repository structure, API
references, user guides, and reference notes. This is the human-readable memory of the project.

---

## 2. Allowed Inputs

- Source changes in `/src` and `/ops`.
- Finalized specs and decisions from `/planning`.
- Checkpoint summaries and run evidence.
- Installed skills in `.agents/skills/`.

---

## 3. Core Process & Execution

1. Review what changed in the codebase and the skill suite.
2. Update API references when interfaces change.
3. Append milestone summaries to `CHANGELOG.md` at checkpoint.
4. Regenerate `structure.md` with `python ops/sync_tree.py`.
5. Keep `CUSTOM_SKILLS.md` in sync with `.agents/skills/`.
6. Move durable reference material into `reference/`.

---

## 4. Expected Outputs

- `CUSTOM_SKILLS.md` — the skill registry.
- `CHANGELOG.md` — permanent audit log, newest first.
- `structure.md` — generated directory map.
- `reference/` — course notes, literature, and background material.
- `[doc_name].md` — API references and user guides.

---

## 5. Local Invariants & NEVER Rules

- **Never duplicate rules from `AGENTS.md`.** Point at the authority.
- **Never let `CUSTOM_SKILLS.md` drift** from the installed skills.
- **Never edit `structure.md` by hand.** Regenerate it.
- **Never put task logs here.** They belong in `/planning/tasks/`.
- **Never quote a number without provenance** (run, rule, or source).

---

## 6. General Guidelines

All changes here follow the 9-step pipeline in [`../CODE_PIPELINE.md`](../CODE_PIPELINE.md).
Use Markdown for all documentation. Keep the changelog hierarchy strict:
`# YYYY-MM-DD` → `## [Title]` → `### Tasks`.
