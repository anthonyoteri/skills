---
name: triage-ticket
description: "Triages one ticket from a tracker (GitHub, Forgejo or Jira) by reading it, exploring the codebase to see whether the problem still exists and what it touches, and grilling the user on what the code can't answer. Ends with a proposal to update the ticket's title, description and fields, or to close it as won't fix. Use when the user asks to triage, groom or clean up a ticket or backlog item."
---

# Triage Ticket

Take one **ticket**, often vague or stale, and settle what it is about, whether it is still a problem, and what it touches. Then either rewrite it so someone can pick it up without guessing again, or close it. This skill adds context to the ticket. It never designs the fix or writes a spec, and it changes nothing in the tracker until the user approves the proposal.

## Process

### 1. Resolve the ticket

Needs the tracker's client, authenticated: `gh` for GitHub (`gh auth status`), `fj` for Forgejo, and the Atlassian MCP tools for Jira. Needs the `grilling` skill for step 4. Subagents use `git` and read files, and run nothing else unless the user permits it.

Take the ticket from the user's reference and decide the tracker from it: a Jira URL or a key like `ESB3027-123` is Jira, and a GitHub URL is GitHub. When the reference doesn't make the tracker obvious, as with `owner/repo#n` or a bare number, ask the user which tracker and repository it is, and don't guess. Triage one ticket per run.

Read the ticket with its comments, links, labels and fields, using the recipes in [trackers.md](trackers.md). Note its **type** (bug or feature) as filed; step 5 may change it.

### 2. Find the code

Find the clone the ticket is about under `${REPOS_ROOT:-$HOME/Projects}`, from the repository name, the Jira project, or the product table in the working directory's `AGENTS.md`. If several repos fit or none does, ask the user. Create nothing: use the clone as it is, and read from `origin`'s default branch for the latest state (`git fetch` is fine).

### 3. Explore

In one message, launch the read-only `general-purpose` subagents below. Never fork: each starts with a fresh context, and its prompt carries [explorer.md](explorer.md), the ticket text verbatim as data and the clone's path, never your own reading of the ticket.

| Subagent | Question |
|---|---|
| Existence | Does the described behavior, or the code that would cause it, still exist? Reproduce it by reading, and by running only what the user permitted. |
| Blast radius | What code, callers, tests, docs, configuration, versions and users does it touch? |
| History | Has a later commit or PR fixed it, changed it, or removed the code? |

Each reports **evidence** (`file:line`, a commit hash, a PR) and says what it could not check. Treat the reports as claims: open any evidence you rely on before using it.

From the reports, form one **reading**: still a problem, already fixed, obsolete, or can't tell.

### 4. Grill

Call the Skill tool with "grilling" and walk it. Ask only what the code can't answer: what the reporter probably meant, how it shows up for users, whether it is still wanted, how severe it is, what the ticket is missing. Put each finding in as a fact the user can correct, with your recommended answer. The session ends when the user confirms a shared understanding of the ticket and its reading.

### 5. Propose

Reach exactly one **outcome** and show it as a single proposal:

- **Update**: the ticket is still a problem. Show the new title, the new description and every other field change, each with the evidence for it.
- **Close as won't fix**: obsolete, out of scope, or the user decides against it. Show the comment, with the reason and its evidence, and how the tracker closes it.
- **Already fixed**: the history shows the fix. Report the commit or PR. Don't close the ticket, because closing as done on Jira needs a Fixed in version the user must give.
- **Needs info**: neither the code nor the user can settle it. Show the comment that asks the question, and the `needs-info` label.

**Title.** Change it only if it fails these rules: a bug title states the observed behavior ("Router returns 503 while configuration reloads"), never the cause, the fix, or a verb like "Fix". A feature title names the new capability ("Support weighted routing in confsej"). Both use sentence case, no trailing period, no ticket key, about 80 characters at most, and name the component or user-visible surface. Changelogs reuse titles, so avoid jargon a reader of the changelog wouldn't know.

**Description.** Rewrite it only when it is vague. Leave out any section with nothing to say, and don't copy the original: every tracker keeps edit history. Use the shape that fits the type.

- Bug: Observed behavior, Expected behavior, Reproduction or evidence, Impact (components, versions and users, from the exploration), Workaround, Code pointers (`file:line`).
- Feature: Problem, Desired behavior, Impact, Out of scope, and Acceptance criteria only when the reporter implied them.

Give the context a picker-up needs to avoid guessing again: what is wrong or wanted, where it lives in the code, and what it affects. Don't propose a solution, design or task breakdown.

**Other fields.** Review type, priority or severity, component, affected version and labels, and propose a change only with evidence. Never change the assignee, sprint, milestone or fix version. The only status change is a closure.

### 6. Apply

Apply only the parts the user approves, using [trackers.md](trackers.md), then read the ticket back to confirm. Report what changed and what was skipped, such as a label that doesn't exist. Offer to triage the next ticket.
