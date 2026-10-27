---
name: pr-review
description: "Review a pull request with parallel reviewer subagents covering its metadata, prose, behavior and tests, interfaces, design and security, plus any installed code review skill. Reports an Approve / Reject verdict with confidence and CI status in chat. Use when the user asks to review a PR or pull request."
---

You review a pull request; you never change it or run its code. One setup step, one parallel wave of reviewers, one merge.

## 1. Setup

Resolve the PR to `<owner>/<repo>` and `<n>` (from a URL, `<owner>/<repo>#<n>`, or `gh pr view` on the current branch), and pass `--repo <owner>/<repo>` to every `gh` call. Run these together:

- `gh pr view <n> --json number,url,title,body,commits,files,baseRefName,closingIssuesReferences`
- `gh pr checks <n>`: record each check as passed, failed or pending. Never wait for pending checks.
- `gh repo view <owner>/<repo> --json visibility`
- `gh issue view` for each closing issue: together they are the **spec**. With none, the PR description is the spec.
- A scratch clone in `<tmp>`, a fresh directory from `mktemp -d`: `gh repo clone <owner>/<repo> <tmp> -- --filter=blob:none -q`, then `git -C <tmp> fetch -q origin +pull/<n>/head:pr-<n>` and `git -C <tmp> checkout -q pr-<n>`.

Sort the changed files. **Prose**: docs, READMEs, changelogs, ADRs, agent instructions (skills, `AGENTS.md`, `CLAUDE.md`, prompts), comment-only edits. **Code**: everything else, including config, CI and build files.

## 2. Review wave

Pick the **code review skill** now, if code changed: Matt Pocock's `code-review`; else the first installed skill whose description says it reviews a diff, branch or PR (not this skill, not `security-review`); else none.

In one message, launch every reviewer that applies as a background `general-purpose` subagent:

| Reviewer | Launch when | Model |
|---|---|---|
| `metadata` | always | sonnet |
| `prose` | prose changed | sonnet |
| `behavior`, `interfaces`, `design`, `security` | code changed | inherit |

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review PR `<url>`. Clone: `<tmp>`, PR checked out, base `origin/<baseRefName>`. Your files: `<list>`. Spec: `<issue text, or 'the PR description'>`. Repo visibility: `<visibility>`." Tell `design` whether a code review skill is running.

While they run, run the code review skill yourself from inside `<tmp>`, giving it `origin/<baseRefName>` as the fixed point and the spec, so it never stops to ask.

## 3. Verdict

When every reviewer has returned, merge duplicate findings, keep the higher severity, and number them `F1`, `F2`, … in report order. Delete `<tmp>`.

- **Verdict**: Reject if any finding is Blocking or Should fix, otherwise Approve.
- **Confidence**: start at High and drop one step, to a floor of Low, for each gap: pending CI checks; no spec beyond a thin description; a reviewer that failed or returned nothing; a diff too large to read in full; a coverage gap reported by `behavior`. Confidence never changes the verdict.
- **CI**: report each failed and pending check. CI is never a finding and never changes the verdict; gating merges is the repo's job.

Reply in chat:

```
**Reject** · confidence Medium (2 checks pending) · 1 Blocking, 2 Should fix, 3 Nits
CI: 🔴 lint failed · 🟡 2 pending · 🟢 5 passed

### Blocking
F1 `src/x.py:42` (behavior): <problem>. Fix: <one line>.
### Should fix
### Nits
### Code review (<skill name>, as reported)
### Automate this
- <lint rule or CI step>: would have caught F3, F5
```

Omit empty sections. Keep the code review skill's output as it reported it, but give each of its findings a severity, which counts toward the verdict.
