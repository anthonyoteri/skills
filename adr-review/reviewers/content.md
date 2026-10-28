# Content reviewer

Every word in an ADR carries weight, because it can't be taken back once merged. Less is more.

- **Decision present**: the decision is stated plainly, ideally in one sentence. It is the only required element; without it the ADR fails (Blocking).
- **Provably true now**: verify each claim about the code, the system, its users or its constraints against the default branch and history. A claim you can't prove is Blocking.
- **Not a plan**: no development plans, roadmaps, steps, tickets, timelines or intended future work. Blocking.
- **Not in flight**: no mention of work that isn't merged, such as a parallel workstream, an open PR or a branch, since it may never land. Blocking.
- **Durable**: no detail likely to change while the decision holds (file paths, versions, counts, team names, current performance numbers) unless the decision depends on it. Blocking.
- **No filler**: background, history, restatement, hedging, enthusiasm or explanation that the decision, alternatives and consequences don't need. Blocking, with the cut in `Fix`.
- **Alternatives**: the considered alternatives, each with why it was rejected. Missing is a Nit, since they are good practice rather than required; present but vague is Should fix.
- **Consequences**: the known downstream consequences of the decision, good and bad. Missing is a Nit; present but vague is Should fix.
- **Precise**: each sentence has one reading. A word a future reader could interpret two ways is Blocking.
