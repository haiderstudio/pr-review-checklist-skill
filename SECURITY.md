# Security Policy

This skill reads one local diff (`git diff`, `git diff --cached`,
`git diff <base>...<head>`, or `gh pr diff`). It sends nothing
anywhere, edits no file, writes no code, installs no tool, and
needs no API key or secret. It never approves, requests changes,
merges, deletes, or posts on a pull request.

If you find a case where it could do otherwise, please open an
issue describing the exact diff and input. Do not include any
real secret in the report.
