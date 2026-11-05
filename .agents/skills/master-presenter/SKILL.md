---
name: master-presenter
description: Turn a finished body of analysis into a walkthrough a person can follow start to finish — a PDF deck of figures plus a matching markdown narration, one section per page. Use when asked to present, explain, or walk someone through findings; to build a talk, a deck, or a report from results that already exist; or when a body of work has become too scattered across findings docs and agent reports to be understood in order. Not for generating the analysis itself, and not for a technical dashboard over metrics — that is `scientific-pdf-dashboard`.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
metadata:
    skill-author: distilled from the peri-event investigation walkthrough, 2026-08-06
    reference-implementation: ops/presentation/
---

# Master Presenter

## What this produces

**Two artefacts, read side by side.**

| file | what it is | what goes in it |
|---|---|---|
| `presentation.pdf` | the deck | one page per idea: title, the figure, and a two-line *where to look* |
| `presentation.md` | the narration | one section per page, in the same order, ≤260 words each |

Plus the machinery that keeps them honest: `build_figures.py`, `build_pdf.py`, `figure_data.md`.

The deck is what a person looks at. The markdown is what they read alongside, or what you read
aloud. **Neither is a summary of the other** — the deck carries the evidence, the markdown carries
the reasoning.

The reference implementation is `ops/presentation/` in this repo. Read it before building a new
one; it is a worked example of every rule below.

---

## The five hard rules

These are not style preferences. Each one exists because breaking it produced a document nobody
could follow.

### 1. Every page uses only what came before it

No forward references. Not "as we will see", not "using the method from page 20", not a term
defined later. **Test it: can a reader who has seen pages 1..N−1 and nothing else understand page
N?** If not, either move the page or move what it depends on.

This is the rule that costs the most and buys the most. It forces the order of the argument to be
the order of the explanation, which is usually *not* the order the work happened in.

### 2. Maximum 260 words per page

If a page runs over, one of two things is true and both are fixable:

- **you are prosing** — cut the throat-clearing, the hedging, the second example; or
- **the page holds two ideas** — split it, and give the second one its own figure.

Enforce it with a script, not by eye. See *Verification gates*.

### 3. One idea per page, and the page title is that idea

The title is a claim or a question, not a label. "The floor" and "Suspect 2: is the comparison
broken?" work. "Results" and "Analysis 3" do not.

### 4. Guide the eye on every figure page

The *where to look* line must say, in plain words:

- what is on the horizontal axis and what is on the vertical one;
- what the colours or series mean;
- **where to look and what to notice** — the single thing this figure exists to show.

A reader should never have to reverse-engineer a plot. If a figure needs more than two lines of
guidance, it is doing two jobs — split it.

### 5. Limitations go on the page where the number appears

Not in a footnote, not in a caveats slide at the end. If a number rests on one animal, seven
sessions, or a truncated run, **that sits next to the number**. A reader who stops halfway must
not be left with a false impression.

---

## The arc

Most investigations fit this shape. Use it unless the work genuinely does not.

| act | pages | what it does |
|---|---|---|
| **Setup** | 4–6 | what we record, what we ask, and how the current method works — written out mechanically so later pages have something concrete to point at |
| **The crack** | 2–3 | the measurement that shows something is wrong, and what it depends on |
| **Suspects** | 1 per suspect | each candidate explanation tested and eliminated, one page each |
| **The pivot** | 2–3 | the decisive experiment, its design, and its result |
| **What replaces it** | 3–5 | the alternative, and the evidence it would work |
| **Close** | 1–2 | what is firm, what is not, what happens next |

**Two things about this shape that matter.**

**The suspects act is not padding.** A conclusion with four alternatives eliminated is worth far
more than the same conclusion asserted, and a reader who has watched four suspects acquitted will
accept the fifth explanation without argument. Give each one a page even if the answer is short.

**Identify the pivot page before you write.** There is usually exactly one page where the story
turns — where "we cannot tell which answer is right" becomes "neither answer was ever right". Know
which page that is, and build everything before it as the case for taking it seriously.

---

## Workflow

### Step 1 — inventory the data before planning the deck

Find every result file the story rests on and read its **schema**, not just its name. Column names,
row counts, what one row is. Two failures happen here constantly:

- **The same quantity computed two ways.** Different runs, different gates, different windows.
  Pin down which is which *before* plotting, or the deck will mix definitions across pages.
- **"One row per session" is usually a lie.** Check whether a row is a session, or a
  session × condition unit. Say which on the figure.

### Step 2 — write the page plan first, then specify every figure

Decide the pages and their order *before* any plotting. Then, for each figure, write a spec that
states: what is on each axis, what the series are, what is filtered out, what is annotated.

**Specify the figure, then delegate the drawing.** Because you wrote the spec, the narration you
write will match what was drawn. If you delegate the *design*, the text and the plot drift apart
and you will not notice.

Require the plotter to produce `figure_data.md`: for every figure, the exact numbers plotted, the
n, the source file, and any row filtering. **You write the narration from that file, not from
memory.**

### Step 3 — write the narration against the figure data

Every number in the text must be traceable to `figure_data.md` or to a figure. If you cannot find
it there, do not write it.

### Step 4 — assemble

`build_pdf.py` lays out title + figure + caption. Two properties worth copying from the reference
implementation:

- **resolve figures at run time**, preferring a pooled or final variant when one exists, so the
  deck can be rebuilt after any figure change without editing the page list;
- **text-only pages** for the setup, the summary tables, and the close. A deck of nothing but
  plots has nowhere to state the argument.

### Step 5 — run the gates, then rebuild

See below. Then rebuild the PDF and re-run the gates. Numbers move; the narration must move with
them.

---

## Verification gates

Run these as scripts. Every one of them has caught a real error.

**Word count per page.** Parse the markdown, count words per section, fail on anything over 260.

**Figure coverage.** Every figure referenced by the page plan exists; every figure built is either
used or deliberately dropped.

**Number traceability.** Spot-check that headline numbers in the narration appear in
`figure_data.md`. When a figure is rebuilt, diff the old and new numbers and **grep the narration
for every value that moved.**

**The forward-reference check.** Read the page titles in order and ask whether each is intelligible
given only the ones above it. This one is manual; do it anyway.

---

## Anti-patterns

**Writing the narration from the analysis rather than the figures.** The analysis knows things the
reader cannot see. Write from what is on the page.

**A caveats slide.** Caveats belong next to the number they qualify. A reader who stops at page 12
must not be misled by page 12.

**Softening a negative result.** If a method failed, say so on its own page, with the number. The
negative result is usually the load-bearing one, and hedging it makes the whole deck untrustworthy.

**Jargon smuggled in as a defined term.** Defining "conditional exactness" on page 9 does not make
it plain language. Find the everyday phrasing, or explain the mechanism and skip the name.

**Dense pages that "cover" a topic.** Coverage is not the goal; being followed is. Two clear pages
beat one complete one.

**Letting figures and text drift.** Every rebuild is a chance for the text to become wrong. Treat a
figure change as a text change until proven otherwise.

---

## When the numbers change under you

They will. Analyses finish, second subjects land, bugs get fixed. Three habits:

- Keep the page list and the figure resolution in code, so a rebuild is one command.
- When a figure agent reports a moved number, **grep the narration for the old value immediately**
  and fix it before doing anything else.
- If a conclusion changes rather than a number, the page changes — and often the pages after it. A
  conclusion that moved is a signal to re-read the arc, not to patch one sentence.

The reference implementation had two claims that were true of one subject and false of two. Both
were caught by diffing the rebuilt figure data against the narration. Neither would have been
caught by re-reading.
