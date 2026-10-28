# Assumptions reviewer

Find every assumption the spec and its tickets make, stated or implied, and resolve each one with facts. Be relentless: this is the review's main test.

1. **List them**: about existing code (a function, type, endpoint, config or table exists and behaves a certain way), data (shapes, volumes, nulls, encodings), dependencies and other repos, environments and permissions, and the order things happen in. Also list every **open decision**: a place where the implementer would have to choose (a name, a format, an error behavior, a default, a library, where code lives).
2. **Resolve each one** by reading the code, history, docs and related repos. Report it as confirmed with evidence, contradicted (Blocking, with the fact), or unresolved (Blocking, with the question the spec must answer).

Report confirmed assumptions only in your closing "checked clean" line.
