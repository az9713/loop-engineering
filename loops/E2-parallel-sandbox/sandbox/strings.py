"""strings — one intentional bug. Owned by worktree `fix/strings`."""


def shout(s):
    # BUG: lowercases and omits the "!". Should be s.upper() + "!".
    return s.lower()
