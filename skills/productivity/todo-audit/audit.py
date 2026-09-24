#!/usr/bin/env python3
"""todo-audit: report which todo task files are missing metadata. Read-only.

Usage:
    python audit.py [todo-dir] [--checks paths,done-date|all]

Checks:
    paths     ## Related files section is empty outside todo/preop (not
              visible on the board — Bases reads frontmatter only)
    done-date status done and no done date (done files are filtered off the
              board; sweep needs the date to pick the archive folder)

jira/phase are NOT checked — emptiness is visible on the board's columns.
Excludes archive/, .obsidian/, and the list files (inbox.md, backlog.md,
misc.md, jira.md). Unknown check names are an error (exit 2).
"""
import argparse
import re
import sys
from pathlib import Path

KNOWN_CHECKS = {"paths", "done-date"}
LIST_FILES = {"inbox.md", "backlog.md", "misc.md", "jira.md"}


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


def section_body(text, title):
    pat = re.compile(
        r"^##\s+" + re.escape(title) + r"\s*$(.*?)(?=^##\s+|\Z)", re.M | re.S
    )
    m = pat.search(text)
    return m.group(1).strip() if m else ""


def main():
    ap = argparse.ArgumentParser(description="Report todo task files missing metadata.")
    ap.add_argument("todo_dir", nargs="?", default="todo")
    ap.add_argument("--checks", default="all",
                    help="comma list of paths,done-date or all (default)")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if args.checks.strip().lower() == "all":
        selected = None
    else:
        selected = {c.strip() for c in args.checks.split(",") if c.strip()}
        unknown = selected - KNOWN_CHECKS
        if unknown:
            print(f"error: unknown checks: {', '.join(sorted(unknown))}")
            print(f"known checks: {', '.join(sorted(KNOWN_CHECKS))} (or 'all')")
            return 2

    def on(name):
        return selected is None or name in selected

    root = Path(args.todo_dir)
    if not root.is_dir():
        print(f"error: directory not found: {args.todo_dir}")
        return 1

    task_files = []
    no_status = []
    for p in sorted(root.rglob("*.md")):
        parts = {x.lower() for x in p.parts}
        if "archive" in parts or ".obsidian" in parts:
            continue
        if p.name.lower() in LIST_FILES:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if not fm.get("status"):
            no_status.append(p)
            continue
        task_files.append((p, text, fm))

    rows = []
    counts = {}
    for p, text, fm in task_files:
        missing = []
        if on("paths") and fm.get("stage") not in {"todo", "preop"} and not section_body(text, "Related files"):
            missing.append("paths")
        if on("done-date") and fm.get("status") == "done" and not fm.get("done"):
            missing.append("done-date")
        if missing:
            rows.append((p, missing))
            for k in missing:
                counts[k] = counts.get(k, 0) + 1

    print(f"# todo-audit — {args.todo_dir} ({len(task_files)} task files)")
    if rows:
        print()
        print("| File | Missing |")
        print("|---|---|")
        for p, missing in rows:
            print(f"| {p.relative_to(root).as_posix()} | {', '.join(missing)} |")
        print()
        summary = ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
        print(f"Counts — {summary} ({len(rows)} files affected)")
    else:
        print()
        print("All checks passed — nothing missing.")

    if no_status:
        print()
        print("Note — files without a status frontmatter (skipped):")
        for p in no_status:
            print(f"- {p.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
