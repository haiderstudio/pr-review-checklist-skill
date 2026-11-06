---
name: pr-review-checklist-skill
description: Review a pull request against a fixed 10-check list and write a short report, one line per check. Use when asked to review a pull request, a diff, or a branch before it is merged. Report-only: it never approves, requests changes, merges, deletes, or comments on the pull request itself. A human reads the report and decides.
---

# pr-review-checklist-skill

Review a pull request against ten checks and write the
report. One job: read the diff, check it against the
fixed list, and say what passed, what failed, and what
could not be told from the diff. The report is the
whole output. Nothing is approved, merged, or posted
for you.

## When to use this skill

Use it when the user asks to:
- Review a pull request before it is merged.
- Check a diff or a branch against a review list.
- Give a second pair of eyes to a change, in writing,
  before a human approves it.

## When NOT to use it

- Do not use it to approve, request changes, merge, or
  close a pull request. This skill writes a report. The
  human who asked for the review makes the call. If the
  user wants the review posted on the pull request, say
  so plainly and stop — posting it is a different job.
- Do not use it as a full code review. Ten checks is
  the whole list. Deep design review, architecture
  review, and performance testing are different jobs.
- Do not use it on a pull request you cannot read. If
  there is no diff — no branch, no patch, no pull
  request number — say "I have no diff to review" and
  stop. Do not review from a description alone.
- Do not use it to rewrite the code. If a check fails,
  report the failure with the file and line. The author
  does the fixing.

## The 10 checks

Run every check, in this order, on every pull request.
Each check gets one status: PASS, FAIL, or SKIP. SKIP
means the diff does not give enough to judge — say why
in one line. Never guess a PASS.

1. **Title and description say what the change does.**
   A reader who never saw the code can say what the
   pull request is for. FAIL if the title is vague
   ("fix stuff", "updates") or the description is
   empty.
2. **The diff does what the description says, and nothing extra.** Every changed file serves the
   described change. FAIL if a file is changed for a
   different reason — a typo fix, a drive-by refactor,
   an unrelated feature — with no note in the
   description.
3. **Tests cover the changed logic, not just the happy
   path.** New or changed behaviour has a test that
   exercises it, including at least one unhappy path
   where the code has one. FAIL if behaviour changed
   and no test changed, or the tests only cover the
   easy case.
4. **No secrets or credentials in the diff.** No keys,
   tokens, passwords, or private keys in added lines.
   FAIL if any appear. If a value looks secret-shaped
   but is a placeholder (`YOUR_API_KEY_HERE`) or an
   example value, say so and PASS.
5. **No new security hole in the changed lines.** No
   SQL, shell, or template injection from untrusted
   input; no auth check dropped; no data shown to a
   user who should not see it. FAIL if one is found.
   SKIP if the change has no user input, no auth, and
   no data access to judge.
6. **Failure paths are handled.** When the code can
   fail — bad input, a missing file, a service down —
   it fails with a message a user or a log can act on.
   FAIL if an error is swallowed silently or an
   invalid input is ignored without a word. SKIP if
   the change has no failure path.
7. **No breaking change left undocumented.** If the
   change alters an API, a behaviour, or a data shape
   that other code depends on, the description says
   so. FAIL if a breaking change is in the diff and
   the description does not mention it.
8. **No leftover debug, dead code, or commented-out code added.** No `print` or `console.log` debug
   lines, no unused function or variable added, no
   block of commented-out code. FAIL if any appear
   in added lines.
9. **No new dependency, config, or workflow change without a reason in the description.** A new
   package, a config edit, or a CI change needs one
   line in the description saying why. FAIL if one
   appears with no reason given.
10. **Size is readable.** A reviewer can read the
    whole diff in one sitting — roughly under 400
    changed lines. FAIL if it is bigger, and say how
    big it is. A big pull request is not wrong, it is
    just not reviewable as one piece.

## Workflow

### 1. Get the diff and the description

Get the pull request's title and description, then the
diff. Use whichever of these fits:

```bash
gh pr diff <number>
```

```bash
git diff <base>...<head>
```

```bash
git diff
git diff --cached
```

- `gh pr diff` when the pull request is on GitHub and
  `gh` is installed. `git diff <base>...<head>` when
  both branches are local. `git diff` and
  `git diff --cached` when the change is uncommitted.
- Read only the diff. Do not read files the diff does
  not touch. Do not run `git log` to judge the change;
  the diff and the description are the evidence.
- If no diff can be fetched, stop: "I have no diff to
  review." If the title or description is missing, run
  the checks anyway and mark check 1 FAIL.

### 2. Count the diff

Before judging anything, count:

- Files changed, by name.
- Added lines and removed lines.
- Whether any test file changed.

Write the counts down. Checks 3, 9, and 10 need them,
and the report prints them. A count is a fact; a
judgement is not a count.

### 3. Run the 10 checks, in order

Go through the list, one check at a time. For each
check, look at the diff lines that bear on it and
nothing else:

- A check passes only on evidence in the diff or the
  description. "Probably fine" is not evidence — that
  is a SKIP, with the reason in one line.
- A check fails only on something in the diff. Name
  the file and line. "Might be a problem" is not a
  failure — that is a SKIP, or a question in the
  report's notes, never a FAIL.
