# Loop Engineering: A Grounded Synthesis

*A report grounded in Addy Osmani's "Loop Engineering" (Substack, June 2026) and the eleven essays it draws on, plus the "backpressure" essay raised in its comments.*

> **Quote policy.** Lines in quotation marks are reproduced from primary text I could verify directly: Osmani's *Loop Engineering* article, and the *Long-Running Agents* / *Orchestration Tax* essays (re-confirmed word-for-word during fetching). All other source claims are **paraphrased** — fetched through a summariser, so I do not present them as exact wording. One linked slug, `adversarial-code-review`, returns a 404; that material actually lives inside the *Loop Engineering* article and is cited there.

---

## TL;DR

For two years, getting work out of a coding agent meant *you* held the tool: type, read, type the next thing. Loop engineering moves you up one level. As Osmani puts it: **"Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead."** A loop is "a recursive goal where you define a purpose and the AI iterates until complete."

The thing that makes this *now* and not a someday: the pieces stopped being a personal pile of bash and started shipping inside the products. Osmani identifies **five building blocks plus a sixth** — automations, worktrees, skills, plugins/connectors, sub-agents, and **memory** — and notes that **Claude Code and Codex both have all five (six) now**, under slightly different names. Once you see the shape is the same, you stop arguing about which tool and just design a loop that survives in either.

But — and this is the load-bearing caveat that runs through every essay he links — **the loop changes the work; it does not delete you from it.** Three problems get *sharper*, not easier, as the loop gets better: verification, comprehension, and the temptation to stop having an opinion. His closing instruction: **"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."**

This report (1) places loop engineering in the layered stack of Osmani's prior work, (2) grounds each of the six blocks in the essay that argues for it, (3) covers the backpressure / verifiable-stopping-condition layer that makes loops self-correct, (4) lays out the three risks and the human ceiling, and (5) gives **four non-trivial, ready-to-apply loop designs** — each exercising all six blocks and mapped to both Codex and Claude Code.

---

## 1. The thesis, in context

Osmani is not the originator of the framing — he credits **Peter Steinberger** ("You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents") and **Boris Cherny**, head of Claude Code ("I don't prompt Claude anymore. I have loops running that prompt Claude... My job is to write loops").

His own contribution is the *map*: showing that the capability has been productised, that the same six-part shape exists in both major tools, and — crucially — refusing the triumphalist reading. His final section is a warning, not a victory lap: **"Cherny's point isn't that the work got easier. It's that the leverage point moved."** And the line that captures the whole essay's ambivalence: **"Two people can build the exact same loop and get completely opposite results. One uses it to move faster on work they understand deeply. The other uses it to avoid understanding the work at all. The loop doesn't know the difference. You do."**

---

## 2. The layered stack: harness → loop → factory

Loop engineering does not stand alone. It is the middle floor of a three-storey structure Osmani has been building across earlier essays:

| Layer | Essay | What it is | Relationship to the loop |
|---|---|---|---|
| **Harness** (below) | *Agent Harness Engineering* | Everything around the model: system prompts, tools, sandbox, hooks, observability, context management — the per-agent substrate. Osmani's formula: **Agent = Model + Harness; "If you're not the model, you're the harness."** | The loop runs *inside* a harness. A loop is, in his words, "the harness but it runs on a timer, it spawns little helpers, and it feeds itself." |
| **Loop** (this report) | *Loop Engineering* | A scheduled, self-feeding system that finds work, dispatches it, checks it, records state, and decides the next thing — without you prompting each turn. | — |
| **Factory** (above) | *The Factory Model* | Fleets of loops running in parallel against precise specs, with quality control and reliable environment provisioning. "You are no longer just writing code. You are building the factory that builds your software." | Many loops, orchestrated. The factory is what loops become at organisational scale. |

Two harness principles carry directly into loop design. First, **every constraint should trace to a real past failure** — instruction files and skills accrete rules because mistakes justified them, not pre-emptively. Second, harness work argues *against* self-grading agents and *for* separated verification and fresh-context restarts — which is exactly the maker/checker split and the memory-on-disk pattern the loop depends on.

