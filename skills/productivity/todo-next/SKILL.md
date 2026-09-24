---
name: todo-next
description: "Use when the user says \"todo next\", \"หางานถัดไป\", \"มีงานอะไรเหลือ\", \"what should I work on\", or wants a summary of open todo tasks with a recommendation."
---

# Todo Next

Summarize open work and help pick the next task.

Use the user's target project; if none is named, use the current workspace. Scan that project's `todo/`, not a skill source or cache directory.

## Workflow

1. Scan task frontmatter in `todo/` (exclude `archive/`) and skip files without `status: open`. For `stage: todo` or `preop`, stop at frontmatter: do not read the body or recommend them. The dev prepares these files.
2. For `stage: mise`, `wip`, and `test`, present a summary table: file, title, stage, phase, type, jira, last progress date. List `test` separately as waiting for dev test, Jira, or Tester.
3. Append a short section listing leftovers: one-liners in `misc.md` and section titles in `backlog.md` — they never appear on the board, so surface them here.
4. Recommend up to 5 `mise` or `wip` tasks, each with a one-line reason. Rank `mise` first and `wip` next; within a stage prefer older `created` dates, no recent progress, and the user's stated focus. Read the last `## Progress` line for `wip` rework. Never recommend `test` for implementation; if no actionable tasks exist, say so.
5. Wait for the user's choice. Do not start work unasked.
6. On choice:
   - If the chosen work is only a line in `misc.md` or a section in `backlog.md`, promote it to a `stage: todo` task file (todo-triage template), remove the line/section from its list file, and stop for dev preparation. Promotion also happens on direct command — e.g. "promote <topic> from backlog".
   - Start only an open `mise` or `wip` task. Read its full file, then set `mise → wip`; an existing `wip` stays `wip`. For a direct request naming `todo` or `preop`, leave the file to the dev without reading its body.
   - Follow the `## Skills` ticks — the file is the source of truth. Only suggest an addition when something is clearly missing (e.g. vague spec without `grill-with-choice` ticked). Pick names from the host's available skills list; consult skill-navigator only when unsure.
   - Jira status: never assume it — Jira is the source of truth; ask the user to confirm anything status-related.
7. Before work starts: if `## Related files` is empty or incomplete, offer to search the repo and fill it. Skip silently if `## Progress` already records the files.
