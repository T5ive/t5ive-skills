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
| New feature, no codebase | `/grill-me` → `/tdd` |
| New feature, existing codebase | `/setup-matt-pocock-skills` (1st) → `/grill-with-docs` → `/tdd` |
| Bug (reproducible) | `/debug-mantra` → `/post-mortem` |
| Bug (flaky / perf) | `/diagnose` → `/post-mortem` |
| Review / before merge | `/scrutinize` |
| Review diff for over-engineering | `/ponytail-review` |
| Audit whole repo for bloat | `/ponytail-audit` |
| Context window full | `/handoff` |
| Report to management | `/management-talk` |
| Understand codebase | `/zoom-out` |
| Architecture review | `/improve-codebase-architecture` |
| Break spec into issues | `/to-prd` → `/to-issues` |
| Write minimal code (lazy mode) | `/ponytail` |
| Reduce token usage, respond in Thai | `/pordee` |

**karpathy-guidelines** — always-on plugin, no invoke needed.
**pordee** — always-on once activated, no re-invoke needed per session.
