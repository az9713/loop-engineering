# Graph Report - .  (2026-06-08)

## Corpus Check
- Corpus is ~7,250 words - fits in a single context window. You may not need a graph.

## Summary
- 62 nodes · 86 edges · 7 communities
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.9)
- Token cost: 0 input · 64,625 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Loop Stack, Tools & Originators|Loop Stack, Tools & Originators]]
- [[_COMMUNITY_Automation & Backpressure|Automation & Backpressure]]
- [[_COMMUNITY_Skills, Connectors & Intent|Skills, Connectors & Intent]]
- [[_COMMUNITY_Memory & Applied Loops|Memory & Applied Loops]]
- [[_COMMUNITY_The Three Risks|The Three Risks]]
- [[_COMMUNITY_Sub-agents & Verification|Sub-agents & Verification]]
- [[_COMMUNITY_Worktrees & Human Ceiling|Worktrees & Human Ceiling]]

## God Nodes (most connected - your core abstractions)
1. `Loop Engineering` - 15 edges
2. `Loop Engineering (synthesis)` - 11 edges
3. `Skills` - 6 edges
4. `Automations` - 5 edges
5. `Sub-agents` - 5 edges
6. `Sub-agents (Block 5)` - 5 edges
7. `Worktrees` - 4 edges
8. `Plugins and Connectors` - 4 edges
9. `Memory` - 4 edges
10. `Comprehension Debt` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Agent Skills (essay)` --semantically_similar_to--> `Skills`  [INFERRED] [semantically similar]
  Loop-Engineering-Synthesis-Report.md → raw_text.txt
- `Loop Engineering (synthesis)` --semantically_similar_to--> `Loop Engineering`  [EXTRACTED] [semantically similar]
  Loop-Engineering-Synthesis-Report.md → raw_text.txt
- `Agent Harness Engineering (essay)` --semantically_similar_to--> `Agent Harness Engineering`  [INFERRED] [semantically similar]
  Loop-Engineering-Synthesis-Report.md → raw_text.txt
- `The Factory Model (essay)` --semantically_similar_to--> `The Factory Model`  [INFERRED] [semantically similar]
  Loop-Engineering-Synthesis-Report.md → raw_text.txt
- `Long-Running Agents (essay)` --semantically_similar_to--> `Long-Running Agents`  [INFERRED] [semantically similar]
  Loop-Engineering-Synthesis-Report.md → raw_text.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The Six Building Blocks of a Loop** — raw_text_automations, raw_text_worktrees, raw_text_skills, raw_text_plugins_connectors, raw_text_subagents, raw_text_memory [EXTRACTED 1.00]
- **The Three Risks (verification, comprehension debt, cognitive surrender)** — raw_text_verification_burden, raw_text_comprehension_debt, raw_text_cognitive_surrender [EXTRACTED 1.00]
- **Layered Stack: Harness / Loop / Factory** — loop_engineering_synthesis_report_harness, loop_engineering_synthesis_report_loop_layer, loop_engineering_synthesis_report_factory_layer [EXTRACTED 1.00]

## Communities (7 total, 0 thin omitted)

### Community 0 - "Loop Stack, Tools & Originators"
Cohesion: 0.15
Nodes (14): Agent Harness Engineering (essay), Factory Layer, The Factory Model (essay), Harness Layer, Loop B — Flaky-Test Hunter & Quarantine, Loop Layer, Addy Osmani, Agent Harness Engineering (+6 more)

### Community 1 - "Automation & Backpressure"
Cohesion: 0.27
Nodes (10): Automations (Block 1), Backpressure, Stop Babysitting Your Coding Agent (essay), Verifiable Stopping Condition, Automations, Backpressure, Bilgin Ibryam, /goal (verifiable stopping condition) (+2 more)

### Community 2 - "Skills, Connectors & Intent"
Cohesion: 0.28
Nodes (9): Agent Skills (essay), Intent Debt (essay), Plugins & Connectors (Block 4), Skills (Block 3), Intent Debt, MCP, Plugins and Connectors, SKILL.md (+1 more)

### Community 3 - "Memory & Applied Loops"
Cohesion: 0.28
Nodes (9): Long-Running Agents (essay), Loop A — Nightly Dependency & Security Upgrade, Loop C — Incident Postmortem Draft, Loop D — Docs-Drift Reconciliation, Loop Engineering (synthesis), Memory (Block 6), Long-Running Agents, Memory (+1 more)

### Community 4 - "The Three Risks"
Cohesion: 0.32
Nodes (8): Cognitive Surrender (Risk 3), Cognitive Surrender (essay), Comprehension Debt (Risk 2), Comprehension Debt (essay), Verification Burden (Risk 1), Cognitive Surrender, Comprehension Debt, Verification Burden

### Community 5 - "Sub-agents & Verification"
Cohesion: 0.47
Nodes (6): The Code Agent Orchestra (essay), Code Review AI (essay), Sub-agents (Block 5), Adversarial Code Review, The Code Agent Orchestra, Sub-agents

### Community 6 - "Worktrees & Human Ceiling"
Cohesion: 0.40
Nodes (6): The Human GIL / Review Ceiling, The Orchestration Tax (essay), Worktrees (Block 2), git worktree, The Orchestration Tax, Worktrees

## Knowledge Gaps
- **13 isolated node(s):** `/loop`, `MCP`, `git worktree`, `SKILL.md`, `Codex` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Loop Engineering` connect `Loop Stack, Tools & Originators` to `Automation & Backpressure`, `Skills, Connectors & Intent`, `Memory & Applied Loops`, `Sub-agents & Verification`, `Worktrees & Human Ceiling`?**
  _High betweenness centrality (0.505) - this node is a cross-community bridge._
- **Why does `Loop Engineering (synthesis)` connect `Memory & Applied Loops` to `Loop Stack, Tools & Originators`, `Automation & Backpressure`, `Skills, Connectors & Intent`, `Sub-agents & Verification`, `Worktrees & Human Ceiling`?**
  _High betweenness centrality (0.420) - this node is a cross-community bridge._
- **Why does `Sub-agents (Block 5)` connect `Sub-agents & Verification` to `Automation & Backpressure`, `Memory & Applied Loops`?**
  _High betweenness centrality (0.309) - this node is a cross-community bridge._
- **What connects `/loop`, `MCP`, `git worktree` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._