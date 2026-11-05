# Context: planning

> Room contract for `/planning`. Governs what is allowed and expected in this folder.
> Consult [`../AGENTS.md`](../AGENTS.md) for project-wide routing and rules.

## 1. Role & Purpose

Task tracking, feature specifications, architecture decisions, and the 80/20 planning phase. Every
non-trivial change starts here before code is touched.

---

## 2. Allowed Inputs

- User requirements, GitHub issues, and research notes.
- Existing specs, decisions, and the task archive.
- Findings from `/src`, `/ops`, and `/data` needed to scope a change.

---

## 3. Core Process & Execution

1. Clarify the request; never assume.
2. Write or update a spec under `specs/`.
3. Create an active task log under `tasks/task_<name>.md` with binary checkboxes.
4. Record major architectural choices as an ADR under `decisions/`.
5. Hand the spec to `/src` or `/ops` for implementation.
6. At checkpoint, archive the completed task log to `tasks/archive/`.

---

## 4. Expected Outputs

- `[feature_name]_spec.md` -> `specs/`
- `task_<name>.md` -> `tasks/`
- `[YYYY-MM-DD]-[decision].md` -> `decisions/`
- Completed task logs -> `tasks/archive/`

---

## 5. Local Invariants & NEVER Rules

- **Never write task notes to the repository root.**
- **Never start coding without a task log** for multi-step work.
- **Never leave a completed task in `tasks/`**; archive it at checkpoint.
- **Never restate a threshold or formula in a spec** without naming its authority file.
- **Never mark a task complete without evidence** (test output, run output, or a cited file).

---

## 6. General Guidelines

Use `writing-plans` and `strict-agent-pipeline` for specs and task decomposition. Keep specs short
enough to be read in one sitting; link to the relevant `CONTEXT.md` and code instead of copying it.
