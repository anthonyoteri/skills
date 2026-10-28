# Reviews

The language of the review skills: how work is judged and how the judgment is reported.

## Language

**Finding**:
One problem a reviewer found, with its location, evidence and a suggested fix.
_Avoid_: Issue, comment, note

**Confidence**:
How strong the evidence behind a review's outcome is: High, Medium or Low, lowered by each gap in what the review could check.
_Avoid_: Certainty, score, Extreme

**Reviewer**:
A subagent that examines one area and reports findings, starting from a fresh context.
_Avoid_: Angle, agent, checker

**Code review skill**:
An installed skill that reviews a diff, run alongside the reviewers; its findings count like a reviewer's.
_Avoid_: Code reviewer, review plugin

**Spec**:
What a change is meant to do.
_Avoid_: Requirements, specification, plan

**Ticket**:
One issue the spec is split into, implemented and reviewed as one pull request.
_Avoid_: Task, sub-task, story

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
What an ADR's decision requires of the code. The intent can't change after merge; only wording that preserves it, and metadata, may.
_Avoid_: Meaning, spirit

**Jurisdiction**:
What a repo controls, and so all an ADR may bind: its own code, interfaces, builds and processes, never what consumers or other teams do.
_Avoid_: Scope, ownership

**Supersede**:
Replace a merged ADR's decision with a new ADR, leaving the old one in place with its status updated.
_Avoid_: Amend, override
