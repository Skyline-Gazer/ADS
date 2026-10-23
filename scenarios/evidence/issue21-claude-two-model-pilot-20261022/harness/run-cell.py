#!/usr/bin/env python3
"""Driver for the ADS #21 controlled two-model pilot.

Four cells, run independently with a fresh copy of the immutable task fixture
and a fresh throwaway CLAUDE_CONFIG_DIR:

  step5-serial     step-5-preview, one agent, both modules
  step5-multi      step-5-preview, parent dispatches two native children
  grok-serial      grok-4.5,     one agent, both modules
  grok-multi       grok-4.5,     parent dispatches two native children

Every cell gets the SAME task text, the same fail-closed invocation-local
sandbox policy verified in PR #36, and the same tool roster. Nothing global is
written; each cell's config dir is disposable.

Records stdout/stderr/exit code, wall-clock elapsed, and the fixture state
before and after. The independent oracle is executed by the operator, not by
the agent.
"""
import json
import os
import shutil
import subprocess
import sys
import time

CLAUDE = "/opt/homebrew/bin/claude"
HARNESS = "/private/tmp/ads21-pilot-20261022"
TASK_SRC = os.path.join(HARNESS, "task")
SETTINGS = os.path.join(HARNESS, "settings-pilot.json")
AGENTS = os.path.join(HARNESS, "settings-agents.json")
STRIP = ("CLAUDECODE", "CLAUDE_CODE_", "CLAUDE_PID")

MODELS = {
    "step5": "auto/step-5-preview[1m]",
    "grok": "cursor/grok-4.5",
}


def clean_env(config_dir):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(STRIP) or k == "CLAUDE_CONFIG_DIR"}
    env["CLAUDE_CONFIG_DIR"] = config_dir
    return env


def fresh_fixture(tag):
    """Each cell gets its own pristine copy of the immutable task fixture."""
    dest = os.path.join(HARNESS, "cells", tag, "task")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copytree(TASK_SRC, dest)
    return dest


def run_cell(tag, model, prompt_file, out_dir):
    model_id = MODELS[model]
    cfg = os.path.join(HARNESS, "cells", tag, "cfg")
    # Per-cell settings: the sandbox filesystem block is scoped to THIS cell's
    # fixture root, so the policy provably governs the tree the agent works in.
    settings = os.path.join(HARNESS, "cells", tag, "settings-pilot.json")
    fixture = fresh_fixture(tag)
    os.makedirs(cfg, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    probe_outside = os.path.join(HARNESS, "cells", tag, "probe-outside")
    os.makedirs(probe_outside, exist_ok=True)

    with open(os.path.join(HARNESS, prompt_file)) as fh:
        prompt = fh.read().replace("TASKROOT", fixture)

    # BEFORE snapshot, taken by the driver outside the agent.
    before = subprocess.run(
        [sys.executable, "-I", os.path.join(HARNESS, "oracle.py"),
         "snapshot", fixture],
        capture_output=True, text=True)
    with open(os.path.join(out_dir, "oracle-before.json"), "w") as fh:
        fh.write(before.stdout)

    cmd = [CLAUDE, "--print", "--output-format", "json",
           "--model", model_id,
           "--settings", settings,
           "--agents", AGENTS,
           "--tools", "Task,Read,Write,Edit,Bash,WebSearch"]

    env = clean_env(cfg)
    t0 = time.time()
    # The prompt goes through stdin. Passing it as a trailing argv element makes
    # --print fail with "Input must be provided either through stdin or as a
    # prompt argument".
    proc = subprocess.run(cmd, cwd=fixture, env=env, input=prompt,
                          capture_output=True, text=True, timeout=1800)
    elapsed = time.time() - t0

    # AFTER snapshot, also outside the agent.
    after = subprocess.run(
        [sys.executable, "-I", os.path.join(HARNESS, "oracle.py"),
         "snapshot", fixture],
        capture_output=True, text=True)
    with open(os.path.join(out_dir, "oracle-after.json"), "w") as fh:
        fh.write(after.stdout)

    with open(os.path.join(out_dir, "stdout.json"), "w") as fh:
        fh.write(proc.stdout)
    with open(os.path.join(out_dir, "stderr.txt"), "w") as fh:
        fh.write(proc.stderr)
    with open(os.path.join(out_dir, "cmd.txt"), "w") as fh:
        fh.write(" ".join(cmd) + "\n")
    with open(os.path.join(out_dir, "meta.json"), "w") as fh:
        json.dump({
            "tag": tag,
            "requested_model": model_id,
            "exit": proc.returncode,
            "elapsed_s": round(elapsed, 3),
            "fixture": fixture,
            "config_dir": cfg,
            "prompt_file": prompt_file,
            "settings": settings,
            "agents": AGENTS,
            "tools": "Task,Read,Write,Edit,Bash,WebSearch",
            "sandbox": {
                "enabled": True,
                "failIfUnavailable": True,
                "allowUnsandboxedCommands": False,
            },
        }, fh, indent=2)
    print("[%s] model=%s exit=%d elapsed=%.1fs"
          % (tag, model_id, proc.returncode, elapsed))
    return proc


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    cells = {
        "step5-serial": ("step5", "prompt-serial.txt"),
        "step5-multi": ("step5", "prompt-multi.txt"),
        "grok-serial": ("grok", "prompt-serial.txt"),
        "grok-multi": ("grok", "prompt-multi.txt"),
    }
    if which not in cells:
        sys.stderr.write("unknown cell %r; choose from %s\n"
                         % (which, sorted(cells)))
        return 2
    model, prompt = cells[which]
    run_cell(which, model, prompt,
             os.path.join(HARNESS, "runs", which))
    return 0


if __name__ == "__main__":
    sys.exit(main())
