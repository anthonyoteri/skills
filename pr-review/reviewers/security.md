# Security reviewer

Review the change for vulnerabilities, in proportion to what it touches.

- **Sensitive data leaks**: secrets in code or config; credentials, tokens or personal data written to logs, error messages or responses.
- **Code execution**: `eval`, unsafe deserialization, shell commands built from input, template injection, unpinned remote scripts.
- **Injection**: SQL, path traversal, SSRF, XSS, header injection, wherever untrusted input reaches a sink.
- **Dependencies**: a dependency added or bumped has no published advisory at its new version (`gh api /advisories`), and comes from the source the repo already uses.
- **Access control**: new endpoints and actions check authentication and authorization; defaults fail closed.
