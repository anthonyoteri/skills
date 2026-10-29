# Contributing

Skills follow [CODING_STANDARDS.md](CODING_STANDARDS.md).

## Commits and pull request titles

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `<type>(<scope>): <subject>`.

- **Type**: `feat` for a new skill or capability, `fix` for a correction, `docs` for documentation outside a skill, `refactor` for a rewrite that keeps behavior, `chore` for repo maintenance.
- **Scope**: the skill's folder name (`pr-review`). Leave it out for changes across the repo.
- **Subject**: imperative mood, no trailing period, the whole line about 60 characters.

Pull requests are squash-merged, so the PR title becomes the commit on `main` and follows the same format. Commits inside a PR can be working history.
