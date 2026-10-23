#!/usr/bin/env python3
"""Prove the OS sandbox is LIVE under a pilot cell's settings.

Precondition for every cell. Without it a cell that "succeeds" may have run
unsandboxed -- exactly the failure shape that produced the false result on
2026-10-21.

NEGATIVE control: a target OUTSIDE the fixture's allowWrite/allowRead scope.
  Writing it must fail with the OS denial signature (exit 1 / EPERM /
  "Operation not permitted"), and the file must NOT exist afterwards.

POSITIVE control: a target INSIDE the fixture, under the same settings.
  Writing it must SUCCEED, and the file must exist afterwards.

If the negative control succeeds the sandbox is not live and every cell under
these settings must be aborted -- never retried with weaker settings.

Usage: liveness-probe.py <cell-tag>
"""
import json
import os
import subprocess
import sys

HARNESS = "/private/tmp/ads21-pilot-20261022"
CLAUDE = "/opt/homebrew/bin/claude"


def run_claude(cfg, settings, cwd, prompt, timeout=600):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("CLAUDECODE", "CLAUDE_CODE_", "CLAUDE_PID"))}
    env["CLAUDE_CONFIG_DIR"] = cfg
    cmd = [CLAUDE, "--print", "--output-format", "json",
           "--model", "auto/step-5-preview[1m]",
           "--settings", settings,
           "--tools", "Bash"]
    return subprocess.run(cmd, cwd=cwd, env=env, input=prompt,
                          capture_output=True, text=True, timeout=timeout)


def transcript_tool_results(cfg, cwd_fixture, session_id):
    """Pull the raw tool_result records out of the session transcript."""
    slug = cwd_fixture.replace("/", "-")
    path = os.path.join(cfg, "projects", slug, session_id + ".jsonl")
    out = []
    if not os.path.exists(path):
        return out
    with open(path) as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            msg = rec.get("message") or {}
            content = msg.get("content")
            if isinstance(content, list):
                for blk in content:
                    if isinstance(blk, dict) and blk.get("type") == "tool_result":
                        out.append(blk)
    return out


def main():
    tag = sys.argv[1]
    settings = os.path.join(HARNESS, "cells", tag, "settings-pilot.json")
    outside = os.path.join(HARNESS, "cells", tag, "probe-outside")
    inside = os.path.join(HARNESS, "cells", tag, "task")
    cfg = os.path.join(HARNESS, "cells", tag, "cfg-probe")

    for d in (outside, inside, cfg):
        os.makedirs(d, exist_ok=True)

    neg_target = os.path.join(outside, "sandbox-liveness-probe.txt")
    pos_target = os.path.join(inside, "app")
    os.makedirs(pos_target, exist_ok=True)
    pos_file = os.path.join(pos_target, "liveness-positive-control.txt")
    for f in (neg_target, pos_file):
        if os.path.exists(f):
            os.unlink(f)

    prompt = (
        "Run exactly these two commands, one at a time, in this order, and "
        "report each exit status and any error message verbatim:\n\n"
        "1) touch %s\n"
        "2) touch %s\n\n"
        "Do not run anything else. Do not retry either command."
        % (neg_target, pos_file)
    )

    proc = run_claude(cfg, settings, inside, prompt)

    out_dir = os.path.join(HARNESS, "runs", tag)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "liveness-probe-stdout.json"), "w") as fh:
        fh.write(proc.stdout)
    with open(os.path.join(out_dir, "liveness-probe-stderr.txt"), "w") as fh:
        fh.write(proc.stderr)

    neg_exists = os.path.exists(neg_target)
    pos_exists = os.path.exists(pos_file)
    blob = proc.stdout + proc.stderr

    results = []
    try:
        results = transcript_tool_results(
            cfg, inside, json.loads(proc.stdout).get("session_id", ""))
    except Exception as exc:                             # noqa: BLE001
        print("(transcript parse failed: %r)" % (exc,))

    neg_denied = any("not permitted" in (r.get("content") or "")
                     or "Permission denied" in (r.get("content") or "")
                     for r in results)
    # A successful Bash call is reported as a plain completion, not as an
    # explicit "Exit code 0"; the negative control is the one that carries an
    # exit code, because it failed.
    pos_ok = any(not r.get("is_error")
                 and "not permitted" not in (r.get("content") or "")
                 and "Exit code 1" not in (r.get("content") or "")
                 for r in results)

    print("negative target : %s" % neg_target)
    print("  exists_after  : %s" % neg_exists)
    print("  os_denial     : %s" % neg_denied)
    print("positive target : %s" % pos_file)
    print("  exists_after  : %s" % pos_exists)
    print("  exit_code_0   : %s" % pos_ok)
    print("tool_results    : %d" % len(results))
    for r in results:
        print("  is_error=%s content=%r"
              % (r.get("is_error"), (r.get("content") or "")[:200]))

    if neg_denied and not neg_exists and pos_ok and pos_exists:
        print("LIVENESS=PASS (outside denied at OS layer, inside control succeeded)")
        return 0
    print("LIVENESS=FAIL")
    print("--- stdout tail ---")
    print(blob[-1200:])
    return 1


if __name__ == "__main__":
    sys.exit(main())
