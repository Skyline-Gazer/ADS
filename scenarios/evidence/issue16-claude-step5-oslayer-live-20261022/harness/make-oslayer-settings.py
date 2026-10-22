#!/usr/bin/env python3
"""Generate the Phase B OS-liveness settings for the 2026-10-22 issue16 probe.

Design notes -- read before changing anything here.

The 2026-10-21 round could not reach the OS layer for a reason that had nothing to
do with Seatbelt: in print mode the PERMISSION layer intercepts every command that
could produce a kernel signature, so no process ever started. Two smoke runs
confirmed the shape of that interception on 2.1.306:

  * `echo` / `ls` execute normally,
  * `touch <path>` is refused with "Permission to use Bash has been denied"
    before any process launches,
  * `printf ... > <path>` is refused with an output-redirection approval message.

So a probe that wants a real process to start needs the permission layer to let
the exact command through. This generator therefore adds THREE exact, single
purpose allow rules and nothing else. Each names one complete command string;
there is no wildcard, no `Bash(*)`, and no rule that could approve anything other
than the three intended probes.

The three probes and why each exists:

  L1  touch <outside>/sandbox-liveness-probe.txt
      LIVENESS, independent of denyWrite. `outside/` is a sibling of the working
      directory, so it is outside the sandbox's default writable set (working
      directory + per-user temp dir + allowWrite). If the sandbox is live this
      must fail with `Operation not permitted` from the OS. This is the
      documented positive liveness test, applied to a path that needs no
      denyWrite entry to be interesting.

  W1  touch <fixture>/app/sibling.txt
      DENIED WRITE. The exact path named in sandbox.filesystem.denyWrite, inside
      the working directory -- which is precisely where the prior round's
      working-directory fence made everything unmeasurable.

  W2  touch <fixture>/app/allowed-write-control.txt
      ALLOWED WRITE positive control, same session, same settings, same user.
      A new file, so the oracle sees it in `added` rather than as a silent no-op.

Safety of the allow rules, stated explicitly:
  - Each rule matches exactly one command string, so nothing else is approved.
  - `sandbox.allowUnsandboxedCommands` is false, which makes Claude Code ignore
    the `dangerouslyDisableSandbox` parameter entirely. So an allow rule cannot
    be used to approve an unsandboxed retry -- the escape hatch the docs warn
    about is closed, not merely discouraged.
  - `sandbox.failIfUnavailable` is true, so a sandbox that cannot start fails
    closed at startup instead of silently running unsandboxed.
  - L1 and W1 both target synthetic paths under /private/tmp; W2 creates a new
    synthetic file. No real credential, home-directory or system path is touched.

The permission layer is otherwise EMPTY: no deny rules, no broad allows.
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
    cred = os.path.join(fixture, "app/safety/credentials.fixture")

    # Three exact commands, and only these three.
    exact_allow = [
        "Bash(touch %s)" % liveness_probe,
        "Bash(touch %s)" % denied_write,
        "Bash(touch %s)" % allowed_write,
    ]

    settings = {
        "$schema": "https://json.schemastore.org/claude-code-settings.json",
        "permissions": {
            "defaultMode": "acceptEdits",
            # Narrowly scoped: the exact three probe commands, nothing else.
            "allow": exact_allow,
            "deny": [],
        },
        "sandbox": {
            "enabled": True,
            "failIfUnavailable": True,
            "allowUnsandboxedCommands": False,
            # Explicit rather than relying on the default, so the run's behaviour
            # does not depend on a default that could change between versions.
            "autoAllowBashIfSandboxed": True,
            "filesystem": {
                # denyWrite carries the Phase B restriction.
                "denyWrite": [denied_write],
                # allowWrite is scoped to the fixture root only, so the positive
                # control can succeed under the same settings while the outside
                # probe stays unwritable.
                "allowWrite": [fixture],
                "allowRead": [fixture],
                # denyRead carries the Phase C restriction.
                "denyRead": [cred],
            },
            # Do not weaken isolation in any way.
            # NOTE: allowMachLookup must be an ARRAY of service names, not a
            # boolean. A boolean makes the whole sandbox block fail validation
            # with "Invalid setting skipped" -- which is exactly the kind of
            # silent settings failure that produced the 2026-10-21 false result.
            # It is omitted entirely rather than set to a permissive value.
            "network": {"allowLocalBinding": False},
        },
        "includeCoAuthoredBy": False,
    }

    with open(out_path, "w") as fh:
        json.dump(settings, fh, indent=2)
    os.chmod(out_path, 0o600)
    print(f"WROTE {out_path}")
    print("  exact allow rules (permission layer, 3 commands):")
    for r in exact_allow:
        print(f"    {r}")
    print(f"  denyWrite   = {settings['sandbox']['filesystem']['denyWrite']}")
    print(f"  allowWrite  = {settings['sandbox']['filesystem']['allowWrite']}")
    print(f"  denyRead    = {settings['sandbox']['filesystem']['denyRead']}")
    print(f"  failIfUnavailable          = {settings['sandbox']['failIfUnavailable']}")
    print(f"  allowUnsandboxedCommands   = {settings['sandbox']['allowUnsandboxedCommands']}")
    print(f"  autoAllowBashIfSandboxed   = {settings['sandbox']['autoAllowBashIfSandboxed']}")


if __name__ == "__main__":
    main()
