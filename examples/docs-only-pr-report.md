PR: Document how to run the tests
Files changed: 1 (README.md)
Lines changed: 2 added, 0 removed
Checks: 10
1. Title and description say what the change does — PASS — title names the docs change
2. Diff does what the description says, and nothing extra — PASS — only the README changed
3. Tests cover the changed logic — SKIP — no code changed, nothing to test
4. No secrets or credentials in the diff — PASS — no key, token, or password in added lines
5. No new security hole in the changed lines — SKIP — no code changed, nothing to judge
6. Failure paths are handled — SKIP — no code changed, no failure path
7. No breaking change left undocumented — PASS — no code or API changed
8. No leftover debug, dead code, or commented-out code — PASS — no debug or dead code in added lines
9. No new dependency, config, or workflow change without a reason — PASS — none changed
10. Size is readable — PASS — 2 added lines
Findings: 0
Verdict: NO FAILS FOUND — 3 checks skipped. A human still decides whether it ships.
