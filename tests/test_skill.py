"""Tests for the pr-review-checklist-skill: frontmatter, the ten
checks in order, required sections, .gitignore, the three example
diffs counted and mechanically checked against their reports,
the reports matching the README and SKILL.md, a real git
walkthrough on a temp repo, and no placeholders or absolute
paths anywhere in the repo. Standard library only — no
third-party imports (a clean CI runner does not have them)."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "pr-review-checklist-skill" / "SKILL.md"
README = ROOT / "README.md"
MESSY = ROOT / "examples" / "messy-pr.patch"
MESSY_REPORT = ROOT / "examples" / "messy-pr-report.md"
CLEAN = ROOT / "examples" / "clean-pr.patch"
CLEAN_REPORT = ROOT / "examples" / "clean-pr-report.md"
DOCS = ROOT / "examples" / "docs-only-pr.patch"
DOCS_REPORT = ROOT / "examples" / "docs-only-pr-report.md"
GITIGNORE = ROOT / ".gitignore"
CI = ROOT / ".github" / "workflows" / "ci.yml"
BANNED = ["TODO", "FIXME", "lorem", "coming soon"]

CHECKS = [
    "Title and description say what the change does",
    "diff does what the description says, and nothing extra",
    "Tests cover the changed logic",
    "No secrets or credentials in the diff",
    "No new security hole in the changed lines",
    "Failure paths are handled",
    "No breaking change left undocumented",
    "No leftover debug, dead code, or commented-out code",
    "No new dependency, config, or workflow change without a reason",
    "Size is readable",
]

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?:ghp_|gho_|ghu_|ghs_|ghr_|github_pat_)[A-Za-z0-9_]{20,}"),
    re.compile(r"sk_live_[A-Za-z0-9]{16,}"),
]
DEBUG_PATTERNS = [re.compile(r"\bprint\s*\("), re.compile(r"console\.log\s*\(")]


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        sys.exit(1)


def parse_patch(text):
    """Parse a unified diff.

    Returns (files, added, removed) where files is a list of
    changed file names in order, added is a list of
    (file, new line number, text), and removed is a count."""
    files = []
    added = []
    removed = 0
    current = None
    new_no = 0
    for raw in text.splitlines():
        m = re.match(r"diff --git a/\S+ b/(\S+)", raw)
        if m:
            current = m.group(1)
            if current not in files:
                files.append(current)
            continue
        m = re.match(r"\+\+\+ b/(\S+)", raw)
        if m:
            current = m.group(1)
            if current not in files:
                files.append(current)
            continue
        if raw.startswith("--- "):
            continue
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
        if m:
            new_no = int(m.group(1))
            continue
        if raw.startswith("+"):
            added.append((current, new_no, raw[1:]))
            new_no += 1
        elif raw.startswith("-"):
            removed += 1
        elif raw.startswith(" ") or raw == "":
            new_no += 1
    return files, added, removed


def report_statuses(report_text):
    """Return the list of (number, status) from a report's 10 lines."""
    out = []
    for line in report_text.splitlines():
        m = re.match(r"(\d+)\. .* — (PASS|FAIL|SKIP) — ", line)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def is_test_file(name):
    return (name.startswith("test_") or name.endswith("_test.py")
            or "/tests/" in name or name.startswith("tests/"))


