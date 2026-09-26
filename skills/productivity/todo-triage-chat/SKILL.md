---
name: todo-triage-chat
description: Create a todo task from the current conversation when asked; reuse known details, ask for missing ones, and use Matt's grilling skill when no task context exists.
---

# Todo Triage Chat

Create a todo task from the current conversation when the user explicitly asks. Do not start implementing the task.

## Workflow

1. Resolve the target project and read its `## Todo workflow` in `AGENTS.md`. If `todo/` is missing, tell the user to run `todo-init` first and stop.
2. Review the conversation. Reuse details already given; do not ask the user to repeat them.
   - If it contains a concrete problem or goal, identify only the missing details needed for a useful task: expected outcome or acceptance criteria, scope or constraints, related files/features, desired or relevant skills, and phase when the project uses phases.
   - Batch known missing details into one round. Use the host's native choice UI for genuine option questions; ask for paths or descriptions as concise free-text questions. After the answer, reassess and ask another round only if an essential detail remains unresolved. The user may answer `unknown` or `none` for files or skills; leave those fields empty rather than inventing them. If no usable task context exists, use Matt's `grilling` skill instead of guessing.
3. When context is missing, activate Matt's `grilling` skill and interview the user about what happened and what they want to change. If the skill is unavailable, explain the dependency and stop. Follow its question rounds until the task is clear, then present the task summary—including related files and skills—and wait for the user's confirmation before creating the document.
4. Reuse the task template and folder layout in `../todo-triage/SKILL.md`, but always create a task file for a chat request: bugs go in `bugs/`, other work in `features/` or the explicitly matching `phase-X/`. Do not route it to `misc.md` or `backlog.md`. Inspect only `todo/` task files for duplicates, not project source code. If one open task matches, update it; if added scope belongs to a task at `stage: test`, return it to `stage: wip`. Ask if multiple tasks match. Keep `todo/inbox.md` unchanged.
5. Write the confirmed request and relevant agreed context in `## Raw`; put concrete agreed outcomes in `## Tasks` when useful. Record related paths the user provided under `## Related files`. Select only clearly relevant skills from the task template, ticking `diagnosing-bugs` for a bug. Leave unknown or unselected details blank.
6. Create a new task file with `stage: todo` and today's `created` date. When updating an existing task, keep its current stage except for the `test` → `wip` change above. Report the task path and a short summary.
