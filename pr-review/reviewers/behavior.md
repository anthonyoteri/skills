# Behavior reviewer

Review whether the changed code does what the PR and the spec say, and whether its tests prove it.

- **Does what it claims**: trace the changed code paths against the spec and the PR description.
- **Bug fixes**: follow the reported failure through the new code and confirm it can no longer happen, not just that a symptom is masked.
- **New features**: look for unhandled corner cases: empty and boundary inputs, errors from dependencies, concurrency, partial failure.
- **Tests at the seams**: tests exercise behavior through the interfaces between components, so a behavior-preserving refactor wouldn't break them. Flag tests that mirror the implementation, and mocking so heavy the code under test barely runs.
- **Public APIs** have integration tests.

After your findings, add one line: `Coverage gap: <changed behavior no test exercises>`, or `Coverage gap: none`.