- Do not add an 11th check. Do not drop a check
  because it is awkward. If a check does not fit the
  change — a docs-only pull request has no code to
  test — mark it SKIP and say why. All ten lines
  appear in every report.

### 4. Write the report, then stop

Write the report in this fixed shape, and no other
shape:

```markdown
PR: <title>
Files changed: <number> (<file names>)
Lines changed: <added> added, <removed> removed
Checks: 10
1. Title and description say what the change does — PASS/FAIL/SKIP — <one line of evidence>
2. Diff does what the description says, and nothing extra — PASS/FAIL/SKIP — <one line of evidence>
3. Tests cover the changed logic — PASS/FAIL/SKIP — <one line of evidence>
4. No secrets or credentials in the diff — PASS/FAIL/SKIP — <one line of evidence>
5. No new security hole in the changed lines — PASS/FAIL/SKIP — <one line of evidence>
6. Failure paths are handled — PASS/FAIL/SKIP — <one line of evidence>
7. No breaking change left undocumented — PASS/FAIL/SKIP — <one line of evidence>
8. No leftover debug, dead code, or commented-out code — PASS/FAIL/SKIP — <one line of evidence>
9. No new dependency, config, or workflow change without a reason — PASS/FAIL/SKIP — <one line of evidence>
10. Size is readable — PASS/FAIL/SKIP — <one line of evidence>
Findings: <number of FAILs>
Verdict: NEEDS WORK — <number> checks failed. A human decides whether it ships. / NO FAILS FOUND — a human still decides whether it ships.
```

Rules for the report:

- One line per check, in order, with the check's
  short name, its status, and one line of evidence:
  a file and line, a count, or the words that show it.
- If there is even one FAIL, the verdict is NEEDS
  WORK. If there are no FAILs, the verdict is NO
  FAILS FOUND. Either way, the last line is the same
  plain fact: a human decides whether it ships.
  This skill never approves a pull request.
- SKIP is not a fail and not a pass. Say how many
  checks were skipped in the verdict line only if
  any were skipped: "NO FAILS FOUND — 3 checks
  skipped. A human still decides whether it ships."
- Then stop. Do not edit a file, do not fix a
  failure, do not post the report on the pull
  request, do not approve, do not merge. The report
  is the output.

## Good examples

A messy pull request, 3 fails, verdict NEEDS WORK
(full worked example: the diff in
`examples/messy-pr.patch`, the report in
`examples/messy-pr-report.md`):

```markdown
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
```

A clean pull request, no fails, verdict NO FAILS
FOUND (full worked example: `examples/clean-pr.patch`
and `examples/clean-pr-report.md`):

```markdown
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
```

A docs-only pull request, no fails, 3 checks skipped
(full worked example: `examples/docs-only-pr.patch`
and `examples/docs-only-pr-report.md`):

```markdown
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
```

## Bad examples (do not write like this)

> Reviews the pull request and approves it.

The skill never approves. The report ends with "a
human decides whether it ships" and the skill stops.
Approving is the human's job, under the human's name.

> Finds a problem and fixes the code, then reports PASS.

Fixing the code is not the review. Report the failure
with the file and line, and let the author fix it. A
report that says PASS after a quiet fix is a lie about
what the diff contained.

> Reports FAIL on a check with no evidence in the diff.

"Might be slow" or "could be a security issue" with no
line to point at is not a failure. That is a SKIP, or
one line in the notes if the user asked for questions.
A FAIL names the file and line.

> Reports PASS on tests because a test file exists.

A test file that exists but does not cover the changed
logic is not coverage. Check 3 passes only when a test
exercises the new or changed behaviour, including an
unhappy path where one exists.

> Skips check 2 because the extra change is small.

A one-line typo fix in an unrelated file is still an
extra change. Small does not mean in scope. Mark it
FAIL and name the file.

> Writes a long essay about the code instead of the report.

Ten lines, one per check, then the verdict. The report
shape is fixed. Extra prose hides the result.

## Output rules

- Output one report per pull request, in its own code
  block, in the fixed shape above.
- Every FAIL names a file and a line. Every SKIP
  names the reason in one line.
- Never claim a check was run that was not run. If a
  check was skipped, say SKIP, not PASS.
- Never say a pull request is ready to merge, safe,
  or approved. Say how many checks failed, and that
  a human decides.
- Never say the code has no bugs. Ten checks are not
  a proof. Say what the ten checks found, nothing
  wider.

## Limits and safety rules

- This skill reads one diff, on this machine only. It
  sends nothing anywhere, needs no API key, and
  installs no tool. It works with `git diff`,
  `git diff --cached`, `git diff <base>...<head>`,
  or `gh pr diff`.
- It never edits, deletes, merges, approves, or
  requests changes on a pull request. It never posts
  a comment or a review. It reports, and stops.
- It checks ten things only. A bug outside those ten
  checks will not be found. A NO FAILS FOUND verdict
  is not a promise the code is correct.
- Checks 5 and 6 need judgement. Where the diff does
  not give enough to judge, mark SKIP — never guess
  a PASS to keep the report clean.
- All diffs in this repo's examples are made-up
  sample code. Never put a real pull request, a real
  secret, or a real credential in an example, a test,
  or a report.
