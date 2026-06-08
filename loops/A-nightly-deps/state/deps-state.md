# Deps State — Loop A Memory

Persistent memory for the nightly dependency-upgrade loop. The loop reads this first: it logs what was upgraded, and lists deferrals it must NOT re-attempt until their reason no longer holds.

## Upgraded
| date | package | from → to | PR |
| --- | --- | --- | --- |
| _seed_ | _none yet_ | _–_ | _–_ |

## Deferred (do not re-attempt)
| package | current | target | reason | ticket |
| --- | --- | --- | --- | --- |
| react-router | 6.x | 7.x | breaking route API; needs manual refactor | TICKET-412 |
