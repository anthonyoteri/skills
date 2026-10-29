#!/usr/bin/env python3
"""Check that no .md file uses a multi-word _Avoid_ phrase from GLOSSARY.md (CODING_STANDARDS.md, Terms).

Usage: check_glossary_terms.py [repo-root]
"""
import re
import sys
from pathlib import Path

# shortcut: only Avoid entries with a space or hyphen are checked; single words ("agent", "scope") need a
# reader's judgment and are left to reviewers. There is no way to mark an exception: reword the line instead.
AVOID_LINE = re.compile(r"^_Avoid_: (.*)$", re.M)


def phrases(glossary):
    entries = [p.strip() for line in AVOID_LINE.findall(glossary) for p in line.split(",")]
    return [p for p in entries if re.search(r"[ -]", p)]


def hits(text, phrase):
    pattern = re.compile(r"(?<![\w-])" + re.escape(phrase) + r"s?(?![\w-])", re.I)
    return [n for n, line in enumerate(text.splitlines(), 1) if pattern.search(line)]


def check(root):
    glossary = root / "GLOSSARY.md"
    avoid = phrases(glossary.read_text())
    problems = []
    for path in sorted(root.rglob("*.md")):
        if path == glossary or ".git" in path.parts:
            continue
        text = path.read_text()
        for phrase in avoid:
            for n in hits(text, phrase):
                problems.append(f"{path}:{n}: uses '{phrase}', which GLOSSARY.md says to avoid")
    return problems


def self_check():
    assert phrases("_Avoid_: Repo rules, house style, guidelines\n_Avoid_: Agent, sub-task") == ["Repo rules", "house style", "sub-task"]
    assert hits("ok\nSpawn sub-agents in parallel.", "Sub-agent") == [2]
    assert hits("Repo Rules beat best practices.", "repo rules") == [1]
    assert hits("a pre-sub-agent hook, a sub-agentic flow", "sub-agent") == []


if __name__ == "__main__":
    self_check()
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    problems = check(root)
    print("\n".join(problems) or "No file uses a multi-word phrase GLOSSARY.md says to avoid.")
    sys.exit(1 if problems else 0)
