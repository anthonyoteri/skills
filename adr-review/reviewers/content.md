# Content reviewer

Every word in an ADR carries weight, because it can't be taken back once merged. Less is more.

- **Decision present**: the decision is stated plainly, ideally in one sentence. It is the only required element; without it the ADR fails (Blocking).
- **Provably true now**: verify each claim about the code, the system, its users or its constraints against the default branch and history. A claim you can't prove is Blocking.
- **Not a plan**: no development plans, roadmaps, steps, tickets, timelines or intended future work. Blocking.
- **Not in flight**: no mention of work that isn't merged, such as a parallel workstream, an open PR or a branch, since it may never land. Blocking.
- **Within jurisdiction**: the ADR binds only what this repo controls: its own code, interfaces, builds and processes. It may state what the repo guarantees to others and what it enforces on what it accepts, never what consumers, other services or other teams must do, such as how they use what the repo provides. Blocking.
- **Durable**: no detail likely to change while the decision holds (file paths, versions, counts, team names, current performance numbers) unless the decision depends on it. Blocking.
- **No filler**: background, history, restatement, hedging, enthusiasm or explanation that the decision, alternatives and consequences don't need. Blocking, with the cut in `Fix`.
- **Alternatives**: the alternatives considered when the decision was made, each with why it was rejected, as the authors knew them then. Missing is a Nit, since they are good practice rather than required. Vague is Blocking when the wording blurs what the authors knew, and Should fix when what they knew was itself thin.
- **Consequences**: the downstream consequences known when the decision was made, good and bad. Missing is a Nit; vague is graded as for alternatives.
- **Precise**: each sentence has one reading. A word a future reader could interpret two ways is Blocking.
