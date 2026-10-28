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


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "templates" / "host-security" / "probe-manifest.json"


def _sha256(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(adapter_id, evidence_path, host_label):
    a = load_adapter(adapter_id)
    raw = Path(evidence_path).read_text()
    manifest = json.loads(MANIFEST_PATH.read_text())

    # --- mandatory probe manifest integrity ---
    current_gen_sha = _sha256(Path(__file__).resolve().parents[1] / "templates" / "host-security" / "gen_project_sandbox.py")
    if manifest.get("manifest_version") != 1:
        return _fail("unsupported manifest_version")
    if manifest.get("generator_sha256") != current_gen_sha:
        return _fail(f"manifest generator_sha256 {manifest.get('generator_sha256','')[:12]} does not match current generator {current_gen_sha[:12]} — regenerate manifest")
    required = manifest["required_checks"]
    req_names = [c["name"] for c in required]
    if len(req_names) != len(set(req_names)):
        return _fail("manifest contains duplicate probe names")
    expected_by_name = {c["name"]: c["expected"] for c in required}

    # --- parse evidence ---
    if evidence_path.endswith(".jsonl"):
        rows = [json.loads(l) for l in raw.splitlines() if l.strip()]
        summary = next((r for r in rows if "summary" in r), {})
        observed_rows = [r for r in rows if "name" in r]
        if " 0 failed" not in summary.get("summary", ""):
            return _fail(f"suite reported failures: {summary.get('summary')}")
        profile_sha = summary.get("profile_sha256")
    else:
        return _fail("JSON evidence format is not trusted; run verify-sandbox.sh to produce JSONL")

    # --- provenance: producer must be the bundled probe script ---
    if manifest.get("probe_script") != "scripts/verify-sandbox.sh":
        return _fail("manifest producer mismatch")

    # --- profile digest binding + freshness ---
    if not profile_sha or len(profile_sha) != 64:
        return _fail("missing or malformed profile_sha256")
    ev_profile = evidence_profile_path(evidence_path, profile_sha)
    if ev_profile is None:
        return _fail(f"profile file for sha256 {profile_sha[:12]} not found or not registered in ~/.omp/sandbox")
    live_sha = _sha256(ev_profile)
    if live_sha != profile_sha:
        return _fail(f"profile changed since run: evidence {profile_sha[:12]} vs live {live_sha[:12]}")

    # --- host identity binding ---
    if a["adapter"] == "macos-cli-seatbelt" and not host_label.startswith("macOS"):
        return _fail(f"host label {host_label!r} incompatible with adapter")

    # --- completeness / uniqueness ---
    obs_names = [r["name"] for r in observed_rows]
    dupes = {n for n in obs_names if obs_names.count(n) > 1}
    if dupes:
        return _fail(f"duplicate observed probes: {sorted(dupes)}")
    missing = set(req_names) - set(obs_names)
    extra = set(obs_names) - set(req_names)
    if missing:
        return _fail(f"omitted mandatory probes: {sorted(missing)}")
    if extra:
        return _fail(f"unregistered probes present: {sorted(extra)}")

    # --- expected outcomes come from the manifest, never the evidence ---
    errors = []
    for r in observed_rows:
        want = expected_by_name[r["name"]]
        got = r.get("observed")
        if got != want:
            errors.append(f"{r['name']}: expected {want}, observed {got}")
    if errors:
        print(f"GATE_UNSAFE: {adapter_id}: " + "; ".join(errors[:5]))
        return 2

    # --- adapter status must independently claim support ---
    if a.get("status") != "supported":
        return _fail(f"adapter status is {a.get('status')}; no support claim permitted")

    print(f"GATE_VERIFIED_BOUNDED: {adapter_id} on {host_label} profile={profile_sha[:12]} probes={len(observed_rows)}")
    return 0


def evidence_profile_path(evidence_path, profile_sha):
    """Bind evidence to a live profile file registered under ~/.omp/sandbox."""
    import glob
    for cand in glob.glob(str(Path.home() / ".omp" / "sandbox" / "*.sb")):
        try:
            if _sha256(cand) == profile_sha:
                return cand
        except OSError:
            continue
    return None


def _fail(reason):
    print(f"GATE_FAIL: {reason}")
    return 2


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
