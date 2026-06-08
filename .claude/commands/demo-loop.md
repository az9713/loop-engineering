---
description: Run the zero-dependency sandbox loop (fix broken code until the tests pass) — a quick end-to-end loop test
---

Invoke the `demo-loop` skill and run it to its stop condition: `python -m unittest test_calc` (inside `loops/E-demo-sandbox/sandbox/`) exits 0.

Use the `demo-maker` and `demo-checker` sub-agents for the fix/verify split — the checker runs the tests and has no edit tool, so it cannot grade its own work.

Looped usage: `/loop 10m /demo-loop` runs it on a cadence (it will idle GREEN until you `reset` the sandbox, then react). Reset with `loops/E-demo-sandbox/reset.ps1` (or `reset.sh`).

$ARGUMENTS
