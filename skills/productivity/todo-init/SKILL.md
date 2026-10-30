---
name: todo-init
description: "Use when the user says \"todo init\", \"set up todo\", \"สร้างระบบ todo\", or wants to bootstrap the todo/ task system in a project. Runs the bundled init.py to create folders, inbox, AGENTS.md rules, .gitignore, _board.base and optional Jira artifacts."
---

# Todo Init

Bootstrap the `todo/` markdown task system in the user's target project; if none is named, use the current workspace. Keep that project root separate from this skill's directory. The deterministic parts run via the bundled `init.py` — idempotent, same output every time.

## Workflow

### 1. Ask once and wait

Use the host's native choice UI when available. If it is unavailable or the call fails, show all questions together as numbered choices in one chat message. Wait for the user's answer before running init; an accepted/pending UI request or silence is not an answer, and defaults are not silently selected.

- Does this project use phases? If yes, which numbers (e.g. `2,3,4`)? Default: no phases → `features/`.
- Is there a legacy notes file to seed the inbox from (e.g. an old `TODO` file)? Ask for the path.
- Create the Obsidian board (`_board.base`)? Default: yes.
- Does this project use Jira? Require an explicit yes/no answer.
- If it uses Jira, create `jira.md` (live JQL via the community Jira Issue plugin)? Default: yes if the user uses that plugin, otherwise no.

### 2. Run the bundled script

Resolve `init.py` from the activated skill's directory. Pass the target project root explicitly. `--from` is resolved from the command's working directory, so pass an absolute path to the legacy file.

```bash
python "<skill-dir>/init.py" "<project-root>" --phases "2,3,4" --from "<project-root>/TODO"
```

Pass `--jira` or `--no-jira-support` from the user's answer. `--no-jira-support` omits the Jira board column, `jira.md`, and Jira workflow rules. If Jira is enabled but the user does not use the community Jira Issue plugin, pass `--no-jira` to skip only `jira.md`. `--no-board` skips the board. The script creates, idempotently:

- `todo/` skeleton: `features/` or `phase-N/` folders (from `--phases`), `bugs/`, `archive/` (empty folders get a `.gitkeep`)
- `todo/inbox.md` with default headers: `## General`, `## Misc`, `## Phase N` (only the chosen phases)
- `todo/backlog.md`, `todo/misc.md`
- `todo/_board.base` — seven tables (Obsidian Bases), all filtered to files that have `status` and `status != "fin"`:
  - **All** — every open task: columns name (title)/stage/type/phase*/created (shown as `DD/MM/YYYY`), plus `jira` only when Jira is enabled and a narrow `file.name` for click-to-open (`phase` only in phase projects), sorted by the raw `created` date (oldest first) → `type` (ASC = bug < feature < refactor, so bugs float up) → `name` (a–z). All stage views share its columns, sort and widths; `phase` appears in every view for phase projects.
  - **Todo** — `stage == "todo"`: newly triaged work waiting for the dev to prepare; AI does not start these tasks.
  - **Preop** — `stage == "preop"`: short-term information or test results the dev is waiting for; AI does not start these tasks.
  - **Mise** — `stage == "mise"`: details prepared by the dev, ready for todo-next or todo-parallel.
  - **WIP** — `stage == "wip"`: work in flight, including Tester-rejected rework — pick it up again via todo-next.
  - **Probe** — `stage == "probe"`: implementation complete, awaiting dev testing. After the dev explicitly confirms their test passed, set `gate` manually or via todo-finish --pass. Automated tests passing alone do not qualify. Rejection returns to `wip` with the reason in `## Progress`.
  - **Gate** — `stage == "gate"`: dev-confirmed pass, awaiting Tester or final acceptance (Jira may also be part of acceptance when enabled). Adds editable `status` and `done` columns after `stage`: rejection returns to `wip` with its reason in Progress; normal acceptance closes by setting the `done` date **first** and `status: fin` second (the row leaves the board the moment status flips), or via todo-finish --done. An explicit todo-finish closure closes eligible Gate tasks regardless of Jira status; a bare invocation means `--done all`.
  Filled-vs-empty is read straight from the values; related-files completeness cannot appear here — Bases reads frontmatter only, that check belongs to todo-audit.
- `todo/jira.md` — created only when Jira is enabled and the user wants the community *Jira Issue* plugin view: one block for all unresolved work of the current user, plus an optional compact per-project table block (`query:` / `columns:` / `limit:`) the user customizes
- `## Todo workflow` rules in `AGENTS.md` (created if missing; skipped if the heading exists) — common rules live in init.py's `RULES`; Jira-specific rules are appended only when Jira is enabled. It includes the destination for user-requested recap: append a dated `## Before / After` report in the task file and reply with a link, unless the user requests another destination. It does not invoke recap automatically.
- `/todo/.obsidian/` line in `.gitignore`

`--from` copies the legacy file **verbatim** — format-agnostic by design: its `##` headers are preserved, content before the first `##` header lands under `## General`. Decoding tries utf-8-sig (UTF-8 with or without BOM) → cp874 → latin-1. A legacy file named TODO/todo that blocks the `todo/` folder is renamed to `todo.imported` after seeding.

### 3. Seed manually instead of `--from` only when

- multiple legacy files must be merged,
- the user wants a selective import (only some sections), or
- the script's import came out garbled.

### 4. No python on the machine → manual fallback

Create the same pieces by hand — the exact contents live as constants in init.py (`INBOX_INTRO`, `BACKLOG`, `MISC`, `JIRA_MD`, `RULES`, `JIRA_RULES`); copy them from there, never from memory. For `_board.base` there is **no constant** — build the YAML from the description in step 2, including the `created_display` formula (`if(created, created.format("DD/MM/YYYY"), "")`) and its `created` display name; sort by raw `created`; include the `jira` column only when Jira is enabled. Never leave `{...}` placeholders in the file.

### 5. Closing summary — after the script, tell the user

- If the board was created: enable the **Bases core plugin** in Obsidian, open `todo/_board.base`, refine columns/sort in its editor. Built-in view types are `table` and `cards` only — never write `type: board` (unknown-view error).
- For an existing project, `init.py` leaves `_board.base`, an existing `## Todo workflow` in `AGENTS.md`, and `todo/jira.md` untouched. Report which pieces were created or skipped; do not rewrite or delete existing rules, views, or Jira files. Keep `backlog.md` as-is.
- If `jira.md` was created: it needs the community **Jira Issue** plugin + auth (Cloud and Server both supported) — and on Jira Cloud enable the **"Use 2025 search api"** toggle in the plugin's Account settings, otherwise `jira-search` blocks fail with `Missing API`. Scope the JQL with `project = KEY` or `sprint in openSprints()` — there is no `board` field in JQL.
- Limitation: entries inside `misc.md`/`backlog.md` are list lines, not files — they never appear on the board; `todo-next` surfaces them instead.
- `todo/` items only land in `misc.md` when they came from a `## Misc` inbox section or the dev said so — never by AI's own judgment.
