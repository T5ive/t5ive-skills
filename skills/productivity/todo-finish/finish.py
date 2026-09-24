#!/usr/bin/env python3
"""todo-finish: close or revert tasks sitting at stage: test.

Usage:
    python finish.py [todo-dir]                          # list stage: test tasks
    python finish.py [todo-dir] --done FILE [FILE ...]   # status: done + done: <today>
    python finish.py [todo-dir] --done all [--date YYYY-MM-DD]
    python finish.py [todo-dir] --revert FILE [FILE ...] # stage: back to wip
    python finish.py [todo-dir] --revert all

--done touches only stage: test + status: open files (RULES 2: the done date is
date-only YYYY-MM-DD — sweep picks the archive month from it). --revert touches
only stage: test files (RULES 3: rejected work goes back to wip). Anything else
is skipped with a reason; unknown file names abort before anything is written.
Excludes archive/, .obsidian/, and the list files (inbox.md, backlog.md,
misc.md, jira.md). Exit codes: 0 ok, 1 todo dir not found, 2 usage error.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

LIST_FILES = {"inbox.md", "backlog.md", "misc.md", "jira.md"}
ENCODINGS = ("utf-8-sig", "cp874", "latin-1")


def read_text_guess(path):
    for enc in ENCODINGS:
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text):
    fm = {}
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            value = m.group(2).split("#", 1)[0].strip().strip('"').strip("'")
            fm[m.group(1)] = value
    return fm


def line_terminator(line):
    return line[len(line.rstrip("\r\n")):]


def update_frontmatter(text, updates):
    """Set frontmatter keys; the body and every other line stay byte-identical.
    Missing keys are inserted right after the status line. Returns None when the
    file has no parseable frontmatter block."""
    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].lstrip("\ufeff").startswith("---"):
        return None
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None
    found = {}
    for i in range(1, end):
        m = re.match(r"^([A-Za-z_-]+):", lines[i])
        if m and m.group(1) in updates:
            found[m.group(1)] = i
    for key, i in found.items():
        lines[i] = f"{key}: {updates[key]}{line_terminator(lines[i])}"
    anchor = found.get("status", 0)
    term = line_terminator(lines[anchor]) or "\n"
    for key in updates:
        if key not in found:
            lines.insert(anchor + 1, f"{key}: {updates[key]}{term}")
            anchor += 1
    return "".join(lines)


def write_text_exact(path, text):
    # newline="" so LF files stay LF instead of being rewritten to CRLF on Windows.
    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def main():
    ap = argparse.ArgumentParser(
        description="Close or revert stage: test tasks in todo/.")
    ap.add_argument("todo_dir", nargs="?", default="todo")
    action = ap.add_mutually_exclusive_group()
    action.add_argument("--done", nargs="+", metavar="FILE",
                        help="task file(s) to close — status: done + done date; or 'all'")
    action.add_argument("--revert", nargs="+", metavar="FILE",
                        help="task file(s) back to stage: wip (rejected work); or 'all'")
    ap.add_argument("--date", default=None, metavar="YYYY-MM-DD",
                    help="done date override (default: today)")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    done_date = args.date or date.today().isoformat()
    if args.date:
        try:
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", args.date):
                raise ValueError("format")
            date.fromisoformat(args.date)
        except ValueError:
            print(f"error: --date must be a valid YYYY-MM-DD date, got: {args.date}")
            return 2

    root = Path(args.todo_dir)
    if not root.is_dir():
        print(f"error: directory not found: {args.todo_dir}")
        return 1

    tasks = {}
    for p in sorted(root.rglob("*.md")):
        parts = {x.lower() for x in p.parts}
        if "archive" in parts or ".obsidian" in parts:
            continue
        if p.name.lower() in LIST_FILES:
            continue
        text = read_text_guess(p)
        fm = parse_frontmatter(text)
        if not fm.get("status"):
            continue
        rel = p.relative_to(root).as_posix()
        tasks[rel.lower()] = (p, rel, text, fm)

    def expand(names, label):
        if any(n.lower() == "all" for n in names):
            if len(names) > 1:
                print(f"error: --{label}: 'all' cannot be combined with file names")
                return None
            return [k for k, (_, _, _, fm) in tasks.items() if fm.get("stage") == "test"]
        keys = []
        for name in names:
            n = name.replace("\\", "/")
            if n.startswith("./"):
                n = n[2:]
            if not n.endswith(".md"):
                n += ".md"
            if n.lower() in tasks:
                keys.append(n.lower())
            else:
                print(f"error: --{label}: no task file matches {name} (inside {args.todo_dir})")
                return None
        return keys

    if not args.done and not args.revert:
        in_test = [(rel, fm) for _, rel, _, fm in tasks.values()
                   if fm.get("stage") == "test"]
        print(f"# todo-finish — {args.todo_dir} ({len(in_test)} at stage: test)")
        if in_test:
            print()
            print("| File | name | jira | created | status |")
            print("|---|---|---|---|---|")
            for rel, fm in in_test:
                print(f"| {rel} | {fm.get('name', '')} | {fm.get('jira', '')} "
                      f"| {fm.get('created', '')} | {fm.get('status', '')} |")
            print()
            print("Close: --done all | --done <file> [--date YYYY-MM-DD]    "
                  "Revert: --revert <file>")
        else:
            print()
            print("Nothing at stage: test.")
        return 0

    done_keys = expand(args.done, "done") if args.done else []
    if args.done and done_keys is None:
        return 2
    revert_keys = expand(args.revert, "revert") if args.revert else []
    if args.revert and revert_keys is None:
        return 2

    print(f"# todo-finish — {args.todo_dir}")
    changed = 0
    if args.done:
        if not done_keys:
            print("= nothing at stage: test to close")
        else:
            print(f"done date: {done_date}")
        for k in done_keys:
            p, rel, text, fm = tasks[k]
            if fm.get("stage") != "test":
                print(f"= skipped: {rel} (stage={fm.get('stage') or '?'}, not test)")
                continue
            if fm.get("status") != "open":
                print(f"= skipped: {rel} (already {fm.get('status')})")
                continue
            out = update_frontmatter(text, {"status": "done", "done": done_date})
            if out is None:
                print(f"= skipped: {rel} (no parseable frontmatter)")
                continue
            write_text_exact(p, out)
            print(f"+ done: {rel} (done: {done_date})")
            changed += 1
    if args.revert:
        if not revert_keys:
            print("= nothing at stage: test to revert")
        for k in revert_keys:
            p, rel, text, fm = tasks[k]
            if fm.get("stage") != "test":
                print(f"= skipped: {rel} (stage={fm.get('stage') or '?'}, not test)")
                continue
            if fm.get("status") != "open":
                print(f"= skipped: {rel} (already {fm.get('status')} — reopening a done file is out of scope)")
                continue
            out = update_frontmatter(text, {"stage": "wip"})
            if out is None:
                print(f"= skipped: {rel} (no parseable frontmatter)")
                continue
            write_text_exact(p, out)
            print(f"+ reverted: {rel} (stage: wip — append the rejection reason to ## Progress)")
            changed += 1
    if changed:
        print(f"{changed} file(s) changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
