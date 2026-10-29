# skills

Agent skills for Claude Code. Copy a skill's folder into `~/.claude/skills/` to install it.

| Skill | What it does |
|---|---|
| [`pr-review`](pr-review/SKILL.md) | Reviews a pull request with parallel subagents (metadata, context, prose, behavior, interfaces, design, security) against the repo's own rules or best practices, and replies in chat with an Approve / Reject verdict, confidence and CI status. Uses Matt Pocock's [`code-review`](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md) and [`unslop`](https://github.com/theclaymethod/unslop) when installed, and hands ADRs to `adr-review`. |
| [`spec-review`](spec-review/SKILL.md) | Reviews a spec issue and its tickets with parallel subagents (assumptions, problem, use cases, tests, breakdown, impact, docs, coding standards), checking that an agent with no context could implement it without guessing, and replies in chat with an Approve / Reject verdict and confidence. |
| [`improve-codebase-compliance`](improve-codebase-compliance/SKILL.md) | Audits the codebase against its documented coding standards, or official and tier-1 style guides for any language or area it leaves undocumented, opens a ranked HTML report of findings with a lint or check to enforce each, then grills through the ones you pick to a shared understanding of what to change. Changes no code. A fork of Matt Pocock's [`improve-codebase-architecture`](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md); needs his [`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md). |
| [`adr-review`](adr-review/SKILL.md) | Reviews an ADR in the current repo with parallel subagents. Before merge: whether it warrants existing and whether every word is true and necessary. After merge: whether it still warrants existing and whether edits keep its intent. Replies in chat with a verdict and confidence. |