The factory layer adds the scaling lesson loops inherit: in *The Factory Model*, Osmani warns that an ambiguous spec "propagates through dozens of parallel autonomous runs, each one going slightly wrong in a slightly different direction," and that a flaky test a single developer would route around "become[s a] systemic blocker when you have forty agents hitting the same flaky test simultaneously. The factory stalls." Spec quality and environment reliability stop being hygiene and become throughput.

---

## 3. The six building blocks, grounded

Osmani's framing: *"A loop needs five things and then one place to remember stuff."* Here is each, with the essay that justifies it and the concrete primitive in each tool.

### Block 1 — Automations (the heartbeat)
What turns "a run you did once" into an actual loop: a scheduled, autonomous trigger that does discovery and triage and brings findings *to* you.

- **Codex:** the **Automations tab** — pick project, prompt, cadence, and whether it runs on your local checkout or a background worktree. Hits go to a **Triage inbox**; empty runs self-archive.
- **Claude Code:** **`/loop`** (re-run on a cadence), **cron** tasks, **lifecycle hooks**, or **GitHub Actions** to keep running after you close the laptop.
- The deeper primitive Osmani highlights: **`/goal`** (both tools) — keeps going until a *verifiable* condition holds, with a **separate small model checking after each turn whether you're done**, "so the agent that wrote the code isn't the one grading it." (See §4.)

### Block 2 — Worktrees (parallel without chaos)
The moment you run more than one agent, files collide — "the exact same headache as two engineers committing to the same lines." A **git worktree** is a separate working directory on its own branch sharing repo history, so one agent's edits can't touch another's checkout.

- **Codex:** built-in worktree support for concurrent threads on one repo.
- **Claude Code:** `git worktree`, a `--worktree` flag to open a session in its own checkout, and an `isolation: worktree` setting on a subagent so each helper gets a self-cleaning checkout.
- **Grounding — *The Orchestration Tax*:** worktrees remove the *mechanical* collision but not the *human* one. **"The right number of paralell agents is how many you can actually code review properly. For most of us this is a low single digit."** (typo original). You are the GIL; worktrees raise the ceiling on machines, not on your judgement.

### Block 3 — Skills (stop re-explaining your project)
A **`SKILL.md`** — a folder with instructions + metadata (plus optional scripts/assets) that the agent reads every run, so it stops guessing your conventions. Both tools use the same format; a skill auto-fires when the task matches its description, "which is the reason a tight boring description beats a clever one."

- **Grounding — *Agent Skills*:** a skill is a **workflow, not an essay** — steps with checkpoints that emit evidence and end in an exit criterion. Prose gets paraphrased and skipped; workflows get executed. Osmani's framing: a senior engineer's job is mostly the parts that don't show up in the diff (specs, tests, scope discipline), and skills make those parts non-optional "even when the engineer is a model."
- **Grounding — *Intent Debt*:** an agent "starts most sessions cold" and "will fill any gap in your intent with a plausible guess." A skill is intent written on the *outside* — the "we don't do it like this because of that one incident" — so the loop *compounds* knowledge instead of re-deriving your project from zero every cycle. Intent is the one debt your agents can't pay back for you, and its cost is now multiplied by every agent and every session.

### Block 4 — Plugins & Connectors (touch the real tools)
**Connectors are built on MCP** and let the agent read your issue tracker, query a DB, hit a staging API, post to Slack. Because both tools speak MCP, a connector written for one usually works in the other. **Plugins** bundle connectors *and* skills so a teammate installs your whole setup in one go. (Note the relationship Osmani draws: a **skill is the authoring format; a plugin is how you ship it**.)

This is the difference between an agent that says "here is the fix" and a loop that opens the PR, links the ticket, and pings the channel once CI is green — "the connectors are the reason the loop can act inside your actual environment instead of just telling you what it would do if it could."

### Block 5 — Sub-agents (keep the maker away from the checker)
**"The most useful structural thing in a loop, by far, is splitting the one who writes from the one who checks."** The model that wrote the code is too generous grading its own homework; a second agent with different instructions — and often a different model — catches what the first talked itself into.

