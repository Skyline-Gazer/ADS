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

QUOTE = re.compile(r"^(?: {0,3}> ?)+")
FENCE_OPEN = re.compile(r"^(?P<indent> {0,3})(?P<chars>`{3,}|~{3,})(?P<info>[^`]*)$")
# Commands that would disclose environment values or credentials must never ship in ADS code
# blocks, including as negative examples: state the prohibition in prose instead.
# Accepted, documented false-positive class: a credential-named variable is flagged whenever it is
# interpolated, even when the script only passes a variable name.
UNSAFE_PROBES = tuple(
    (re.compile(pattern), reason)
    for pattern, reason in (
        (r"(?i:\bprintenv\b)", "printenv dumps environment values"),
        (r"(?i:\benv\b(?=[ \t]*(?:\||$)))", "bare `env` dumps environment values"),
        (r"(?i:\bset\b(?=[ \t]*(?:\||$)))", "bare `set` dumps shell variables"),
        (r"(?i:\bexport\s+-p\b)", "`export -p` dumps environment values"),
        (r"(?i:\bdeclare\s+-x\b)", "`declare -x` dumps exported variables"),
        (r"(?i:\bcompgen\s+-v\b)", "`compgen -v` lists variable names"),
        (r"(?i:\bos\.(?:environ|getenv)\b)", "reads process environment values"),
        (r"(?i:--env-file\b)", "passes an environment file into a process"),
        (
            r"(?i:\b(?:cat|bat|less|more|head|tail|open|xxd|base64|strings|grep|awk|sed|source"
            r"|ls|find)\b)[^\n]*(?:\.env(?!\.(?:dist|example|sample|template))\b"
            r"|\bid_(?:rsa|ed25519)\b(?!\.pub)|\.aws/credentials\b|\.git-credentials\b|\.netrc\b"
            r"|\.kube/config\b|\.docker/config\.json\b)",
            "reads a credential or environment file",
        ),
        (
            r"(?i:\b(?:curl|scp|sftp|rsync|nc)\b)[^\n]*(?:\bid_(?:rsa|ed25519)\b(?!\.pub)"
            r"|\.aws/credentials\b|\.git-credentials\b|\.netrc\b|\.kube/config\b"
            r"|\.docker/config\.json\b)",
            "transfers a credential file",
        ),
        (r"(?i:\bgh\s+auth\b(?=[^\n]*\btoken\b))", "prints a GitHub token"),
        (r"secrets\.[A-Z][A-Z0-9_]+", "interpolates a CI secret context"),
        (
            r"\$\{?[A-Za-z_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|CREDENTIAL)[A-Za-z_]*\}?",
            "interpolates a credential-named variable",
        ),
    )
)


def code_regions(text):
    """Split Markdown into code regions: fenced (optionally blockquoted, indented up to 3) and 4-space-indented."""
    blocks = []
    fence_errors = []
    fence = None  # (fence character, minimum closing length, opening line number)
    indented = False
    for number, raw in enumerate(text.splitlines(), 1):
        line = QUOTE.sub("", raw)
        expanded = line.expandtabs(4)
        if fence:
            if re.match(rf"^ {{0,3}}{re.escape(fence[0])}{{{fence[1]},}}\s*$", line):
                fence = None
            else:
                blocks.append((number, line))
            continue
        opener = FENCE_OPEN.match(expanded)
        if opener:
            fence = (opener.group("chars")[0], len(opener.group("chars")), number)
        elif expanded.startswith("    ") and line.strip():
            indented = True
            blocks.append((number, line))
        elif not (indented and not line.strip()):
            indented = False
    if fence:
        fence_errors.append(f"unterminated code fence opened on line {fence[2]}")
    return blocks, fence_errors


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
    relative = file.relative_to(ROOT)
    blocks, fence_errors = code_regions(file.read_text(encoding="utf-8"))
    for message in fence_errors:
        errors.append(f"{relative}: {message}")
    for number, line in blocks:
        for pattern, reason in UNSAFE_PROBES:
            if pattern.search(line):
                errors.append(
                    f"{relative}:{number}: unsafe environment probe ({reason}): {line.strip()[:60]}"
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
