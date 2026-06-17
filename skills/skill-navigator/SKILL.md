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
| New feature, existing codebase | `/setup-matt-pocock-skills` (1st) → `/grill-with-docs` → `/tdd` |
| Bug (reproducible) | `/debug-mantra` → `/post-mortem` |
| Bug (flaky / perf) | `/diagnose` → `/post-mortem` |
| Hard bug / perf regression (deep) | `/diagnosing-bugs` → `/post-mortem` |
| Review / before merge | `/scrutinize` |
| Review diff for over-engineering | `/ponytail-review` |
| Audit whole repo for bloat | `/ponytail-audit` |
| Context window full | `/handoff` |
| Report to management | `/management-talk` |
| Understand codebase | `/zoom-out` |
| Architecture review | `/improve-codebase-architecture` |
| Break spec into issues | `/to-prd` → `/to-issues` |
| Move issues through triage | `/triage` |
| Write minimal code (lazy mode) | `/ponytail` |
| Reduce token usage, respond in Thai | `/pordee` |
| Learn a new concept over sessions | `/teach` |
| Sharpen domain terminology / ADRs | `/grill-with-docs` or `/domain-modeling` |
| Design module with clean seam | `/codebase-design` |
| Write or edit a skill | `/writing-great-skills` |
| Configure repo for MP skills | `/setup-matt-pocock-skills` |

**karpathy-guidelines** — always-on plugin, no invoke needed.
**pordee** — always-on once activated, no re-invoke needed per session.

## Skill Taxonomy (mattpocock v1.0)

**User-invoked** (you type them): `ask-matt`, `grill-me`, `grill-with-docs`, `triage`, `improve-codebase-architecture`, `setup-matt-pocock-skills`, `to-issues`, `to-prd`, `prototype`, `handoff`, `teach`, `writing-great-skills`

**Model-invoked** (agent reaches for automatically): `diagnosing-bugs`, `tdd`, `domain-modeling`, `codebase-design`, `grilling`

User-invoked may invoke model-invoked. Never the reverse.
