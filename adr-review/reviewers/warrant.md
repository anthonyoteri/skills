# Warrant reviewer

Decide whether the ADR warrants existing. It must pass all three tests; if the answer to any is questionable, it fails (Blocking).

1. **Architectural**: the decision shapes the system's structure for a long time downstream, such as a framework or pattern, or how code is split (many small crates versus one). Choosing a third-party library or dependency fails, unless that choice reshapes the architecture the way a framework like React does.
2. **Hard to reverse**: undoing it takes significant thought and redesign. A mechanical change or a simple revert fails.
3. **Non-obvious**: someone used to similar codebases and patterns, arriving with fresh eyes, would genuinely have expected something different. Check against the codebase, its ecosystem's conventions and the alternatives the ADR names.

**When the ADR is merged**, ask again with what is true today: the code, history and docs since the merge. If it no longer warrants existing, or its decision is now wrong, propose a replacement ADR in full that would supersede it, written to pass these tests, or propose rejecting it outright when no decision should take its place. Rejecting needs significant just cause: cite the evidence. Without it, the ADR stands.

End with one line: `Merged verdict: Keep`, `Merged verdict: Supersede`, `Merged verdict: Reject`, or `Merged verdict: n/a` for a pre-merge ADR.
