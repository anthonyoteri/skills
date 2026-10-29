---
name: pr-review
description: "Reviews a pull request with parallel reviewer subagents covering its metadata, its fit with the surrounding code, prose, behavior and tests, interfaces, design and security, plus any installed code review skill. Reports an Approve / Reject verdict with confidence and CI status in chat. Use when the user asks to review a PR or pull request."
---

You review a pull request; you never change it or run its code. One setup step, one parallel wave of reviewers, one merge.

## 1. Setup

Needs `git`, `curl` and `gh`, authenticated (`gh auth status`). Uses the `adr-review` and `unslop` skills, and a code review skill (see step 2), if installed.

Resolve the PR to `<owner>/<repo>` and `<n>` (from a URL, `<owner>/<repo>#<n>`, or `gh pr view` on the current branch), and pass `--repo <owner>/<repo>` to every `gh` call. Run these together:

- `gh pr view <n> --json number,url,title,body,commits,files,baseRefName,closingIssuesReferences`
- `gh pr checks <n>`: record each check as passed, failed or pending. Never wait for pending checks.
- `gh repo view <owner>/<repo> --json visibility`
- `gh issue view` for each closing issue: together they are the **spec**. With none, the PR description is the spec.
- A scratch clone in `<tmp>`, a fresh directory from `mktemp -d`: `gh repo clone <owner>/<repo> <tmp> -- --filter=blob:none -q`, then `git -C <tmp> fetch -q origin +pull/<n>/head:pr-<n>` and `git -C <tmp> checkout -q pr-<n>`.

**Rounds**: when an earlier round in this conversation reviewed this PR, or the user gives `since <sha>`, this round is **incremental** from that round's head `<since>`, unless the user asks for `full`. Fetch it (`git -C <tmp> fetch -q origin <since>`); if that fails or `<since>` isn't an ancestor of `HEAD`, as after a force push, review the whole PR. In an incremental round, the changed files and size below come from `<since>..HEAD`, keeping only files the PR itself changes (`origin/<baseRefName>...HEAD`), so a merge from the base branch doesn't count.

Sort the changed files. **ADRs**: files in the repo's ADR directory, when the `adr-review` skill is installed; otherwise they are prose. **Prose**: docs, READMEs, changelogs, agent instructions (skills, `AGENTS.md`, `CLAUDE.md`, prompts), comment-only edits. **Code**: everything else, including config, CI and build files.

The code's **size** is its added lines, summed over the code files in `git -C <tmp> diff --numstat origin/<baseRefName>...HEAD`, leaving out lockfiles and **generated** files, the ones the base branch's `.gitattributes` marks `linguist-generated`.

## 2. Review wave

Pick the **code review skill** now, if code changed: Matt Pocock's `code-review`; else the first installed skill whose description says it reviews a diff, branch or PR (not this skill, not `security-review`); else none.

In one message, launch every reviewer that applies as a background `general-purpose` subagent:

| Reviewer | Launch when | Model |
|---|---|---|
| `metadata` | always | sonnet |
| `context` | unless dependency-only | inherit |
| `prose` | prose changed | sonnet |
| `behavior`, `interfaces`, `design`, `security` | code changed | inherit |

Generated files aren't reviewed, and lockfiles go to one `interfaces` reviewer.

A PR is **dependency-only** when every code file is a lockfile or a dependency manifest whose only changes are dependency versions, as in a Dependabot or Renovate bump. Launch only `metadata`, `interfaces`, `security`, and `prose` if prose changed, and skip the code review skill.

If the size is more than one reviewer can read with care (about 1,500 lines of Python; more for verbose code, less for dense), split the code files by directory into **batches** within that limit, and launch each code reviewer once per batch. `context` still runs once, over the whole PR.

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review PR `<url>`. Clone: `<tmp>`, PR checked out, base `origin/<baseRefName>`. Your files: `<list>`. Spec: `<issue text, or 'the PR description'>`. Repo visibility: `<visibility>`." In an incremental round, add "Since: `<since>`" to every prompt but `metadata`'s, and give each reviewer the earlier rounds' findings in its area that the user didn't reject or defer. Tell `design` whether a code review skill is running, and `metadata` and `context` whether the code was batched.

While they run, run the code review skill yourself from inside `<tmp>`, giving it `<since>` in an incremental round, otherwise `origin/<baseRefName>`, as the fixed point and the spec, so it never stops to ask. Then run `adr-review` from inside `<tmp>` on each ADR, by path.

## 3. Verdict

When every reviewer has returned, merge duplicate findings and keep the higher severity. Re-check every finding, including those of the code review skill and `adr-review`, against the PR's goal (Follow-on in `reviewers/common.md`), and move any outside it to Follow-on whatever severity it was given. Number the rest `F1`, `F2`, … in report order. Delete `<tmp>`.

- **Verdict**: Reject if any finding is Blocking, naming in the header the findings whose fixes would turn it to Approve; otherwise Approve. Should fix, Nits and Follow-on never hold up approval.
- **Rulings**: drop any finding the user rejected or deferred in an earlier round of this conversation, unless what it's about has changed since, and give the count in the header.
- **Split**: when a reviewer names a file it couldn't read in full, raise `metadata`'s proposed split, or propose one yourself, as Should fix.
- **Confidence**: start at High and drop one step, to a floor of Low, for each gap: pending CI checks; no spec beyond a thin description; a reviewer that failed or returned nothing; any reviewer naming a file it couldn't read in full (once); a coverage gap reported by `behavior`. Confidence never changes the verdict.
- **CI**: report each failed and pending check. CI is never a finding and never changes the verdict; gating merges is the repo's job.

Reply in chat:

```
**Reject** · confidence Medium (2 checks pending) · approves once F1 is fixed · 1 Blocking, 2 Should fix, 3 Nits, 1 Follow-on · 2 omitted per earlier rulings
Reviewed: `a1b2c3d` (incremental since `9f8e7d6`)
CI: 🔴 lint failed · 🟡 2 pending · 🟢 5 passed

### Blocking
F1 `src/x.py:42` (behavior): <problem>. Fix: <one line>.
### Should fix
### Nits
### Follow-on
F7 `src/y.py:10` (design): <title for a separate issue>. Outside the goal: <why>.
### Automate this
- <lint rule or CI step>: would have caught F3, F5
```

Omit empty sections. Merge the findings of the code review skill and `adr-review` with the reviewers', giving each a severity. Report each finding once: list under Automate this only automation that isn't already a finding's fix.
