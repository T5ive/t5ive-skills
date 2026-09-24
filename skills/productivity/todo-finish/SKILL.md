---
name: todo-finish
description: "Use when the user says \"ปิดงาน test\", \"จบงาน test\", \"mark test done\", \"test ไม่ผ่าน\", \"คืนงาน test\", or asks to close stage: test tasks (status: done + done date) or send them back to wip. Runs only on explicit command."
---

# Todo Finish

Close or revert tasks sitting at `stage: test` — the batch counterpart to editing the board's Testing view by hand.

## Workflow

1. Run the bundled script (relative to this skill's base directory) to list what's waiting:

   ```bash
   python finish.py <todo-dir>
   ```

2. Show the list and wait for the user's pick. Do nothing unasked.
3. Close (`status: done` + `done:` date, today by default) or revert (`stage: wip`, rejected work):

   ```bash
   python finish.py <todo-dir> --done all
   python finish.py <todo-dir> --done features/foo.md --date 2026-09-24
   python finish.py <todo-dir> --revert features/foo.md
   ```

4. On revert, remind the dev to append the rejection reason to the task file's `## Progress` (`- YYYY-MM-DD: Tester ไม่ผ่าน — เพราะ ...`) — todo-next ranks the rework from that line, and chat context does not survive the session.
5. After closing, suggest todo-sweep when the user wants the done files archived.

## Safety

- Only `stage: test` files are touched; anything else is skipped with a reason.
- `--done` additionally requires `status: open` — never re-date an already-done file.
- `done` is date-only `YYYY-MM-DD` (RULES 2) — todo-sweep picks the archive month from it.
- File arguments are relative to the todo dir; unknown names abort before anything is written.
