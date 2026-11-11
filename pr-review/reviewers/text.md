# Text reviewer

Review the PR's description, issue links and changed prose, for accuracy.

- **Description**: it tells a reviewer what changed and why, matches what the code actually does (`git diff --stat` and the changed files), and says nothing that misleads. Fill the PR template if the repo has one.
- **Issue link**: an issue the PR resolves is referenced with a closing keyword (`Closes #123`) so merging closes it; a bare mention won't.
- **Docs and prose**: changed documentation, READMEs, changelogs and agent instructions are accurate and don't contradict the code. Relative links point at files and anchors that exist in the PR.
- **Repo rules**: title format, commit-message rules, spelling, markup and external links only where the repo documents a rule for them (`CONTRIBUTING.md`, PR template, commitlint config, title-check workflows, prose linter configs). Otherwise, leave style alone.
