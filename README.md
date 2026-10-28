# skills

Agent skills for Claude Code. Copy a skill's folder into `~/.claude/skills/` to install it.

| Skill | What it does |
|---|---|
| [`pr-review`](pr-review/SKILL.md) | Reviews a pull request with parallel subagents (metadata, context, prose, behavior, interfaces, design, security) against the repo's own rules or best practices, and replies in chat with an Approve / Reject verdict, confidence and CI status. Uses Matt Pocock's [`code-review`](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md) and [`unslop`](https://github.com/theclaymethod/unslop) when installed, and hands ADRs to `adr-review`. |
| [`spec-review`](spec-review/SKILL.md) | Reviews a spec issue and its tickets with parallel subagents (assumptions, problem, use cases, tests, breakdown, impact, docs, repo rules), checking that an agent with no context could implement it without guessing, and replies in chat with an Approve / Reject verdict and confidence. |
| [`adr-review`](adr-review/SKILL.md) | Reviews an ADR in the current repo with parallel subagents. Before merge: whether it warrants existing and whether every word is true and necessary. After merge: whether it still warrants existing and whether edits keep its intent. Replies in chat with a verdict and confidence. |
