# Reviews

The language of the `pr-review`, `spec-review` and `adr-review` skills: how a pull request, a spec or an ADR is judged and how the judgment is reported.

## Language

**Finding**:
One problem a reviewer found in the pull request, spec or ADR, with its location, evidence and a suggested fix.
_Avoid_: Issue, comment, note

**Verdict**:
The review's single outcome: Reject when any finding is Blocking or Should fix, otherwise Approve. For a merged ADR: Keep, Supersede or Reject.
_Avoid_: Recommendation, decision, request changes

**CI status**:
The state of the pull request's checks (passed, failed or pending), reported as red flags beside the verdict. It is never a finding and never changes the verdict; gating merges is the repository's job.
_Avoid_: CI finding, check failure finding

**Confidence**:
How strong the evidence behind the verdict is: High, Medium or Low, lowered by each gap in what the review could check. It never changes the verdict.
_Avoid_: Certainty, score, Extreme

**Severity**:
How much a finding matters: Blocking (merging, or implementing the spec as written, ships a defect, a vulnerability, or a break of a documented repo rule; or, for a spec, leaves the implementer to guess or the problem unsolved), Should fix, or Nit.
_Avoid_: Priority, level, Critical/High/Medium/Low

**Reviewer**:
A subagent that examines one area of the pull request, spec or ADR and reports findings, starting from a fresh context.
_Avoid_: Angle, agent, checker

**Code review skill**:
An installed skill that reviews a diff, run alongside the reviewers; its findings count toward the verdict.
_Avoid_: Code reviewer, review plugin

**Spec**:
What a change is meant to do. For a pull request, the issues it closes, or its description when it closes none. For a spec review, the spec issue together with its tickets.
_Avoid_: Requirements, specification, plan

**Ticket**:
One issue the spec is split into, implemented and reviewed as one pull request.
_Avoid_: Task, sub-task, story

**Reference**:
Anything the spec cites that it doesn't define itself, especially the issue or report describing the problem it solves.
_Avoid_: Link, source

**Assumption**:
Something the spec takes as true without stating the evidence. Resolved when facts confirm or contradict it; one the facts can't settle is a gap in the spec.
_Avoid_: Premise, guess

**Deletion test**:
Removing a use case from the spec and asking whether the outcome measurably changes. A use case that fails it adds nothing.
_Avoid_: Necessity check

**Cutover point**:
The ticket after which landed code stops being inert and changes what the system does.
_Avoid_: Switch-over, go-live

**Door**:
How reversible a change is: two-way when reverting it undoes it, one-way when it can only be superseded (migrated data, a published format, a merged ADR).
_Avoid_: Reversibility, risk level

**Repo rules**:
The conventions a repository documents for itself, which always take precedence over best practices.
_Avoid_: Standards, house style

**Best practices**:
The widely accepted conventions a reviewer applies where the repo rules are silent.
_Avoid_: Defaults

**ADR**:
An architectural decision record: a decision that is architectural, hard to reverse and non-obvious, which once merged binds every later change until a superseding ADR replaces it.
_Avoid_: Design doc, RFC, decision log

**Warrant**:
Whether an ADR deserves to exist: it passes all three tests (architectural, hard to reverse, non-obvious), and fails if any is questionable.
_Avoid_: Justification, eligibility

**Intent**:
What an ADR's decision requires of the code. It can't change after merge; wording that keeps it exactly, and metadata, can.
_Avoid_: Meaning, spirit

**Supersede**:
Replace a merged ADR's decision with a new ADR, leaving the old one in place with its status updated.
_Avoid_: Amend, override

**Grandfathered**:
Code that existed before an ADR merged, which that ADR doesn't bind. Code landing with the ADR, in the same pull request or commit, is bound.
_Avoid_: Legacy, exempt
