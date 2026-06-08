# How each loop maps to Addy's six building blocks

Addy Osmani frames a loop as **five building blocks + a sixth**: *"A loop needs five things and then one place to remember stuff."*

1. **Automations** — the heartbeat (an autonomous trigger that fires without you)
2. **Worktrees** — parallel isolation
3. **Skills** — externalized project knowledge
4. **Plugins & Connectors** — reach your real tools (*connectors* = the MCP link; *plugins* = how you package & ship skills+connectors)
5. **Sub-agents** — split the maker from the checker
6. **Memory** — state that lives outside the single conversation

All four loops in this repo implement the full set — nothing *required* is missing. But in two places a component takes a **non-obvious form**, and one sub-component (plugin packaging) is **deliberately unused**. This doc maps every loop to every component and is honest about the modified / weak / unused cells.

---

## Master matrix

| Component | A · `upgrade-deps` | B · `triage-flaky` | C · `draft-postmortem` | D · `reconcile-docs` |
|---|---|---|---|---|
| **1 Automation** | ✅ cron 02:00 daily | ✅ after each CI run / hourly | ⚠️ **event** (alert webhook), not a clock | ✅ weekly + on-merge |
| **2 Worktrees** | ✅ one per upgrade class | ✅ throwaway repro checkout | ⚠️ **read-only checkout at incident SHA** (temporal, not collision) | ✅ `wt/docs` |
| **3 Skill** | ✅ `upgrade-deps` | ✅ `triage-flaky` | ✅ `draft-postmortem` | ✅ `reconcile-docs` |
| **4a Connectors** | ✅ GitHub, advisories, Slack | ✅ CI, GitHub, Linear, Slack | ✅ obs, GitHub, PagerDuty, Docs, Slack | ✅ GitHub, docs-build, link-checker |
| **4b Plugin (packaging)** | ➖ not packaged | ➖ not packaged | ➖ not packaged | ➖ not packaged |
| **5 Sub-agents** | ✅ maker→checker (security) | ✅ maker→checker (adversarial) | ✅ investigator→redteam | ✅ maker→checker (executes) |
| **6 Memory** | ✅ `deps-state.md` | ✅ `flaky-state.md` + Linear | ✅ `incidents-state.md` | ✅ `docs-state.md` |

✅ present & load-bearing · ⚠️ present but in modified form · ➖ intentionally unused

### Plus Loop E — the sandbox that proves the principle

[Loop E](./E-demo-sandbox/README.md) is a zero-dependency quick-test loop. It is the clearest demonstration that the blocks earn their place against a failure mode — it keeps only **four** of the six and drops the other two on purpose:

| Component | E · `demo-loop` |
|---|---|
| **1 Automation** | ✅ `/demo-loop` · `$demo-loop` · `/loop 10m /demo-loop` |
| **2 Worktrees** | ➖ **dropped** — one agent fixes one file; no collision to isolate |
| **3 Skill** | ✅ `demo-loop` |
| **4 Connectors** | ➖ **dropped** — fully local; touches no external tool |
| **5 Sub-agents** | ✅ `demo-maker` → `demo-checker` |
| **6 Memory** | ✅ `demo-state.md` |

So the **irreducible core of a loop is four blocks** — automation, skill, sub-agents, memory — plus a verifiable stop condition. Worktrees appear when there's parallelism; connectors appear when the loop must act on real systems. A–D are this core plus those two; E shows the core alone, running end-to-end.

---

## Per-loop mapping

### Loop A — Nightly dependency & security upgrade
1. **Automation** — cron / Codex Automation fires at 02:00; nobody types anything. This *is* the heartbeat.
2. **Worktrees** — `wt/patch` / `wt/minor` / `wt/major`, so a failing major bump can't block the safe patch PRs running beside it. Addy's exact rationale (parallel agents not colliding) applies directly.
3. **Skill** — `upgrade-deps` holds the changelog-reading routine and the *pinned-with-reason* list ("router held at 6.x because v7 needs a manual refactor"). Intent-debt insurance.
4. **Connectors** — GitHub (open PRs), security-advisory / `npm audit` feed, Slack digest.
5. **Sub-agents** — `deps-maker` (fast) bumps + fixes; `deps-checker` (stronger, security-focused, **no edit tool**) audits and runs the full suite.
6. **Memory** — `deps-state.md` records deferrals *and why*, so tonight's run never re-attempts a bump it already reasoned about rejecting.

→ **All six, all genuinely needed.**

### Loop B — Flaky-test hunter & quarantine
1. **Automation** — fires after each CI run (or hourly) to drain the suspect queue.
2. **Worktrees** — a throwaway checkout where the suspect is rerun 50× so the rerun storm never disturbs anyone's tree (and multiple suspects can be triaged in parallel).
3. **Skill** — `triage-flaky`: the rerun protocol, the failure-rate threshold, the quarantine-not-delete convention.
4. **Connectors** — CI API (run history/logs), GitHub (commit the `@flaky` tag), Linear (ticket), Slack.
5. **Sub-agents** — `flaky-maker` classifies; `flaky-checker` **adversarially** asks "is this really flaky, or a real intermittent bug you mislabeled?"
6. **Memory** — `flaky-state.md` + a Linear board track failure rates *over time*, so it never re-triages a known test and can spot one getting worse.

