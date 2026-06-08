"""dates — one intentional bug. Owned by worktree `fix/dates`. 0=Mon .. 6=Sun."""


def is_weekend(weekday):
    # BUG: uses > 5, so Saturday (5) is wrongly treated as a weekday.
    return weekday > 5
