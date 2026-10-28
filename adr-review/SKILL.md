---
name: adr-review
description: "Review an architectural decision record (ADR) in the current repo with parallel reviewer subagents. Before merge: whether it warrants existing and whether every word is true and necessary. After merge: whether it still warrants existing, whether later code follows it, and whether edits keep its intent. Reports a verdict with confidence in chat. Use when the user asks to review an ADR or decision record."
---

You review one ADR; you never edit it, the code, or anything else. An ADR is a constitutional amendment: before it merges, anything in it is open to change; once merged, its intent binds all later code until a superseding ADR replaces it. One setup step, one parallel wave of reviewers, one merge.

## 1. Setup

Resolve the argument (a path, or an ADR number or title) to `<path>` in the current repo. Then run:

- `git fetch -q origin` and find `<default>` with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `git log origin/<default> --diff-filter=A --format='%H %as' -- <path>`: the commit and date the ADR **merged**. Empty means it hasn't.
- `git diff origin/<default> -- <path>`: pending **edits** to a merged ADR.
- List the repo's other ADRs and their statuses, from the same directory.

The ADR is **pre-merge** when it isn't on `origin/<default>`, otherwise **merged**.

## 2. Review wave

In one message, launch every reviewer that applies as a background `general-purpose` subagent. Never fork: each starts with a fresh context, and its prompt carries only the brief below, never your own reading of the ADR.

| Reviewer | Launch when | Model |
|---|---|---|
| `warrant` | always | inherit |
| `precedent` | always | sonnet |
| `claims` | pre-merge | inherit |
| `wording` | pre-merge | sonnet |
| `compliance` | merged | inherit |
| `edits` | merged, with pending edits | sonnet |

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review the ADR at `<path>` in `<repo root>`. State: `<pre-merge, or merged at <sha> on <date>>`. Default branch: `origin/<default>`. Other ADRs: `<list with statuses>`."

## 3. Verdict

When every reviewer has returned, merge duplicate findings, keep the higher severity, and number them `F1`, `F2`, … in report order.

- **Pre-merge verdict**: Reject if any finding is Blocking or Should fix, otherwise Approve.
- **Merged verdict**: **Keep**, **Supersede** with the replacement ADR text `warrant` proposed, or **Reject** with no replacement. Reject only on significant just cause: evidence that the decision is now wrong and that no decision should take its place. Pending edits that change intent are rejected separately, whatever the verdict.
- **Confidence**: start at High and drop one step, to a floor of Low, for each gap: a reviewer that failed or returned nothing; a claim or rule no reviewer could check; for a merged ADR, history too large to read since the merge. Confidence never changes the verdict.

Reply in chat:

```
**Supersede** · confidence High · 1 Blocking, 1 Should fix, 0 Nits

### Blocking
F1 `docs/adr/0004-crates.md:12` (warrant): <problem>. Fix: <one line>.
### Should fix
### Nits
### Violations
- `src/x.rs:40` (added <sha>, <date>): <how it breaks the decision>
### Proposed ADR
<replacement text, for Supersede only>
```

Omit empty sections.
