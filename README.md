# pr-review-checklist-skill

Review a pull request against a 10-check list, report only.

[![CI](https://github.com/haiderstudio/pr-review-checklist-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/haiderstudio/pr-review-checklist-skill/actions/workflows/ci.yml) [![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

## What it does

When an AI coding agent loads this skill, it reviews
one pull request against a fixed list of ten checks —
and nothing else — in this order:

1. Title and description say what the change does.
2. The diff does what the description says, and
   nothing extra.
3. Tests cover the changed logic, not just the happy
   path.
4. No secrets or credentials in the diff.
5. No new security hole in the changed lines.
6. Failure paths are handled.
7. No breaking change left undocumented.
8. No leftover debug, dead code, or commented-out
   code added.
9. No new dependency, config, or workflow change
   without a reason in the description.
10. Size is readable — a reviewer can read it in one
    sitting.

Each check gets one status: PASS, FAIL, or SKIP. SKIP
means the diff does not give enough to judge, and the
report says why in one line. The skill writes one
short report — one line per check, then a verdict:
NEEDS WORK if any check failed, NO FAILS FOUND if
none did. Either way the last line is the same plain
fact: a human decides whether it ships.

## What it does NOT do

- It does not approve, request changes, merge, or
  close a pull request. It writes a report. The human
  who asked for the review makes the call.
- It does not post the report on the pull request.
  Posting it is a different job.
- It does not fix anything it finds. A FAIL names
  the file and line; the author does the fixing.
- It does not do a full code review. Ten checks is
  the whole list. Deep design review, architecture
  review, and performance testing are different jobs.
- It does not add an 11th check or drop one that is
  awkward. The list is fixed, so two reviews of the
  same pull request can be compared.
- It does not promise the code is correct. A NO
  FAILS FOUND verdict means the ten checks found
  nothing — nothing wider.

## Who it is for

Developers who use an AI coding agent and want a
second pair of eyes on a pull request before a human
approves it — the same ten checks every time, in
writing, with a file and line for every failure.

## How this differs from similar tools

Pull request review is a crowded field, and the wide
versions of it are owned by others. This skill is the
narrow one — ten checks, one report, no posting:

- CodeRabbit, Claude Code Action, and Greptile are
  automated reviewers that post comments on pull
  requests and can block a merge. This skill posts
  nothing and approves nothing. It writes a report
  for a human.
- read-only-gh-pr-review (jawwadfirdousi/agent-skills)
  is a full read-only review skill with eight risk
  categories, reference files, and a GitHub CLI
  dependency. This skill has one fixed list of ten
  checks and works from a local diff, with no
  reference files and no required tool beyond git.
- aif-review is a general code review skill that
  checks correctness, security, performance, and
  best practices in open-ended form. This skill
  checks a fixed list and reports PASS, FAIL, or
  SKIP per check, so the result is comparable.
- qodo-ai/pr-compliance-templates (15 stars, checked
  Nov 6, 2026) is a library of YAML compliance
  templates for automating review. This skill is not
  a template library — it is a review you run on one
  pull request.
- vintasoftware/pr-reviewer-checklist (5 stars,
  checked Nov 6, 2026) is a set of human guidelines
  for civilised review culture. This skill is a list
  an agent runs against a diff, with a written
  report.
- A GitHub search for the exact name
  "pr-review-checklist-skill" returns 2 results, both
  0 stars (checked Nov 6, 2026), both described as a
  checklist skill installable via npx. This skill is
  a plain folder with a SKILL.md file — no installer,
  no package manager.

None of those were copied. The ten checks, their
order, the fixed report shape, and all three worked
examples here are original.

## Install

This skill follows the open Agent Skills format: a folder with a
`SKILL.md` file.

**Claude Code / Codex / Gemini CLI (project level):**

```bash
mkdir -p .agents/skills
cp -r skills/pr-review-checklist-skill .agents/skills/pr-review-checklist-skill
```

## Usage

Give the agent a pull request to review, and tell it
to use this skill. The agent follows
`skills/pr-review-checklist-skill/SKILL.md`: it gets
the diff (`gh pr diff <number>`, `git diff
<base>...<head>`, or `git diff` / `git diff
--cached`), counts it, runs the ten checks in order,
and writes the report. NEEDS WORK means at least one
check failed. NO FAILS FOUND means none did. Either
way, a human decides whether it ships.

## Example 1 — a messy pull request, verdict NEEDS WORK

The diff (from `examples/messy-pr.patch`) adds a
discount function to `shop.py` — with a debug print
left in, no test, and an unrelated typo fix in the
README. The report (full report in
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

Three fails, each with a file and line or a count.
The debug print, the missing test, and the extra
file are three different checks — that is why the
list is ten checks, not one "looks good".

## Example 2 — a clean pull request, verdict NO FAILS FOUND

The diff (from `examples/clean-pr.patch`) adds the
same discount function, this time with tests for the
happy path, the no-discount path, and the unknown-code
path — and nothing else. The report (full report in
`examples/clean-pr-report.md`):

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

No fails does not mean approved. The last line says
it plainly: a human still decides.

## Example 3 — a docs-only pull request, 3 checks skipped

The diff (from `examples/docs-only-pr.patch`) only
adds two lines to the README. Three checks need code
to judge, so the skill marks them SKIP instead of
guessing a PASS (full report in
`examples/docs-only-pr-report.md`):

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

SKIP is not a pass and not a fail. A report that
guessed PASS on checks it could not run would be a
lie about what was checked.

## How it is tested

```bash
python3 tests/test_skill.py
```

The tests check that `SKILL.md` has valid `name` and
`description` frontmatter and the required workflow
sections; that all ten checks are listed, in order,
in the skill; that `.gitignore` starts with `.env`;
that the three example diffs count as stated (10
added lines in the messy diff, 25 in the clean diff,
2 in the docs-only diff); that the mechanical parts
of the reports match the diffs — the debug print at
shop.py:6, no test file in the messy diff, a test
file in the clean diff, only a README in the
docs-only diff; that all three reports quoted in this
README are the real files; that the install step
copies the skill to a clean folder; and that a real
git walkthrough — base commit, then a branch with
the messy change — counts the same 10 added lines
and finds the same 3 fails. Standard library only —
no third-party imports, so the same command runs on
a clean CI runner. No placeholder text anywhere in
the repo.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests
are welcome; please keep examples real and checkable, and
never put a real pull request, a real secret, or a real
credential in an example, a test, or a report.

## Licence

MIT — see [LICENSE](LICENSE). This is original work. The
related tools named above are listed as related work, not
sources — nothing here was copied from them.
