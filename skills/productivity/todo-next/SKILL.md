---
name: todo-next
description: "Use when the user says \"todo next\", \"หางานถัดไป\", \"มีงานอะไรเหลือ\", \"what should I work on\", or wants a summary of open todo tasks with a recommendation."
---

# Todo Next

Summarize open work and help pick the next task.

Use the user's target project; if none is named, use the current workspace. Scan that project's `todo/`, not a skill source or cache directory.

## Workflow

1. Scan `todo/` (exclude `archive/`) for files with `status: open` in frontmatter. Read each file's frontmatter and its last `## Progress` line.
2. Present a summary table: file, title, phase, type, jira, last progress date.
3. Append a short section listing leftovers: one-liners in `misc.md` and section titles in `backlog.md` — they never appear on the board, so surface them here.
4. Recommend 3–5 next tasks, each with a one-line reason. `stage: todo` means never started — rank it highest; within the same level order by `created`, older first. `stage: wip` means started but unfinished, including rejected rework — read its last `## Progress` line for the rejection reason (the reason lives in the file, never only in chat) and rank it right after `stage: todo`. `stage: test` means the work is done and awaiting Jira's outcome — list it as waiting, don't recommend redoing it. Then prefer: oldest open without recent progress, unblocked, matching the user's stated focus if any.
5. Wait for the user's choice. Do not start work unasked.
6. On choice:
   - If the chosen work is only a line in `misc.md` or a section in `backlog.md`, promote it to a real task file first (todo-triage template), then remove the line/section from its list file. Promotion also happens on direct command — e.g. "promote <topic> from backlog".
   - Read the full task file, then set `stage: wip`.
   - Follow the `## Skills` ticks — the file is the source of truth. Only suggest an addition when something is clearly missing (e.g. vague spec without `grill-with-choice` ticked). Pick names from the host's available skills list; consult skill-navigator only when unsure.
   - Jira status: never assume it — Jira is the source of truth; ask the user to confirm anything status-related.
7. Before work starts: if `## Related files` is empty or incomplete, offer to search the repo and fill it. Skip silently if `## Progress` already records the files.
