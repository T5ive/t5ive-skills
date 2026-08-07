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

## Don't Know Which Skill to Use

**Invoke:** `/ask-matt`

Routes over all user-invoked skills in mattpocock/skills. Describes situation → get the right chain.

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

**Chain:** `/setup-matt-pocock-skills` (once per repo) → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement`

**setup-matt-pocock-skills** — configures issue tracker, triage labels, CONTEXT.md location. Run once per repo.
Required before: `/to-spec`, `/to-tickets`, `/triage`, `/diagnosing-bugs`, `/tdd`, `/improve-codebase-architecture`.

**grill-with-docs** — same as grill-me but reads CONTEXT.md + ADRs and updates them inline.
Keeps naming consistent with project domain language.

**to-spec** — synthesizes the conversation into a spec, published to your issue tracker. (Formerly `to-prd`.)

**to-tickets** — breaks a spec/plan into tracer-bullet tickets with declared blocking edges. (Merged from `to-plan` + `to-issues`.)

**implement** — builds work from specs/tickets, invoking `/tdd` at agreed points and closing each ticket with `/code-review`. This is the skill that actually writes the feature; `/tdd` and `/code-review` fire automatically inside it, no need to call them separately in this chain.

---

## Large / Unclear-Scope Effort

**Invoke:** `/wayfinder`

For work too big or ambiguous to spec directly. Plans the effort as a sequence of decision tickets, resolving one at a time until the path forward is clear enough to hand off to `/to-spec` → `/to-tickets` → `/implement`.

---

## Bug — Hard / Performance / Regression (Deep Diagnosis)

**Chain:** `/diagnosing-bugs` → `/post-mortem`

**diagnosing-bugs** (model-invoked) — disciplined diagnosis loop:
1. Reproduce → minimise → hypothesise → instrument → fix → regression-test
Adds: minimisation step, ranked hypotheses, mandatory `[DEBUG-xxx]` tagging.

vs `/debug-mantra`: debug-mantra is 4 quick mantras; diagnosing-bugs is the full 6-phase loop for harder problems.
vs `/diagnose` (local skill): diagnosing-bugs is the mattpocock upstream version.

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

**Chain:** `/scrutinize` or `/code-review`

**scrutinize** (local skill) — 4 steps (no skipping):
1. **Intent** — state goal in 1 sentence + ask if simpler approach exists (mandatory)
2. **Trace** — walk real code path from entry, not just the diff
3. **Verify** — each claim the PR makes: does traced path actually produce that behavior?
4. **Report** — blocker → major → nit + verdict: ship / fix-then-ship / rework / reject

Rules: no rubber-stamp, every claim cites `file:line`, no flattery.

**code-review** (mattpocock, model-invoked) — reviews changes since a fixed point along two axes in parallel sub-agents: **Standards** (matches this repo's documented conventions?) and **Spec** (matches what the originating issue/spec asked for?). Reports both side by side. This is also what `/implement` calls automatically to close out a ticket.

---

## Context Window Full

**Chain:** `/handoff`

Summarizes: work done, decisions made, pending tasks, key context.
Copy output into new session.

---

## Learn a Concept / Skill

**Invoke:** `/teach`

Multi-session teaching. Uses current directory as stateful workspace. Tracks progress across sessions.

---

## Sharpen Domain Terminology / ADRs

**Chain:** `/grill-with-docs` or `/domain-modeling`

**grill-with-docs** (user-invoked) — grilling session that builds domain model inline. Updates CONTEXT.md + ADRs during the conversation.

**domain-modeling** (model-invoked) — challenge terms against glossary, stress-test with edge-case scenarios, update CONTEXT.md + ADRs. Agent reaches for this automatically when domain consistency matters.

---

## Design a Module with a Clean Interface

**Invoke:** `/codebase-design` (model-invoked)

Shared discipline for designing deep modules: lots of behaviour behind a small interface, placed at a clean seam, testable through that interface.

---

## Write or Edit a Skill or Agent Doc

**Invoke:** `/writing-for-agents` (formerly `writing-great-skills`)

Reference for vocabulary and principles that make agent-consumed documents predictable — skill SKILL.md files, AGENTS.md/CLAUDE.md, and other docs an agent reads rather than a human.

---

## Understand / Improve Codebase

- `/improve-codebase-architecture` — scans the codebase for deepening opportunities using CONTEXT.md + ADRs, presents candidates as an HTML report. Use after `/diagnosing-bugs` finds architecture as root cause, or as periodic review.

(`/zoom-out` was removed upstream — went unused. For general code understanding, just ask directly; no dedicated skill covers it anymore.)

---

## Break Spec into Tickets

**Chain:** `/to-spec` → `/to-tickets`

- `/to-spec` — synthesizes conversation into a spec → submits to your issue tracker (formerly `/to-prd`)
- `/to-tickets` — breaks a spec/plan into tracer-bullet tickets with declared blocking edges (merged from `/to-plan` + `/to-issues`; vertical slices, not horizontal layers)

Typically followed by `/implement` to actually build the tickets.

---

## Async Questionnaire for Stakeholders

**Invoke:** `/to-questionnaire`

Converts decisions made in conversation into an async Markdown questionnaire for specific stakeholders to answer outside the session.

---

## Model Too Verbose / Answer Unclear

**Invoke:** `/wait-what`

Re-pitches an unclear or overlong response in plain English, using your project's CONTEXT.md vocabulary. Single-word trigger for "say that again, simpler."

---

## Research a Question Against Sources

**Invoke:** `/research` (model-invoked)

Investigates a question against high-trust primary sources, captures findings as a cited Markdown file in the repo. Use when reading legwork should be delegated and documented rather than answered from memory.

---

## Resolve Merge Conflicts

**Invoke:** `/resolving-merge-conflicts` (model-invoked)

Works through an in-progress git merge/rebase conflict hunk-by-hunk, resolving each by tracing the intent of both sides rather than guessing.

---

## Generate a Manual-Step Wizard

**Invoke:** `/wizard` (model-invoked)

Generates an interactive bash wizard for steps only a human can perform — provisioning infrastructure, setting up credentials/CI secrets, an unfamiliar third-party dashboard, a one-off migration. Don't use for steps the agent can do itself.

---

## Prototype (Throwaway / UI Variations)

**Invoke:** `/prototype`

Two modes:
- **Terminal app** — for state/business-logic questions (fast, no UI)
- **UI variations** — several radically different UI designs, all togglable from one route

Use to flesh out design before committing to an implementation.

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
