# Coding standards

Skills follow Anthropic's [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), tracking the live guide as it changes. This file only adds to it or overrides it. Commit and PR titles follow [CONTRIBUTING.md](CONTRIBUTING.md).

## Additions

- **Terms**: use the terms in [GLOSSARY.md](GLOSSARY.md), not their _Avoid_ words.
- **Tools**: a skill's setup step names every CLI it needs, and whether it must be authenticated (`gh auth status`). It also names every other skill it needs, and says "if installed" for one it can do without. CI checks this against a watchlist of CLIs in [`scripts/check_skill_setup.py`](scripts/check_skill_setup.py).
- **Spelling**: American English.

## Overrides

- **Description**: a skill with `disable-model-invocation: true` has a one-line summary for humans, with no "when to use" clause.
