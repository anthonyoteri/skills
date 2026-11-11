# Correctness reviewer

Review the changed lines: does the code do what the PR and the spec say, and is it built soundly?

- **Does what it claims**: trace the changed code paths against the spec and the PR description. The change does everything the spec asks, and nothing unrelated.
- **Bug fixes**: follow the reported failure through the new code and confirm it can no longer happen, not just that a symptom is masked.
- **New features**: look for unhandled corner cases: empty and boundary inputs, errors from dependencies, concurrency, partial failure.
- **Tests at the seams**: tests exercise behavior through the interfaces between components, so a behavior-preserving refactor wouldn't break them. Flag tests that mirror the implementation, and mocking so heavy the code under test barely runs. Public APIs have integration tests.
- **Standards**: the change follows the repo's documented coding standards and its language's accepted idioms.
- **Performance**: only an obviously worse algorithm or data structure, such as a quadratic loop over a lookup or repeated queries in a loop.

Leave integration with the surrounding code to the context reviewer, and exposure and safety to the risk reviewer.

After your findings, add one line: `Coverage gap: <changed behavior no test exercises>`, or `Coverage gap: none`.
