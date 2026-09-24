---
name: todo-parallel
description: "Use when the user says \"todo parallel\", \"ทำงานหลายงานพร้อมกัน\", \"run these tasks in parallel\", or names 2–3 unrelated todo task files to execute concurrently."
---

# Todo Parallel

Run 2–3 unrelated todo tasks concurrently with separate commits at the end.

Use the user's target project; if none is named, use the current workspace. Resolve task files and code paths under that project root.

## Workflow

1. Collect the chosen task files (from todo-next selection or explicit names).
2. Overlap check: read each file's `## Related files` and expected code areas. A task with an empty related-files section → ask the dev to fill it (or confirm the target files) and wait before spawning. If two tasks touch the same files, warn and run them sequentially instead.
3. Spawn one background subagent per task. Each agent gets:
   - its task file path — read first: `## Raw`, `## Tasks`, `## Skills` ticks
   - the files it may touch
   - HARD RULE: implement only — no commits, no `git add`, no branch/stash; leave changes in the working tree
4. Wait for all agents. Review each task's diff (`git diff -- <paths>`).
5. Append one Progress line per task file (`- YYYY-MM-DD: <what happened>`) and set `stage: test` — work complete, awaiting Jira.
6. Commit separately, one commit per task: `git add <paths of that task>` (include its task file), then commit following the git-commit skill format.
7. Large independent tasks → suggest git worktrees instead (one branch per task, merged later).

## Safety

- The orchestrator is the only one who commits.
- Never merge two tasks into one commit.
- An agent failed → commit the successful tasks, then report the failure with its task file path.
