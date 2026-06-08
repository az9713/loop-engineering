# Loop C — Incident → Postmortem Draft

This loop turns an incident alert into a blameless postmortem draft with a root-cause hypothesis that has survived adversarial red-teaming. It is **alert-triggered** (spawned by the incident webhook, not a clock) and **human-gated**: an investigator drafts the cause read-only, a different-model redteam attacks it, and the loop then STOPS for a human to sign off. It deliberately demonstrates a loop where backpressure is SOFT — causal claims are not unit-testable — so a mandatory human gate stands in where the machine cannot close the loop.

## How to trigger

### Codex
- Wire the incident/alert webhook (PagerDuty/incident tool) to a Codex **Automation** that runs `$draft-postmortem` when an incident fires.
- Or run `$draft-postmortem` manually after an incident.

### Claude Code
- One-shot: `/draft-postmortem`.
- A **lifecycle hook on the incident webhook** that spawns the loop when an alert fires.
- Natural language, e.g. "write up the outage from last night", "draft a postmortem", "what caused the outage", "RCA for the API 5xx spike".
- NOTE: there is no `/loop` interval — this loop is **event-driven**, not scheduled.

**This loop NEVER auto-publishes.** It drafts and red-teams the cause, then stops for a human. A human MUST sign off before the postmortem is published.

## Stop condition
SOFT + human-gated. Stop when (a) the redteam can find NO contradicting evidence in the logs for the root-cause hypothesis, AND (b) a HUMAN signs off on the draft before publish. Condition (a) alone is never sufficient — causal claims are not machine-verifiable, so the human gate in (b) is mandatory.

## The six building blocks

| Block | In this loop |
| --- | --- |
| Automation/cadence | ALERT-triggered, not a clock. Codex Automation invoked by the incident hook; Claude Code lifecycle hook on the incident webhook. No fixed interval. |
| Worktrees | READ-ONLY investigation worktree at the SHA deployed when the incident began (git-bisect territory); analysis can't mutate anything. |
| Skill | `draft-postmortem` — postmortem template, blameless-writing rules, trace-pulling routine, timeline-construction steps. |
| Connectors (MCP) | Observability/logs (Datadog/Grafana), GitHub (deploys, `git blame`, bisect), PagerDuty/incident tool, Google Docs (write draft), Slack (incident channel). |
| Sub-agents | `incident-investigator` (maker) correlates logs/deploys/metrics + builds timeline + drafts hypothesis & postmortem; `incident-redteam` (checker, DIFFERENT model) attacks the causal claim and hunts contradicting evidence. |
| Memory | The postmortem doc + `state/incidents-state.md` linking incidents → causes so recurring causes surface. |

## Memory
Recurring-cause memory lives in [`state/incidents-state.md`](state/incidents-state.md) — it links each incident to its root cause so patterns (e.g. "3rd time this quarter: connection-pool exhaustion") surface across incidents. It is written only AFTER a human signs off.