- **Codex:** spawns subagents on request, runs them concurrently, folds results back. You define agents as **TOML files in `.codex/agents/`** — name, description, instructions, optional model and reasoning effort (so your security reviewer can be a strong model on high effort while your explorer is a fast read-only one).
- **Claude Code:** subagents in **`.claude/agents/`** plus agent teams that pass work between them. Usual split: one explores, one implements, one verifies against the spec.
- **Grounding — *Code Agent Orchestra*:** "the bottleneck is no longer generation, it's verification"; the orchestra operationalises the split as a dedicated read-only reviewer that auto-triggers after every task and runs only lint/test/security tools, so the lead receives pre-reviewed code.
- **Grounding — *AI writes code faster…* (code-review-ai):** run code through *different* LLMs (one to generate, a security-focused one to audit) to catch model-specific biases; AI review is the first-pass reviewer, never the final arbiter — **"A computer can never be held accountable. That's your job as the human in the loop."**
- Osmani's note on cost: subagents burn more tokens (each does its own model + tool work), so spend them where a second opinion is worth paying for. And `/goal` is itself this pattern applied to the *stop condition* — a fresh model decides if the loop is done.

### Block 6 — Memory (the spine)
The sixth thing, easy to dismiss as too dumb to matter: a place outside the single conversation — **a markdown file, a Linear board** — that holds what's done and what's next. "The agent forgets, the repo doesn't."

- **Grounding — *Long-Running Agents*:** this is the whole backbone. **"The model forgets. It declares 'task complete' when it isn't. It re-introduces a bug it fixed nine turns ago."** Context windows fill and, worse, **"context rot, the steady degradation of model performance as the window gets full, kicks in well before the hard limit."** And the scale argument: **"A 24-hour run is not going to fit in any context window the field has on its roadmap."** The resolution is to externalise state: **"The agent itself is amnesiac, but the filesystem isn't."** Each iteration reconstructs context by *reading disk*, not by recalling. The known failure mode to design around: across repeated resets, agents **drift** — the original goal loses fidelity — so a structured handoff/state file beats naive re-summarisation.

> **The synthesis:** Blocks 1–5 produce work; Block 6 is what lets the work survive the gaps between runs. Memory is also the block people silently drop — verify your loop has all six, not five.

### Reference: the same block in each tool

| Block | Codex | Claude Code |
|---|---|---|
| Automations | Automations tab → Triage inbox; local or background worktree | `/loop`, cron, hooks, GitHub Actions |
| Stop condition | `/goal` (verifiable, pause/resume/clear) | `/goal` (separate model grades each turn) |
| Worktrees | Built-in worktree support | `git worktree`, `--worktree`, `isolation: worktree` |
| Skills | `SKILL.md`, invoke via `$`/`/skills` or auto-match | `SKILL.md`, same format & auto-match |
| Connectors | MCP connectors | MCP connectors |
| Sub-agents | `.codex/agents/*.toml` (per-agent model + effort) | `.claude/agents/` + agent teams |
| Memory | Markdown / Linear / external store | Markdown / Linear / external store |

---

## 4. Backpressure & verifiable stopping conditions

This is the layer raised in the article's comments (by Bilgin Ibryam, *The Generative Programmer*) and it is the mechanical heart of what makes a loop trustworthy enough to walk away from. The essay's argument, paraphrased: a coding agent is a *fast producer* and a human reviewer is a *slow consumer*; if every mistake has to reach a human, the human becomes the compiler, the linter, the test runner, and the reviewer — and that is not review, it is babysitting.

**Backpressure** is any automated signal that pushes back on bad output *before* a human spends attention on it. Its defining nuance is **timing**: a check that fires *after* the agent finishes is a passive **gate**; the *same* check becomes **backpressure** only when the agent *sees the failure while working* and reacts to it. The concrete mechanisms, layered by speed:

- **Inner loop (fast):** typecheck, lint, focused tests, build, screenshots.
- **Pre-PR (slower):** full + integration tests, structural/architecture rules, security checks.
- **Scheduled (slowest):** mutation testing, fuzzing, semantic evals, drift review.

Two design rules from the essay (paraphrased): **better feedback, not more** — signal must be informative, valid, non-redundant; "success should be compressed, failure should be actionable." And the growth heuristic: **when you correct the same agent mistake twice, turn it into backpressure** — a test, a type, a lint rule, a build check.

**How this connects to Osmani:** `/goal` keeps running "until a verifiable stopping condition holds." The *strength of that stopping condition equals the strength of the backpressure you installed.* A weak condition (compiles + existing tests pass) is exactly the green-build-is-not-enough trap. *(Caveat: the phrase "verifiable stopping condition" is Osmani's framing, not the backpressure essay's — that author never uses it. I keep them attributed separately.)*

