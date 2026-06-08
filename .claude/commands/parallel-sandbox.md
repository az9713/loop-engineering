---
description: Run the parallel-worktree sandbox loop (3 makers in 3 worktrees → integrator merges → full suite) — a quick test where worktrees are load-bearing
---

Invoke the `parallel-sandbox` skill and run it to its stop condition: after merging the per-module branches, `python -m unittest discover -p "test_*.py"` (in `loops/E2-parallel-sandbox/sandbox/`) exits 0.

Fan out one `parallel-module-maker` per module (`calc`, `strings`, `dates`) into its own git worktree/branch, then use `parallel-integrator` to merge and run the full suite. The integrator has no edit tool — it integrates and gates, it does not hand-fix code.

Verify the plumbing first if you like: `python loops/E2-parallel-sandbox/verify_pipeline.py`.
Looped usage: `/loop 15m /parallel-sandbox`. Reset with `loops/E2-parallel-sandbox/reset.ps1` (or `reset.sh`).

$ARGUMENTS
