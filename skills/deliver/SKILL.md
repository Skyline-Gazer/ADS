---
name: deliver
description: Execute an approved software goal through implementation, relevant testing, PR and permitted merge without repeated phase approval.
---
# Goal-driven delivery

1. Define observable success and scope. Follow Git and PR rules declared in the project root `AGENTS.md`. When the project enabled [strict Git governance](../../profiles/strict-git-governance/README.md) or the task is in the ADS repository itself, follow [git-governance.md](../../docs/git-governance.md) fully.
2. Before access-sensitive local TUI work, confirm project-only read+write boundaries per [host-filesystem-boundary.md](../../docs/host-filesystem-boundary.md) when personal data is at risk.
3. Run one short capability check: declared build/test commands, runtimes, reusable fixtures, native Skills. Reuse for the whole task.
4. Implement with minimum sufficient change; use native subagents only when overlap clearly wins—see [native-subagent-safety.md](../../docs/native-subagent-safety.md) before sensitive delegation.
5. Run relevant tests and CI; fix related failures. Do not claim mocks prove live integration.
6. Open or update a focused PR per project rules; report checks and risks. Merge only when authorized, low risk, and required checks pass.
7. When the owner tracks Phases in GitHub Project, reconcile at milestone end ([milestone-reconciliation.md](../../docs/milestone-reconciliation.md)). Check ADS submodule upgrades only on owner request ([how-to-update.md](../../docs/how-to-update.md)).
8. Summarize implemented vs verified vs merged vs deployed. Continue on the existing branch/PR until done or `BLOCKED_WITH_EVIDENCE`.

No per-stage approval ritual or duplicate evidence archive.

## Optional profiles

- **Strict lifecycle:** [execution-and-drift-governance.md](../../docs/execution-and-drift-governance.md) when enabled in `AGENTS.md`.
- **Consumer toolchain preflight:** [consumer-dev-toolchain.md](../../docs/consumer-dev-toolchain.md) when enabled in `AGENTS.md`.
- **CNB Primary:** [git-provider.md](../../docs/git-provider.md), [cnb-review.md](../../docs/cnb-review.md), [cnb-sync.md](../../docs/cnb-sync.md) when configured—do not duplicate GitHub PRs.
