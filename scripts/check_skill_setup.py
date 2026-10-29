#!/usr/bin/env python3
"""Check that each skill's setup step names the CLIs and skills its files use (CODING_STANDARDS.md, Tools)."""
import re
import sys
from pathlib import Path

# shortcut: a fixed watchlist misses a CLI nobody added here; add one when a skill adopts it.
WATCHLIST = ["gh", "curl", "jq", "glab", "ssh", "docker", "npm", "npx", "node", "python3", "kubectl"]
CLI = re.compile(r"`(" + "|".join(WATCHLIST) + r")\b")
SKILL = re.compile(r'`([a-z0-9-]+)` skill|Skill tool with "([a-z0-9-]+)"')
FIRST_STEP = re.compile(r"^#{2,3} 1\. .*$", re.M)


def setup_paragraph(skill_md):
    text = skill_md.read_text()
    heading = FIRST_STEP.search(text)
    if not heading:
        return None
    return text[heading.end():].strip().split("\n\n")[0]


def check(root):
    problems = []
    for skill_md in sorted(root.glob("*/SKILL.md")):
        skill = skill_md.parent
        setup = setup_paragraph(skill_md)
        if setup is None:
            problems.append(f"{skill_md}: no '1.' step heading")
            continue
        used = set()
        for path in sorted(skill.rglob("*.md")):
            text = path.read_text()
            used |= set(CLI.findall(text))
            used |= {a or b for a, b in SKILL.findall(text)}
        used.discard(skill.name)
        for name in sorted(used):
            if f"`{name}`" not in setup:
                problems.append(f"{skill_md}: setup step doesn't name `{name}`")
    return problems


if __name__ == "__main__":
    problems = check(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
    print("\n".join(problems) or "Every setup step names the CLIs and skills its skill uses.")
    sys.exit(1 if problems else 0)
