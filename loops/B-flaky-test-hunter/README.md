# Loop B — Flaky-Test Hunter & Quarantine

A reactive automation loop that fires after a CI run, hunts the test that fails intermittently, and resolves it before it stalls a parallel agent fleet. It pulls the suspect from CI, spins a throwaway worktree, reruns the test 50x to get a real failure rate, has an adversarial sub-agent confirm the classification, then either quarantines the test with a `@flaky` tag + Linear ticket or opens a green fix-PR — recording everything to memory so it never re-triages the same test and can detect a test getting worse.

## How to trigger

### Codex

- **Automation:** triggered after each CI run (or hourly) with prompt `$triage-flaky` on a background worktree.
- **Manual:** run `$triage-flaky` directly.
- Sub-agents (`flaky-maker`, `flaky-checker`) auto-spawn from `.codex/agents/`.

### Claude Code

- **One-shot:** `/triage-flaky`
- **Looped:** `/loop 1h /triage-flaky` (drains the suspect queue)
- **Hook:** a hook on the CI-failure event kicks off the loop automatically.
- **Natural language:** e.g. "this test keeps failing randomly, triage it" or "is this test flaky?"

## Stop condition

Suspect classified at **>=95% confidence** AND either **quarantined-with-ticket** OR **fix-PR-opened-and-green**. The 50-run reproduction harness is the backpressure — a strong, machine-checkable signal.

## The six building blocks

| Block | In this loop |
| --- | --- |
| Automation/cadence | Codex Automation after each CI run (or hourly); Claude CI-failure hook + `/loop 1h /triage-flaky`. |
| Worktrees | A throwaway repro worktree where the suspect is rerun 50x in isolation, never touching anyone's branch. |
| Skill | `triage-flaky` — the rerun protocol, quarantine convention, and flaky-vs-regression rules. |
| Connectors (MCP) | CI API (run history + logs), GitHub (commit the tag), Linear (raise the ticket), Slack (notify). |
| Sub-agents | `flaky-maker` (reproduce + classify) and `flaky-checker` (different model, adversarial verify). |
| Memory | Linear "Flaky tests" board + `state/flaky-state.md` — rates over time, already-quarantined tests. |

## Memory

State lives in [`state/flaky-state.md`](state/flaky-state.md): failure rates over time and already-quarantined tests, so the loop never re-triages the same test and can detect one getting worse.