---

## 5. What the loop still does not do for you

Osmani is emphatic that a *better* loop makes three problems *worse*, because a faster loop simply widens the gap each problem describes.

**1. Verification is still on you.** **"A loop running unattended is also a loop making mistakes unattended."** The maker/checker split exists to make the loop's "it's done" mean something — but even then, "done" is a claim, not a proof. The binding principle (verified against the article, lowercase as written): **"your job is to ship code you confirmed works."** *Code Review AI* sharpens it: by early 2026, >30% of senior devs ship mostly AI-generated code, yet AI logic errors run ~75% more frequent than human ones — "if your pull request doesn't contain evidence that it works, you're not shipping faster, you're just moving work downstream."

**2. Comprehension debt grows faster.** *Comprehension Debt* defines it as the gap between how much code exists and how much any human genuinely understands. A loop's entire purpose is to maximise the *generation rate over the evaluation rate* — so every unattended iteration adds to code-that-exists without adding to code-that-is-understood, and the gap grows at exactly the loop's throughput. Worse, the loop's own success signals (tests pass, ticket closed) are the *same* metrics that stay green while comprehension hollows out. Osmani's line: a smooth loop "just makes it grow faster unless you read what the loop made." Design implication: **spend some of the loop's speed advantage buying comprehension back** — specs, explanations, review artefacts a human actually ingests.

**3. Cognitive surrender is the comfortable failure.** *Cognitive Surrender* distinguishes healthy *offloading* (you delegate but still own the answer) from *surrender* (the AI's output quietly becomes yours and there's nothing you feel you need to check). Cited evidence: when the AI was wrong, study participants accepted the wrong answer ~73% of the time — while their confidence *rose*. A loop is structurally a surrender machine: fluent, compiling, test-passing output delivered in bulk to a tired human. The article's verdict: **"Designing the loop is the cure when you do it with judgement and the accelerant when you do it to avoid thinking, same action, opposite result."**

**The ceiling underneath all three — *The Orchestration Tax*:** even with perfect memory and perfect backpressure, throughput is bounded by *you*. **"You are the GIL of your AI agents. They all can run at once. But when any of their work needs genuine understanding of the architecture or resolving merge conflicts, that work has to acquire the lock. There is one lock. You hold it."** And: **"You can run 20 agents and feel completely busy. But thats not 20 agents worth of shipped work."** (typos original.) Cap loop concurrency to your *true* review capacity and **batch reviews** (reviewing several in one sitting is far cheaper than returning to each one cold).

---

## 6. Four loop designs you can apply now

Each design exercises **all six blocks** (verify: automation, worktree, skill, connectors, sub-agents, memory) plus an explicit **stopping condition / backpressure**, and is mapped to **both Codex and Claude Code**. They are deliberately different *shapes* — a scheduled batch, a post-CI reactor, an alert-triggered investigation, and a delta-on-merge reconciler — so they stress the blocks differently. Start with one, get it boring and trustworthy, then add a second.

> **Concurrency note (applies to all four):** keep the number of loops whose output you actually review to a low single digit (*Orchestration Tax*). These four are a portfolio to grow into, not to launch simultaneously.

---

### Loop A — Nightly dependency & security upgrade

*Shape: scheduled batch. The classic "keep the lights on" loop.*

| Block | Concrete artefact |
|---|---|
| **Automation** | **Codex:** Automation `nightly-deps`, 02:00 daily, on a background worktree → Triage inbox. **Claude:** scheduled **GitHub Action** (survives laptop-off) or overnight `/loop`. |
| **Worktree** | One worktree **per upgrade class** — `wt/patch`, `wt/minor`, `wt/major` — so a failing major bump never blocks the safe patch PRs. |
| **Skill** | `/upgrade-deps` `SKILL.md`: the package manager, the changelog-reading routine, and the *pinned-with-reason* list (e.g. "router held at 6.x — v7 needs a manual route refactor, see LIN-412"). This is intent-debt insurance. |
| **Connectors** | GitHub (open PRs) · GitHub Security Advisories / `npm audit` / `pip-audit` (MCP) · Slack (digest). |
| **Sub-agents** | **Maker** (fast model): bump versions, fix breaking changes. **Checker** (security-focused *different* model): audit the diff, run the full suite, read changelogs for *behavioural* changes a green build hides. |
| **Memory** | `deps-state.md`: what was bumped, what was deferred **and why**, so tonight's run doesn't re-attempt a deferral it already reasoned about. |
| **Stop condition** | `/goal`: "build + full tests + typecheck green AND no high/critical advisories." Self-corrects up to N attempts; otherwise files the group to Triage. Backpressure = the audit + test suite seen *during* the fix. |

