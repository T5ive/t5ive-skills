---
name: todo-finish
description: "Use when the user says \"ปิดงาน test\", \"จบงาน test\", \"mark test done\", \"test ไม่ผ่าน\", \"คืนงาน test\", or asks to close stage: test tasks (status: done + done date) or send them back to wip. Runs only on explicit command."
---

# Todo Finish

Close or revert tasks sitting at `stage: test` — the batch counterpart to editing the board's Testing view by hand.

Use the user's target project; if none is named, use the current workspace. Resolve its `todo/` separately from this skill's directory.

## Workflow

1. Resolve `finish.py` from the activated skill's directory and pass the target project's absolute `todo/` path to list what's waiting:

   ```bash
   python "<skill-dir>/finish.py" "<project-root>/todo"
   ```

2. If the user already named the task, use it. Otherwise show the list and wait for the user's pick. Do nothing unasked.
3. Close (`status: done` + `done:` date, today by default) or revert (`stage: wip`, rejected work):

   ```bash
   python "<skill-dir>/finish.py" "<project-root>/todo" --done all
   python "<skill-dir>/finish.py" "<project-root>/todo" --done features/foo.md --date 2026-09-24
   python "<skill-dir>/finish.py" "<project-root>/todo" --revert features/foo.md
   ```

4. On revert, append the supplied rejection reason to the task file's `## Progress` (`- YYYY-MM-DD: Tester ไม่ผ่าน — เพราะ ...`) in the same turn. If no reason was supplied, ask the dev for it before reverting; todo-next reads the reason from the file, not chat history.
5. After closing, suggest todo-sweep when the user wants the done files archived.

## Safety

- Only `stage: test` files are touched; anything else is skipped with a reason.
- `--done` additionally requires `status: open` — never re-date an already-done file.
- `done` is date-only `YYYY-MM-DD` (RULES 2) — todo-sweep picks the archive month from it.
- File arguments are relative to the todo dir; unknown names abort before anything is written.
