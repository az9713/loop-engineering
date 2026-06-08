# Loop E — Demo Sandbox (zero-dependency quick loop test)

The other four loops (A–D) are built to touch your real systems (GitHub, CI, Slack, observability) through MCP connectors, so none runs fully end-to-end without setup. **This loop has none of that.** Its entire world is the local filesystem and Python's stdlib `unittest`, so you can watch a loop actually converge in seconds — on any machine with Python.

It ships **deliberately broken code** (`sandbox/calc.py`, three bugs) with passing-spec tests (`sandbox/test_calc.py`). The loop's job: make the tests pass.

## The stop condition

```
cd loops/E-demo-sandbox/sandbox
python -m unittest test_calc        # exit 0 == done
```

That exit code is the whole backpressure signal: **RED → keep going, GREEN → stop.**

## Try it in 30 seconds (no agent — prove the harness)

```bash
cd loops/E-demo-sandbox/sandbox
python -m unittest test_calc -v     # see 3 FAILs, exit 1  ← this is the RED the loop reacts to
```

You'll see `add` returns -1 not 5, `is_even(4)` is False, `factorial(5)` is 24 not 120.

## Run the loop — Claude Code

- **One-shot:** `/demo-loop`
- **Natural language:** *"run the quick loop test"* / *"make the sandbox tests pass"* (auto-triggers the skill)
- **On a cadence:** `/loop 10m /demo-loop` — it idles GREEN until you `reset`, then reacts on the next tick

It dispatches **demo-checker** (runs the tests, no edit tool) → **demo-maker** (fixes `calc.py`) → **demo-checker** again, looping until GREEN (max 5 attempts), then updates `state/demo-state.md`.

## Run the loop — Codex

- **Skill:** `$demo-loop` (or `/skills` → demo-loop)
- **Natural language:** *"run the demo loop"*
- Sub-agents `demo-maker` / `demo-checker` spawn from `.codex/agents/`.

## Reset (run it again)

```
pwsh loops/E-demo-sandbox/reset.ps1     # Windows
bash loops/E-demo-sandbox/reset.sh      # macOS/Linux
```
Restores the broken `calc.py` from `.broken/calc.py` so the loop has something to do again.

## How it maps to the six blocks

| Block | In this loop |
|---|---|
| **Automation** | `/demo-loop` / `$demo-loop` one-shot, or `/loop 10m /demo-loop` |
| **Worktrees** | ➖ **dropped** — one agent fixes one file; no parallel collision to isolate |
| **Skill** | `demo-loop` (workflow + stop condition) |
| **Connectors** | ➖ **dropped** — fully local; touches no external tool *(this is the only thing separating it from Loops A–D)* |
| **Sub-agents** | `demo-maker` (edits) vs `demo-checker` (runs tests, no edit) |
| **Memory** | `state/demo-state.md` (records each run + known fixes) |

This is the **irreducible core** of a loop. Loops A–D are this plus worktrees (when there's parallelism) plus connectors (to act on your real systems). See [`../COMPONENT-MAPPING.md`](../COMPONENT-MAPPING.md) for why dropping worktrees/connectors is the right call when there's no collision and no external tool.

## What to watch for (the teaching moment)

The point isn't the bug fix — it's the **loop shape**: a verifiable RED/GREEN signal drives an autonomous fix/verify cycle, the *checker can't edit what it grades*, and the run is written to memory so the next run starts informed. That's every loop in miniature.
