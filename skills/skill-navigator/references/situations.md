# Situations Reference

## Always-On Plugins (no invoke needed once loaded)

### karpathy-guidelines

| Principle | Prevents |
|---|---|
| Think Before Coding | Silent assumptions → wrong direction |
| Simplicity First | Overengineering, unrequested abstractions |
| Surgical Changes | Touching unrelated files |
| Goal-Driven Execution | Vague tasks → wrong output |

### pordee

Reduces token usage 60-75% by switching Claude's prose to concise Thai while keeping technical English terms intact.

- `/pordee` / `/pordee full` — activate (max compression, default)
- `/pordee lite` — remove polite particles only, keep full grammar
- `/pordee stop` / `หยุดพอดี` — deactivate
- `/pordee-stats` — show token savings

**vs ponytail:** ponytail governs *what code to write* (YAGNI, stdlib first). pordee governs *how Claude talks* (Thai, terse). Both can be active simultaneously.
**vs karpathy-guidelines:** karpathy-guidelines is always-on and passive. pordee must be activated once per session, then persists.

---

## New Feature — No Codebase

**Chain:** `/grill-me` → `/tdd`

**grill-me** — interviews relentlessly until every decision branch is resolved.
Asks one question at a time, provides recommended answer each time.
Explores codebase instead of asking when possible.

**tdd** — vertical slices only. One test → one impl → repeat.
Never write all tests first (horizontal slicing = imagined behavior).

---

## New Feature — Existing Codebase

**Chain:** `/setup-matt-pocock-skills` (once per repo) → `/grill-with-docs` → `/tdd`

**setup-matt-pocock-skills** — configures issue tracker, triage labels, CONTEXT.md location.
Required before: `/to-issues`, `/to-prd`, `/triage`, `/diagnose`, `/tdd`, `/improve-codebase-architecture`, `/zoom-out`.

**grill-with-docs** — same as grill-me but reads CONTEXT.md + ADRs and updates them inline.
Keeps naming consistent with project domain language.

---

## Bug — Reproducible

**Chain:** `/debug-mantra` → `/post-mortem`

**debug-mantra** — 4 mantras in order, no skipping:
1. Reproduce (deterministic or high-rate)
2. Trace the fail path (entry → crash)
3. Falsify the hypothesis
4. Cross-reference every breadcrumb

**post-mortem** — refuses to draft without: repro + known root cause + fix + validation.
Sections: Summary · Symptom · Root cause · Fix · How found · Why slipped · Validation · Action items.

---

## Bug — Flaky / Performance / Can't Reproduce

**Chain:** `/diagnose` → `/post-mortem` → `/improve-codebase-architecture` (if arch is root cause)

**diagnose** — 6 phases:
1. **Build feedback loop** (most important) — try: failing test → curl script → CLI diff → Playwright → trace replay → throwaway harness → fuzz → bisect → differential → HITL script
2. Reproduce — confirm it's the right bug
3. Hypothesise — 3-5 ranked falsifiable hypotheses, show user before testing
4. Instrument — one variable at a time, tag all debug logs `[DEBUG-xxx]`
5. Fix + regression test — write test before fix if correct seam exists
6. Cleanup — remove `[DEBUG-xxx]` tags, document winning hypothesis in commit

vs debug-mantra: diagnose adds Minimise + ranked Hypothesise + mandatory debug tagging.

---

## Review / Before Merge

**Chain:** `/scrutinize`

4 steps (no skipping):
1. **Intent** — state goal in 1 sentence + ask if simpler approach exists (mandatory)
2. **Trace** — walk real code path from entry, not just the diff
3. **Verify** — each claim the PR makes: does traced path actually produce that behavior?
4. **Report** — blocker → major → nit + verdict: ship / fix-then-ship / rework / reject

Rules: no rubber-stamp, every claim cites `file:line`, no flattery.

---

## Context Window Full

**Chain:** `/handoff`

Summarizes: work done, decisions made, pending tasks, key context.
Copy output into new session.

---

## Report to Management

**Chain:** `/management-talk` → specify channel

Channels: `→ slack` · `→ jira` · `→ email` · `→ standup`

Removes: function names, file paths, debug iterations, rejected hypotheses.
Keeps: impact (who, how bad), status, next steps, ETA.

---

## Understand / Improve Codebase

- `/zoom-out` — explain code in context of whole system
- `/improve-codebase-architecture` — find refactor opportunities using CONTEXT.md + ADRs; use after `/diagnose` finds arch as root cause, or as periodic review

---

## Break Spec into Issues

**Chain:** `/to-prd` → `/to-issues`

- `/to-prd` — synthesizes conversation into PRD → submits as GitHub issue
- `/to-issues` — breaks PRD into vertical-slice GitHub issues (not horizontal layers)

---

## Write Minimal Code / Fight Over-Engineering

**Invoke:** `/ponytail` (persistent mode) or sub-skills one-shot

**ponytail** (lazy mode) — active every response until disabled. Enforces a ladder:
1. Does this need to exist? (YAGNI)
2. Stdlib does it? Use it.
3. Native platform covers it? Use it.
4. Already-installed dep solves it? Use it.
5. One line? One line.
6. Only then: minimum code that works.

Levels: `lite` (suggest lazier alternative) · `full` (enforce ladder, default) · `ultra` (YAGNI extremist, challenge requirements)
Off: "stop ponytail" / "normal mode"

**When to use ponytail vs karpathy-guidelines:**
- karpathy-guidelines = always-on, prevents common LLM mistakes (assumptions, surgical changes)
- ponytail = invoke when you want to *actively* fight complexity: YAGNI, delete over add, stdlib first

**Sub-skills (one-shot, no persistent mode):**

**`/ponytail-review`** — review a diff for over-engineering only. Not correctness, not security.
Output: `L<n>: <tag> <what to cut>. <replacement>.` Tags: `delete` · `stdlib` · `native` · `yagni` · `shrink`
Use after writing code or before merge, as complement to `/scrutinize`.

**`/ponytail-audit`** — same as ponytail-review but scans entire repo. Use for periodic cleanup or when codebase feels bloated.

**`/ponytail-debt`** — collects all `ponytail:` comments (deliberate shortcuts) into a ledger. Use when you want to revisit deferred simplifications.

**`/ponytail-help`** — quick reference card for all ponytail commands and levels.
