# CLAUDE.md — project instructions

This project hosts a synthesis of "Loop Engineering" plus four **applied automation loops** scaffolded for Claude Code (and Codex) in **project scope**. Everything lives under `.claude/` and `.codex/` at the repo root — nothing is installed globally.

## Automation loops

Each loop is installed three ways: a **skill** (`.claude/skills/<slug>/SKILL.md`), a **slash command** (`.claude/commands/<slug>.md`), and a **maker/checker sub-agent pair** (`.claude/agents/`).

| Command | Skill triggers (natural language) | Cadence example |
|---|---|---|
| `/upgrade-deps` | "upgrade dependencies", "bump deps", "security upgrade", "patch vulnerabilities" | `/loop 1d /upgrade-deps` |
| `/triage-flaky` | "flaky test", "triage flaky", "test fails intermittently" | `/loop 1h /triage-flaky` |
| `/draft-postmortem` | "draft a postmortem", "root cause analysis", "RCA", "what caused the outage" | event-driven (hook) — no `/loop` |
| `/reconcile-docs` | "docs are stale", "doc drift", "update docs to match code" | `/loop 7d /reconcile-docs` |
| `/demo-loop` | "run the demo loop", "quick loop test", "make the sandbox tests pass" | `/loop 10m /demo-loop` |
| `/parallel-sandbox` | "parallel loop test", "run the parallel sandbox", "worktree loop demo" | `/loop 15m /parallel-sandbox` |

**Quick test:** `/demo-loop` runs a zero-dependency sandbox loop (fixes broken code until `python -m unittest` passes) — the fastest way to see the machinery work end-to-end with no connectors. See [`loops/E-demo-sandbox/`](./loops/E-demo-sandbox/README.md). `/parallel-sandbox` is the parallel variant where worktrees are load-bearing — see [`loops/E2-parallel-sandbox/`](./loops/E2-parallel-sandbox/README.md).

**Three ways to fire a loop:** (1) describe the task in natural language → the skill auto-triggers; (2) the slash command for a one-shot run; (3) `/loop <interval> /<command>` to run it on a cadence. For laptop-off runs, schedule the command via GitHub Actions.

## Sub-agents (`.claude/agents/`)

Each loop spawns a **maker** (writes the change, `model: sonnet`) and a **checker** (verifies it, `model: opus`). The checker sub-agents have **no `Edit` tool** by design — they run tests/audits/link-checkers and execute examples to produce a PASS/FAIL verdict, but cannot modify the work they grade. This maker/checker split is what lets a running loop's *"it's done"* be trustworthy.

- `deps-maker` / `deps-checker` · `flaky-maker` / `flaky-checker` · `incident-investigator` / `incident-redteam` · `docs-maker` / `docs-checker` · `demo-maker` / `demo-checker` · `parallel-module-maker` / `parallel-integrator`

## Working conventions

- **Don't let the writer certify its own work.** Always route verification through the checker sub-agent.
- **Memory lives on disk.** Each loop reads/updates `loops/<X>/state/` — read it first to skip deferred work, update it last.
- **Loop C (`/draft-postmortem`) never auto-publishes** — human sign-off is mandatory before a postmortem leaves draft.
- **Start with `/reconcile-docs`** — its backpressure (do the doc examples run?) is the cheapest and most trustworthy, so it's the safest loop to run unattended first.

See [`loops/README.md`](./loops/README.md) for the full trigger guide, and [`Loop-Engineering-Synthesis-Report.md`](./Loop-Engineering-Synthesis-Report.md) §6 for the design rationale.
