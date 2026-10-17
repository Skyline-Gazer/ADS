#!/usr/bin/env python3
"""Validate ADS markdown links, agent skill metadata and unsafe probe examples, without dependencies."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
if not skills:
    errors.append("no Skills found")

def strip_fences(text):
    return re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", text, flags=re.S | re.M)

FENCES = re.compile(r"^(?:```|~~~)[^\n]*\n(.*?)^(?:```|~~~)[^\n]*$", re.S | re.M)
# Commands that would disclose environment values or credentials must never ship in ADS code blocks,
# including as negative examples: describe the prohibition in prose instead.
UNSAFE_PROBES = (
    (r"^\s*printenv\b", "printenv dumps environment values"),
    (r"^\s*env\s*(?:\||$)", "bare `env` dumps environment values"),
    (r"^\s*set\s*(?:\||$)", "bare `set` dumps shell variables"),
    (r"^\s*export\s+-p\b", "`export -p` dumps environment values"),
    (r"^\s*(?:cat|less|head|tail|bat|open)\s+\S*\.env\b", "reads a .env file"),
    (r"^\s*gh\s+auth\s+token\b", "prints a GitHub token"),
    (r"\$\{?[A-Za-z_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|CREDENTIAL)[A-Za-z_]*\}?",
     "interpolates a credential variable"),
    (r"\.aws/credentials|\.git-credentials|\.netrc\b|\bid_rsa\b", "reads a credential store"),
)


for file in ROOT.rglob("*.md"):
    relative = file.relative_to(ROOT)
    content = file.read_text(encoding="utf-8")
    if "Skyline-Gazer/PAS" in content:
        errors.append(f"{relative}: stale repository link")
    prose = strip_fences(content)
    inline = re.finditer(
        r"\]\(\s*(?:<([^<>]+)>|([^\s)]+))(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^()]*\)))?\s*\)", prose
    )
    definitions = re.finditer(
        r"^ {0,3}(?!\[\^)\[[^\]]+\]:\s*(?:<([^<>]+)>|(\S+))", prose, re.M
    )
    for match in list(inline) + list(definitions):
        link = (match.group(1) or match.group(2)).split("#", 1)[0].replace("\\ ", " ")
        if "://" in link or link.startswith("mailto:") or not link:
            continue
        dest = (file.parent / link).resolve()
        if not dest.is_relative_to(ROOT) or not dest.exists():
            errors.append(f"{relative}: missing link {link}")

skill_dirs = {skill.parent.name: skill.parent for skill in skills}
for file in ROOT.rglob("*.md"):
    text = strip_fences(file.read_text(encoding="utf-8"))
    for name, asset in re.findall(r"skill://([\w.-]+)(?:/([^\s)\]`\"'<>]+))?", text):
        base = skill_dirs.get(name)
        if base is None:
            # Foreign namespaces (for example MCP-served skills) are not ours to validate.
            continue
        asset = asset.split("#", 1)[0].rstrip(".,;:")
        dest = (base / asset).resolve() if asset else base / "SKILL.md"
        if not dest.is_relative_to(base.resolve()) or not dest.exists():
            errors.append(f"{file.relative_to(ROOT)}: missing skill asset skill://{name}/{asset}")

for file in ROOT.rglob("*.md"):
    for block in FENCES.finditer(file.read_text(encoding="utf-8")):
        for line in block.group(1).splitlines():
            for pattern, reason in UNSAFE_PROBES:
                if re.search(pattern, line):
                    errors.append(
                        f"{file.relative_to(ROOT)}: unsafe environment probe ({reason}): {line.strip()[:60]}"
                    )

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
print(f"ADS validation passed: {len(skills)} skills, Markdown links and probe examples checked")
