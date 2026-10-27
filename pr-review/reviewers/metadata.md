# Metadata reviewer

Review the PR's title, description, commits and issue links, plus any other PR rule the repo documents (labels, changelog, sign-off). Repo rules come from `CONTRIBUTING.md`, the PR template, commitlint config, and title-check workflows.

**Title**: imperative mood ("Add retry to upload"), about 60 characters (66 at most), no trailing period, saying what changes for the project's users. A bug fix names the fixed behavior, not the mechanism. Conventional-commit format only if the repo documents it or most of its last 20 merged PR titles use it (`gh pr list --state merged --limit 20`); then the type and scope must fit the change.

**Description**: fills the PR template if there is one. Otherwise it tells a reviewer what changed and why, how it was verified, and what could break.

**Issue links**: an issue the PR resolves is referenced with a closing keyword (`Closes #123`) so merging closes it; a bare mention won't.

**Commits**: find the merge strategy from the repo's settings (`gh api repos/<owner>/<repo> --jq '{merge: .allow_merge_commit, rebase: .allow_rebase_merge, squash: .allow_squash_merge}'`, where `null` means unknown), documented policy, and `git log --merges` on the base branch.

- **Squash-merge only**: commit messages end up in the squash commit's body, so each one describes its change accurately.
- **Otherwise**: commits land on the base branch as-is, so each subject meets the title rules, bodies explain why, and each commit is one small, atomic change, with no `WIP` or `fixup!` commits.
