# Risk reviewer

Review the changed lines for anything bad or hard to reverse if we got it wrong, in proportion to what the change touches.

- **Hard to undo**: database migrations, data deletion or rewriting, changed file or wire formats, published package or API contracts, and changes that can't be rolled back by reverting the PR.
- **Public interfaces**: public APIs, API definitions and schemas (OpenAPI, JSON Schema, protobuf, GraphQL, migrations) match the code and are updated alongside it. Documentation of a changed interface is updated.
- **Dependencies**: a dependency added or changed is pinned the way the ecosystem expects, with the lockfile updated in the same PR, and has no published advisory at its new version (`gh api /advisories`). For a version bump, read the release notes between the old and new versions, and check (`git grep`) whether the repo uses anything they break or remove. Read lockfiles only for what dependencies changed.
- **Sensitive data**: secrets in code or config; credentials, tokens or personal data written to logs, errors or responses. When the repo is private or internal, no proprietary source or internal hostnames reach public docs, API responses, error messages or published packages.
- **Code execution and injection**: `eval`, unsafe deserialization, shell commands or SQL built from input, path traversal, SSRF, XSS, unpinned remote scripts.
- **Access control**: new endpoints and actions check authentication and authorization; defaults fail closed.

Leave whether the code does what it claims to the correctness reviewer.
