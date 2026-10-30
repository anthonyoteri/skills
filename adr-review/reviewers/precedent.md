# Precedent reviewer

Review the ADR against the repo's other ADRs and every document it references.

**References**: find every ADR and document the ADR points to: links, ADR numbers or titles ("ADR 0004"), and named docs such as `CODING_STANDARDS.md` or a style guide. Read each one in full before judging the ADR. A reference you couldn't open counts against the ADR.

- **Resolves**: the target exists, and an ADR the decision relies on is active, not superseded or rejected. Blocking.
- **Described truly**: what the ADR says a target says or decides matches the target. Blocking.
- **Conflicts**: it contradicts an active ADR or a referenced document without superseding it explicitly. Blocking.
- **Duplicates**: an active ADR or a referenced document already records the same decision or rule, or most of it, and the ADR restates it instead of pointing to it.
- **Supersession**: an ADR it replaces is named, and that ADR's status and superseded-by link are updated with it. For a merged ADR, a later ADR that replaces it is reflected in its status.

Check unreferenced active ADRs for conflicts and duplicates too, reading any whose title or scope overlaps the ADR's. In your last line, name every document you read in full.
