#!/usr/bin/env python3
"""Diff the live global config against its own most recent backup.

Answers the GLOBAL_CONFIG_DRIFT question for the ADS #21 pilot: what actually
changed in ~/.claude.json and ~/.claude/settings.json, and therefore whether the
pilot cells wrote anything. Every cell ran with CLAUDE_CONFIG_DIR pointed at a
throwaway directory, so a pilot-caused change is not expected -- but the
pre/post hashes recorded for the experiment differ, so the cause has to be
established rather than assumed.
"""
import glob
import hashlib
import json
import os
import sys

HOME = os.path.expanduser("~")


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def diff_json(a, b, label):
    keys = set(a) | set(b)
    out = []
    for k in sorted(keys):
        if a.get(k) != b.get(k):
            out.append((k, a.get(k), b.get(k)))
    print("%s: %d differing key(s)" % (label, len(out)))
    for k, va, vb in out:
        print("  - %s" % k)
        print("      before: %s" % repr(va)[:160])
        print("      after : %s" % repr(vb)[:160])
    return out


def main():
    live_json = os.path.join(HOME, ".claude.json")
    live_settings = os.path.join(HOME, ".claude", "settings.json")
    backup_dir = os.path.join(HOME, ".claude", "backups")

    print("live ~/.claude.json        %s" % sha(live_json))
    print("live ~/.claude/settings.json %s" % sha(live_settings))

    backups = sorted(glob.glob(os.path.join(backup_dir, ".claude.json.backup.*")))
    if not backups:
        print("no .claude.json backups found")
        return 1
    prev = backups[-1]
    print("newest backup              %s (%s)"
          % (os.path.basename(prev), sha(prev)))

    a = json.load(open(prev))
    b = json.load(open(live_json))
    diffs = diff_json(a, b, "~/.claude.json vs newest backup")

    # Which top-level keys grew or shrank is the useful signal: ordinary
    # bookkeeping churn (counters, timestamps, per-project history) is benign;
    # any permissions/allow/deny/hooks change is not.
    interesting = [k for k, _, _ in diffs
                   if any(t in k.lower() for t in
                          ("permission", "allow", "deny", "hook", "sandbox",
                           "apiKey", "token", "credential", "settings"))]
    print()
    print("security-relevant differing keys: %s" % (interesting or "NONE"))

    settings_backups = sorted(glob.glob(os.path.join(backup_dir, "settings*.backup*")))
    print("settings backups available : %d" % len(settings_backups))
    return 0


if __name__ == "__main__":
    sys.exit(main())
