---
name: adr-review
description: "Review an architectural decision record (ADR) in the current repo with parallel reviewer subagents. Before merge: whether it warrants existing and whether every word is true and necessary. After merge: whether it still warrants existing and whether edits keep its intent. Reports a verdict with confidence in chat. Use when the user asks to review an ADR or decision record."
---

You review one ADR; you never edit it, the code, or anything else. An ADR is a constitutional amendment: before it merges, anything in it is open to change; once merged, its intent can't change until a superseding ADR replaces it.

## 1. Setup

Resolve the argument (a path, or an ADR number or title found in the repo's ADR directory) to `<path>`, and list the repo's other ADRs with their statuses.

Find the default branch `origin/<default>` with `git fetch -q origin && git symbolic-ref --short refs/remotes/origin/HEAD`, which prints it. The ADR is **merged** when it exists there (`git cat-file -e origin/<default>:<path>`), whatever branch is checked out, otherwise **pre-merge**. For a merged ADR, `git diff origin/<default> -- <path>` shows any pending **edits**.

Record the ADR as this round sees it with `git hash-object -w <path>`, which stores a copy in the object database, leaving the working tree and history alone, and prints its `<blob>`.

**Rounds**: when an earlier round in this conversation reviewed this ADR, or the user gives `since <blob>`, this round is **incremental** from that round's `<since>`, unless the user asks for `full`. Review the whole ADR instead if `<since>` isn't in the repo (`git cat-file -e <since>`) or the ADR has merged since. If `<blob>` equals `<since>`, reply that the ADR is unchanged and stop. In an incremental round of a merged ADR, skip `warrant` and carry over the earlier round's merged verdict, if this conversation has one.

## 2. Review wave

In one message, launch every reviewer that applies as a background `general-purpose` subagent, so each starts with a fresh context and its prompt carries only the brief below, never your own reading of the ADR. When the user asks for the review to use context from the conversation, fork each reviewer instead (`subagent_type: "fork"`, which runs on your own model) and add to its prompt what from the conversation to weigh.

| Reviewer | Launch when | Model |
|---|---|---|
| `warrant` | always | inherit |
| `precedent` | always | sonnet |
| `content` | pre-merge | inherit |
| `edits` | merged, with pending edits | sonnet |

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review the ADR at `<path>` in `<repo root>`. State: `<pre-merge or merged>`. Default branch: `origin/<default>`. Other ADRs: `<list with statuses>`." In an incremental round, add "Since: `<since>`, now `<blob>`", and give each reviewer the earlier rounds' findings in its area that the user didn't reject or defer.

## 3. Verdict

When every reviewer has returned, merge duplicate findings, keep the higher severity, and number them `F1`, `F2`, … in report order.

- **Pre-merge verdict**: Reject if any finding is Blocking, naming in the header the findings whose fixes would turn it to Approve; otherwise Approve. Should fix and Nits never hold up approval.
- **Merged verdict**: **Keep**, **Supersede** with the replacement ADR text `warrant` proposed, or **Reject** with no replacement. Reject only on significant just cause: evidence that the decision is now wrong and that no decision should take its place. Report any pending edit that changes intent as Blocking, alongside the verdict.
- **Rulings**: drop any finding the user rejected or deferred in an earlier round of this conversation, unless what it's about has changed since, and give the count in the header.
- **Confidence**: start at High and drop one step, to a floor of Low, for each gap: a reviewer that failed or returned nothing; a claim or rule no reviewer could check. Confidence never changes the verdict.

Reply in chat:

```
**Supersede** · confidence High · 1 Blocking, 1 Should fix, 0 Nits · 1 omitted per earlier rulings
Reviewed: `<blob>` (incremental since `<since>`)

### Blocking
F1 `docs/adr/0004-crates.md:12` (warrant): <problem>. Fix: <one line>.
### Should fix
### Nits
### Proposed ADR
<replacement text, for Supersede only>
```

Omit empty sections.
