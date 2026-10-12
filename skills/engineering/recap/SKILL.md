---
name: recap
description: Summarize before-and-after changes with evidence on user request. Use for "recap", "สรุปก่อน–หลัง", or "เปรียบเทียบก่อน vs หลัง"; optional technical detail.
---

# Recap

Explain changes and their effects in Thai. Default to a short behavior-and-results report; when detail is requested, include relevant logic, APIs, dependencies, and structure. Run only on user request.

## Workflow

1. Resolve the scope in the user's project. Use their baseline, otherwise context/Git evidence clearly tied to the change. Identify both endpoints; include task-related committed and uncommitted changes, including untracked files. The latest commit is not automatically the baseline.
2. Collect evidence with read-only checks. Distinguish observed results from code-based conclusions. Use measurements only from comparable runs; state missing evidence and limitations.
3. Choose destination: explicit user request → applicable AGENTS rules → chat. If scope, baseline, or document is ambiguous, ask and wait for an explicit answer. Use a blocking question tool if available, otherwise chat.
4. When writing a document, append a dated report in the appropriate section, preserving existing reports, metadata, and unrelated content. Reply briefly with a link.

## Report

Give a short summary, the before/after references, and this table. Link evidence; end with verification results and limitations.

| ประเด็น | ก่อน | หลัง | ผลกระทบ/หลักฐาน |
|---|---|---|---|

This is reporting only: preserve task state and code; acceptance requires separate confirmation.
