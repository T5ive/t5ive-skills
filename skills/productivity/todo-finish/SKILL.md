---
name: todo-finish
description: "Record dev-test passes, close Gate tasks (a bare invocation closes all eligible Gate tasks), or return Probe/Gate tasks to WIP. Use when the user says \"dev test ผ่าน\", \"ปิดงาน\", \"จบงาน\", \"mark task done\", \"test ไม่ผ่าน\", or \"คืนงาน\". Runs only on explicit command."
---

# Todo Finish

Record a dev-confirmed pass (`probe → gate`), close Gate tasks (`status: fin`), or return rejected Probe/Gate work to WIP. A bare invocation closes all eligible open Gate tasks. The same actions can be done manually in the board.

Use the user's target project; if none is named, use the current workspace. Resolve its `todo/` separately from this skill's directory.

## Workflow

1. Resolve `finish.py` from the activated skill's directory and use the target project's absolute `todo/` path. If the user invokes `todo-finish` without an action or file, treat it as `--done all` and run it directly; do not list tasks or ask for an action, selection, or Jira status. This is the user's instruction to close all eligible Gate tasks, including Jira-linked tasks regardless of Jira status.

   ```bash
   python "<skill-dir>/finish.py" "<project-root>/todo" --done all
   ```

2. For a request that specifies an action or file but leaves the other missing, list open Probe/Gate tasks and ask only for the missing selection:

   ```bash
   python "<skill-dir>/finish.py" "<project-root>/todo"
   ```

   Use a blocking native question tool when available; otherwise ask in chat and stop dependent work. Wait for an explicit answer; silence, a pending request, or an empty reply is not a selection. For rejection, obtain the reason before running the command.
3. Run exactly one action. A dev pass requires the dev's explicit confirmation; automated tests passing alone do not qualify. An explicit `--done` request or a bare invocation authorizes closure of the selected eligible Gate tasks, including Jira-linked tasks; do not ask for Jira status.

   ```bash
   python "<skill-dir>/finish.py" "<project-root>/todo" --pass features/foo.md
   python "<skill-dir>/finish.py" "<project-root>/todo" --pass all
   python "<skill-dir>/finish.py" "<project-root>/todo" --done all
   python "<skill-dir>/finish.py" "<project-root>/todo" --done features/foo.md --date 2026-09-24
   python "<skill-dir>/finish.py" "<project-root>/todo" --revert features/foo.md
   ```

4. After each successful change (not skipped files), append a dated line to that task's `## Progress` using the session's local date. Pass: `Dev test ผ่าน — probe → gate`; close: `ปิดงาน — status: fin` with the user's closure instruction; revert: the supplied rejection reason. Preserve previous entries. The script changes frontmatter only; this skill owns the Progress append in the same turn.
5. Report changed and skipped files. After closing, suggest todo-sweep when the user wants the closed files archived.

## Safety

- All actions require `status: open`. `--pass` accepts only `probe`; `--done` only `gate`; `--revert` either. Anything else is skipped with a reason; closed files keep their date and stage.
- `--done` sets `status: fin` and `done:` (today unless supplied), keeping the stage unchanged. On the board, set the date before setting `status: fin`, because the row then disappears.
- `done` remains date-only `YYYY-MM-DD` (RULES 2) — todo-sweep picks the archive month from it.
- File arguments are relative to the todo dir; unknown names abort before anything is written. Every action supports multiple names or `all` (only eligible open tasks); `all` cannot be mixed with names. Actions are mutually exclusive.
