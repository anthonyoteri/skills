---
name: finalize-pr
description: "Brings a pull request to a mergeable state with a capped pr-review and fix loop, and reports the result in one PR comment."
disable-model-invocation: true
---

You take one pull request and loop review, fix and push until the reviewer approves and every required check passes, or the round cap runs out. You never change the PR's draft or ready state, never split it, and never force-push.

## 1. Setup

Needs `git` and `gh`, authenticated (`gh auth status`), and the `pr-review` skill.

Arguments: the PR (number, URL or `<owner>/<repo>#<n>`), then optional `rounds=N` (default 5), then any free text: the **instructions**, which bind every step and the fixer.

Pass `--repo <owner>/<repo>` to every `gh` call, and run these together:

- `gh pr view <n> --json number,url,headRefName,baseRefName,isCrossRepository,closingIssuesReferences`. Stop if `isCrossRepository`: you can't push to a fork.
- `gh issue view` for each closing issue: together they are the **spec**. With none, the PR description is the spec.
- The report comment: `gh api repos/<owner>/<repo>/issues/<n>/comments --paginate --jq '.[] | select(.body | contains("<!-- finalize-pr -->")) | .id'`. Reuse it if found, so a rerun updates the same comment.
- A worktree in a fresh `mktemp -d` directory, from the repo's clone: `git fetch -q origin <headRefName>`, then `git worktree add --detach <wt> origin/<headRefName>`.

## 2. Rounds

A **round** is one CI wait, one `pr-review`, and one fix pass if needed. Run up to N rounds:

1. **Wait for CI** on the PR's head, polling `gh pr checks <n> --required --json name,state,startedAt,link` every 30 seconds. A **required check** still queued or pending 10 minutes after the push (or after setup, in round 1) is **not run**; once one has started, wait for it to finish, however long. `SUCCESS`, `NEUTRAL` and `SKIPPED` pass; `FAILURE` and `ERROR` fail; any other finished state (`CANCELLED`, `TIMED_OUT`, `STARTUP_FAILURE`, `ACTION_REQUIRED`, `STALE`) is not run. Other checks are informational: never wait for them.
2. **Review**: call the Skill tool with "pr-review" on the PR. Tell it that findings you pushed back on in earlier rounds count as rulings the user rejected.
3. **Done** when the verdict is Approve and no required check failed. Required checks that didn't run never hold this up; they lower confidence and are flagged in the report.
4. **Fix**, unless this was round N: launch one `general-purpose` subagent with "Read `<skill dir>/fixer.md`, then fix PR `<url>` in `<wt>`. Spec: `<spec>`. Findings: `<every Blocking, Should fix and Nit, with IDs>`. Failed required checks: `<name and link each>`. Instructions: `<instructions, or none>`." It commits and returns each finding's outcome.
5. **Push**: `git -C <wt> push origin HEAD:<headRefName>`. If it's rejected because the branch moved, stop and tell the user; a rebase needs a force-push, which is theirs to make.
6. **Report**: create or update the report comment (step 4).

## 3. Follow-ons

After the last round, list in chat, numbered, every Follow-on from the latest round, every Should fix the fixer left, and every finding it pushed back on, each with your recommendation. Ask the user to reply in one message with a choice per item:

- **File**: `gh issue create` with the finding as the body, opening with "Follow-on from #<spec> found in #<n>."
- **Fix**: one more fix pass, push and round on just these, past the cap.
- **Drop**: listed in the report, unlinked. For a pushed-back finding, this keeps the pushback.

Skip this step when the list is empty.

## 4. Report

One PR comment, rewritten in full after each round and after step 3: create it with `gh pr comment <n> --body-file <file>`, update it with `gh api -X PATCH repos/<owner>/<repo>/issues/comments/<id> -F body=@<file>`.

```
<!-- finalize-pr -->
**Approve** · confidence Medium (1 required check not run) · round 3 of 5 · CI: 🟢 4 required passed
⚠️ Required check not run: `integration-tests` (cancelled)

### Fixed
- F1 `src/x.py:42`: <problem> · a1b2c3d
### Pushed back
- F4 `src/y.py:10`: <problem>. <reason>
### Follow-ons
- #123 <title>
- <title> (dropped)
### Nits not fixed
- F9 `src/z.py:3`: <problem>
```

The header is the latest verdict; on Reject, add a line naming the unresolved Blocking findings. Put the ⚠️ line first under the header whenever a required check didn't run or failed in the latest round. Omit empty sections, and wrap any section with more than 5 items in `<details><summary>Fixed (12)</summary>` … `</details>`. Finding IDs restart each `pr-review` round, so prefix them with the round once there's more than one (`R2-F1`).

When done, `git worktree remove <wt>`, and reply in chat with the header line and the comment's link.
