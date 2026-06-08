# Loop D — Docs-Drift Reconciliation

This is the **recommended FIRST loop to adopt** — the cheapest, highest-trust automation loop. It runs delta-on-merge (plus a weekly sweep): whenever code merges to main, it reconciles only the doc pages invalidated by that change, rewrites their examples, and proves every example runs and every documented API signature still matches the source. Backpressure here is cheap and strong (runnable examples + link checker + signature-matches-source check), which is exactly why it's the safest place to start.

## How to trigger

### Codex
- **Automation:** schedule weekly, or trigger on merge-to-main, running `$reconcile-docs` on a background worktree (`wt/docs`).
- **Manual:** run `$reconcile-docs` from the Codex CLI.

### Claude Code
- **One-shot:** `/reconcile-docs`
- **Looped sweep:** `/loop 7d /reconcile-docs` to clear the backlog weekly.
- **On merge:** a merge-to-main hook fires `/reconcile-docs` automatically.
- **Natural language:** "our docs are out of date, fix them", "reconcile docs", "docs are stale".

## Stop condition
ALL changed-since-last-run pages reconciled AND every doc code example runs AND no broken links AND every documented API signature matches source.

## The six building blocks
| Block | In this loop |
| --- | --- |
| Automation/cadence | Codex Automation weekly or on merge-to-main; Claude Code merge-to-main hook + `/loop 7d /reconcile-docs` weekly sweep |
| Worktrees | `wt/docs` so doc edits never collide with live feature branches |
| Skill | `reconcile-docs` — doc-page → code-module map, RUNNABLE-examples rule, style guide |
| Connectors (MCP) | GitHub (diff since last run), docs-site build, link-checker, Slack |
| Sub-agents | docs-maker (rewrites affected pages + examples) + docs-checker (DIFFERENT model: executes examples, diffs API vs source) |
| Memory | `state/docs-state.md` — last-reconciled SHA per page + deferred pages, so each run processes only the delta |

## Memory
State lives in [`state/docs-state.md`](state/docs-state.md): the last-reconciled commit SHA per page and the list of known-stale pages deferred, so every run processes only the delta.
