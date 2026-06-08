---
description: Run the autonomous flaky-test triage loop (50x reproduction, adversarial classify, quarantine + ticket)
---

Invoke the `triage-flaky` skill and run it to the stop condition: a suspect test classified at >=95% confidence AND either quarantined-with-ticket or a green fix-PR. Drain the suspect queue, but never re-triage a test already quarantined in `loops/B-flaky-test-hunter/state/flaky-state.md`.

The loop:
1. Read `flaky-state.md` memory.
2. Pull the suspect test + CI history via the CI connector.
3. Spin a throwaway reproduction worktree.
4. Dispatch `flaky-maker` to rerun 50x, compute the failure rate, and classify.
5. Dispatch `flaky-checker` (adversarial, different model) to CONFIRM/REJECT.
6. If flaky: commit the `@flaky` tag + open a Linear ticket. If real regression: open a fix PR.
7. Update `flaky-state.md` and notify Slack.

## Looped usage

`/loop 1h /triage-flaky`

$ARGUMENTS
