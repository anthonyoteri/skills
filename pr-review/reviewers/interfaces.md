# Interfaces reviewer

Review what the change exposes to the outside: public APIs, API definitions, docs and dependencies.

- **Public APIs** are documented where the language expects it (docstrings, doc comments, Javadoc).
- **API definitions and schemas** (OpenAPI, JSON Schema, protobuf, GraphQL, database migrations) match the code: the change follows them, or updates them alongside.
- **Public documentation** describing a changed interface is updated, consistently everywhere it appears.
- **Dependencies** added or changed are pinned the way the ecosystem expects, with the lockfile updated in the same PR.
- **Private code stays private**: when the repo's visibility is private or internal, check that no proprietary source, internal hostnames or internal design reaches public docs, public API responses, error messages or published packages.
