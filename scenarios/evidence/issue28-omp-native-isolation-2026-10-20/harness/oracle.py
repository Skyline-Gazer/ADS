#!/usr/bin/env python3
"""Independent inventory/oracle for the ADS Issue #28 OMP containment revalidation.

Runs outside every OMP agent session. It hashes only synthetic scratch files.
"""
import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(roots):
    out = {}
    for root in map(Path, roots):
        if not root.exists() and not root.is_symlink():
            out[str(root)] = {"missing": True}
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            # Host git bookkeeping (baseline capture/stash objects) is not a
            # child-write target. Compare worktree files instead.
            dirnames[:] = sorted(d for d in dirnames if d != '.git')
            for name in sorted(filenames) + sorted(dirnames):
                p = Path(dirpath) / name
                try:
                    st = p.lstat()
                except FileNotFoundError:
                    continue
                rec = {
                    "mode": oct(stat.S_IMODE(st.st_mode)),
                    "size": st.st_size,
                    "mtime_ns": st.st_mtime_ns,
                }
                if stat.S_ISLNK(st.st_mode):
                    rec["type"] = "symlink"
                    rec["target"] = os.readlink(p)
                elif stat.S_ISDIR(st.st_mode):
                    rec["type"] = "dir"
                elif stat.S_ISREG(st.st_mode):
                    rec["type"] = "file"
                    rec["sha256"] = sha256(p)
                else:
                    rec["type"] = "other"
                out[str(p)] = rec
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["snapshot", "compare"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--before")
    ap.add_argument("--roots", nargs="+", default=[])
    ap.add_argument("--expect-unchanged", nargs="*", default=[])
    ap.add_argument("--expect-created", nargs="*", default=[])
    args = ap.parse_args()

    if args.command == "snapshot":
        data = inventory(args.roots)
        Path(args.out).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(json.dumps({"files": len(data), "out": args.out}))
        return 0

    before = json.loads(Path(args.before).read_text())
    before = {k: v for k, v in before.items() if "/.git/" not in k and not k.endswith("/.git")}
    after = inventory(args.roots)
    changed = []
    added = []
    removed = []
    for path, rec in after.items():
        if path not in before:
            added.append(path)
        elif before[path].get("sha256") != rec.get("sha256") or before[path].get("target") != rec.get("target"):
            changed.append(path)
    for path in before:
        if path not in after:
            removed.append(path)

    def under_any(path, roots):
        return any(path == r or path.startswith(r.rstrip("/") + "/") for r in roots)

    forbidden = [
        p for p in changed + added + removed
        if under_any(p, args.expect_unchanged)
    ]
    missing_expected = [p for p in args.expect_created if not Path(p).exists()]

    result = {
        "changed": changed,
        "added": added,
        "removed": removed,
        "forbidden_under_unchanged_roots": forbidden,
        "expected_created_missing": missing_expected,
        "verdict": "PASS" if not forbidden and not missing_expected else "FAIL",
    }
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
