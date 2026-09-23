---
name: todo-audit
description: "Use when the user says \"todo audit\", \"ไฟล์ไหนยังไม่มีไฟล์ที่เกี่ยวข้อง\", or wants a report of todo task files missing metadata. Read-only."
---

# Todo Audit

Report which task files are missing which data. Read-only — change nothing.

## Checks

Only what the board cannot show. jira/phase emptiness is visible on the board's columns — not audited.

| Key | Argument | Flag a file when |
|---|---|---|
| Related paths | `paths` | `## Related files` is empty (Bases reads frontmatter only, so this never appears on the board) |
| Done date | `done-date` | `status: done` and `done:` is empty (done files are filtered off the board, and sweep needs the date) |

## Workflow

1. Determine the checks: from the command if specified (`paths`, `done-date`, combinable; `all` = everything). If unspecified, ask once with multi-select choices.
2. Scan `todo/` (exclude `archive/`): read the frontmatter and the `## Related files` section of every task file. Do not scan the codebase.
3. Report one table: file → missing items. End with counts per check.
4. Suggest fixes (e.g. "ask BA for missing tickets", "fill paths before starting work") but edit nothing.
