---
name: deliver
description: Execute an authorized software goal with adaptive path selection, real-state verification, and convergence inside existing authorization.
---
# Goal-driven delivery (Adaptive Goal Execution)

Design constraint: keep ADS Lite — no new framework, no mandatory ceremony beyond a short Goal Contract when useful.

## 1. Goal Contract (session-local)

Before meaningful edits, state a compact contract in the session (or reuse clear Issue/PR text). **Do not** create a new file for ordinary tasks.

| Field | Meaning |
| --- | --- |
| Goal | What must be true when done |
| Invariants | What must not change (security, deprecated contracts, production) |
| Acceptance | How completion is proved (matched to task risk) |
| Scope | Allowed resources / paths / operations |
| Adaptation | What implementation details may change |
| Stop | When to stop or ask (actual authorization, required functional acceptance) |

If a proposed path would violate an Invariant, change architecture for its own sake, revive a deprecated contract, switch Provider, or widen privilege, **stop** and realign to the Goal — do not silently drift.

## 2. Path: environment first, then adapt

Reuse installed runtimes, declared scripts, hosted CI, and native Skills. Prefer the smallest existing facility.

When the current path fails, classify and act:

| Class | Action |
| --- | --- |
| Fixable technical fault | Narrow repair; re-verify |
| Environment mismatch | Switch to a documented alternate that still meets Acceptance (e.g. remote CI instead of heavy local) |
| Auth / safety / Provider ceiling | Request the exact missing Owner action; continue only independent safe work |

Do not treat permission denial or missing production authority as a prompt to bypass. Same strategy with no new evidence → stop mechanical retries; re-diagnose.

## 3. Evidence: Process / State / Outcome

Report which class you actually have ([QUALITY.md](../../QUALITY.md)):

- **Process** — the operation was invoked (API/CLI exited)
- **State** — the system of record changed (remote SHA, branch tip, artifact)
- **Outcome** — the Goal’s Acceptance holds in the target that matters

Command Success, Review `passed`, or CI green alone is Process (or partial State), not Outcome. After Git/Review/merge, **re-read** live refs and Review HEAD. After partial failure, re-read actual state before the next edit.

For CNB Primary comment disposition and fresh-head re-review, follow [cnb-review.md](../../docs/cnb-review.md) — do not duplicate it here.

## 4. Implement and verify

1. Follow Git rules in project `AGENTS.md`. ADS itself, or projects that enable [strict-git-governance](../../profiles/strict-git-governance/README.md), follow [git-governance.md](../../docs/git-governance.md).
2. ADS does not provide host isolation. [Filesystem containment](../../docs/host-filesystem-boundary.md) is optional; missing Docker, sandbox or synthetic probes must not block ordinary authorized coding. Report unverified enforcement accurately without treating instructions as an OS boundary.
3. Minimum sufficient change; native subagents only when overlap wins — [native-subagent-safety.md](../../docs/native-subagent-safety.md). Main agent owns integration and final verification.
4. Run the lowest-cost checks that can detect the changed behavior. Do not claim mocks prove live integration.

## 5. Convergence (authorized closure)

Default end state is **not** “PR opened.” Inside existing authorization:

1. Prefer one task branch/PR; before opening another, search for an open PR/branch for the same Goal and **take over**.
2. Drive CI and material review comments to closure on the **current** head SHA.
3. Merge when already authorized, low risk, required checks pass, and review gates for this Provider are satisfied.
4. Re-read the target branch SHA after merge. Close Issues / update Project only for work that Acceptance actually proves.
5. Stop at `BLOCKED_WITH_EVIDENCE` when a real ceiling remains.

**Convergence never authorizes:** production deploy, Provider switch, IAM/secret expansion, unrelated file access or bypassing existing functional CI/Review requirements “to finish.”

## Optional profiles

- Strict lifecycle: [execution-and-drift-governance.md](../../docs/execution-and-drift-governance.md) when listed in `AGENTS.md`
- Consumer toolchain: [consumer-dev-toolchain.md](../../docs/consumer-dev-toolchain.md) when listed
- CNB Primary: [git-provider.md](../../docs/git-provider.md), [cnb-review.md](../../docs/cnb-review.md), [cnb-sync.md](../../docs/cnb-sync.md) — no duplicate GitHub development PRs

No per-stage approval ritual or second evidence archive.
