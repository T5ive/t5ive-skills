---
name: grill-with-choice
description: Run Matt's grilling workflow with selectable answers for each question round.
---

Run the host's `grilling` skill, presenting each question through native choice UI (`request_user_input_async` in Codex or `AskUserQuestion` in Claude Code). If unavailable, show numbered choices. If `grilling` is unavailable, explain that dependency and stop.
