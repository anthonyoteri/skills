# skills

Agent skills for Claude Code. Copy a skill's folder into `~/.claude/skills/` to install it.

| Skill | What it does |
|---|---|
| [`pr-review`](pr-review/SKILL.md) | Reviews a pull request with parallel subagents (metadata, prose, behavior, interfaces, design, security) against the repo's own rules or best practices, and replies in chat with an Approve / Reject verdict, confidence and CI status. Uses Matt Pocock's [`code-review`](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md) and [`unslop`](https://github.com/theclaymethod/unslop) when installed. |
