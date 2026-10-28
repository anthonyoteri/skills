# Claims reviewer

Every statement in the ADR must stay true for as long as the ADR stands. Check each sentence:

- **Provably true now**: verify each claim about the code, the system, its users or its constraints against the default branch and history. A claim you can't prove is Blocking.
- **Not a plan**: no development plans, roadmaps, steps, tickets, timelines or intended future work. Blocking.
- **Not in flight**: no mention of work that isn't merged, such as a parallel workstream, an open PR or a branch, since it may never land. Blocking.
- **Durable**: no detail likely to change while the decision holds (file paths, versions, counts, team names, current performance numbers) unless the decision depends on it.