---

### Loop B — Flaky-test hunter & quarantine

*Shape: reactive, fires after CI. Targets the exact thing the Factory Model says stalls a fleet.*

| Block | Concrete artefact |
|---|---|
| **Automation** | **Codex:** Automation triggered after each CI run (or hourly). **Claude:** **hook** on the CI-failure event + a `/loop` that drains the suspect queue. |
| **Worktree** | A throwaway **reproduction worktree** where the suspect test is re-run 50× in isolation, never touching anyone's branch. |
| **Skill** | `/triage-flaky` `SKILL.md`: the rerun protocol (N runs → failure rate), the quarantine convention (`@flaky` tag + ticket, *quarantine not delete* below a threshold), and what counts as "flaky" vs a real regression. |
| **Connectors** | CI API (run history + logs) · GitHub (commit the quarantine tag) · Linear (open/raise the flaky ticket) · Slack. |
| **Sub-agents** | **Maker:** reproduce, compute failure rate, classify, draft quarantine-or-fix. **Checker** (*different* model, **adversarial**): "is this *actually* flaky, or did the maker mislabel a real bug as flaky?" — verifies the stats and the classification. |
| **Memory** | Linear "Flaky tests" board + `flaky-state.md`: failure rates over time, already-quarantined tests — so it never re-triages the same test and can *detect a test getting worse*. |
| **Stop condition** | `/goal`: "suspect classified at ≥95% confidence AND either quarantined-with-ticket or fix-PR-opened-and-green." Backpressure here *is* the 50-run harness — a strong, machine-checkable signal. |

---

### Loop C — Incident → postmortem draft

*Shape: alert-triggered investigation. Deliberately shows a loop where backpressure is **soft** and a human gate is mandatory.*

| Block | Concrete artefact |
|---|---|
| **Automation** | Triggered by an **alert webhook**, not a clock. **Codex:** Automation invoked by the incident hook. **Claude:** lifecycle **hook** on the incident webhook → spawns the loop. |
| **Worktree** | A **read-only investigation worktree** checked out at the SHA that was *deployed when the incident began* (git-bisect territory) — analysis can't mutate anything. |
| **Skill** | `/draft-postmortem` `SKILL.md`: the company template, blameless-writing rules, the trace-pulling routine, and timeline-construction steps. |
| **Connectors** | Observability/logs (Datadog/Grafana MCP) · GitHub (recent deploys, `git blame`, bisect) · PagerDuty/incident tool · Google Docs (write the draft) · Slack (post to the incident channel). |
| **Sub-agents** | **Maker:** correlate logs + deploys + metrics, build the timeline, draft a root-cause hypothesis. **Checker** (*different* model, **red-team**): "what evidence *contradicts* this cause? what's a plausible alternative?" — adversarial verification of a *causal claim*. |
| **Memory** | The postmortem doc + `incidents-state.md` linking incidents → causes, so recurring causes surface ("3rd time this quarter: connection-pool exhaustion"). |
| **Stop condition** | Causal claims aren't unit-testable, so backpressure is weak: stop when **the checker can't find contradicting evidence in the logs** *and* a **human signs off before publish**. This loop is honest about where automation ends. |

---

### Loop D — Docs-drift reconciliation

*Shape: delta-on-merge. Cheap, high-trust, a good **first** loop.*

