# Breakdown reviewer

Review how the spec is split into tickets and the order they land in. If it isn't split, propose a split.

- **Atomic and sized**: each ticket is one coherent unit of work that stands on its own. Merge a ticket too small to justify its own review (a 2-line change split off a 5,000-line one) or one that isn't atomic without another. Split a ticket that bundles unrelated work. Prefer several reviewable changes (three of 500 lines) over one large one (1,500 lines).
- **Lands well**: find how changes reach the default branch (`gh api repos/<owner>/<repo> --jq '{merge: .allow_merge_commit, rebase: .allow_rebase_merge, squash: .allow_squash_merge}'` and `git log` on it). Each ticket lands as a commit worth a changelog entry, and leaves the default branch working.
- **Parallel**: dependencies between tickets are stated, and a different split would let more of them proceed at once.
- **Cutover points**: find the change after which landed code stops being inert. Prefer an order where most tickets land early and inert (behind a flag, unused, or additive) and one small ticket switches them on, over one where everything rides on a late merge.
- **Guards first**: static checks, lint rules, types, schemas or CI steps that would stop an implementer committing a mistake reviewers would otherwise catch belong in an early ticket. List each under `Automate`.
