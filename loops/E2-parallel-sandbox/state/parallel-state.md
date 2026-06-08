# E2 parallel loop - memory

The loop reads this first and updates it last. One row per module per run, so a
re-run knows which worktree/branch handled what.

## Runs

| date | result | modules fixed | merge | notes |
|---|---|---|---|---|
| (none yet) | - | - | - | seed - run `/parallel-sandbox` or `$parallel-sandbox` |

## Module -> worktree/branch map

| module | test command | worktree branch |
|---|---|---|
| calc | `python -m unittest test_calc` | `fix/calc` |
| strings | `python -m unittest test_strings` | `fix/strings` |
| dates | `python -m unittest test_dates` | `fix/dates` |
