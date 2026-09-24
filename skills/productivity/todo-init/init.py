#!/usr/bin/env python3
"""todo-init: bootstrap the todo/ task system in a project. Idempotent.

Usage:
    python init.py [project-root] [--phases "2,3,4"] [--from legacy-notes-file]

Creates the todo/ skeleton (features/ or phase-N/ folders, bugs/, archive/),
inbox.md with default headers (General, Misc, Phase N), backlog.md, misc.md,
_board.base (starter Obsidian Bases config) and jira.md (live JQL list via
the community Jira Issue plugin); appends the Todo workflow rules to AGENTS.md
(created if missing, skipped if the section exists); ensures /todo/.obsidian/
is gitignored. --from seeds inbox.md with an existing notes file verbatim
(its ## headers are preserved; header-less content lands under ## General).
Reports created vs skipped for every piece.
"""
import argparse
import os
import re
import sys
from pathlib import Path

RULES = """## Todo workflow

Task files live in `todo/` — 1 file = 1 feature/bug/refactor, kebab-case English filename, short title (Thai or English) in the `name` property (no `#` heading needed).

1. Jira is the only source of truth for acceptance. Files use `status: open|done` and `stage: todo|wip|test` (dev-side workflow) — never mirror Jira's InProgress/Test into the file.
2. Set `status: done` + `done: YYYY-MM-DD` when Jira reaches Done, or when the user declares a ticket-less task finished.
3. Set `stage: wip` when work starts, `stage: test` when a session ends with the work complete, back to `wip` for fixing rejected work.
4. Never delete or move task files. Archiving happens only via the sweep command.
5. Read the task file before starting work on it.
6. When starting work, fill `## Related files` if the user left it empty or incomplete; skip if `## Progress` already records the files.
7. At the end of a work session append one line to the task file: `- YYYY-MM-DD: <what happened>` (append only).
8. When a Jira ticket is created for this task, set `jira: JIRA:KEY-123` (Jira Issue plugin inline format).
9. Customer change requests are `type: feature`: append to the still-open original feature file; create a new file only if the original is done or archived.
"""

INBOX_INTRO = """# Inbox

"""

BACKLOG = """# Backlog

Wait / low priority
"""

MISC = """# Misc

Misc / questions / remarks
"""

def stage_view(name: str, stage: str) -> str:
    """One table view pinned to a single stage. Columns stage/status/done are on
    purpose — Obsidian Bases tables edit them inline, so rejected work goes back
    to wip and finished work gets its done date without opening the file."""
    return (
        "  - type: table\n"
        f"    name: {name}\n"
        "    filters:\n"
        "      and:\n"
        f'        - stage == "{stage}"\n'
        "    order:\n"
        "      - name\n"
        "      - stage\n"
        "      - status\n"
        "      - done\n"
        "      - jira\n"
        "      - created\n"
        "      - file.name\n"
        "    sort:\n"
        "      - property: created\n"
        "        direction: ASC\n"
    )


def board_yaml(with_phase: bool) -> str:
    """Build the _board.base content. No placeholders — the returned string is final."""
    phase_col = "      - phase\n" if with_phase else ""
    return (
        "filters:\n"
        "  and:\n"
        '    - file.hasProperty("status")\n'
        '    - status != "done"\n'
        "views:\n"
        "  - type: table\n"
        "    name: All\n"
        "    order:\n"
        "      - name\n"
        "      - stage\n"
        "      - type\n"
        + phase_col +
        "      - created\n"
        "      - jira\n"
        "      - file.name\n"
        "    sort:\n"
        "      - property: created\n"
        "        direction: ASC\n"
        "      - property: type\n"
        "        direction: ASC\n"
        "      - property: name\n"
        "        direction: ASC\n"
        "    columnSize:\n"
        "      note.type: 94\n"
        "      file.name: 120\n"
        + stage_view("WIP", "wip")
        + stage_view("Testing", "test")
    )