def main():
    skill = SKILL.read_text()
    m = re.match(r"---\n(.*?)\n---\n", skill, re.S)
    check("test_skill_frontmatter",
          bool(m) and "name: pr-review-checklist-skill" in m.group(1)
          and "description:" in m.group(1))
    for section in ["When to use this skill", "When NOT to use it",
                    "The 10 checks", "Workflow", "Good examples",
                    "Bad examples", "Output rules",
                    "Limits and safety rules"]:
        check("test_skill_sections_" + section.split()[0], section in skill)
    # All ten checks listed, in order, in the skill.
    positions = [skill.index(c) for c in CHECKS]
    check("test_skill_ten_checks_in_order",
          positions == sorted(positions) and len(set(positions)) == 10)
    check("test_skill_no_yaml_import", "import yaml" not in skill)
    check("test_gitignore_env_first",
          GITIGNORE.read_text().splitlines()[0] == ".env")
    for f in [SKILL, README, MESSY, MESSY_REPORT, CLEAN, CLEAN_REPORT,
              DOCS, DOCS_REPORT]:
        check("test_no_placeholders_" + f.name,
              not any(b in f.read_text() for b in BANNED))

    # Messy diff: 2 files, 10 added, 1 removed; 3 fails (2, 3, 8).
    files, added, removed = parse_patch(MESSY.read_text())
    check("test_messy_files", files == ["shop.py", "README.md"])
    check("test_messy_added", len(added) == 10)
    check("test_messy_removed", removed == 1)
    debug = [(f, n) for f, n, t in added
             if any(p.search(t) for p in DEBUG_PATTERNS)]
    check("test_messy_debug_print", debug == [("shop.py", 6)])
    check("test_messy_no_test_file",
          not any(is_test_file(f) for f in files))
    check("test_messy_no_secrets",
          not any(p.search(t) for _, _, t in added for p in SECRET_PATTERNS))
    report = MESSY_REPORT.read_text()
    check("test_messy_report_counts",
          "Files changed: 2 (shop.py, README.md)" in report
          and "Lines changed: 10 added, 1 removed" in report)
    statuses = report_statuses(report)
    check("test_messy_report_ten_lines",
          [n for n, _ in statuses] == list(range(1, 11)))
    check("test_messy_report_fails",
          [s for _, s in statuses]
          == ["PASS", "FAIL", "FAIL", "PASS", "PASS", "PASS", "PASS",
              "FAIL", "PASS", "PASS"])
    check("test_messy_report_verdict",
          "Findings: 3" in report
          and "Verdict: NEEDS WORK" in report)
    check("test_messy_report_debug_line", "shop.py:6" in report)

    # Clean diff: 2 files, 25 added, 0 removed; 0 fails.
    files, added, removed = parse_patch(CLEAN.read_text())
    check("test_clean_files", files == ["shop.py", "test_shop.py"])
    check("test_clean_added", len(added) == 25)
    check("test_clean_removed", removed == 0)
    check("test_clean_has_test_file",
          any(is_test_file(f) for f in files))
    check("test_clean_no_debug",
          not any(p.search(t) for _, _, t in added
                  for p in DEBUG_PATTERNS))
    check("test_clean_no_secrets",
          not any(p.search(t) for _, _, t in added for p in SECRET_PATTERNS))
    # The clean test file really tests the unhappy path.
    test_added = [t for f, _, t in added if f == "test_shop.py"]
    check("test_clean_tests_unknown_path",
          any("test_unknown" in t for t in test_added)
          and any("ValueError" in t for t in test_added))
    report = CLEAN_REPORT.read_text()
    check("test_clean_report_counts",
          "Files changed: 2 (shop.py, test_shop.py)" in report
          and "Lines changed: 25 added, 0 removed" in report)
    statuses = report_statuses(report)
    check("test_clean_report_ten_lines",
          [n for n, _ in statuses] == list(range(1, 11)))
    check("test_clean_report_all_pass",
          all(s == "PASS" for _, s in statuses))
    check("test_clean_report_verdict",
          "Findings: 0" in report
          and "Verdict: NO FAILS FOUND" in report)

    # Docs-only diff: 1 file, 2 added, 0 removed; 0 fails, 3 skips.
    files, added, removed = parse_patch(DOCS.read_text())
    check("test_docs_files", files == ["README.md"])
    check("test_docs_added", len(added) == 2)
    check("test_docs_removed", removed == 0)
    check("test_docs_only_markdown",
          all(f.endswith(".md") for f in files))
    report = DOCS_REPORT.read_text()
    check("test_docs_report_counts",
          "Files changed: 1 (README.md)" in report
          and "Lines changed: 2 added, 0 removed" in report)
    statuses = report_statuses(report)
    check("test_docs_report_ten_lines",
          [n for n, _ in statuses] == list(range(1, 11)))
    check("test_docs_report_skips",
          [s for _, s in statuses]
          == ["PASS", "PASS", "SKIP", "PASS", "SKIP", "SKIP", "PASS",
              "PASS", "PASS", "PASS"])
    check("test_docs_report_verdict",
          "Findings: 0" in report
          and "Verdict: NO FAILS FOUND — 3 checks skipped" in report)

    # The reports quoted in the README and SKILL.md are the real files.
    readme = README.read_text()
    for name, path in [("messy", MESSY_REPORT), ("clean", CLEAN_REPORT),
                       ("docs", DOCS_REPORT)]:
        text = path.read_text()
        check("test_" + name + "_report_in_readme", text.strip() in readme)
        check("test_" + name + "_report_in_skill", text.strip() in skill)

    # CI is valid plain YAML shape and runs only stdlib tests.
    ci = CI.read_text()
    check("test_ci_valid",
          "python3 tests/test_skill.py" in ci
          and "actions/checkout@v4" in ci
          and "runs-on: ubuntu-latest" in ci)
    check("test_ci_no_pip_install", "pip install" not in ci)

    # No third-party imports anywhere in the repo's Python, and
    # no absolute local paths or .env file anywhere. (Match real
    # import lines only — the literal "import yaml" also appears
    # inside this check itself.)
    for path in ROOT.rglob("*.py"):
        text = path.read_text()
        check("test_stdlib_only_" + path.name,
              not re.search(r"(?m)^(import|from) (yaml|requests|pytest)\b",
                            text))
        check("test_no_abs_path_" + path.name,
              not re.search(r"/(home|Users)/[A-Za-z]", text))
    check("test_no_env_file", not (ROOT / ".env").exists())
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in (".md", ".yml"):
            check("test_no_abs_path_" + path.name,
                  "/home/" not in path.read_text(errors="ignore"))

    # Install step from the README works on a clean folder.
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / ".agents" / "skills"
        dest.mkdir(parents=True)
        shutil.copytree(ROOT / "skills" / "pr-review-checklist-skill",
                        dest / "pr-review-checklist-skill")
        check("test_install_copies_skill",
              (dest / "pr-review-checklist-skill" / "SKILL.md").exists())

    # Walkthrough on a real git repo: base commit, then a branch
    # with the messy change, staged. git diff --cached must count
    # the same 10 added / 1 removed, with the debug print at
    # shop.py:6, no test file, and the README extra change.
    with tempfile.TemporaryDirectory() as tmp:
        run = lambda *args: subprocess.run(
            ["git", *args], cwd=tmp, capture_output=True, text=True,
            check=True)
        run("init", "-q")
        run("config", "user.email", "test@example.com")
        run("config", "user.name", "Test")
        (Path(tmp) / "shop.py").write_text(
            "def total(items):\n"
            "    return sum(item[\"price\"] for item in items)\n")
        (Path(tmp) / "README.md").write_text("# Shop\nA tiny shop.\n")
        run("add", "shop.py", "README.md")
        run("commit", "-qm", "base")
        (Path(tmp) / "shop.py").write_text(
            "def total(items):\n"
            "    return sum(item[\"price\"] for item in items)\n"
            "\n"
            "\n"
            "def apply_discount(total, code):\n"
            "    print(\"DEBUG total\", total)\n"
            "    if code == \"HALF\":\n"
            "        return total / 2\n"
            "    if code == \"NONE\":\n"
            "        return total\n"
            "    raise ValueError(\"unknown discount code\")\n")
        (Path(tmp) / "README.md").write_text("# Shoppe\nA tiny shop.\n")
        run("add", "shop.py", "README.md")
        diff = subprocess.run(["git", "diff", "--cached"], cwd=tmp,
                              capture_output=True, text=True,
                              check=True).stdout
        files, added, removed = parse_patch(diff)
        check("test_walkthrough_files",
              files == ["README.md", "shop.py"]
              or files == ["shop.py", "README.md"])
        check("test_walkthrough_added", len(added) == 10)
        check("test_walkthrough_removed", removed == 1)
        debug = [(f, n) for f, n, t in added
                 if any(p.search(t) for p in DEBUG_PATTERNS)]
        check("test_walkthrough_debug_print", debug == [("shop.py", 6)])
        check("test_walkthrough_no_test_file",
              not any(is_test_file(f) for f in files))
        check("test_walkthrough_extra_file", "README.md" in files)
        # The real diff counts match the example patch counts.
        efiles, eadded, eremoved = parse_patch(MESSY.read_text())
        check("test_walkthrough_matches_example",
              len(added) == len(eadded) and removed == eremoved
              and set(files) == set(efiles))
    print("All tests passed.")


if __name__ == "__main__":
    main()
