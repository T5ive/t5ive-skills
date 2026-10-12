#!/usr/bin/env python3
"""todo-finish: record dev-test passes, close, or revert Probe/Gate tasks.

Usage:
    python finish.py [todo-dir]                          # list open Probe/Gate tasks
    python finish.py [todo-dir] --pass FILE [FILE ...]   # probe -> gate
    python finish.py [todo-dir] --pass all
    python finish.py [todo-dir] --done FILE [FILE ...]   # status: fin + done: <today>
    python finish.py [todo-dir] --done all [--date YYYY-MM-DD]
    python finish.py [todo-dir] --revert FILE [FILE ...] # stage: back to wip
    python finish.py [todo-dir] --revert all

All actions require status: open. --pass touches only probe, --done only gate,
and --revert probe or gate. The done date is date-only YYYY-MM-DD; sweep uses
its month. Other tasks are skipped with a reason. Unknown file names abort
before anything is written. The skill appends Progress after successful actions.
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
            with path.open(encoding=enc, newline="") as fh:
                return fh.read()
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
        description="Record dev-test passes, close, or revert Probe/Gate tasks in todo/.")
    ap.add_argument("todo_dir", nargs="?", default="todo")
    action = ap.add_mutually_exclusive_group()
    action.add_argument("--pass", dest="passed", nargs="+", metavar="FILE",
                        help="dev-confirmed passes — probe to gate; or 'all'")
    action.add_argument("--done", nargs="+", metavar="FILE",
                        help="gate tasks to close — status: fin + done date; or 'all'")
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

    def expand(names, label, stages):
        if any(n.lower() == "all" for n in names):
            if len(names) > 1:
                print(f"error: --{label}: 'all' cannot be combined with file names")
                return None
            return [k for k, (_, _, _, fm) in tasks.items()
                    if fm.get("status") == "open" and fm.get("stage") in stages]
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

    if not args.passed and not args.done and not args.revert:
        waiting = [(rel, fm) for _, rel, _, fm in tasks.values()
                   if fm.get("status") == "open" and fm.get("stage") in {"probe", "gate"}]
        print(f"# todo-finish — {args.todo_dir} ({len(waiting)} open at probe/gate)")
        if waiting:
            print()
            print("| File | name | stage | jira | created | status |")
            print("|---|---|---|---|---|---|")
            for rel, fm in waiting:
                print(f"| {rel} | {fm.get('name', '')} | {fm.get('stage', '')} | {fm.get('jira', '')} "
                      f"| {fm.get('created', '')} | {fm.get('status', '')} |")
            print()
            print("Dev passed: --pass all | --pass <file>    "
                  "Close: --done all | --done <file> [--date YYYY-MM-DD]    "
                  "Revert: --revert <file>")
        else:
            print()
            print("Nothing open at probe/gate.")
        return 0

    if args.passed:
        label, names, stages = "pass", args.passed, {"probe"}
        updates = {"stage": "gate"}
        result = "passed"
        detail = "stage: gate — append dev-test confirmation to ## Progress"
    elif args.done:
        label, names, stages = "done", args.done, {"gate"}
        updates = {"status": "fin", "done": done_date}
        result = "fin"
        detail = f"done: {done_date}"
    else:
        label, names, stages = "revert", args.revert, {"probe", "gate"}
        updates = {"stage": "wip"}
        result = "reverted"
        detail = "stage: wip — append the rejection reason to ## Progress"

    keys = expand(names, label, stages)
    if keys is None:
        return 2

    print(f"# todo-finish — {args.todo_dir}")
    changed = 0
    if not keys:
        print(f"= nothing eligible for --{label}")
    for k in keys:
        p, rel, text, fm = tasks[k]
        if fm.get("status") != "open":
            print(f"= skipped: {rel} (status={fm.get('status')}, requires open)")
            continue
        if fm.get("stage") not in stages:
            print(f"= skipped: {rel} (stage={fm.get('stage') or '?'}, requires {'/'.join(sorted(stages))})")
            continue
        out = update_frontmatter(text, updates)
        if out is None:
            print(f"= skipped: {rel} (no parseable frontmatter)")
            continue
        write_text_exact(p, out)
        print(f"+ {result}: {rel} ({detail})")
        changed += 1
    if changed:
        print(f"{changed} file(s) changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
