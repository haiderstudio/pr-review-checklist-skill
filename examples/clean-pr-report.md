PR: Add discount support
Files changed: 2 (shop.py, test_shop.py)
Lines changed: 25 added, 0 removed
Checks: 10
1. Title and description say what the change does — PASS — title and description name the discount change
2. Diff does what the description says, and nothing extra — PASS — both files serve the discount change
3. Tests cover the changed logic — PASS — test_shop.py tests HALF, NONE, and unknown code
4. No secrets or credentials in the diff — PASS — no key, token, or password in added lines
5. No new security hole in the changed lines — PASS — no user input, auth, or data access changed
6. Failure paths are handled — PASS — unknown code raises ValueError, tested
7. No breaking change left undocumented — PASS — no API or behaviour change
8. No leftover debug, dead code, or commented-out code — PASS — no debug or dead code in added lines
9. No new dependency, config, or workflow change without a reason — PASS — none changed
10. Size is readable — PASS — 25 added lines
Findings: 0
Verdict: NO FAILS FOUND — a human still decides whether it ships.
