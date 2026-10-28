#!/usr/bin/env python3
"""Agent Runtime Security Gate — discovery, preflight, evidence check, fail-closed verdict.

Dependency-free. Runtime-agnostic: works from adapter descriptors in
templates/host-security/adapters/*.json. Does not enforce anything itself;
it classifies a runtime's security posture and refuses PASS without evidence.

Usage:
  python3 runtime_security_gate.py discover                    # list adapters + statuses
  python3 runtime_security_gate.py preflight --adapter <id>    # run discovery commands
  python3 runtime_security_gate.py verify --adapter <id> \    # evaluate evidence file
      --evidence evidence.json --host "macOS 27.0.1"
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ADAPTER_DIR = Path(__file__).resolve().parents[1] / "templates" / "host-security" / "adapters"
VERDICTS = ("VERIFIED_BOUNDED", "PROMPT_ONLY", "UNVERIFIED", "UNSAFE", "BLOCKED")
SENSITIVE_REQUIRED = "VERIFIED_BOUNDED"


def load_adapter(adapter_id):
    path = ADAPTER_DIR / f"{adapter_id}.json"
    if not path.exists():
        raise SystemExit(f"ADAPTER_NOT_FOUND: {adapter_id}")
    return json.loads(path.read_text())


def all_adapters():
    return {p.stem: json.loads(p.read_text()) for p in sorted(ADAPTER_DIR.glob("*.json"))}


def discover():
    rows = []
    for aid, a in all_adapters().items():
        kinds = ",".join(a.get("runtime_kinds", []))
        rows.append(f"{aid:28} {a.get('status','?'):9} kinds={kinds:24} reason={a.get('status_reason','')[:60]}")
    print("\n".join(rows))


def preflight(adapter_id):
    a = load_adapter(adapter_id)
    out = {"adapter": adapter_id, "discovery": {}}
    for cmd in a.get("discovery", {}).get("commands", []):
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        out["discovery"][cmd] = {"rc": r.returncode, "output": r.stdout.strip()[:400]}
    print(json.dumps(out, indent=2))
    return 0


def verify(adapter_id, evidence_path, host_label):
    a = load_adapter(adapter_id)
    raw = Path(evidence_path).read_text()
    if evidence_path.endswith(".jsonl"):
        rows = [json.loads(l) for l in raw.splitlines() if l.strip()]
        summary = next((r for r in rows if "summary" in r), {})
        checks = [r for r in rows if "name" in r]
        ev = {"adapter": adapter_id, "host": host_label, "checks": checks,
              "profile_sha256": summary.get("profile_sha256"), "summary": summary.get("summary")}
        if summary.get("summary") and " 0 failed" not in summary["summary"]:
            ev["checks"].append({"name": "suite", "expected": "0 failed", "observed": summary["summary"]})
    else:
        ev = json.loads(raw)
    errors = []
    if ev.get("adapter") != adapter_id:
        errors.append("evidence adapter mismatch")
    if ev.get("host") != host_label:
        errors.append("evidence host mismatch")
    if not isinstance(ev.get("checks"), list) or not ev["checks"]:
        errors.append("no recorded checks")
    else:
        for n, c in enumerate(ev["checks"]):
            if not {"name", "expected", "observed"} <= set(c):
                errors.append(f"checks[{n}] incomplete")
            elif c["observed"] != c["expected"]:
                errors.append(f"checks[{n}] {c['name']}: expected {c['expected']}, observed {c['observed']}")
    verdict = "BLOCKED" if a.get("status") != "supported" else ("VERIFIED_BOUNDED" if not errors else "UNSAFE" if any("observed" in e for e in errors) else "UNVERIFIED")
    if verdict != SENSITIVE_REQUIRED and ev.get("sensitive_data"):
        print(f"GATE_FAIL: sensitive-data task requires {SENSITIVE_REQUIRED}, verdict {verdict}")
        return 2
    print(f"GATE_{verdict}: {adapter_id} on {host_label}" + (f" errors={errors}" if errors else ""))
    return 0 if verdict == "VERIFIED_BOUNDED" else 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["discover", "preflight", "verify"])
    p.add_argument("--adapter")
    p.add_argument("--evidence")
    p.add_argument("--host", default="macOS 27.0.1")
    a = p.parse_args()
    if a.action == "discover":
        discover()
        return 0
    if a.action == "preflight":
        return preflight(a.adapter) if a.adapter else (print("--adapter required"), 2)[1]
    if not (a.adapter and a.evidence):
        print("--adapter and --evidence required", file=sys.stderr)
        return 2
    return verify(a.adapter, a.evidence, a.host)


if __name__ == "__main__":
    raise SystemExit(main())
