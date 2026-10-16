#!/usr/bin/env python3
"""Validate ADS markdown links and agent skill metadata, without dependencies."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
if not skills:
    errors.append("no Skills found")

for file in ROOT.rglob("*.md"):
    relative = file.relative_to(ROOT)
    content = file.read_text(encoding="utf-8")
    if "Skyline-Gazer/PAS" in content:
        errors.append(f"{relative}: stale repository link")
    for link in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", content):
        if "://" in link or link.startswith("mailto:"):
            continue
        dest = (file.parent / link.split("#", 1)[0]).resolve()
        if not dest.is_relative_to(ROOT) or not dest.exists():
            errors.append(f"{relative}: missing link {link}")

for skill in skills:
    content = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not match:
        errors.append(f"{skill.relative_to(ROOT)}: missing YAML frontmatter")
        continue
    fields = dict(re.findall(r"^(name|description):\s*(.+)$", match.group(1), re.M))
    if fields.get("name") != skill.parent.name or not fields.get("description"):
        errors.append(f"{skill.relative_to(ROOT)}: invalid name/description")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"ADS validation passed: {len(skills)} skills and Markdown links checked")
