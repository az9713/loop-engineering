# E2 parallel loop - memory

The loop reads this first and updates it last. One row per module per run, so a
re-run knows which worktree/branch handled what.

## Runs

| date | result | modules fixed | merge | notes |
|---|---|---|---|---|
| 2026-06-08 | PASS | calc, strings, dates | 3 clean (0 conflicts) | 3 worktrees fanned out, each module GREEN on its own gate, full suite GREEN after merge; worktrees + branches cleaned up |
| 2026-06-08 | PASS (2 rounds) | calc, strings, dates | clean | under-fix demo: R1 gate FAILED on dates (premature done caught by integrator); R2 re-dispatched dates only -> correct -> full suite GREEN |

## Module -> worktree/branch map

| module | test command | worktree branch |
|---|---|---|
| calc | `python -m unittest test_calc` | `fix/calc` |
| strings | `python -m unittest test_strings` | `fix/strings` |
| dates | `python -m unittest test_dates` | `fix/dates` |
