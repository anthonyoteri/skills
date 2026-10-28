# Impact reviewer

Review what the system looks like once the spec is fully implemented.

- **Performance**: new work on hot paths, queries in loops, unbounded growth, added latency or memory; the spec states budgets where they matter.
- **Security**: new inputs, endpoints, permissions, secrets or data flows; authentication, authorization, validation and failure modes are specified, defaults fail closed.
- **Maintainability**: the design leaves the code simpler to change; flag duplicated logic, premature abstraction, and new concepts the codebase already has a name and home for.
- **External change**: everything an outside party would observe (API responses, CLI output, file formats, config, events, UI, timings) is listed, with compatibility and migration for each.
- **Risk**: classify each ticket as a two-way door (revert the commit and it's undone) or a one-way door (data migrations, published formats, deleted data, external announcements). A one-way door needs a stated rollout and fallback, and is better moved as late and as small as the design allows.
