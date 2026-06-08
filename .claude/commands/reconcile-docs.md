---
description: Run the autonomous docs-drift reconciliation loop (rewrite affected pages, verify every example runs)
---
Invoke the `reconcile-docs` skill and run it to the stop condition: ALL changed-since-last-run pages reconciled, every doc code example runs, no broken links, and every documented API signature matches source.

Follow the skill's workflow exactly — read `loops/D-docs-drift/state/docs-state.md` for the last-reconciled SHA per page, diff the CODE since then, map changed modules to affected pages, work in a `wt/docs` worktree, dispatch docs-maker to rewrite and docs-checker (a different model) to EXECUTE every example and diff the documented API against source, run the link checker, open a docs PR, and update `docs-state.md` per page.

## Looped usage
- Sweep the backlog weekly: `/loop 7d /reconcile-docs`
- Also runs automatically on merge-to-main via a hook.

$ARGUMENTS
