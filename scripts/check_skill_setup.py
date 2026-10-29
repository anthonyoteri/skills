#!/usr/bin/env python3
"""Check that each skill's setup step names the CLIs and skills its files use (CODING_STANDARDS.md, Tools).

Usage: check_skill_setup.py [repo-root]
"""
import re
import sys
from pathlib import Path

# shortcut: only watched CLIs in inline code in .md files are seen; one missing here, only in a fenced block,
# or only in another file type slips through. Extend this when a skill needs it.
WATCHLIST = ["gh", "curl", "jq", "glab", "ssh", "docker", "npm", "npx", "node", "python3", "kubectl"]
CLI = re.compile(r"`(" + "|".join(WATCHLIST) + r")(?=[`\s])")
SKILL_NAMED = re.compile(r"`([a-z0-9-]+)` skill")
SKILL_TOOL = re.compile(r'Skill tool with "([a-z0-9-]+)"')
FIRST_STEP = re.compile(r"^#{2,3} 1\. .*$", re.M)


def uses(text):
    return set(CLI.findall(text)) | set(SKILL_NAMED.findall(text)) | set(SKILL_TOOL.findall(text))


def setup_paragraph(text):
    heading = FIRST_STEP.search(text)
    if not heading:
        return None
    return text[heading.end():].strip().split("\n\n")[0]


def check(root):
    problems = []
    for skill_md in sorted(root.glob("*/SKILL.md")):
        skill = skill_md.parent
        setup = setup_paragraph(skill_md.read_text())
        if setup is None:
            problems.append(f"{skill_md}: no '1.' step heading")
            continue
        used = set()
        for path in sorted(skill.rglob("*.md")):
            used |= uses(path.read_text())
        used.discard(skill.name)
        for name in sorted(used):
            if f"`{name}`" not in setup:
                problems.append(f"{skill_md}: setup step doesn't name `{name}`")
    return problems


def self_check():
    assert uses("run `gh pr view <n>`, then `curl -sIL <url>` and `gh`") == {"gh", "curl"}
    assert uses("`gh-pages`, `node.js`, `ssh-keygen`, `<owner>/<repo>`") == set()
    assert uses("the `unslop` skill, if installed") == {"unslop"}
    assert uses('call the Skill tool with "grilling"') == {"grilling"}
    assert setup_paragraph("# T\n\n## 1. Setup\n\nNeeds `gh`.\n\nThen `curl`.") == "Needs `gh`."
    assert setup_paragraph("# T\n\n## Steps\n\nNeeds `gh`.") is None


if __name__ == "__main__":
    self_check()
    problems = check(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
    print("\n".join(problems) or "Every setup step names the CLIs and skills its skill uses.")
    sys.exit(1 if problems else 0)
