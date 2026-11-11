---
name: pr-review
description: "Reviews a pull request with a few fresh-context reviewer subagents, checking that it does what it claims and introduces nothing bad or hard to reverse. Reports an Approve / No verdict / Reject verdict and actionable findings in chat. Use when the user asks to review a PR or pull request."
---

You review a pull request; you never change it or run its code. One setup step, one parallel wave of reviewers, one merge. Reviewers are subagents so they see the PR without the development conversation.

## 1. Setup

Needs `git` and `gh`, authenticated (`gh auth status`). Uses the `adr-review` skill if installed.

Resolve the PR to `<owner>/<repo>` and `<n>` (from a URL, `<owner>/<repo>#<n>`, or `gh pr view` on the current branch), and pass `--repo <owner>/<repo>` to every `gh` call. Run these together:

- `gh pr view <n> --json number,url,title,body,commits,files,baseRefName,closingIssuesReferences`
- `gh pr checks <n>`: record each check as passed, failed or pending. Never wait for pending checks.
- `gh repo view <owner>/<repo> --json visibility`
- `gh issue view` for each closing issue: together they are the **spec**. With none, the PR description is the spec.
- A scratch clone in `<tmp>`, a fresh directory from `mktemp -d`: `gh repo clone <owner>/<repo> <tmp> -- --filter=blob:none -q`, then `git -C <tmp> fetch -q origin +pull/<n>/head:pr-<n>` and `git -C <tmp> checkout -q pr-<n>`.

**Rounds**: when an earlier round in this conversation reviewed this PR, or the user gives `since <sha>`, this round is **incremental** from that round's head `<since>`, unless the user asks for `full`. Fetch it (`git -C <tmp> fetch -q origin <since>`); if that fails or `<since>` isn't an ancestor of `HEAD`, as after a force push, review the whole PR. In an incremental round, the changed files and size below come from `<since>..HEAD`, keeping only files the PR itself changes (`origin/<baseRefName>...HEAD`), so a merge from the base branch doesn't count.

Sort the changed files. **ADRs**: files in the repo's ADR directory, when the `adr-review` skill is installed. **Prose**: docs, READMEs, changelogs, agent instructions (skills, `AGENTS.md`, `CLAUDE.md`, prompts), comment-only edits. **Code**: everything else, including config, CI and build files.

The code's **size** is its added lines, summed over the code files in `git -C <tmp> diff --numstat origin/<baseRefName>...HEAD`, leaving out lockfiles and **generated** files, the ones the base branch's `.gitattributes` marks `linguist-generated`. Generated files aren't reviewed.

A PR is **small** when its size is about 300 lines or fewer, or it is **dependency-only**: every code file is a lockfile or a dependency manifest whose only changes are dependency versions, as in a Dependabot or Renovate bump.

## 2. Review wave

In one message, launch every reviewer that applies as a background `general-purpose` subagent. Use `model: sonnet` for all, unless the user said `deep`: then omit `model`, so they inherit the session's.

| PR | Reviewers |
|---|---|
| Small | one `combined` reviewer over all the code, plus `text` if prose or the PR text needs it |
| Otherwise | `correctness`, `risk`, `context`, plus `text` if prose or the PR text needs it |
| ADRs changed | add `adr-review`, run as its own subagent from inside `<tmp>`, one per ADR, by path |

`text` runs when prose changed, or the PR description or closing-issue link needs checking (always, unless the PR is dependency-only).

If the size is more than about 2,500 lines, split the code files by directory into **batches** within that limit, and launch `correctness` and `risk` once per batch. `context` and `text` run once, over the whole PR.

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review PR `<url>`. Clone: `<tmp>`, PR checked out, base `origin/<baseRefName>`. Your files: `<list>`. Spec: `<issue text, or 'the PR description'>`. Repo visibility: `<visibility>`." For `combined`, name `correctness.md`, `risk.md` and `context.md`. In an incremental round, add "Since: `<since>`" to every prompt, and give each reviewer the earlier rounds' findings that the user didn't reject or defer.

## 3. Verdict

When every reviewer has returned, merge duplicate findings, and drop any a reviewer reported that fails the bar in `reviewers/common.md`. Drop any the user rejected or deferred in an earlier round of this conversation, unless what it's about has changed since. Number the rest `F1`, `F2`, … in report order. Delete `<tmp>`.

- **Approve**: merge as is, or once the reported findings are fixed.
- **Reject**: given everything the reviewers found, reported or not, you would recommend against merging without significant corrections. Name the findings, or the underlying problem, that decide it.
- **No verdict**: you can neither confidently approve nor reject. A gap leads here: a reviewer that failed or returned nothing, a file a reviewer couldn't read in full, no spec beyond a thin description. Say in one line why.
- **CI**: report each failed and pending check. CI never changes the verdict; gating merges is the repo's job.

Reply in chat, omitting empty sections:

```
**Approve** once F1 and F2 are fixed · 1 Blocking, 2 Should fix, 1 Nit
Reviewed: `a1b2c3d` (incremental since `9f8e7d6`)
CI: 🔴 lint failed · 🟡 2 pending · 🟢 5 passed

### Blocking
F1 `src/x.py:42` (correctness): <problem>. Fix: <one line>.
### Should fix
### Nits
```

Every finding is one the user should act on, so "fix anything reported" is a complete reply. Report each finding once. A finding from `adr-review` goes through the same bar.
