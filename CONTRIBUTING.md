# Contributing

Small, focused improvements are welcome.

- Open an issue first for anything larger than a typo or a clearer example, so the scope can be agreed before work starts.
- Never weaken the safety rules: the skill must stay report-only — it must never approve, request changes, merge, delete, or post on a pull request — and it must never claim a check it did not run.
- Do not add an 11th check or drop one of the ten. The list is fixed. A new check needs its own issue and a reason why ten is not enough.
- Every claim in a proposed change must be verifiable: a command must be runnable, a report line must trace to an added line in a diff, a FAIL must name a file and line.
- Run `python3 tests/test_skill.py` before opening a pull request. It must pass.
- Do not add placeholder text, invented features, or copied content without attribution.
- Python standard library only — no new dependency without a reason in the issue.
- Never put a real pull request, a real secret, or a real credential in an example, a test, or a report.
