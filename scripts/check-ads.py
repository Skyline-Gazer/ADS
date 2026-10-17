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
    targets = [m.group(1) or m.group(2) for m in re.finditer(r"\]\(\s*(?:<([^<>]+)>|([^\s)]+))(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)", content)]
    definitions = re.findall(r"^\[[^\]]+\]:\s*(\S+)", content, re.M)
    for raw in targets + definitions:
        link = raw.split("#", 1)[0]
        if "://" in link or link.startswith("mailto:") or not link:
            continue
        dest = (file.parent / link).resolve()
        if not dest.is_relative_to(ROOT) or not dest.exists():
            errors.append(f"{relative}: missing link {link}")

skill_dirs = {skill.parent.name: skill.parent for skill in skills}
for file in ROOT.rglob("*.md"):
    for name, asset in re.findall(r"skill://([\w.-]+)/([^\s)\]`\"'<>]+)", file.read_text(encoding="utf-8")):
        base = skill_dirs.get(name)
        if base is None:
            errors.append(f"{file.relative_to(ROOT)}: unknown skill://{name}")
            continue
        dest = (base / asset).resolve()
        if not dest.is_relative_to(base.resolve()) or not dest.exists():
            errors.append(f"{file.relative_to(ROOT)}: missing skill asset skill://{name}/{asset}")

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
