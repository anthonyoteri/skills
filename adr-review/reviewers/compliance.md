# Compliance reviewer

Check whether code bound by the ADR follows its decision: code alongside it on the current branch (`git diff origin/<default>...HEAD`), code in the commit that merged it, and every change since. Code from before that commit is grandfathered: never report it.

1. Turn the decision into concrete checks: what following it looks like in code, and what breaking it looks like (a pattern, an import, a dependency, a file layout).
2. Review the code alongside, the merge commit itself (`git show <merge sha>`), and every change on the default branch since (`git log --format='%h %as %s' <merge sha>..origin/<default>`), using `git grep` and `git show` on the commits that touch the decision's area.
3. Confirm with `git blame` that each violation came from the code alongside, the merge commit or a later one.

Report each violation as a finding with the file, line, commit and date. After your findings, add one line: `Violations: <count>`, or `Violations: none`, plus any check you couldn't turn into a search.
