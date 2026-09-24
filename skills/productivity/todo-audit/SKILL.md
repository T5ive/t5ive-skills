---
name: todo-audit
description: "Use when the user says \"todo audit\", \"ไฟล์ไหนยังไม่มีไฟล์ที่เกี่ยวข้อง\", or wants a report of todo task files missing metadata. Read-only."
---

# Todo Audit

Report which task files are missing which data. Read-only — change nothing.

Use the user's target project; if none is named, use the current workspace. Resolve `todo/` under that project root, not under this skill's directory.

## Checks

Only what the board cannot show. jira/phase emptiness is visible on the board's columns — not audited.

| Key | Argument | Flag a file when |
|---|---|---|
| Related paths | `paths` | `## Related files` is empty and `stage` is neither `todo` nor `preop` (dev is still preparing those files) |
| Done date | `done-date` | `status: done` and `done:` is empty (done files are filtered off the board, and sweep needs the date) |

## Workflow

1. Determine the checks from the command if specified (`paths`, `done-date`, combinable; `all` = everything). If unspecified, ask once with multi-select choices: `paths`, `done-date`, or both. Use native choice UI when available; otherwise show numbered choices in chat. Wait for the answer before scanning; an accepted/pending UI request or silence is not a selection.
2. Resolve `audit.py` from the activated skill's directory and run it against the target project's absolute `todo/` path. Pass the selected checks with `--checks`; use `all` for both. If Python is unavailable, do the same read-only scan manually. Exclude `archive/`; read each task file's frontmatter and `## Related files` section only. Do not scan the codebase.
3. Report one table: file → missing items. End with counts per check.
4. Suggest fixes (e.g. "ask for the missing ticket links", "fill paths before starting work") but edit nothing.

```bash
python "<skill-dir>/audit.py" "<project-root>/todo" --checks paths,done-date
```
