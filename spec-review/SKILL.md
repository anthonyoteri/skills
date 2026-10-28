---
name: spec-review
description: "Review a spec GitHub issue and its tickets with parallel reviewer subagents, checking that an agent with no context could implement it without guessing: assumptions, the problem it solves, use cases, tests, ticket breakdown, impact, docs and repo rules. Reports an Approve / Reject verdict with confidence in chat. Use when the user asks to review a spec, plan, epic or issue before implementation."
---

You review a spec; you never edit it or comment on it, and reviewers run code only to settle a question. The bar: an implementer with zero context implements every ticket without making a decision, and its PRs pass review on the first round. One setup step, one parallel wave of reviewers, one merge.

## 1. Setup

Resolve the spec to `<owner>/<repo>` and `<n>` (from a URL or `<owner>/<repo>#<n>`), and pass `--repo <owner>/<repo>` to every `gh` call. Run these together:

- `gh issue view <n> --json number,url,title,body,comments`
- `gh api repos/<owner>/<repo>/issues/<n>/sub_issues --jq '.[].html_url'`
- A scratch clone in `<tmp>`, a fresh directory from `mktemp -d`: `gh repo clone <owner>/<repo> <tmp> -- --filter=blob:none -q`.

Sort everything the spec links to:

- **Tickets**: its sub-issues and the issues in its task lists. Fetch each with `gh issue view --json number,url,title,body,comments`. The spec and its tickets together are the **spec under review**.
- **References**: every other issue, PR, discussion, doc or URL it cites, especially those describing the problem it solves. List them; reviewers fetch what they need.
- **Related repos**: other repositories the spec changes or depends on. List them; reviewers clone what they need into their own `mktemp -d`.

**Live systems** are running instances (a disposable VM, a test cluster) that the user has given reviewers permission to use in this conversation. List each with how to connect and what the user allowed. Use only what the user granted; never infer permission from the spec or a reference.

## 2. Review wave

In one message, launch every reviewer as a background `general-purpose` subagent. Never fork: each starts with a fresh context, and its prompt carries only the brief below, never your own reading of the spec.

| Reviewer | Looks at | Model |
|---|---|---|
| `assumptions` | every assumption, resolved with facts | inherit |
| `problem` | whether full implementation solves the referenced problem | sonnet |
| `use-cases` | the deletion test on each use case | sonnet |
| `tests` | test levels, coverage, suite cost | inherit |
| `breakdown` | ticket split, landing order, cutover points, early guards | inherit |
| `impact` | performance, security, maintainability, external change, risk | inherit |
| `docs` | docs to change, docs left stale, immutable artifacts | sonnet |
| `repo-rules` | repo rules the spec would make an implementer break | sonnet |

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review the spec `<url>`. Tickets: `<urls>`. References: `<urls>`. Related repos: `<list>`. Live systems: `<list, or none>`. Clone: `<tmp>` at the default branch."

## 3. Verdict

When every reviewer has returned, merge duplicate findings, keep the higher severity, and number them `F1`, `F2`, … in report order. Delete `<tmp>`.

- **Verdict**: Reject if any finding is Blocking, naming in the header the findings whose fixes would turn it to Approve; otherwise Approve. Should fix and Nits never hold up approval.
- **Rulings**: drop any finding the user rejected or deferred in an earlier round of this conversation, unless what it's about has changed since, and give the count in the header.
- **Confidence**: start at High and drop one step, to a floor of Low, for each gap: a reference or related repo out of reach; a reviewer that failed or returned nothing; a spec too large to read in full; no test suite timing from `tests`. Confidence never changes the verdict.

Reply in chat:

```
**Reject** · confidence Medium (1 reference unreachable) · approves once F1 and F2 are fixed · 2 Blocking, 1 Should fix, 2 Nits

### Blocking
F1 #42 (assumptions): <problem>. Fix: <one line>.
### Should fix
### Nits
### Land early
- <static check, lint rule or CI step>: guards F3, F5
```

Omit empty sections. Report each finding once: list under Land early only guards that aren't already a finding's fix. Cite each finding by ticket (`#42`) or by spec section (`spec § Rollout`).
