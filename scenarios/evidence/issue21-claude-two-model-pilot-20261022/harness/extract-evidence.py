#!/usr/bin/env python3
"""Extract per-agent token/cost evidence from a pilot cell's transcripts.

The --output-format json result reports only the PARENT session's modelUsage.
The children's own usage lives in their sidechain transcripts, so it has to be
summed from there to give a full parent+child cost figure.
"""
import glob
import json
import os
import sys

HARNESS = "/private/tmp/ads21-pilot-20261022"


def agent_usage(path):
    """Read usage across one transcript, and record the models it reported.

    Two things matter here, both found by inspecting the 2.1.306 transcripts:

    1. The usage object sits on the assistant MESSAGE, not on the transcript
       record, so a record-level lookup alone returns zeros.
    2. The keys are snake_case in the transcript (input_tokens) but camelCase
       in the --output-format json result (inputTokens). Both are read.
    3. Every assistant turn restates CUMULATIVE usage, so summing across turns
       multiplies the total. The maximum seen per key is taken instead, which is
       the final cumulative figure for that agent.

    Sidechain transcripts in 2.1.306 carry zero usage on some turns, so the
    maximum is taken over all turns rather than the last one.
    """
    totals = {"inputTokens": 0, "outputTokens": 0,
              "cacheReadInputTokens": 0, "cacheCreationInputTokens": 0}
    key_pairs = {
        "inputTokens": ("input_tokens", "inputTokens"),
        "outputTokens": ("output_tokens", "outputTokens"),
        "cacheReadInputTokens": ("cache_read_input_tokens",
                                 "cacheReadInputTokens"),
        "cacheCreationInputTokens": ("cache_creation_input_tokens",
                                     "cacheCreationInputTokens"),
    }
    models = set()
    n_assistant = 0
    found = 0
    with open(path) as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            msg = rec.get("message") or {}
            if msg.get("model"):
                models.add(msg["model"])
            if msg.get("role") == "assistant":
                n_assistant += 1
            u = msg.get("usage") or rec.get("usage")
            if isinstance(u, dict):
                for camel, variants in key_pairs.items():
                    for k in variants:
                        v = u.get(k)
                        if isinstance(v, int):
                            totals[camel] = max(totals[camel], v)
                            break
                if any(totals.values()):
                    found += 1
    return totals, sorted(models), n_assistant, found


def main():
    cell = sys.argv[1]
    runs = os.path.join(HARNESS, "runs", cell)
    d = json.load(open(os.path.join(runs, "stdout.json")))
    sid = d["session_id"]

    cfg = os.path.join(HARNESS, "cells", cell, "cfg")
    parent_files = glob.glob(os.path.join(cfg, "projects", "*", sid + ".jsonl"))
    if not parent_files:
        print("no parent transcript found")
        return 1

    print("=== %s ===" % cell)
    print("session_id = %s" % sid)
    pt, pm, pa, pf = agent_usage(parent_files[0])
    print("PARENT  models=%s" % pm)
    print("  input=%d output=%d cacheRead=%d cacheCreate=%d assistant_msgs=%d usage_records=%d"
          % (pt["inputTokens"], pt["outputTokens"],
             pt["cacheReadInputTokens"], pt["cacheCreationInputTokens"], pa, pf))

    grand = dict(pt)
    children = []
    # Sidechain transcripts live in a `subagents/` directory INSIDE the session
    # id's own directory, not beside it:
    #   .../<sessionId>.jsonl
    #   .../<sessionId>/subagents/agent-<agentId>.jsonl
    parent_dir = os.path.dirname(parent_files[0])
    subdir = os.path.join(parent_dir, sid, "subagents")
    if not os.path.isdir(subdir):
        subdir = os.path.join(parent_dir, "subagents")
    if os.path.isdir(subdir):
        for f in sorted(glob.glob(os.path.join(subdir, "agent-*.jsonl"))):
            aid = os.path.basename(f)[len("agent-"):-len(".jsonl")]
            meta_p = f[:-len(".jsonl")] + ".meta.json"
            meta = {}
            if os.path.exists(meta_p):
                meta = json.load(open(meta_p))
            t, m, na, uf = agent_usage(f)
            children.append((aid, meta.get("agentType"), t, m, na, uf))
            for k in grand:
                grand[k] += t[k]

    for aid, atype, t, m, na, uf in children:
        print("CHILD   %s (%s) models=%s" % (aid, atype, m))
        print("  input=%d output=%d cacheRead=%d cacheCreate=%d assistant_msgs=%d usage_records=%d"
              % (t["inputTokens"], t["outputTokens"],
                 t["cacheReadInputTokens"], t["cacheCreationInputTokens"], na, uf))

    print("PARENT+CHILDREN TOTAL")
    print("  input=%d output=%d cacheRead=%d cacheCreate=%d"
          % (grand["inputTokens"], grand["outputTokens"],
             grand["cacheReadInputTokens"], grand["cacheCreationInputTokens"]))
    print("reported parent costUSD = %s" % d.get("total_cost_usd"))

    out = {
        "cell": cell,
        "session_id": sid,
        "parent": {"models": pm, "usage": pt, "usage_records": pf},
        "children": [{"agentId": a, "agentType": t_, "usage": u,
                      "models": m, "usage_records": uf}
                     for a, t_, u, m, _, uf in children],
        "grand_total_usage": grand,
        "reported_total_cost_usd": d.get("total_cost_usd"),
    }
    with open(os.path.join(runs, "agent-usage.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote %s" % os.path.join(runs, "agent-usage.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
