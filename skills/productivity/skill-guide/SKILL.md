---
name: skill-guide
description: Recommend an available skill or workflow without running it. Use when the user asks what skill fits, wants to compare skill options, or describes a situation and asks where to start.
---

# Skill Guide

Read `../../references/skill-catalog.md` when the task involves choosing among skills or workflow chains.

Use the user's existing context. If the situation or goal is unclear, ask one short, adaptive question about what they are facing or trying to achieve. Offer concrete choices that fit the context and include an option to describe something else. If multiple workflows fit, present them as selectable options and mark the recommendation.

Use the host's native choice UI when available: `request_user_input_async` in Codex or `AskUserQuestion` in Claude Code. If neither is available, show a short numbered list and accept a number or free-form reply.

Recommend the best available skill or sequence, explain briefly why and in what order, and give the host-appropriate invocation names. Check availability before recommending external plugin skills. Do not invoke or start a recommended workflow; wait for the user's decision.
