---
name: skill-navigator
description: Choose and run the best available skill workflow for a task. Use when the user asks the agent to pick the right skill and carry out the task, or asks to route and do the work. Use skill-guide when they only want recommendations.
---

# Skill Navigator

Choose and use a workflow; do not stop after recommending one.

1. Read `../../references/skill-catalog.md` for routing boundaries.
2. Check which named skills are available in the current host. Choose the smallest suitable skill or sequence.
3. Activate the chosen skill using the host's skill mechanism. If the host exposes its instructions but no invocation action, load and follow those instructions in this task. If the skill is unavailable, say so and use a close available alternative only when it fits.
4. Continue the user's task through the selected workflow. Ask only for decisions or information that materially blocks the next step.

If the user only asks which skill fits and does not ask you to act, use `skill-guide` and wait for their choice.
