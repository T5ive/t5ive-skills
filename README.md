# t5ive-skills

T5ive's Codex and Claude Code plugin for skill routing, review workflows, interactive grilling, Thai commit messages, and a markdown `todo/` task system.

## Skills

| Skill | Category | What it does |
|---|---|---|
| `skill-navigator` | Engineering | Chooses and runs a suitable available skill workflow. |
| `git-commit` | Engineering | Writes Thai Conventional Commit messages with emoji. |
| `review-with-choice` | Engineering | Offers review approaches, recommends one, then runs the selected skill. |
| `skill-guide` | Productivity | Recommends a skill or workflow and waits for the user's decision. |
| `grill-with-choice` | Productivity | Runs Matt's `grilling` workflow with selectable answers in each round; requires that skill in the host. |
| `todo-init` | Productivity | Bootstraps the `todo/` system, including All/Todo/Preop/Mise/WIP/Testing board views and workflow rules. |
| `todo-triage` | Productivity | Sorts inbox notes into `stage: todo` files; keeps inbox headers intact. |
| `todo-next` | Productivity | Recommends `mise`/`wip` tasks, lists `test` as waiting, and skips `todo`/`preop` content. |
| `todo-audit` | Productivity | Reports missing related paths outside `todo`/`preop`, plus missing done dates. |
| `todo-sweep` | Productivity | Moves `status: done` files into `todo/archive/YYYY-MM/` and proposes a commit. |
| `todo-parallel` | Productivity | Runs 2–3 unrelated `mise`/`wip` tasks as background subagents, then commits each task separately. |
| `todo-finish` | Productivity | Closes `test` tasks or returns failures to `wip` with the reason recorded in Progress. |

Workflow diagrams for the todo system (lifecycle + worked scenario): [skills/references/todo-diagrams.md](skills/references/todo-diagrams.md) — raw `.mmd` sources in `assets/`.

## Required companion skills

Install these skill sets in the same agent to use every workflow. The `t5ive-skills` plugin itself can be installed independently.

| Skill set | Repositories |
|---|---|
| Matt Pocock | [mattpocock/skills](https://github.com/mattpocock/skills) |
| 9arm | [Original: thananon/9arm-skills](https://github.com/thananon/9arm-skills) · [Codex plugin fork: T5ive/9arm-skills](https://github.com/T5ive/9arm-skills) |
| Karpathy guidelines | [Original: multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) · [Codex plugin fork: T5ive/andrej-karpathy-skills](https://github.com/T5ive/andrej-karpathy-skills) |
| Ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |

The original and fork links show both the source and the Codex plugin distribution. Install each skill set once; for Codex, use the T5ive forks of 9arm and Karpathy guidelines.

## Install

### Codex

```bash
codex plugin marketplace add T5ive/t5ive-skills
codex
```

Open `/plugins`, select the `t5ive-skills` marketplace, and install the single `t5ive-skills` plugin.

### Claude Code

```text
/plugin marketplace add T5ive/t5ive-skills
/plugin install t5ive-skills@t5ive-skills
```

Plugin skills use the `/t5ive-skills:<skill>` namespace in Claude Code.

### Skills only

```bash
npx skills add T5ive/t5ive-skills
```

### Local plugin development

Codex:

```bash
codex plugin install .
```

Claude Code:

```bash
claude --plugin-dir .
```