| Block | Concrete artefact |
|---|---|
| **Automation** | **Codex:** Automation weekly, or triggered on merge-to-main. **Claude:** **hook** on merge-to-main + weekly `/loop` to sweep the backlog. |
| **Worktree** | A `wt/docs` worktree so doc edits never collide with live feature branches. |
| **Skill** | `/reconcile-docs` `SKILL.md`: the doc-page → code-module map, the "examples in `/docs` must be runnable" rule, and the style guide. |
| **Connectors** | GitHub (diff since last run) · docs-site build · link-checker · Slack. |
| **Sub-agents** | **Maker:** detect code changes that invalidate docs (changed signatures, removed flags), rewrite affected pages + examples. **Checker** (*different* model): **execute** the doc code examples and diff the documented API against the *actual current source*. |
| **Memory** | `docs-state.md`: last-reconciled commit SHA **per page** + known-stale pages deferred — so each run processes only the delta. |
| **Stop condition** | `/goal`: "all changed-since-last-run pages reconciled AND all examples run AND no broken links." Backpressure = runnable examples + link checker + API-signature-matches-source check. |

---

### Why these four, not four variants of one

Osmani's own worked example is a morning triage loop. These deliberately diverge so each teaches something different:

- **A** is a *batch* loop with **strong** backpressure (tests/audit) and a model split by *security expertise*.
- **B** is *reactive* and shows **adversarial** checking — the verifier's job is to *doubt the maker's classification*.
- **C** is *event-driven* with **soft** backpressure, demonstrating that some loops must keep a mandatory human gate because the claim (causation) isn't machine-verifiable.
- **D** is a *delta* loop with the **cheapest, most trustworthy** backpressure (does the example run?) — the right place to start.

Across them the connectors differ (audit APIs vs CI vs observability vs link-checkers), the maker/checker model splits differ (security vs adversarial-classification vs red-team vs execution), and the memory artefacts differ (deferral log vs failure-rate history vs incident→cause map vs per-page SHA). That diversity is the point: a loop is a *composition* of the six blocks, not a template.

---

## 7. How to start (minimal first loop)

1. **Pick Loop D or a thin slice of A.** Low blast radius, strong machine-checkable backpressure.
2. **Write the skill first.** It is your intent, externalised — the loop re-reads it every cold start (*Intent Debt*).
3. **Add the memory file before the automation.** A loop without durable state silently re-does and drifts (*Long-Running Agents*).
4. **Wire the maker/checker split with *different* models** before you let it run unattended — the verifier is the only reason you can walk away (*Loop Engineering*, *Code Agent Orchestra*).
5. **Make the stopping condition specific and verifiable.** "Tests in `test/auth` pass and lint is clean," not "looks done." Turn every twice-corrected mistake into new backpressure.
6. **Cap concurrency to what you can truly review, and batch the reviews** (*Orchestration Tax*).
7. **Read what the loop made.** Budget some of the speed gain for comprehension, or you convert velocity straight into invisible debt (*Comprehension Debt*, *Cognitive Surrender*).

---

## 8. Closing

The leverage point moved; the accountability did not. The same six blocks that let you walk away are the ones that, used to *avoid* thinking, let your understanding rot behind a green dashboard. Osmani's last line is the right one to build by:

> **"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."**

---

## Sources

Primary article:
- Addy Osmani, **"Loop Engineering"** — addyo.substack.com/p/loop-engineering *(quotes verified against extracted text)*

Referenced essays (Osmani, addyosmani.com/blog):
- **Agent Harness Engineering** — `/agent-harness-engineering/`
- **The Factory Model** — `/factory-model/`
- **Long-Running Agents** — `/long-running-agents/` *(quotes re-confirmed word-for-word)*
- **The Orchestration Tax** — `/orchestration-tax/` *(quotes re-confirmed word-for-word; original typos preserved)*
- **Agent Skills** — `/agent-skills/` *(paraphrased)*
- **Intent Debt** — `/intent-debt/` *(paraphrased)*
- **The Code Agent Orchestra** — `/code-agent-orchestra/` *(paraphrased)*
- **AI writes code faster. Your job is still to prove it works.** — `/code-review-ai/` *(paraphrased)*
- **Comprehension Debt** — `/comprehension-debt/` *(paraphrased)*
- **Cognitive Surrender** — `/cognitive-surrender/` *(paraphrased)*

Raised in comments:
- Bilgin Ibryam (*The Generative Programmer*), **"Stop Babysitting Your Coding Agent"** — generativeprogrammer.com/p/stop-babysitting-your-coding-agent *(paraphrased; "verifiable stopping condition" is Osmani's framing, not this author's)*

Note: `addyosmani.com/blog/adversarial-code-review/` returns **404** — the maker/checker / adversarial-review material lives inside the *Loop Engineering* article and is cited there, not as a separate source.
