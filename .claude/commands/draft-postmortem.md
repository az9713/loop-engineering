---
description: Draft a blameless postmortem with a red-teamed root cause (human sign-off required before publish)
---
Invoke the `draft-postmortem` skill and run it to its stop condition.

Concretely: read `loops/C-incident-postmortem/state/incidents-state.md` for recurring causes, identify the SHA deployed when the incident began, open a READ-ONLY investigation worktree at that SHA, dispatch `incident-investigator` to correlate logs/deploys/metrics and draft a timeline + root-cause hypothesis + postmortem, then dispatch `incident-redteam` (a different model) to attack the cause and hunt for contradicting evidence. If contradicted, loop back and revise; if not, mark the draft "ready for human review", post it to Google Docs + the incident Slack channel as a DRAFT, and STOP.

This loop is **alert-triggered**, not interval-driven — there is no `/loop` cadence; it is spawned by the incident webhook (or run manually after an incident).

**Publishing requires human approval.** This loop NEVER auto-publishes — causal claims are not machine-verifiable, so a human MUST sign off before the postmortem is published. Only after that sign-off do you record the incident → cause mapping in `incidents-state.md`.

$ARGUMENTS
