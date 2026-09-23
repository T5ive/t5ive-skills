---
name: review-with-choice
description: Present review workflow choices, recommend one for the requested review, then run the workflow the user selects. Use when the user wants help choosing a review style or asks for a review menu.
---

# Review With Choice

Read `../../references/skill-catalog.md` for the review boundaries. Use the host's native choice UI when available (`request_user_input_async` in Codex or `AskUserQuestion` in Claude Code); otherwise show numbered options and accept a number or free-form reply. Use the same choice UI for the per-finding actions in the second route.

Use the user's stated goal to recommend one available route, then let them select before starting:

- **End-to-end review:** 9arm `scrutinize` traces the actual behavior and checks the change against its goal.
- **End-to-end review with finding actions:** run 9arm `scrutinize`, then offer a choice for each finding: fix it, skip it, or investigate further. Do not edit until the user selects a finding to fix.
- **Complexity-only review:** Ponytail `ponytail-review` looks for unnecessary complexity in a diff.
- **Standards and spec review:** Matt `code-review` compares changes from a fixed point against repo conventions and the originating spec.

Show only routes whose skills are available in the current host. After the user selects a route, activate that skill using the host's skill mechanism and follow its workflow. If the selected skill is unavailable, explain that and offer the remaining choices instead of imitating it. Keep each tool's review scope and output intact; the finding-action choices apply only to the second route.
