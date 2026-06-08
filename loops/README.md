# Loop Engineering — Applied Loops (Codex + Claude Code)

Four ready-to-run automation loops, scaffolded for **both Codex and Claude Code** in **project scope** (the `.claude/` and `.codex/` directories at the repository root — nothing is installed globally). Each loop implements all six building blocks from the [synthesis report](../Loop-Engineering-Synthesis-Report.md) §6: **automation · worktrees · skill · connectors · sub-agents · memory**, plus a verifiable stop condition.

> These are **starter kits**, not turnkey systems. The skills and sub-agents encode the workflow and the maker/checker split; you wire the connectors (MCP servers for GitHub/CI/Slack/etc.), set real package managers and CI commands, and confirm the model ids your Codex/Claude Code provide. Treat each `SKILL.md` as the source of truth and edit it for your repo.

## The four loops

| Loop | Slug | Shape | Sub-agents (maker → checker) | Stop condition |
|---|---|---|---|---|
| **A** — Nightly dependency & security upgrade | `upgrade-deps` | scheduled batch | `deps-maker` → `deps-checker` (security, stronger model) | build + tests + typecheck green **and** no high/critical advisories |
| **B** — Flaky-test hunter & quarantine | `triage-flaky` | reactive (post-CI) | `flaky-maker` → `flaky-checker` (adversarial) | classified ≥95% **and** quarantined-with-ticket or fix-PR-green |
| **C** — Incident → postmortem draft | `draft-postmortem` | alert-triggered | `incident-investigator` → `incident-redteam` | redteam finds no contradiction **and** human sign-off (never auto-publishes) |
| **D** — Docs-drift reconciliation | `reconcile-docs` | delta-on-merge | `docs-maker` → `docs-checker` (executes examples) | pages reconciled **and** every example runs **and** no broken links |

**Want to just watch a loop run, with zero setup?** → **[Loop E — Demo Sandbox](./E-demo-sandbox/README.md)**. It needs no GitHub/CI/MCP — it fixes deliberately-broken code until `python -m unittest` passes, so you can see the maker/checker/memory/stop-condition machinery converge in seconds. (A–D below touch your real systems and need their connectors wired first.)

**Start with Loop D** (of the real ones) — its backpressure (do the doc examples run?) is the cheapest and most trustworthy, so it's the safest first loop to let run unattended.

> 📐 **[How each loop maps to Addy's six building blocks →](./COMPONENT-MAPPING.md)** — a full component matrix plus an honest breakdown of where a block takes a non-obvious form (Loop C's event trigger and read-only worktree), where it's the weakest link, and why plugin packaging is intentionally skipped in project scope.

---

## How to trigger — Claude Code

All four are installed as project **skills** (`.claude/skills/<slug>/`), **slash commands** (`.claude/commands/<slug>.md`), and **sub-agents** (`.claude/agents/`). Three ways to fire one:

1. **Natural language** — just describe the task; the skill auto-triggers on its description. e.g. *"our docs are out of date, fix them"* → `reconcile-docs`.
2. **Slash command (one-shot)** — `/upgrade-deps`, `/triage-flaky`, `/draft-postmortem`, `/reconcile-docs`.
3. **On a cadence with `/loop`** — `/loop <interval> <command>` re-runs it on a timer:
   - `/loop 1d /upgrade-deps` — nightly dependency sweep
   - `/loop 1h /triage-flaky` — drain the flaky queue hourly
   - `/loop 7d /reconcile-docs` — weekly docs reconciliation
   - Loop C is **event-driven** (alert webhook), so it has no `/loop` interval — wire it to a hook instead.

For laptop-off runs, schedule the command via **GitHub Actions** (or the built-in scheduler). The maker/checker sub-agents in `.claude/agents/` are spawned automatically by each skill — the checker uses a stronger model and has **no `Edit` tool** so it cannot grade its own work.

## How to trigger — Codex

All four are installed as project **skills** (`.codex/skills/<slug>/`) and **sub-agents** (`.codex/agents/*.toml`). Three ways:

1. **Natural language** — describe the task; Codex runs the matching skill by description.
2. **Skill invocation** — `$upgrade-deps` (or `/skills` to pick one).
3. **Automations tab** — create an Automation with the prompt `$<slug>`, pick the cadence, and run it on a **background worktree** so findings land in the **Triage inbox**:
   - `$upgrade-deps` — daily at 02:00
   - `$triage-flaky` — after each CI run (or hourly)
   - `$reconcile-docs` — weekly or on merge-to-main
   - `$draft-postmortem` — triggered by your incident/alert webhook (not a clock)

Codex spawns the sub-agents defined in `.codex/agents/` when the skill asks; each has its own `model` and `reasoning_effort` (the checker runs at `high`).

> **Set your model ids.** The `.codex/agents/*.toml` files use a placeholder `model = "gpt-5-codex"`. Change it to a model your Codex actually provides.

---

## Per-loop details

Each loop has its own folder with a README (trigger steps, the six-block table, the stop condition) and a seed **memory** file under `state/`:

- [`A-nightly-deps/`](./A-nightly-deps/README.md) — memory: `state/deps-state.md`
- [`B-flaky-test-hunter/`](./B-flaky-test-hunter/README.md) — memory: `state/flaky-state.md`
- [`C-incident-postmortem/`](./C-incident-postmortem/README.md) — memory: `state/incidents-state.md`
- [`D-docs-drift/`](./D-docs-drift/README.md) — memory: `state/docs-state.md`
- [`E-demo-sandbox/`](./E-demo-sandbox/README.md) — **zero-dependency quick test** · memory: `state/demo-state.md` (deliberately drops worktrees + connectors)

## The maker/checker discipline (why the checker can't edit)

Every loop splits the agent that *writes* from the agent that *checks*, on a **different model**, because a model grades its own work too generously. In these scaffolds the checker sub-agents are deliberately given **read + run** tools only (no `Edit`/write) — they can run tests, audits, link-checkers, and execute examples to produce a PASS/FAIL verdict, but they cannot quietly "fix" the thing they're supposed to judge. That separation is what lets the loop's *"it's done"* mean something, and it's the only reason you can walk away from a running loop.
