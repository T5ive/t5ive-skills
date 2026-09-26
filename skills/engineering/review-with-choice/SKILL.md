---
name: review-with-choice
description: Present review workflow choices, recommend one for the requested review, then run the workflow the user selects. Use when the user wants help choosing a review style or asks for a review menu.
---

# Review With Choice

Read `../../references/skill-catalog.md` for the review boundaries. Use the host's native choice UI for the route selector and follow-up actions (`request_user_input_async` in Codex or `AskUserQuestion` in Claude Code). If the UI is unavailable or the call fails, show numbered options in chat and wait for the user's reply. A pending choice request is not a selection.

Use the user's stated goal to recommend one available route, then wait for their selection before starting:

- **End-to-end review:** 9arm `scrutinize` traces the actual behavior and checks the change against its goal.
- **Complexity-only review:** Ponytail `ponytail-review` looks for unnecessary complexity in a diff.
- **Standards and spec review:** Matt `code-review` compares changes from a fixed point against repo conventions and the originating spec.

Show only routes whose skills are available in the current host. After the user selects a route, activate that skill using the host's skill mechanism and follow its workflow. If the selected skill is unavailable, explain that and offer the remaining choices instead of imitating it.

Let the selected skill finish its review and return its normal explanation and findings. Preserve that response intact. Only after it finishes, offer a concise recommendation and a choice for each actionable finding: **fix**, **investigate further**, or **skip**. Use the native choice UI or the numbered chat fallback. Wait for each selection before acting; investigate within the selected skill's workflow, and make no edits until the user chooses to fix that finding. If there are no actionable findings, say the review is complete and no follow-up is needed; do not show an empty menu.
