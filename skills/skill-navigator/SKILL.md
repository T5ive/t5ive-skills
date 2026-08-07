---
name: skill-navigator
description: >
  Guide for choosing which Claude Code skill to use.
  Use when user asks "what skill should I use", "which skill for X",
  "where do I start", "skill workflow", or describes a situation
  (starting feature, hit a bug, doing review) and wants to know the right tool.
---

# Skill Navigator

Read `references/situations.md` for full decision tree.

## Quick Map

| Situation | Skill Chain |
|---|---|
| Don't know which skill to use | `/ask-matt` |
| New feature, no codebase | `/grill-me` → `/tdd` |
| New feature, existing codebase | `/setup-matt-pocock-skills` (1st) → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` |
| Large / unclear-scope effort | `/wayfinder` |
| Bug (reproducible) | `/debug-mantra` → `/post-mortem` |
| Bug (flaky / perf) | `/diagnose` → `/post-mortem` |
| Hard bug / perf regression (deep) | `/diagnosing-bugs` → `/post-mortem` |
| Review / before merge | `/scrutinize` or `/code-review` (Standards + Spec axes) |
| Review diff for over-engineering | `/ponytail-review` |
| Audit whole repo for bloat | `/ponytail-audit` |
| Context window full | `/handoff` |
| Understand / improve codebase | `/improve-codebase-architecture` |
| Break spec into tickets | `/to-spec` → `/to-tickets` |
| Move issues through triage | `/triage` |
| Resolve merge conflicts | `/resolving-merge-conflicts` |
| Research a question with sources | `/research` |
| Write minimal code (lazy mode) | `/ponytail` |
| Reduce token usage, respond in Thai | `/pordee` |
| Learn a new concept over sessions | `/teach` |
| Sharpen domain terminology / ADRs | `/grill-with-docs` or `/domain-modeling` |
| Design module with clean seam | `/codebase-design` |
| Write/edit a skill or agent doc | `/writing-for-agents` |
| Configure repo for MP skills | `/setup-matt-pocock-skills` |
| Prototype a design question | `/prototype` |
| Async questionnaire for stakeholders | `/to-questionnaire` |
| Model too verbose / unclear | `/wait-what` |
| Generate a manual-step wizard | `/wizard` |

**karpathy-guidelines** — always-on plugin, no invoke needed.
**pordee** — always-on once activated, no re-invoke needed per session.

## Skill Taxonomy (mattpocock v1.2)

**Engineering, user-invoked**: `ask-matt`, `grill-with-docs`, `triage`, `improve-codebase-architecture`, `setup-matt-pocock-skills`, `to-spec`, `to-tickets`, `implement`, `wayfinder`

**Engineering, model-invoked**: `prototype`, `diagnosing-bugs`, `research`, `tdd`, `domain-modeling`, `codebase-design`, `code-review`, `resolving-merge-conflicts`, `wizard`

**Productivity, user-invoked**: `grill-me`, `handoff`, `teach`, `to-questionnaire`, `wait-what`

**Productivity, model-invoked**: `grilling`, `writing-for-agents`

User-invoked may invoke model-invoked. Never the reverse.

Renamed since v1.0: `to-prd`→`to-spec`, `to-issues`(+`to-plan`)→`to-tickets`, `diagnose`→`diagnosing-bugs`, `writing-great-skills`→`writing-for-agents`. Removed: `zoom-out`, `management-talk` (no longer in upstream).
