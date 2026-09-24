---
name: todo-init
description: "Use when the user says \"todo init\", \"set up todo\", \"สร้างระบบ todo\", or wants to bootstrap the todo/ task system in a project. Runs the bundled init.py to create folders, inbox, AGENTS.md rules, .gitignore, _board.base and jira.md."
---

# Todo Init

Bootstrap the `todo/` markdown task system in the user's target project; if none is named, use the current workspace. Keep that project root separate from this skill's directory. The deterministic parts run via the bundled `init.py` — idempotent, same output every time.

## Workflow

### 1. Ask once and wait

Use the host's native choice UI when available. If it is unavailable or the call fails, show all questions together as numbered choices in one chat message. Wait for the user's answer before running init; an accepted/pending UI request or silence is not an answer, and defaults are not silently selected.

- Does this project use phases? If yes, which numbers (e.g. `2,3,4`)? Default: no phases → `features/`.
- Is there a legacy notes file to seed the inbox from (e.g. an old `TODO` file)? Ask for the path.
- Create the Obsidian board (`_board.base`)? Default: yes.
- Create `jira.md` (live JQL via the community Jira Issue plugin)? Default: yes if the user uses that plugin, otherwise no.

### 2. Run the bundled script

Resolve `init.py` from the activated skill's directory. Pass the target project root explicitly. `--from` is resolved from the command's working directory, so pass an absolute path to the legacy file.

```bash
python "<skill-dir>/init.py" "<project-root>" --phases "2,3,4" --from "<project-root>/TODO"
```

All flags optional. Pass `--no-board` / `--no-jira` for anything declined in step 1. The script creates, idempotently:

- `todo/` skeleton: `features/` or `phase-N/` folders (from `--phases`), `bugs/`, `archive/` (empty folders get a `.gitkeep`)
- `todo/inbox.md` with default headers: `## General`, `## Misc`, `## Phase N` (only the chosen phases)
- `todo/backlog.md`, `todo/misc.md`
- `todo/_board.base` — six tables (Obsidian Bases), all filtered to files that have `status` and `status != "done"`:
  - **All** — every open task: columns name (title)/stage/type/phase*/created/jira + a narrow `file.name` for click-to-open (`phase` only in phase projects), sorted by `created` (oldest first) → `type` (ASC = bug < feature < refactor, so bugs float up) → `name` (a–z).
  - **Todo** — `stage == "todo"`: newly triaged work waiting for the dev to prepare; AI does not start these tasks.
  - **Preop** — `stage == "preop"`: short-term information or test results the dev is waiting for; AI does not start these tasks.
  - **Mise** — `stage == "mise"`: details prepared by the dev, ready for todo-next or todo-parallel.
  - **WIP** — `stage == "wip"`: work in flight, including Tester-rejected rework — pick it up again via todo-next.
  - **Testing** — `stage == "test"`: complete, awaiting dev test, Jira, or Tester. Columns stage/status/done are editable inline in the table: revert stage to `wip` on rejection and record the reason in `## Progress`, or close by setting the `done` date **first** and `status: done` second (the row leaves the board the moment status flips) — or close in one command with todo-finish.
  Filled-vs-empty is read straight from the values; related-files completeness cannot appear here — Bases reads frontmatter only, that check belongs to todo-audit.
- `todo/jira.md` — live JQL via the community *Jira Issue* plugin: one block for all unresolved work of the current user, plus an optional compact per-project table block (`query:` / `columns:` / `limit:`) the user customizes
- `## Todo workflow` rules in `AGENTS.md` (created if missing; skipped if the heading exists) — the rules text lives in init.py's `RULES` constant, single source of truth
- `/todo/.obsidian/` line in `.gitignore`

`--from` copies the legacy file **verbatim** — format-agnostic by design: its `##` headers are preserved, content before the first `##` header lands under `## General`. Decoding tries utf-8-sig (UTF-8 with or without BOM) → cp874 → latin-1. A legacy file named TODO/todo that blocks the `todo/` folder is renamed to `todo.imported` after seeding.

### 3. Seed manually instead of `--from` only when

- multiple legacy files must be merged,
- the user wants a selective import (only some sections), or
- the script's import came out garbled.

### 4. No python on the machine → manual fallback

Create the same pieces by hand — the exact contents live as constants in init.py (`INBOX_INTRO`, `BACKLOG`, `MISC`, `JIRA_MD`, `RULES`); copy them from there, never from memory. For `_board.base` there is **no constant** — build the YAML from the description in step 2 (six tables: the shared `status != "done"` filter, per-view `filters` pinning Todo/Preop/Mise/WIP/Testing to one stage, plus `order` + `sort` + `columnSize`). Never leave `{...}` placeholders in the file.

### 5. Closing summary — after the script, tell the user

- If the board was created: enable the **Bases core plugin** in Obsidian, open `todo/_board.base`, refine columns/sort in its editor. Built-in view types are `table` and `cards` only — never write `type: board` (unknown-view error).
- For an existing project, `init.py` leaves `_board.base` and an existing `## Todo workflow` in `AGENTS.md` untouched. Add the Todo view by hand using another stage view as a model and `stage == "todo"`; update any missing Preop/Mise views and stage rules (1 and 3) from `RULES` in `init.py`, then classify existing `todo` files as `todo`, `preop`, or `mise`. Keep `backlog.md` as-is.
- If `jira.md` was created: it needs the community **Jira Issue** plugin + auth (Cloud and Server both supported) — and on Jira Cloud enable the **"Use 2025 search api"** toggle in the plugin's Account settings, otherwise `jira-search` blocks fail with `Missing API`. Scope the JQL with `project = KEY` or `sprint in openSprints()` — there is no `board` field in JQL.
- Limitation: entries inside `misc.md`/`backlog.md` are list lines, not files — they never appear on the board; `todo-next` surfaces them instead.
- `todo/` items only land in `misc.md` when they came from a `## Misc` inbox section or the dev said so — never by AI's own judgment.
