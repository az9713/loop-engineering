# Docs-Drift State (memory)

This file is the loop's memory. Each run reads the last-reconciled commit SHA **per page** to fetch only the code diff since then, and records any pages deliberately deferred. Update it at the end of every run.

## Last reconciled (per page)
| doc page | last-reconciled SHA | date |
| --- | --- | --- |
| docs/getting-started.md | abc1234 | 2026-06-01 |

## Known stale (deferred)
| doc page | reason | ticket |
| --- | --- | --- |
| docs/advanced/plugins.md | plugin API mid-refactor; defer until lands | DOCS-142 |
