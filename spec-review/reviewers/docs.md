# Docs reviewer

Review the documentation the spec will change.

- **Specified**: each ticket names the docs it updates (README, guides, API reference, changelog if kept by hand, comments on public interfaces, agent instructions).
- **Left stale**: search the repo (`git grep`) for docs that describe behavior, names, commands, config or paths the spec changes but doesn't mention. Each is a Should fix, naming the file.
- **Immutable artifacts**: ADRs, published API specs, schemas, RFCs, released changelogs, or anything else that once merged or published can only be superseded, not edited. Flag each the spec creates or changes, and check it is correct and complete before it lands; one written too early or too vaguely is Blocking.
