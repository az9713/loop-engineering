# Loop E2 — Parallel Sandbox (worktrees are load-bearing here)

The sibling of [Loop E](../E-demo-sandbox/README.md). Loop E is sequential, so it
*drops* worktrees. **E2 is parallel**, so worktrees earn their place: it fixes
three independent modules **at the same time**, each in its **own git worktree on
its own branch**, then merges and runs the full suite. Still **zero connectors** —
fully local.

This is the before/after teaching pair:

| | blocks | worktrees | why |
|---|---|---|---|
| **E** `demo-loop` | 4 (core) | ➖ dropped | one maker, one file — no collision |
| **E2** `parallel-sandbox` | 5 | ✅ load-bearing | three makers editing concurrently — worktrees stop them colliding |

## The partition (and why it's by module)

Three modules, one bug each, **one module per worktree**:

| module | bug | worktree branch | local gate |
|---|---|---|---|
| `calc.py` | `add` subtracts | `fix/calc` | `python -m unittest test_calc` |
| `strings.py` | `shout` lowercases, drops `!` | `fix/strings` | `python -m unittest test_strings` |
| `dates.py` | `is_weekend` uses `> 5` not `>= 5` | `fix/dates` | `python -m unittest test_dates` |

The branches touch **disjoint files**, so merging all three is **conflict-free**.
That's the whole reason to partition by module: worktrees isolate writers *during*
the work, but they don't merge divergent edits *afterward* — so split the work
along the boundary the merge respects (one file per worktree), never multiple
edits to one shared file.

## Stop condition

After merging the branches, the **full** suite passes:
```
cd loops/E2-parallel-sandbox/sandbox
python -m unittest discover -p "test_*.py"      # exit 0 == done
```
Each worktree also has a local pre-merge gate (its own module's test).

## Prove the plumbing in 5 seconds (no agent)

```
python loops/E2-parallel-sandbox/verify_pipeline.py
```
This stands up a throwaway git repo, creates the three worktrees, applies a
reference fix in each, merges them, and asserts the full suite goes green —
**without touching your real repo** (everything happens in a temp dir that is
removed at the end). It's the deterministic proof that the worktree→merge→suite
pipeline converges. *(Verified: RED baseline → 3 isolated fixes → 3 clean merges → full suite green.)*

## Run the loop — Claude Code

- **One-shot:** `/parallel-sandbox`
- **Natural language:** *"run the parallel worktree loop"*
- **On a cadence:** `/loop 15m /parallel-sandbox`

It fans out one `parallel-module-maker` per module (each in its own worktree via
`isolation: worktree` / `git worktree add`), then `parallel-integrator` merges the
branches and runs the full suite. The integrator has **no edit tool** — it
integrates and gates, it never hand-fixes code.

## Run the loop — Codex

- **Skill:** `$parallel-sandbox` (or `/skills` → parallel-sandbox)
- Sub-agents `parallel-module-maker` / `parallel-integrator` spawn from `.codex/agents/`; run the makers on background worktrees.

## Reset (run it again)

```
pwsh loops/E2-parallel-sandbox/reset.ps1     # Windows
bash loops/E2-parallel-sandbox/reset.sh      # macOS/Linux
```

## What to watch for (the teaching moment)

E2 shows worktrees doing their *actual* job: **isolating concurrent writers**.
Note what makes it work — the work is partitioned so the merge is clean, the
local module gate is separate from the full-suite integration gate, and the
integrator (a different model, no edit tool) is the one that certifies the merged
result. Compare with E: same machinery minus the parallelism, minus the worktree.
See [`../COMPONENT-MAPPING.md`](../COMPONENT-MAPPING.md).
