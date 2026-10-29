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

The spec's **size** is the line count of the spec and ticket bodies together.

**Rounds**: note this round's time `<at>`, the latest `updatedAt` across the spec, its tickets and their comments. When an earlier round in this conversation reviewed this spec, or the user gives `since <time>`, this round is a **re-review** from that round's `<since>`, unless the user asks for `full`. If nothing changed after `<since>` (no edits, comments or tickets), reply that the spec is unchanged and stop. Otherwise, write these **re-review references** to files in a fresh `mktemp -d`:

- **Diff**: for the spec and each ticket, a unified diff from its body at `<since>` to its body now. Take the earlier body from the earlier round in this conversation, or else from the latest revision at or before `<since>` in the issue's edit history: `gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){userContentEdits(first:100){nodes{editedAt diff}}}}}' -F o=<owner> -F r=<repo> -F n=<n>`, where each node's `diff` is that revision's full body. A ticket added since is wholly new.
- **Rulings**: each decision the user made since `<since>`, in this conversation or in a comment on the spec or a ticket, with the reason the user gave.
- **Previous verdict**: the earlier round's verdict, minus findings the user rejected or deferred.

They are facts about the spec's history, not your reading of it.

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

If the size is more than one reviewer can read with care (about 800 lines), split the spec and its tickets by section into **batches** within that limit, and launch each reviewer once per batch. `problem` and `breakdown` still run once, over the whole spec. If a single section is still more than one reviewer can read, as with a long inventory, review it anyway and recommend in the verdict that the spec be split.

Prompt each with: "Read `<skill dir>/reviewers/common.md` and `<skill dir>/reviewers/<name>.md`, then review the spec `<url>`. Tickets: `<urls>`. Your sections: `<list, or all>`. References: `<urls>`. Related repos: `<list>`. Live systems: `<list, or none>`. Clone: `<tmp>` at the default branch." In a re-review, add "Re-review since `<since>`. Diff, rulings and previous verdict: `<paths>`."

## 3. Verdict

When every reviewer has returned, merge duplicate findings and keep the higher severity. Then **verify** each Blocking finding: re-read or re-run its evidence yourself, in `<tmp>` or at its URL. Drop a finding whose evidence doesn't hold, and mark one you couldn't check *unverified*. Number the rest `F1`, `F2`, … in report order. Delete `<tmp>` and the re-review references.

- **Verdict**: Reject if any finding is Blocking, naming in the header the findings whose fixes would turn it to Approve; otherwise Approve. Should fix and Nits never hold up approval.
- **Rulings**: drop any finding the user rejected or deferred in an earlier round, unless what it's about has changed since, and give the count in the header.
- **Coverage**: a section of the spec or a ticket that no reviewer read in full is **unread**.
- **Confidence**: start at High and drop one step, to a floor of Low, for each gap: a reference or related repo out of reach; a reviewer that failed or returned nothing; any unread section; any unverified finding; no test suite timing from `tests`. Confidence never changes the verdict.

Reply in chat:

```
**Reject** · confidence Medium (1 reference unreachable) · approves once F1 and F2 are fixed · 2 Blocking, 1 Should fix, 2 Nits · 1 omitted per earlier rulings
Reviewed: `<at>` (re-review since `<since>`)
Unread: spec § Inventory

### Blocking
F1 #42 (assumptions, missed): <problem>. Fix: <one line>.
### Should fix
### Nits
### Land early
- <static check, lint rule or CI step>: guards F3, F5
```

Omit empty sections and empty header lines. In a re-review, give each Blocking finding's origin after its reviewer. Report each finding once: list under Land early only guards that aren't already a finding's fix. Cite each finding by ticket (`#42`) or by spec section (`spec § Rollout`).
