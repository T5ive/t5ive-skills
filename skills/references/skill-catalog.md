# Skill Catalog and Routing

Use this reference to distinguish nearby workflows. Check the current host's skill list before recommending or starting an external skill; installed plugins differ between environments.

## T5ive

- `skill-navigator`: choose and run a suitable available skill workflow.
- `skill-guide`: recommend available skills, explain the fit and sequence, and wait for the user's decision.
- `review-with-choice`: show review options, recommend one, and start the user's selection.
- `git-commit`: create a Conventional Commit message in Thai.
- `grill-with-choice` runs Matt's `grilling` skill with host-native selectable answers in each round; it requires that skill in the current host.
- `todo-init`: bootstrap a project's `todo/` task system, including All/Todo/Preop/Mise/WIP/Testing board views and workflow rules.
- `todo-triage`: sort raw `todo/inbox.md` notes into `stage: todo` files; keeps inbox headers.
- `todo-next`: recommend `mise`/`wip` work, list `test` as waiting, and leave `todo`/`preop` content to the dev.
- `todo-audit`: report missing related paths outside `todo`/`preop` and missing done dates.
- `todo-sweep`: archive `status: done` task files into `todo/archive/YYYY-MM/`.
- `todo-parallel`: run unrelated `mise`/`wip` tasks as parallel subagents; commit explicitly selected tasks only after dev tests pass.
- `todo-finish`: close or revert `stage: test` tasks — `status: done` + done date, or back to `wip` with the rejection reason in Progress.

## Matt Pocock v1.2.3

Recommend these only when the Matt plugin is available in the host.

| Need | Skill or workflow |
|---|---|
| Stress-test an idea without project docs | `grill-me` → `grilling` |
| Stress-test a design while updating domain docs | `grill-with-docs` → `grilling` and `domain-modeling`; records vocabulary and decisions in project docs |
| Debug a hard, flaky, or performance issue | `diagnosing-bugs` |
| Review a diff against repo standards and its originating spec | `code-review` |
| Design a deep, testable module | `codebase-design` |
| Find architecture opportunities | `improve-codebase-architecture` |
| Prototype a state model or UI | `prototype` |
| Research a question with cited sources | `research` |
| Turn a conversation into a spec or tickets | `to-spec` → `to-tickets` |
| Implement a spec or ticket | `implement`, with `tdd` as needed |
| Resolve an active merge conflict | `resolving-merge-conflicts` |
| Maintain domain terms and ADRs | `domain-modeling` |
| Prepare a repo for Matt engineering workflows | `setup-matt-pocock-skills` |
| Triage issues and external PRs | `triage` |
| Learn a concept over multiple sessions | `teach` |
| Hand work to a fresh context | `handoff` |

The v1.2.3 release adds secret redaction guidance to `diagnosing-bugs`, makes several subagent-dispatch instructions harness-neutral, and removes time estimates from `wizard`.

## 9arm

Recommend only when the 9arm plugin is available.

- `scrutinize`: outsider review of intent, real code paths, behavior, and claims.
- `debug-mantra`: short debugging discipline—reproduce, trace, falsify, cross-check.
- `post-mortem`: records a validated fix and how it escaped detection.
- `qwen-agent`: delegates suitable mechanical work to the Qwen-backed agent.
- `qwenchance`: helps recover from a long task that is looping or losing direction.
- `management-talk`: rewrites technical updates for engineering leadership.

## Ponytail and Karpathy

- `ponytail`: persistent simplicity and YAGNI mode.
- `ponytail-review`: checks a diff for over-engineering only.
- `ponytail-audit`: scans a whole repo for removable complexity.
- `ponytail-debt`, `ponytail-gain`, and `ponytail-help`: one-shot debt, impact, and command references.
- `karpathy-guidelines`: broad coding heuristics that apply without an explicit invocation.

## Choose by the actual review question

| Review goal | Best fit | Boundary |
|---|---|---|
| Verify intent, trace actual behavior, and challenge claims | 9arm `scrutinize` | Broad outsider review; not limited to a diff's style. |
| Check a fixed diff against repo standards and its spec | Matt `code-review` | Uses two review axes and needs a base point and spec context. |
| Find unnecessary complexity in a diff | Ponytail `ponytail-review` | Complexity-only; not a correctness review. |
| Find removable complexity across a repo | Ponytail `ponytail-audit` | Deletion and simplification, not architecture deepening. |
| Find opportunities to deepen modules | Matt `improve-codebase-architecture` | Architecture direction, not a bloat audit. |

`review-with-choice` presents the available review routes and runs the one the user selects. Its “Scrutinize with finding choices” route runs 9arm `scrutinize`, then asks per finding whether to fix it, skip it, or investigate further. Make no edits until the user selects a finding to fix.

## Other overlaps

- `debug-mantra` and `diagnosing-bugs` both address bugs: use the former for a concise reproduce-and-trace discipline, and the latter for hard, flaky, or performance diagnosis. Use `post-mortem` after a fix is understood and validated.
- `todo-triage` sorts a personal `todo/inbox.md` into task files; Matt's `triage` triages GitHub issues and PRs. Different domains despite the shared word.
- `grill-with-choice` changes how Matt's `grilling` asks each question; it does not create project documentation. Matt's `grill-with-docs` combines `grilling` with `domain-modeling` to capture vocabulary and decisions as `CONTEXT.md`/ADR docs. They are separate wrappers for selectable answers and persistent docs, and can be used together when both are wanted.
- Ponytail actively reduces complexity; Karpathy's guidelines are broader coding heuristics. They can complement each other without being one workflow.
- `skill-guide` recommends and waits. `skill-navigator` selects and acts. `review-with-choice` is the specialized menu for review workflows.
