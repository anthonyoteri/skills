# Edits reviewer

The ADR is merged and has pending edits (`git diff origin/<default> -- <path>`). Its intent can't change; only wording that keeps the intent exactly, and its metadata (status, superseded-by links), may.

For each hunk, decide whether a reader would follow the decision any differently after the edit than before: a changed scope, condition, exception, strength (must versus should) or alternative. Any change of intent is Blocking, with `Fix: revert, or write a superseding ADR`. Grammar, clarity and metadata edits are fine; judge them for wording only.
