---
name: improve-codebase-compliance
description: Audits the codebase against its coding standards (or best practices wherever it has none), presents ranked findings as a visual HTML report, then grills through whichever you pick.
disable-model-invocation: true
---

# Improve Codebase Compliance

Surface where the codebase drifts from its coding standards, rank the drift, and walk the user to a **shared understanding** of what is worth changing. Treat every standard as a **guideline**: it records what the team usually wants, and a deviation can be deliberate, obsolete, or outside the rule's intent. This skill changes no code; the user decides what to do with the result.

## Process

### 1. Gather the standards

Needs `git`, and the `grilling` skill for step 4.

Search the repo for every file that documents how code should be written: `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md` / `CLAUDE.md`, style guides under `docs/`, ADRs in `docs/adr/`, and rules embedded in READMEs. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

Split the rules in two:

- **Tool-enforced** rules (linters, formatters, type checkers configured in the repo): run the tool and take its output as findings. Spend no reading on them.
- **Prose** rules: the audit's real work.

ADRs and in-code comments that justify a deviation are **exceptions**, and an exception overrides the rule it excuses. The repo's standards are fixed input: audit against them as written.

**Gaps**: wherever the repo documents no standards for a language or area the codebase has (or none at all), fall back to **best practices** for that gap: take the official guide for that language or area (PEP 8, Effective Go, the Rust API Guidelines, Microsoft's .NET coding conventions) or a widely adopted guide from a tier-1 engineering org (Google's style guides, Meta's, Microsoft's). Name the exact guide behind every rule you apply. A best-practice finding is never more than a `Judgment call`: the team never agreed to it.

Done when you can list every standards source with its rule count, each one marked repo-documented or best practice.

### 2. Audit

If the user named a direction (a module, a rule, a language), scope the audit to it. Otherwise audit the whole codebase.

Spawn audit subagents in parallel, one per standards source (split a large source by rule group, or the codebase by top-level area, so each subagent's slice fits comfortably). Paste each subagent its rules verbatim and the known exceptions. Each finding must carry:

- **Rule**: source and the quoted rule.
- **Location**: `path:line`, plus the count of sibling sites when the same violation repeats.
- **Evidence**: the quoted code.
- **Confidence**: `Violation` (the rule plainly applies and is plainly broken) or `Judgment call` (the rule's wording, intent, or reach is ambiguous here).

Done when every prose rule has been applied to its whole slice and every subagent has reported.

### 3. Prioritize and present as an HTML report

Group findings into **batches**: findings that share a rule and a fix shape, so one decision settles them all. Rank the batches by:

1. **Impact**: what the rule protects (security and correctness above consistency above taste).
2. **Locality**: hot spots first. Walk `git log` to find the files that change most; a fix there pays back on every future change.
3. **Cost**: sites touched, and the risk of each change.

For each batch, look for a static lint or check that would enforce its rule from here on, so the drift cannot return: first a rule in a tool the repo already runs (enabling a rule in its linter config), then a new tool or a small custom check. Name the exact rule and the config change. Leave the field empty when the rule needs human judgment to apply.

When any rule came from best practices, the top-ranked candidate is always **Write down the missing standards**, however few best-practice findings there were. Its starting content is the guides you used and the rules that produced findings.

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/compliance-review-<timestamp>.html`. Open it for the user (`open` on macOS, `xdg-open` on Linux, `start` on Windows) and tell them the absolute path. See [HTML-REPORT.md](HTML-REPORT.md) for the scaffold and card format.

After the file is written, ask the user: "Which of these would you like to explore?"

### 4. Grill to a shared understanding

Once the user picks one or more batches, call the Skill tool with "grilling" and walk each one. The design tree for a batch covers:

- **Applicability**: does the rule's intent actually bear on these sites, or only its letter?
- **Exception**: is the deviation deliberate? Read the history (`git log -L`, blame, linked issues) before asking; facts are yours to find.
- **Reach**: every site, hot spots only, or new code only from here on?
- **Fix shape**: the concrete change, shown on one representative site.
- **Blast radius**: public interfaces, persisted data, or callers outside the repo that the change would break.
- **Enforcement**: adopt the suggested lint or check, and does it land with the fix or before it (flagging only new code)?

For the **Write down the missing standards** candidate, the tree is which rules to adopt, which to reject, and where they go: an existing standards file to extend, or a new one. Ask the user, then write them there once they confirm the content.

Done when every picked batch has an agreed reach, fix shape, and file list, or is dropped, and the user confirms the shared understanding. Close with a summary of the agreed scope per batch, including its agreed lint or check, plus any deliberate exceptions uncovered that the user may want to record, so the next audit skips them.
