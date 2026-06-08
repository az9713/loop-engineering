"""A tiny module with THREE intentional bugs, for the demo loop.

The demo loop's job: make `python -m unittest test_calc` pass.
Each function below has exactly one bug — find it from the failing test
output and fix it. Do NOT edit test_calc.py; fix the code here.
"""


def add(a, b):
    # BUG: subtracts instead of adding.
    return a - b


def is_even(n):
    # BUG: returns True for ODD numbers.
    return n % 2 == 1


def factorial(n):
    # BUG: off-by-one — the loop stops one short, so factorial(5) == 24, not 120.
    result = 1
    for i in range(1, n):
        result *= i
    return result
