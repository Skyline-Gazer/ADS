#!/usr/bin/env python3
"""Generate the invocation-local sandbox settings for ONE ADS #21 pilot cell.

Carries forward the fail-closed policy verified in PR #36 (issue16 OS-sandbox
liveness) unchanged in every security-relevant respect:

  1. sandbox.failIfUnavailable is true. Its default of false makes a sandbox
     that cannot start silently run unsandboxed while the run still reports
     success -- the exact trap that produced the 2026-10-21 false result.
  2. sandbox.allowUnsandboxedCommands is false. This makes Claude Code ignore
     the dangerouslyDisableSandbox parameter entirely, so no allow rule can
     approve an unsandboxed retry.
  3. sandbox.network.allowMachLookup is OMITTED. It is an array of service
     names, not a boolean; a boolean makes validation reject the key and log
     "Invalid setting skipped without dialog", which in -p mode silently voids
     the whole sandbox block while the run still reports success.
  4. autoAllowBashIfSandboxed is set explicitly rather than trusting a default.

WHAT DIFFERS FROM PR #36, AND WHY

  * The filesystem block is scoped to THIS cell's fixture root. PR #36 pointed
    its denyRead/denyWrite rules at its own synthetic credential fixture
    (v2/fixture-a/app/...). Those paths do not exist in a pilot cell, so
    carrying them forward verbatim would have produced rules that govern
    nothing -- the sandbox would have started but denied nothing. The pilot
    fixture deliberately contains no synthetic credential, so denyRead and
    denyWrite are empty here rather than aimed at a nonexistent path.

  * OS-sandbox liveness for the pilot is therefore proven SEPARATELY, by the
    operator, against a probe tree under these same settings, rather than
    inferred from the presence of a deny rule that has no target.

  * The exact permission allow rules cover only the canonical oracle
    invocations plus the liveness probe. In print mode a bare command is
    refused pre-execution, so the cell never reaches the OS layer at all; the
    2026-10-22 OS-liveness round established that narrowly scoped exact rules
    are the only way through. No wildcard and no Bash(*) is used.

The previous version of this file emitted rules aimed at PR #36's stale
v2/fixture-a tree. That is the defect this rewrite fixes: the pilot's four
cells were running with a sandbox whose deny rules targeted a directory that
did not exist.
"""
import json
import os
import sys


def main():
    out_path = sys.argv[1]
    fixture = os.path.realpath(sys.argv[2])
    outside = os.path.realpath(sys.argv[3])

    denied_write = os.path.join(fixture, "app/sibling.txt")
    allowed_write = os.path.join(fixture, "app/allowed-write-control.txt")
    liveness_probe = os.path.join(outside, "sandbox-liveness-probe.txt")

    # Exact, single-command rules only. The probe rules are the ones PR #36
    # needed to reach the OS layer at all; the oracle rules stop the print-mode
    # permission layer from refusing the canonical oracle invocation before any
    # process launches. Nothing here is a wildcard.
    exact_allow = [
        # --- OS-sandbox liveness probes (operator-driven, not agent-driven) ---
        "Bash(touch %s)" % liveness_probe,
        "Bash(touch %s)" % denied_write,
        "Bash(touch %s)" % allowed_write,
        # --- the shared correctness oracle, in its canonical invocations ---
        "Bash(python3 -I tests/test_oracle.py)",
        "Bash(python3 -I tests/test_oracle.py:*)",
        "Bash(python3 -I -m pytest tests/test_oracle.py:*)",
        "Bash(python3 -I -m pytest -q tests/test_oracle.py:*)",
    ]

    settings = {
        "$schema": "https://json.schemastore.org/claude-code-settings.json",
        "permissions": {
            "defaultMode": "acceptEdits",
            "allow": exact_allow,
            "deny": [],
        },
        "sandbox": {
            "enabled": True,
            "failIfUnavailable": True,
            "allowUnsandboxedCommands": False,
            "autoAllowBashIfSandboxed": True,
            "filesystem": {
                "denyWrite": [],
                "allowWrite": [fixture],
                "allowRead": [fixture],
                "denyRead": [],
            },
            # allowMachLookup is deliberately absent: it is an array, and a
            # boolean here silently voids the whole sandbox block.
            "network": {"allowLocalBinding": False},
        },
        "includeCoAuthoredBy": False,
    }

    with open(out_path, "w") as fh:
        json.dump(settings, fh, indent=2)
    os.chmod(out_path, 0o600)
    print("WROTE %s" % out_path)
    print("  fixture root                    = %s" % fixture)
    print("  sandbox.enabled                 = %s" % settings["sandbox"]["enabled"])
    print("  sandbox.failIfUnavailable       = %s" % settings["sandbox"]["failIfUnavailable"])
    print("  sandbox.allowUnsandboxedCommands= %s" % settings["sandbox"]["allowUnsandboxedCommands"])
    print("  allowRead / allowWrite          = %s" % settings["sandbox"]["filesystem"]["allowRead"])
    print("  denyRead / denyWrite            = (empty; no synthetic credential in this fixture)")
    print("  exact allow rules               = %d (no wildcard)" % len(exact_allow))


if __name__ == "__main__":
    main()
