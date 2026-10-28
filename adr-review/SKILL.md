---
name: adr-review
description: "Review an architectural decision record (ADR) in the current repo with parallel reviewer subagents. Before merge: whether it warrants existing and whether every word is true and necessary. After merge: whether it still warrants existing. Reports a verdict with confidence in chat. Use when the user asks to review an ADR or decision record."
---

You review one ADR; you never edit it, the code, or anything else. An ADR is a constitutional amendment: before it merges, anything in it is open to change; once merged, its intent can't change until a superseding ADR replaces it.

## 1. Setup

Resolve the argument (a path, or an ADR number or title found in the repo's ADR directory) to `<path>`, and list the repo's other ADRs with their statuses.

The ADR is **merged** when the current branch is the default branch, otherwise **pre-merge**.

## 2. Review wave

In one message, launch every reviewer that applies as a background `general-purpose` subagent. Never fork: each starts with a fresh context, and its prompt carries only the brief below, never your own reading of the ADR.

| Reviewer | Launch when | Model |
|---|---|---|
| `warrant` | always | inherit |
| `precedent` | always | sonnet |
| `content` | pre-merge | inherit |

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review the ADR at `<path>` in `<repo root>`. State: `<pre-merge or merged>`. Other ADRs: `<list with statuses>`."

## 3. Verdict

When every reviewer has returned, merge duplicate findings, keep the higher severity, and number them `F1`, `F2`, … in report order.

- **Pre-merge verdict**: Reject if any finding is Blocking or Should fix, otherwise Approve.
- **Merged verdict**: **Keep**, **Supersede** with the replacement ADR text `warrant` proposed, or **Reject** with no replacement. Reject only on significant just cause: evidence that the decision is now wrong and that no decision should take its place.
- **Confidence**: start at High and drop one step, to a floor of Low, for each gap: a reviewer that failed or returned nothing; a claim or rule no reviewer could check. Confidence never changes the verdict.

Reply in chat:

```
**Supersede** · confidence High · 1 Blocking, 1 Should fix, 0 Nits

### Blocking
F1 `docs/adr/0004-crates.md:12` (warrant): <problem>. Fix: <one line>.
### Should fix
### Nits
### Proposed ADR
<replacement text, for Supersede only>
```

Omit empty sections.
