---
name: todo-sweep
description: "Use when the user says \"เก็บกวาด todo\", \"sweep todo\", \"archive done tasks\", or asks to move finished todo task files into todo/archive/. Runs only on explicit command."
---

# Todo Sweep

Archive done task files in one sweep.

## Workflow

1. Scan `todo/` (exclude `archive/`) for files with `status: done`.
2. Destination per file: `todo/archive/YYYY-MM/` where `YYYY-MM` comes from the file's `done:` field.
3. Show the move list. On confirmation `git mv` each file (create the archive subfolder if needed). Not a git repo → plain move.
4. Propose one commit following the git-commit skill format:

```
chore(🔧todo): เก็บกวาด N ไฟล์ done ลง archive/YYYY-MM
```

## Safety

- Never delete task files.
- Never move a file whose status is not `done`.
- `done:` missing or unparsable → stop for that file and report; never guess the month.
- Nothing to sweep → say so; do not create empty archive folders.
