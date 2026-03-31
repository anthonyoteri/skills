---
name: update-docs
description: Keep documentation in sync with code changes. Use when updating docs, modifying code, or when docs become out of date.
---

# Update Docs

## Quick start

When code changes, check for related documentation and update it:

1. Identify what code changed (read the diff or modified files)
2. Search for docs that reference this code (README, API docs, comments, wikis)
3. Update docs to reflect the new behavior/signature/structure

## Workflows

### When modifying code

- [ ] After changing a function signature → update JSDoc/docstrings
- [ ] After adding/removing features → update README or feature docs
- [ ] After changing behavior → update any usage examples
- [ ] After adding config options → update configuration docs

### When asked to update docs

- [ ] Ask which docs need updating (or infer from context)
- [ ] Read the current docs and the current code
- [ ] Identify mismatches between docs and code
- [ ] Update docs to match current code behavior
- [ ] Flag any ambiguities or outdated examples

### When docs seem stale

- [ ] Search for references to the changed concept
- [ ] Compare documented behavior vs actual code
- [ ] Update stale sections
- [ ] Remove deprecated info; add new info

## Guidelines

- **Prefer accuracy**: Docs should match code, not the other way around
- **Update in the same commit**: When possible, docs change with code
- **Flag uncertainty**: If you're unsure about intended behavior, ask
- **Don't over-document**: Only document non-obvious behavior

## Files to check

Common documentation locations:
- `README.md`, `docs/`, `CHANGELOG.md`
- Inline comments and docstrings
- API reference files (e.g., `API.md`, `docs/api/`)
- Example code snippets in docs
