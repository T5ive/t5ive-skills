---
name: todo-triage
description: "Use when the user says \"triage\", \"todo triage\", \"แยกงาน\", \"จัด inbox\", or asks to sort raw notes from todo/inbox.md into task files."
---

# Todo Triage

Sort raw inbox notes into task files in one pass. No codebase search.

## Workflow

1. Read `## Todo workflow` in `AGENTS.md` for this project's layout (phase folders vs `features/`). No rules found → default layout: `features/`, `bugs/`, `misc.md`, `backlog.md`.
2. Read `todo/inbox.md`. Missing → tell the user to run todo-init first; stop. No items left → say there is nothing to triage and stop.
3. Classify each item with this decision tree:
   - live-system bug → new file in `bugs/`
   - item under an explicitly misc-like inbox header (e.g. `## Misc`) or the user asked for misc → append one list line to `misc.md` — **never route items to misc.md by your own judgment**: a small standalone item gets its own task file; if it seems too small for a file, add it to the ambiguity batch in step 5 instead
   - wait / low priority → append one section to `backlog.md`: `## <short topic>` + 1–3 lines of the raw note (what it waits for / why low)
   - customer change request on an existing feature → `type: feature`: find the original by searching open task files for the feature name (0 or >1 match → add to the ambiguity batch in step 5); append a checkbox + the raw note to the still-open original file (new file only if the original is done/archived)
   - everything else → new file in `features/` or the matching `phase-X/`
4. An item under an inbox header `## Phase N` gets `phase: N`. Under `## General` or before any header → no phase.
5. Batch ALL ambiguous classifications into ONE question round (choice UI if available) before writing anything.
6. Create files with the template below. Filename kebab-case English; `name:` = short title (Thai or English); `created:` = today's date.
7. Never search the repo and never pre-fill `## Related files` — the dev fills it; it may be supplemented only when work starts.
8. Edit `inbox.md`: remove processed items, keep every header (even now-empty ones) so future notes land in the right section.
9. Report a summary table: item → destination.

## Task file template

```markdown
---
status: open
stage: todo          # todo | wip | test — dev-side workflow, AI updates it as work happens
type: feature        # feature | bug | refactor
created: 2026-09-23  # date the file was created — set once at creation, never change
name: <short task title>
phase:               # phase-based projects only, from the inbox header
jira:                # set when BA creates the ticket — JIRA:KEY-123
done:                # set (YYYY-MM-DD) only when Jira reaches Done
---

## Raw

<raw note verbatim — never rewrite or translate>

## Tasks

- [ ] <subtask>     # only for non-trivial features

## Skills

- [ ] grill-with-choice — spec ยังไม่ชัด
- [ ] implement — ลงมือทำงาน
- [ ] tdd — งานที่ต้องมีเทส
- [ ] diagnosing-bugs — งานบัค
- [ ] review-with-choice — รีวิวก่อนจบ

## Related files

## Progress

```

## Skills pre-tick

Decide while classifying (same pass, no extra analysis):

- item is a bug → tick `diagnosing-bugs`
- raw note is vague or lacks acceptance info → tick `grill-with-choice`
- otherwise tick nothing — the dev ticks when reading the file

## Rules

- `refactor` tasks also live in `features/`; the `type` field distinguishes them.
- An open file already covering the same topic → append there, don't duplicate.
