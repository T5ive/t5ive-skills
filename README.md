# t5ive-skills

## Layout

Skills live under `skills/`:

Each skill is its own directory containing a `SKILL.md` (with YAML frontmatter — `name` and `description`) and any bundled reference files.

## Install

### Codex

Add the marketplace:

```bash
codex plugin marketplace add T5ive/t5ive-skills
codex
```

Open `/plugins`, select the `t5ive-skills` marketplace, and install `t5ive-skills`.

### Claude Code

```bash
/plugin marketplace add T5ive/t5ive-skills
/plugin install skill-navigator
/plugin install git-commit
```

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
claude --plugin-dir ./t5ive-skills
```

## Reference

- **[skill-navigator](./skills/skill-navigator/SKILL.md)** — Maps situations to the right skill chain. Describe what you're trying to do (starting a feature, hit a bug, need to review) and AI suggests which skill(s) to invoke.

  **Quick map (v1.0):**

  | Situation | Skill chain |
  |---|---|
  | Don't know which skill | `/ask-matt` |
  | New feature, no codebase | `/grill-me` → `/tdd` |
  | New feature, existing codebase | `/setup-matt-pocock-skills` → `/grill-with-docs` → `/tdd` |
  | Bug (reproducible) | `/debug-mantra` → `/post-mortem` |
  | Bug (hard / flaky / perf) | `/diagnosing-bugs` → `/post-mortem` |
  | Review / before merge | `/scrutinize` |
  | Review diff for over-engineering | `/ponytail-review` |
  | Architecture review | `/improve-codebase-architecture` |
  | Break spec into issues | `/to-prd` → `/to-issues` |
  | Context window full | `/handoff` |
  | Write minimal code | `/ponytail` |
  | Respond in Thai, save tokens | `/pordee` |

  Full decision tree: [`references/situations.md`](./skills/skill-navigator/references/situations.md)

- **[git-commit](./skills/git-commit/SKILL.md)** — Generates Conventional Commits + emoji messages written in Thai. Triggers on `/git-commit` or when asked to commit.
