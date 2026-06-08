"""calc — one intentional bug. Owned by worktree `fix/calc`. (0=Mon..6=Sun n/a here)"""


def add(a, b):
    # BUG: subtracts instead of adding.
    return a - b