→ **All six, all needed.**

### Loop C — Incident → postmortem draft *(the interesting one)*
3. **Skill** ✅ `draft-postmortem` (template, blameless rules).
4. **Connectors** ✅ the heaviest of the four — observability/logs, GitHub bisect, PagerDuty, Google Docs, Slack.
5. **Sub-agents** ✅ `incident-investigator` → `incident-redteam` (adversarial verification of a *causal* claim).
6. **Memory** ✅ `incidents-state.md` (incident → cause, recurrence detection).

Components **1 and 2 appear in modified form** — see the caveats below.

### Loop D — Docs-drift reconciliation
1. **Automation** — weekly sweep + on-merge-to-main hook.
2. **Worktrees** — `wt/docs` so doc rewrites don't collide with live feature branches.
3. **Skill** — `reconcile-docs`: the page→module map and the "examples must be runnable" rule.
4. **Connectors** — GitHub diff-since-last-run, docs-site build, link-checker, Slack.
5. **Sub-agents** — `docs-maker` rewrites; `docs-checker` (**no edit tool**) *executes every example* and diffs the documented API against the real source.
6. **Memory** — `docs-state.md` stores the last-reconciled SHA *per page*, so each run only processes the delta.

→ **All six, all needed.**

---

## Where a component is modified, weak, or unused — and why

The six blocks aren't a checklist where more = better. Each earns its place against a **specific failure mode**; when that failure mode is absent, the block either changes job or becomes optional. Naming that is more useful than forcing a ✅.

**① Loop C's "Automation" is event-driven, not scheduled.** Addy describes automations as things that *"go off on a schedule."* Loop C is triggered by an **alert webhook**, not a clock. The component is still present (an autonomous trigger that fires without you), but a *cron* would be actively wrong here: you don't "discover incidents on a schedule" — an incident announces itself, and the loop should react the instant it does. This is also why Loop C has no `/loop <interval>` form: there's no interval to set.

**② Loop C's "Worktree" is for temporal isolation, not collision-avoidance.** Addy's stated reason for worktrees is *"two agents working in parallel don't step on each other."* Loop C usually runs **one** investigation at a time, so that rationale doesn't apply. The worktree is used for a *different* reason: to check out the **exact SHA that was deployed when the incident began** (git-bisect territory) **read-only**, without moving anyone's `HEAD`. If you were willing to investigate from logs/metrics alone and skip source archaeology, **this is the one component you could legitimately drop** — it is the weakest-justified block in the whole set. It's kept because deploy-time source is usually decisive for root cause.

**③ The "Plugin" half of component 4 is intentionally unused in all four.** A *connector* is the MCP link to your tools; a *plugin* is how you **package and ship** skills + connectors to other repos or teammates. Every loop uses connectors, but **none is packaged as a plugin** — because these are installed in **project scope**, not distributed. Packaging as a plugin only earns its keep when you want the same loop in many repos or in a teammate's setup. For a single project it's pure overhead. *(If you later want Loop D running across five repos, that's exactly when you'd bundle `reconcile-docs` + its connectors into a plugin.)*

**④ "Memory" is the least essential to a single run, essential to the loop.** Any of these could draft one postmortem / bump one package / fix one doc page with *no* state file. Memory earns its place only because these are **recurring**: it's what stops the loop re-attempting a rejected dependency, re-triaging a known-flaky test, or re-reconciling an unchanged doc — and it's what lets Loop C notice "3rd connection-pool exhaustion this quarter." Drop it and the loop still *works* each cycle; it just gets dumber and more wasteful every time.

---

## Bottom line

All four loops implement all six components; nothing required is missing. The only genuinely **droppable** component in the set is **Loop C's worktree** (if you forgo deploy-time source inspection), and the only universally **skipped** sub-component is **plugin packaging** — correctly skipped because these are project-scope, not distributed.

Three principles fall out of this:

- **Automation is the one non-negotiable block** — it's what makes a loop a loop rather than a one-shot. But its *form* (cron vs. event vs. on-merge) is dictated by what surfaces the work; getting the form wrong (e.g. scheduling incident discovery) is a design error even when the block is technically "present."
- **Two components split into a functional half and a scale/durability half:** connectors vs. plugins (4a/4b), and per-run work vs. cross-run memory (6). The functional half is almost always needed; the packaging/durability half is only needed *at scale* (many repos) or *over time* (recurring runs).
- **Worktrees answer collision.** When there's no collision, the block changes job (temporal isolation in C) or becomes optional — it is not free, so don't add it reflexively.

See [`README.md`](./README.md) for trigger instructions and the [synthesis report §6](../Loop-Engineering-Synthesis-Report.md) for the original design tables.
