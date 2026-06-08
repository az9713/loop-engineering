#!/usr/bin/env python3
"""Deterministic self-test of the E2 parallel-worktree pipeline.

This proves the *mechanism* converges, without an LLM agent: it stands up a
throwaway git repo from the sandbox, creates ONE worktree per module on its own
branch, applies the reference fix in each (simulating the parallel makers),
merges all three branches back, and runs the full suite as the integration gate.

Because each module lives in its own file, the three branches touch disjoint
files and merge with ZERO conflicts — that is the whole reason the work is
partitioned by module. Run it:  python loops/E2-parallel-sandbox/verify_pipeline.py

It never touches your real repo: everything happens in a temp directory that is
removed at the end. Exit 0 = pipeline converged.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SANDBOX = os.path.join(HERE, "sandbox")
MODULES = ["calc", "strings", "dates"]

# Reference fixes (one per module) — applied in each module's own worktree.
FIXED = {
    "calc.py": '"""calc — fixed."""\n\n\ndef add(a, b):\n    return a + b\n',
    "strings.py": '"""strings — fixed."""\n\n\ndef shout(s):\n    return s.upper() + "!"\n',
    "dates.py": '"""dates — fixed. 0=Mon .. 6=Sun."""\n\n\ndef is_weekend(weekday):\n    return weekday >= 5\n',
}

GIT = ["git", "-c", "user.email=loop@example.com", "-c", "user.name=loop",
       "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"]


def run(cmd, cwd, check=True, capture=False):
    r = subprocess.run(cmd, cwd=cwd, text=True,
                       stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.STDOUT if capture else None)
    if check and r.returncode != 0:
        if capture:
            print(r.stdout)
        raise SystemExit(f"command failed ({r.returncode}): {' '.join(cmd)}")
    return r


def suite_passes(cwd):
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-p", "test_*.py"],
                       cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode == 0, r.stdout


def main():
    parent = tempfile.mkdtemp(prefix="e2_verify_")
    repo = os.path.join(parent, "repo")
    shutil.copytree(SANDBOX, repo)
    try:
        run(GIT + ["init", "-q"], repo)
        run(GIT + ["add", "-A"], repo)
        run(GIT + ["commit", "-qm", "broken sandbox"], repo)

        ok, out = suite_passes(repo)
        print(f"[1] baseline full suite RED as expected: {not ok}")
        assert not ok, "expected the broken sandbox to FAIL"

        # One worktree per module, each on its own branch, fixed in parallel-style.
        for m in MODULES:
            wt = os.path.join(parent, f"wt-{m}")
            run(GIT + ["worktree", "add", "-q", "-b", f"fix/{m}", wt], repo, capture=True)
            with open(os.path.join(wt, f"{m}.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write(FIXED[f"{m}.py"])
            # Each worktree runs ONLY its own module's test.
            r = subprocess.run([sys.executable, "-m", "unittest", f"test_{m}"],
                               cwd=wt, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(f"[2] worktree fix/{m}: test_{m} GREEN: {r.returncode == 0}")
            assert r.returncode == 0, f"fix/{m} did not pass its own test"
            run(GIT + ["add", "-A"], wt)
            run(GIT + ["commit", "-qm", f"fix {m}"], wt)

        # Integrate: merge each branch back. Disjoint files => no conflicts.
        for m in MODULES:
            res = run(GIT + ["merge", "--no-edit", "-q", f"fix/{m}"], repo, check=False, capture=True)
            conflict = res.returncode != 0
            print(f"[3] merge fix/{m}: clean (no conflict): {not conflict}")
            assert not conflict, f"unexpected merge conflict on fix/{m}"

        ok, out = suite_passes(repo)
        print(f"[4] integration gate - FULL suite GREEN after merge: {ok}")
        if not ok:
            print(out)
        assert ok, "full suite did not pass after merge"

        print("\nPIPELINE CONVERGED OK - 3 worktrees -> 3 isolated fixes -> 3 clean merges -> full suite green")
        return 0
    finally:
        for m in MODULES:
            subprocess.run(GIT + ["worktree", "remove", "--force", os.path.join(parent, f"wt-{m}")],
                           cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.rmtree(parent, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
