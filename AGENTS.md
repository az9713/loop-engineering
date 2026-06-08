# AGENTS.md — Codex project instructions

This project hosts a synthesis of "Loop Engineering" plus four **applied automation loops** scaffolded for Codex (and Claude Code) in **project scope**. Nothing here is installed globally — everything lives under `.codex/` and `.claude/` at the repo root.

## Project skills (`.codex/skills/`)

Invoke with `$<slug>` or `/skills`, or just describe the task in natural language and Codex will run the matching skill by its description.

| Skill | Run it for… | Natural-language triggers |
|---|---|---|
| `$upgrade-deps` | nightly dependency & security upgrades | "upgrade dependencies", "bump deps", "security upgrade", "patch vulnerabilities" |
| `$triage-flaky` | reproduce, classify, and quarantine flaky tests | "flaky test", "triage flaky", "test fails intermittently" |
| `$draft-postmortem` | draft a blameless, red-teamed postmortem | "draft a postmortem", "root cause analysis", "RCA", "what caused the outage" |
| `$reconcile-docs` | reconcile drifted docs with the source | "docs are stale", "doc drift", "update docs to match code" |
| `$demo-loop` | **zero-dependency quick test** — fix broken code until tests pass | "run the demo loop", "quick loop test", "make the sandbox tests pass" |

## Sub-agents (`.codex/agents/*.toml`)

Each loop defines a **maker** and a **checker**, spawned by the skill. The maker writes; the checker — on a different model at `reasoning_effort = "high"` — verifies and returns a PASS/FAIL verdict. The checker must **not** edit code it is judging. Set the `model` field in each TOML to a model your Codex provides (placeholder is `gpt-5-codex`).

- `deps-maker` / `deps-checker`
- `flaky-maker` / `flaky-checker`
- `incident-investigator` / `incident-redteam`
- `docs-maker` / `docs-checker`
- `demo-maker` / `demo-checker` (sandbox quick test)

## Running them as loops

Create an **Automation** (Automations tab) with the prompt `$<slug>`, choose a cadence, and run it on a **background worktree** so findings land in the **Triage inbox**:
- `$upgrade-deps` — daily 02:00 · `$triage-flaky` — after each CI run · `$reconcile-docs` — weekly / on merge-to-main · `$draft-postmortem` — wired to your incident webhook (event-driven, no clock).

## Working conventions

- **Maker/checker is non-negotiable.** Never let the agent that wrote a change be the one that certifies it. The checker's verdict is what makes "done" mean something.
- **Memory lives on disk.** Each loop reads and updates its state file under `loops/<X>/state/`. Always read it first (to skip deferred work) and update it last.
- **Worktrees for isolation.** Parallel work goes in separate worktrees so agents don't collide.
- **Loop C never auto-publishes.** A postmortem requires human sign-off before it leaves the draft stage.

See [`loops/README.md`](./loops/README.md) for the full trigger guide and per-loop details.
