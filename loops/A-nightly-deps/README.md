# Loop A — Nightly Dependency & Security Upgrade

A scheduled nightly "keep the lights on" loop. Every night it reads its memory of what was already bumped and deferred, enumerates outdated dependencies and security advisories, splits the work into patch/minor/major worktrees, and for each class runs a maker (bump + fix) followed by a security-focused checker (full test suite + audit + changelog read). Green classes become PRs (one per upgrade class); red classes self-correct up to 3 times and then go to a human triage inbox. It never re-attempts a deferral it has already reasoned about.

## How to trigger

### Codex
- Create an Automation in the **Automations** tab with prompt `$upgrade-deps`, **daily** cadence, running on a **background worktree** (survives the loop running unattended at night). Name it `nightly-deps`, scheduled for 02:00.
- Or run `$upgrade-deps` manually anytime.
- Sub-agents (`deps-maker`, `deps-checker`) auto-spawn from `.codex/agents/`.

### Claude Code
- One-shot: `/upgrade-deps`.
- Looped: `/loop 1d /upgrade-deps` re-runs it daily.
- Or just say a trigger phrase — e.g. "upgrade our dependencies and open PRs" — to auto-fire the `upgrade-deps` skill.
- For laptop-off runs, schedule it via a **GitHub Action** (cron) so the loop survives the machine being asleep.

## Stop condition
For every upgrade class: build + full test suite + typecheck are green AND no high/critical advisories remain. The maker self-corrects up to 3 attempts; otherwise the group is filed to the Triage inbox for a human. Backpressure is the audit + test suite the maker sees DURING the fix, not after.

## The six building blocks
| Block | Concrete artefact |
| --- | --- |
| Automation/cadence | Codex Automation `nightly-deps` @ 02:00 daily on a background worktree → Triage inbox; or Claude Code GitHub Action / `/loop 1d /upgrade-deps` |
| Worktrees | `wt/patch`, `wt/minor`, `wt/major` — one per upgrade class so a failing major never blocks safe patch PRs |
| Skill | `.claude/skills/upgrade-deps/SKILL.md` (+ identical `.codex/skills/...`) — package manager, changelog routine, pinned-with-reason list |
| Connectors (MCP) | GitHub (open PRs), GitHub Security Advisories / `npm audit` / `pip-audit`, Slack (digest) |
| Sub-agents | `deps-maker` (fast — bump + fix) and `deps-checker` (stronger, high reasoning — audit + test + changelog) |
| Memory | `loops/A-nightly-deps/state/deps-state.md` — what was bumped, what was deferred AND why |

## Memory
Persistent state lives in [`state/deps-state.md`](state/deps-state.md): the log of upgraded packages and the "do not re-attempt" deferral list (with reasons + tickets) so tonight's run never re-litigates a deferral it already reasoned about.
