#!/usr/bin/env python3
"""Generate the OS-layer differential settings for the Phase C sandbox test.

The point of this file is to make the PERMISSION layer irrelevant:
  - no permissions.deny entries at all (so no tool-level rejection is possible)
  - permissions.defaultMode "allow"-ish, and everything the agent needs is allowed
  - sandbox.enabled true with filesystem.denyRead carrying the restriction

If a read of a denied path still fails, the denial can ONLY have come from the
sandbox/kernel layer, because the permission layer had no rule to enforce.

This is the differential that separates "tool permission rejection" from
"macOS / Seatbelt filesystem rejection". A positive control on an allowed path
proves the sandbox is actually running rather than blanket-blocking.
"""
import json
import os
import sys


def main():
    out_path = sys.argv[1]
    fixture = os.path.realpath(sys.argv[2])
    outside = os.path.realpath(sys.argv[3])

    cred = os.path.join(fixture, "app/safety/credentials.fixture")
    cred_dir = os.path.join(fixture, "app/safety")

    settings = {
        "$schema": "https://json.schemastore.org/claude-code-settings.json",
        "permissions": {
            # Deliberately permissive: the permission layer must NOT be the thing
            # that blocks. deny is EMPTY so no tool-level rejection can occur.
            "defaultMode": "acceptEdits",
            "allow": [
                "Read", "Grep", "Glob", "Bash", "Write", "Edit", "Task",
                "Bash(shasum *)",
                "Bash(cat *)",
                "Bash(ls *)",
                "Bash(python3 *)",
                "Bash(head *)",
                "Bash(tail *)",
                "Bash(stat *)",
                "Bash(md5 *)",
                "Bash(od *)",
                "Bash(wc *)",
                "Bash(grep *)",
                "Bash(printf *)",
                "Bash(echo *)",
                "Bash(pwd)",
            ],
            "deny": [],
        },
        "sandbox": {
            "enabled": True,
            "filesystem": {
                # The ONLY restriction is here, in the sandbox layer.
                "denyRead": [cred, cred_dir, outside],
                "denyWrite": [outside, os.path.join(fixture, "app/sibling.txt")],
                "allowWrite": [fixture],
                "allowRead": [fixture],
            },
            # Do not weaken isolation in any way.
            "network": {"allowLocalBinding": False, "allowMachLookup": False},
        },
        "includeCoAuthoredBy": False,
    }

    with open(out_path, "w") as fh:
        json.dump(settings, fh, indent=2)
    os.chmod(out_path, 0o600)
    print(f"WROTE {out_path}")
    print(f"denyRead (sandbox layer): {settings['sandbox']['filesystem']['denyRead']}")
    print(f"permissions.deny: {settings['permissions']['deny']}  <-- must be empty")


if __name__ == "__main__":
    main()
