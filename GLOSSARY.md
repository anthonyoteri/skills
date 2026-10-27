# PR review

The language of the `pr-review` skill: how a pull request is judged and how the judgment is reported.

## Language

**Finding**:
One problem a reviewer found in the pull request, with its location, evidence and a suggested fix.
_Avoid_: Issue, comment, note

**Verdict**:
The review's single outcome for the pull request: Reject when any finding is Blocking or Should fix, otherwise Approve.
_Avoid_: Recommendation, decision, request changes

**CI status**:
The state of the pull request's checks (passed, failed or pending), reported as red flags beside the verdict. It is never a finding and never changes the verdict; gating merges is the repository's job.
_Avoid_: CI finding, check failure finding

**Confidence**:
How strong the evidence behind the verdict is: High, Medium or Low, lowered by each gap in what the review could check. It never changes the verdict.
_Avoid_: Certainty, score, Extreme

**Severity**:
How much a finding matters: Blocking (merging ships a defect, a vulnerability, or a break of a documented repo rule), Should fix, or Nit.
_Avoid_: Priority, level, Critical/High/Medium/Low

**Reviewer**:
A subagent that examines one area of the pull request (metadata, prose, behavior, interfaces, design or security) and reports findings.
_Avoid_: Angle, agent, checker

**Code review skill**:
An installed skill that reviews a diff, run alongside the reviewers; its findings count toward the verdict.
_Avoid_: Code reviewer, review plugin

**Spec**:
What the pull request is meant to do: the issues it closes, or its description when it closes none.
_Avoid_: Requirements, ticket, specification

**Repo rules**:
The conventions a repository documents for itself, which always take precedence over best practices.
_Avoid_: Standards, house style

**Best practices**:
The widely accepted conventions a reviewer applies where the repo rules are silent.
_Avoid_: Defaults
