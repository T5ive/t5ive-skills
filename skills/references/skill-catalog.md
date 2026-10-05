# Skill Catalog and Routing

Use this reference to distinguish nearby workflows. Check the current host's skill list before recommending or starting an external skill; installed plugins differ between environments.

## T5ive

- `skill-navigator`: choose and run a suitable available skill workflow.
- `skill-guide`: recommend available skills, explain the fit and sequence, and wait for the user's decision.
- `review-with-choice`: recommend and run a review route, then offer recommended actions for its findings.
- `git-commit`: create a Conventional Commit message in Thai.
- `grill-with-choice` runs Matt's `grilling` skill with host-native selectable answers in each round; it requires that skill in the current host.
- `todo-init`: bootstrap a project's `todo/` task system, including All/Todo/Preop/Mise/WIP/Testing board views and workflow rules.
- `todo-triage`: sort `todo/inbox.md` notes into task files; reopens matching `test` tasks as `wip` when inbox work is added.
- `todo-triage-chat`: turn the current conversation into a task, asking for missing details or using Matt's `grilling` skill when context is absent.
- `todo-next`: recommend `mise`/`wip` work, list `test` as waiting, and leave `todo`/`preop` content to the dev.
- `todo-audit`: report missing related paths outside `todo`/`preop` and missing done dates.
- `todo-sweep`: archive `status: done` task files into `todo/archive/YYYY-MM/`.
- `todo-parallel`: run unrelated `mise`/`wip` tasks as parallel subagents; commit explicitly selected tasks only after dev tests pass.
- `todo-finish`: close or revert `stage: test` tasks — `status: done` + done date, or back to `wip` with the rejection reason in Progress.

## Matt Pocock v1.3.1

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
| Implement one ticket | `implement` (user-invoked), with `tdd` as needed |
| Implement a whole spec across its ticket graph | `implement-spec` (user-invoked) → parallel implementers on ready tickets, one integration branch, then `code-review` |
| Write a pull request body | `pr` (model-invoked when writing a PR body) |
| Review a coding session for environment improvements | `retro` (user-invoked, after the work) |
| Maintain domain terms and ADRs | `domain-modeling` |
| Prepare a repo for Matt engineering workflows | `setup-matt-pocock-skills` |
| Triage issues and external PRs | `triage` |
| Learn a concept over multiple sessions | `teach` |
| Hand work to a fresh context | `handoff` |

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

`review-with-choice` presents the available review routes and runs the one the user selects. After the selected skill returns its normal review report, the wrapper recommends and offers an action for each finding: fix, skip, or investigate further. Make no edits until the user selects a finding to fix.

## Other overlaps

- `debug-mantra` and `diagnosing-bugs` both address bugs: use the former for a concise reproduce-and-trace discipline, and the latter for hard, flaky, or performance diagnosis. Use `post-mortem` after a fix is understood and validated.
- `todo-triage` sorts a personal `todo/inbox.md`; `todo-triage-chat` turns the current conversation into a task. Matt's `triage` triages GitHub issues and PRs. Different domains despite the shared word.
- `grill-with-choice` changes how Matt's `grilling` asks each question; it does not create project documentation. Matt's `grill-with-docs` combines `grilling` with `domain-modeling` to capture vocabulary in `GLOSSARY.md`/`GLOSSARY-MAP.md` and decisions in ADRs. They are separate wrappers for selectable answers and persistent docs, and can be used together when both are wanted.
- Ponytail actively reduces complexity; Karpathy's guidelines are broader coding heuristics. They can complement each other without being one workflow.
- `skill-guide` recommends and waits. `skill-navigator` selects and acts. `review-with-choice` is the specialized menu for review workflows.

## .NET skills

Use the full `plugin:skill` ID and recommend it only when it appears in the current host.

- C# refactoring / local SDK: `dotnet:csharp-refactoring` preserves behavior; use `dotnet:setup-local-sdk` only for project-local preview or pinned SDK setups. Refactoring is not for ordinary feature/bug work or standalone upgrades.
- MSBuild: `dotnet:msbuild` handles general build failures, performance, and project-file review; `dotnet-msbuild:<skill>` handles a specific binlog, build-performance, or project-file issue.
- ASP.NET Core and data: `dotnet-aspnetcore:dotnet-webapi` is for API endpoint behavior; `dotnet-data:create-datadriven-aspnetcore` scaffolds CRUD from a model/`DbContext`; `dotnet-data:optimizing-ef-core-queries` targets slow EF Core queries.
- Runtime performance: `dotnet-diag:analyzing-dotnet-performance` scans code; `dotnet-diag:dotnet-trace-collect` and `dotnet-diag:dump-collect` collect runtime evidence; `dotnet-diag:microbenchmarking` is for BenchmarkDotNet. Use platform-specific symbolication skills only for matching crash logs.
- Tests: `dotnet-test:code-testing-agent` writes test cases; `dotnet-test:scaffold-dotnet-test-project` creates or repairs test projects; `dotnet-test:run-tests` selects test commands and filters. Choose the matching specialist for test quality, coverage, platform, MSTest, MTP, or testability work.
- `filter-syntax`, `code-testing-extensions`, and `test-analysis-extensions` are internal references; do not recommend them directly.
