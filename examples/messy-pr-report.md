PR: Add discount support
Files changed: 2 (shop.py, README.md)
Lines changed: 10 added, 1 removed
Checks: 10
1. Title and description say what the change does — PASS — title and description name the discount change
2. Diff does what the description says, and nothing extra — FAIL — README.md fixes a typo, not discount support
3. Tests cover the changed logic — FAIL — no test file changed, no test for apply_discount
4. No secrets or credentials in the diff — PASS — no key, token, or password in added lines
5. No new security hole in the changed lines — PASS — no user input, auth, or data access changed
6. Failure paths are handled — PASS — unknown code raises ValueError
7. No breaking change left undocumented — PASS — no API or behaviour change
8. No leftover debug, dead code, or commented-out code — FAIL — shop.py:6 prints "DEBUG total"
9. No new dependency, config, or workflow change without a reason — PASS — none changed
10. Size is readable — PASS — 10 added lines
Findings: 3
Verdict: NEEDS WORK — 3 checks failed. A human decides whether it ships.
