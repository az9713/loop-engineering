# Project status

_Last updated: 2026-06-08._

A snapshot of what exists in this repo and the known open items, so anyone (human or agent) can pick it up cold.

## Where we stand

Complete and pushed to [`az9713/loop-engineering`](https://github.com/az9713/loop-engineering) (public, branch `main`). Working tree clean; no stray git worktrees or branches.

### Built

1. **Synthesis report** — [`Loop-Engineering-Synthesis-Report.md`](./Loop-Engineering-Synthesis-Report.md). Grounds Osmani's *Loop Engineering* in 12 sources (the article + 11 referenced essays + the backpressure piece). Strict quote-fidelity policy: verbatim only where verifiable, everything else paraphrased.
2. **Knowledge graph** — `graphify-out/` (graph.html, graph.json, GRAPH_REPORT.md). 62 nodes / 86 edges / 7 communities. Live page via GitHub Pages: <https://az9713.github.io/loop-engineering/> (root `index.html` embeds the graph).
3. **Latent-structure analysis** — [`Graph-Structure-Analysis.md`](./Graph-Structure-Analysis.md). The barbell topology, two orthogonal spines, gated risks, integration basin.
4. **Four applied loops (A–D)** — scaffolded for **both Codex and Claude Code** in project scope (`.claude/` + `.codex/`), one folder each under [`loops/`](./loops/). See [`loops/README.md`](./loops/README.md) and [`loops/COMPONENT-MAPPING.md`](./loops/COMPONENT-MAPPING.md).
   - A `upgrade-deps` · B `triage-flaky` · C `draft-postmortem` (human-gated) · D `reconcile-docs`
   - Each: skill (mirrored across both tools), slash command, maker/checker sub-agents, per-loop README, seed memory state file.
5. **Two zero-dependency sandbox loops** — runnable with no connectors:
   - **E** [`loops/E-demo-sandbox/`](./loops/E-demo-sandbox/) — the irreducible 4-block core (drops worktrees + connectors).
   - **E2** [`loops/E2-parallel-sandbox/`](./loops/E2-parallel-sandbox/) — adds **worktrees as a load-bearing block**; `verify_pipeline.py` proves convergence with no agent.
6. **Project instructions** — `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code) index every skill/agent and the trigger conventions.

### Verified working

- `python loops/E2-parallel-sandbox/verify_pipeline.py` → exits 0 (RED → 3 isolated fixes → 3 clean merges → full suite green).
- Live agent runs of `parallel-sandbox`: converged in **1 round** (clean), and in **2 rounds** with a staged under-fix (integrator caught the premature "done", re-dispatched only the failed module). Both left `main` pristine.
- All `.codex/agents/*.toml` parse; Claude checker agents have no `Edit` tool; skill mirrors are byte-identical.

### Excluded from the repo (by design)

`.gitignore` keeps out: verbatim third-party source (`raw_text.txt`, `*.mhtml` — attributed by link instead), graphify internals (`graphify-out/.graphify_*`, `cache/`, `cost.json`), `__pycache__/`, and local scratch (`.ignore/`).

## Loose ends

1. **Codex skill discovery path is unconfirmed.** `.codex/skills/<slug>/SKILL.md` follows the SKILL.md convention from Osmani's essay, but exact project-scope skill discovery varies by Codex version. **Action:** run `/skills` in your Codex to confirm pickup; if not found, the `.codex/agents/*.toml` sub-agents and `AGENTS.md` still work, and skills can be relocated to wherever your Codex scans.
2. **Codex model ids are placeholders.** Every `.codex/agents/*.toml` uses `model = "gpt-5-codex"`. **Action:** set to a model your Codex actually provides. (Claude agents use `sonnet`/`opus` aliases and resolve fine.)
3. **Loops A–D are starter kits, not turnkey.** The skills encode the workflow + maker/checker split, but the MCP connectors (GitHub, CI, Slack, observability, Linear, etc.) are **not wired**, and real package-manager / CI / test commands need filling in per repo. **Action:** wire connectors and concrete commands before relying on A–D. Start with D (`reconcile-docs`) — cheapest, most trustworthy backpressure.
4. **`--inject-fault` trigger is not built.** The under-fix / multi-round runs were **hand-staged** by the operator, not a skill feature. There is no reproducible way to *summon* iteration on demand. **Action (optional):** add a documented fault-injection flag (`/parallel-sandbox --inject-fault <module>`) to the skill so the 2-round demo becomes a real, repeatable trigger.
5. **Loop C never auto-publishes** — by design, a postmortem requires human sign-off. Keep that gate when wiring it up.

## Quick start for the next session

- Watch a loop converge, no setup: `python loops/E2-parallel-sandbox/verify_pipeline.py`, or `/demo-loop` / `/parallel-sandbox` in Claude Code.
- Re-arm a sandbox after a run: `loops/E?-*/reset.ps1` (or `reset.sh`).
- Explore the concept graph: open <https://az9713.github.io/loop-engineering/>.
