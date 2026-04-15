---
name: implement-stacked-issues
description: High-autonomy implementation of GitHub issues using a stacked PR workflow with a subagent-driven self-correction loop.
---

# Implement Stacked Issues

Iteratively implement GitHub issues as a stack of dependent pull requests. This process uses a "Subagent Sandbox" for pre-commit reviews to ensure a clean, unbiased audit of the code before any history is created.

## 1. Stack Initialization
- **Map:** Identify the parent PRD and its child issues.
- **Sequence:** Order issues by their dependency tree (`Blocked by` fields).
- **Confirm:** Summarize the stack and ask: "Ready to begin the first unblocked slice?"

## 2. The Implementation Loop
For each issue in the sequence, follow this **Refine -> Sandbox Review -> Verify -> PR** flow:

### Phase A: Implementation & Refactoring
- **Base:** Branch from the previous slice's branch (or `main`).
- **Simplify:** Prioritize the path of least complexity. Integrate new logic into existing patterns/helpers.
- **Vertical Slice:** Build the end-to-end change (Schema, API, Logic, Tests).

### Phase B: Subagent Sandbox Review
Before staging or committing, **invoke a fresh Subagent** to perform an unbiased audit:
- **Isolation:** The subagent must start with a clean context window, focusing only on the current codebase and the specific issue requirements.
- **Audit Criteria:** - Does the implementation match the project's existing Rust/C++ patterns?
    - Are there logic gaps, redundant abstractions, or missing edge cases?
    - Is the code as simple as possible?
- **Correction:** The main agent must address all subagent findings **before** moving to Phase C.

### Phase C: Local Verification (Just/Make)
- **Standardized Checks:** Prefer `Justfile` or `Makefile` targets (e.g., `just check`, `just test`). 
- **Fallback:** Use raw commands (`cargo check`, `cargo test`, `helm lint`) if no task runner is present. 
- **Blocker:** Do not proceed until all local checks pass.

### Phase D: Atomic & Conventional Commits
- **Logical Splits:** Commit by component/layer.
- **Conventional Format:** `type(scope): description`.
- **Bug Fix Rule:** Message must describe the **broken behavior resolved** (e.g., `fix(api): malformed JSON rejected with 401 error code`).

### Phase E: The Stacked PR
- **Create:** `gh pr create --base <previous-branch>`.
- **Review Loop:** Wait for automated AI review/CI comments. Address feedback immediately to ensure a stable base for the next slice.

## 3. The "Next-Slice" Handshake
- **Action:** Ask: "Slice #<number> is finalized. Proceed to the next dependent slice in the stack?"

## Rules of the Stack
- **Clean Context:** Always use subagents for reviews to prevent main-window "hallucination leak."
- **No Dirty Bases:** Resolve all PR feedback before branching for the next issue.
- **Refactor First:** Treat every new feature as a reason to simplify the existing codebase.