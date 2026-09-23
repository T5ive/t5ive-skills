# t5ive-skills

T5ive's Codex and Claude Code plugin for skill routing, review workflows, interactive grilling, and Thai commit messages.

## Skills

| Skill | Category | What it does |
|---|---|---|
| `skill-navigator` | Engineering | Chooses and runs a suitable available skill workflow. |
| `git-commit` | Engineering | Writes Thai Conventional Commit messages with emoji. |
| `review-with-choice` | Engineering | Offers review approaches, recommends one, then runs the selected skill. |
| `skill-guide` | Productivity | Recommends a skill or workflow and waits for the user's decision. |
| `grill-with-choice` | Productivity | Runs Matt's `grilling` workflow with selectable answers in each round; requires that skill in the host. |

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
