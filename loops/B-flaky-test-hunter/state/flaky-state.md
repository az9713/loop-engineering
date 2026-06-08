# Flaky-Test State (Memory)

Tracks failure rates over time and already-quarantined tests so the loop never re-triages the same test and can detect a test getting worse. Mirrors the Linear "Flaky tests" board.

## Quarantined

| date | test | failure rate | ticket |
| --- | --- | --- | --- |
| 2026-06-01 | `auth/test_login.py::test_token_refresh` | 3% (3/50, last 50x harness) | TICKET-220 |

## Watching

| test | failure rate trend | first seen |
| --- | --- | --- |
| `orders/test_checkout.py::test_concurrent_purchase` | 1% → 2% → 4% (rising, re-run harness next cycle) | 2026-05-28 |
