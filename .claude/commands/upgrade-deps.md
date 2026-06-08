---
description: Run the autonomous dependency-upgrade loop (maker/checker, PR per upgrade class)
---
Invoke the `upgrade-deps` skill and run it to its stop condition.

Concretely: read `loops/A-nightly-deps/state/deps-state.md`, enumerate outdated deps + advisories, split them into the `wt/patch` / `wt/minor` / `wt/major` worktrees, and for each class dispatch `deps-maker` to bump + fix and then `deps-checker` to audit + run the full suite. On green, open a PR for that class; on red, let the maker self-correct up to 3 times, otherwise file the group to the Triage inbox. Finish by updating `deps-state.md`.

Do not stop until, for every upgrade class, the build + full test suite + typecheck are green AND no high/critical advisories remain (or the group has been triaged for a human).

**Looped usage:** `/loop 1d /upgrade-deps` re-runs this loop daily (nightly "keep the lights on" cadence). The deferred-with-reason memory in `deps-state.md` ensures tonight's run never re-attempts a deferral it already reasoned about.

$ARGUMENTS
