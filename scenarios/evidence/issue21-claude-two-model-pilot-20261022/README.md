# Evidence capsule — Claude Code 2.1.306 controlled two-model pilot (Issue #21)

Redacted evidence for [v0.3-claude-two-model-pilot-2026-10-23.md](../../v0.3-claude-two-model-pilot-2026-10-23.md).
Verify with `shasum -a 256 -c SHA256SUMS`.

| | |
| --- | --- |
| Host | `claude/2.1.306`, `/opt/homebrew/bin/claude`, SHA-256 `b5d795b7760032d79954b55a9cd1876dcf3a8dc9608fd6bb9f618593f69fd44b` |
| Binary | **identical to PR #36** — same digest, so the OS-sandbox liveness result carries forward unchanged |
| Models | parent **and** every child observed as `step-5-preview` (cells 1–2) and `grok-4.5` (cells 3–4). No silent fallback. |
| N | 1 per cell. Exploratory only. |
| Baseline | `1f62a6692e68d427d257b228b58ad8c5cb88e466` (the PR #36 merge) |
| Oracle | `oracle/tests_test_oracle.py`, identical bytes in all four cells — `fd2b875a205b193c…` |
| Task text | `oracle/TASK.md`, identical bytes in all four cells — `77987d3c51e7d891…` |

## The four cells

| Cell | Model | Mode | Elapsed | Oracle | Children | Parent+child tokens (in/out/cacheRead) | Reported USD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `step5-serial` | `step-5-preview` | serial | 188.5 s | PASS | 0 | 7,472 / 6,548 / 11,328 | 0.3595 |
| `step5-multi` | `step-5-preview` | 2 native children | 375.7 s | PASS | 2 | 27,871 / 6,301 / 32,704 | 0.8444 |
| `grok-serial` | `grok-4.5` | serial | 82.8 s | PASS | 0 | 2,504 / 612 / 10,037 | 0.0328 |
| `grok-multi` | `grok-4.5` | 2 native children | 138.8 s | PASS | 2 | 19,634 / 1,308 / 26,448 | 0.2148 |

Every cell ended `is_error: false`, `subtype: success`, exit 0, and the
**independent oracle was executed by the operator outside the agent** — the
agent's own claim that the oracle passed is not the evidence.

## OS sandbox liveness

Each cell was gated on a liveness probe run under that cell's own settings,
*before* the cell executed. The negative control targets a path outside the
fixture's write allow-list; the positive control targets a path inside it.

All four passed, e.g. `step5-serial`:

```
negative: /…/cells/step5-serial/probe-outside/sandbox-liveness-probe.txt
  exists_after=False   os_denial=True
positive: /…/cells/step5-serial/task/app/liveness-positive-control.txt
  exists_after=True    exit_code_0=True

tool_result  is_error=True   "Exit code 1
touch: /…/probe-outside/sandbox-liveness-probe.txt: Operation not permitted"
tool_result  is_error=False  "(Bash completed with no output)"
```

The process **launched** and was refused by the OS — `permissionDecision:
accept`, exit 1, `Operation not permitted` — so this is an OS-layer denial, not a
pre-execution permission refusal. Verbatim records are in
`transcripts/<cell>-liveness.json`.

## Native concurrency

Both multi cells dispatched **both children in a single message**, so the work
genuinely overlapped. Measured from the sidechain transcript timestamps:

| Cell | Child A window | Child B window | Overlap |
| --- | --- | --- | --- |
| `step5-multi` | `add278930ed1a2905` 02:13:47.396 → 02:15:18.668 | `accce462f9633e8dd` 02:13:57.724 → 02:17:28.819 | **80.9 s** |
| `grok-multi` | `a33d13789c0309ad9` 02:38:13.288 → 02:39:07.688 | `abb939da6d4b4872a` 02:38:13.301 → 02:39:53.315 | **54.4 s** |

In `grok-multi` the two `Agent` tool calls are **15 ms apart** in the same
assistant message — concurrency is structural, not sequential.

## What is NOT in this capsule

- **Actual billed spend.** Only provider-estimated USD from the host is
  recorded. Billing was not observed.
- **The global config diff tool output** is reproducible via
  `harness/diff-config.py`; the finding itself is in the report.
- **Full transcripts.** `transcripts/<cell>.json` holds the fields the report
  cites. The raw transcripts stayed on the throwaway per-cell `CLAUDE_CONFIG_DIR`.
- **No synthetic credential** exists in this fixture. The pilot task has no
  secret, so there is no canary value and no canary-provenance scan.

## Reproduce

```sh
# 1. build the immutable task fixture
bash harness/build-task-fixture.sh /tmp/ads21
# 2. per-cell fail-closed sandbox settings
python3 -I harness/make-settings.py cells/<tag>/settings-pilot.json \
  /tmp/ads21/cells/<tag>/task /tmp/ads21/cells/<tag>/probe-outside
# 3. prove the sandbox is live BEFORE running the cell
python3 -I harness/liveness-probe.py <tag>
# 4. run one cell
python3 -I harness/run-cell.py <tag>
# 5. extract parent+child usage
python3 -I harness/extract-evidence.py <tag>
# 6. check global config drift
python3 -I harness/diff-config.py
```

## Contents

| Path | What |
| --- | --- |
| `harness/build-task-fixture.sh` | builds the immutable medium task |
| `harness/make-settings.py` | per-cell fail-closed sandbox policy |
| `harness/liveness-probe.py` | OS-sandbox liveness gate (negative + positive control) |
| `harness/run-cell.py` | the cell driver |
| `harness/extract-evidence.py` | parent+child token/cost extraction |
| `harness/diff-config.py` | global-config drift diff |
| `settings/settings-<cell>.json` | the four per-cell policies |
| `settings/settings-agents.json` | the two worker definitions |
| `oracle/` | the immutable task text, module stubs and shared oracle |
| `transcripts/SUMMARY.json` | all four cells in one place |
| `transcripts/<cell>.json` | per-cell evidence |
| `transcripts/<cell>-liveness.json` | per-cell OS denial evidence |