JIRA_MD = """# Jira — Open Work

Live list via the community "Jira Issue" plugin — set auth once in plugin settings.
(If you hit `Search error: Missing API`, enable "Use 2025 search api" in the plugin's Account settings.)

## All projects

```jira-search
resolution = Unresolved AND assignee = currentUser() order by updated ASC
```

## Per project (compact table — replace 'project name')

```jira-search
query: status != 'done' AND assignee = currentUser() AND project = 'project name' order by updated ASC
columns: KEY, SUMMARY, UPDATED, STATUS
limit: 20
```

Scope with JQL e.g. `project = YF AND ...` or `sprint in openSprints()` (JQL has no "board" field).
"""

ENCODINGS = ("utf-8-sig", "cp874", "latin-1")


def read_text_guess(path):
    for enc in ENCODINGS:
        try:
            return path.read_text(encoding=enc), enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return path.read_text(encoding="utf-8", errors="replace"), "utf-8?replace"


def main():
    ap = argparse.ArgumentParser(description="Bootstrap the todo/ task system.")
    ap.add_argument("root", nargs="?", default=".", help="project root (default: cwd)")
    ap.add_argument("--phases", default="", help='comma list, e.g. "2,3,4"')
    ap.add_argument("--from", dest="from_file", default=None,
                    help="legacy notes file to seed inbox.md verbatim")
    ap.add_argument("--no-board", action="store_true",
                    help="skip creating todo/_board.base")
    ap.add_argument("--no-jira", action="store_true",
                    help="skip creating todo/jira.md")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: project root not found: {root}")
        return 1

    phases = [p.strip() for p in args.phases.split(",")] if args.phases else []
    if any(not re.fullmatch(r"[0-9]+", p) for p in phases):
        ap.error("--phases must be comma-separated ASCII numbers, e.g. 2,3")
    created, skipped = [], []

    def note(done, msg):
        (created if done else skipped).append(msg)

    # --- read the legacy file early (before touching todo/) ------------------
    todo_root = root / "todo"
    legacy, legacy_enc = "", None
    if args.from_file:
        src = Path(args.from_file)
        if not src.is_file():
            print(f"error: --from file not found: {src}")
            return 1
        legacy, legacy_enc = read_text_guess(src)

    # On case-insensitive filesystems (Windows/NTFS, macOS/APFS) a legacy file
    # named TODO/todo at the root blocks creating the todo/ folder.
    if todo_root.exists() and not todo_root.is_dir():
        same = False
        if args.from_file:
            try:
                same = os.path.samefile(Path(args.from_file), todo_root)
            except OSError:
                same = False
        if same:
            backup = todo_root.with_name(todo_root.name + ".imported")
            n = 2
            while backup.exists():
                backup = todo_root.with_name(f"{todo_root.name}.imported-{n}")
                n += 1
            todo_root.rename(backup)
            note(True, f"file renamed: {todo_root.name} -> {backup.name} "
                       "(content seeded into inbox; safe to delete later)")
        else:
            print(f"error: a file named '{todo_root.name}' exists at the project root and blocks the todo/ folder.")
            print("       pass it as --from (it is renamed to .imported after seeding) or rename/remove it manually.")
            return 1

    # --- folders -----------------------------------------------------------
    task_dirs = [root / "todo" / f"phase-{p}" for p in phases] or [root / "todo" / "features"]
    if (root / "todo").is_dir():
        stray = sorted(d.name for d in (root / "todo").iterdir()
                       if d.is_dir() and d.name not in {"bugs", "archive"}
                       and d.name not in {x.name for x in task_dirs})
        if stray:
            print(f"warning: existing task folders {stray} do not match the requested layout — left in place, clean up manually if unintended.")
    for d in [*task_dirs, root / "todo" / "bugs", root / "todo" / "archive"]:
        if d.exists():
            note(False, f"dir  exists: {d.relative_to(root).as_posix()}")
        else:
            d.mkdir(parents=True)
            (d / ".gitkeep").write_text("", encoding="utf-8")
            note(True, f"dir  created: {d.relative_to(root).as_posix()}")

    # --- inbox -------------------------------------------------------------
    inbox = root / "todo" / "inbox.md"
    misc_in_legacy = bool(re.search(r"^##\s+Misc\s*$", legacy, re.M))
    parts = [INBOX_INTRO, "\n## General\n"]
    if legacy:
        parts.append("\n" + legacy.strip() + "\n")
    if not misc_in_legacy:
        parts.append("\n## Misc\n")
    for p in phases:
        pat = re.compile(rf"^##\s+Phase\s+{re.escape(p)}\s*$", re.M)
        if not pat.search(legacy):
            parts.append(f"\n## Phase {p}\n")

    if inbox.exists():
        note(False, "file exists: todo/inbox.md (left untouched)")
    else:
        inbox.parent.mkdir(parents=True, exist_ok=True)
        inbox.write_text("".join(parts), encoding="utf-8")
        seed = f" + seeded {len(legacy.splitlines())} lines from {args.from_file}" if legacy else ""
        enc = f" (decoded as {legacy_enc})" if legacy_enc else ""
        note(True, f"file created: todo/inbox.md{seed}{enc}")

    # --- list files --------------------------------------------------------
    for name, content in (("backlog.md", BACKLOG), ("misc.md", MISC)):
        f = root / "todo" / name
        if f.exists():
            note(False, f"file exists: todo/{name} (left untouched)")
        else:
            f.write_text(content, encoding="utf-8")
            note(True, f"file created: todo/{name}")

    # --- dashboards -----------------------------------------------------------
    if args.no_board:
        note(False, "board skipped (--no-board)")
    else:
        board = root / "todo" / "_board.base"
        if board.exists():
            note(False, "file exists: todo/_board.base (left untouched)")
        else:
            board.write_text(board_yaml(bool(phases)), encoding="utf-8")
            note(True, "file created: todo/_board.base (enable the Bases core plugin, refine in its editor)")

    if args.no_jira:
        note(False, "jira.md skipped (--no-jira)")
    else:
        jira_md = root / "todo" / "jira.md"
        if jira_md.exists():
            note(False, "file exists: todo/jira.md (left untouched)")
        else:
            jira_md.write_text(JIRA_MD, encoding="utf-8")
            note(True, "file created: todo/jira.md (needs the community Jira Issue plugin + auth)")

    # --- AGENTS.md -----------------------------------------------------------
    agents = root / "AGENTS.md"
    if agents.exists() and "## Todo workflow" in agents.read_text(encoding="utf-8", errors="replace"):
        note(False, "AGENTS.md already has a Todo workflow section (skipped)")
    else:
        with agents.open("a", encoding="utf-8") as fh:
            if agents.exists() and agents.stat().st_size > 0:
                fh.write("\n\n")
            fh.write(RULES)
        note(True, "rules appended: AGENTS.md -> ## Todo workflow")

    # --- .gitignore ----------------------------------------------------------
    gi = root / ".gitignore"
    line = "/todo/.obsidian/"
    current = gi.read_text(encoding="utf-8", errors="replace") if gi.exists() else ""
    if line in current.splitlines():
        note(False, ".gitignore already ignores /todo/.obsidian/")
    else:
        with gi.open("a", encoding="utf-8") as fh:
            if current and not current.endswith("\n"):
                fh.write("\n")
            fh.write(line + "\n")
        note(True, ".gitignore updated: /todo/.obsidian/")

    print(f"# todo-init — {root.resolve()}")
    print(f"layout: {'phase folders ' + ', '.join(phases) if phases else 'features/ (default)'}")
    for m in created:
        print(f"  + {m}")
    for m in skipped:
        print(f"  = {m}")
    nxt = ["run todo-triage on the inbox"]
    if not args.no_board:
        nxt.append("open todo/_board.base in Obsidian (enable the Bases core plugin) and refine in its editor")
    print("Next: " + "; ".join(nxt) + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
