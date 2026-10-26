---
name: deliver
description: Execute an approved software goal through implementation, relevant testing, PR and permitted merge without repeated phase approval.
---
# Goal-driven delivery

1. Define observable success and scope. Inspect local project rules and actual merge-to-production implications. Before implementation, follow the mandatory [Git governance policy](../../docs/git-governance.md): use the latest `dev` as the development baseline, track the task with an Issue, work on an isolated task branch, and open a PR targeting `dev`. Never use direct task commits to `dev` or production `main`; production promotion requires a separate release PR.
2. Run one short capability check before implementing: existing runtimes and package managers, the project's declared build/test command, reusable fixtures and already available host Skills or subagents. Reuse those findings for the whole task; repeat only a check of stale assumptions, not a full environment audit.
3. For simple changes implement directly; for large or uncertain work use one concise plan and platform-native workers where helpful.
4. Treat multi-agent as an efficiency choice, not a required number of workers. If the host's native subagents are actually available and bounded independent tasks exist, delegate with a compact contract (goal, dependencies, permitted paths and operations, verification, output). For sensitive data or potentially unauthorized writes, verify effective **per-child** permission limits and real file/shell containment first; some hosts do **not** inherit parent denials, and worktree isolation does **not** block absolute-path writes. Use [docs/native-subagent-safety.md](../../docs/native-subagent-safety.md) for a proportional preflight. Prefer safe read-only parallel exploration or disjoint writes with enforced isolation; otherwise work serially or stop. No child may exceed the parent's explicit authorization or authorize peers.
5. Main agent owns integration: inspect child results/diffs, resolve conflicts, re-run relevant combined tests and distinguish independently observed results from agent claims. If a worker fails, times out or lacks safe isolation, retry narrowly or fall back to serial work without widening scope.
6. Prefer existing architecture and minimum sufficient implementation; reuse existing test facilities, caches and lockfiles before adding frameworks, containers or services. Use necessary mature dependencies; escalate consequential architecture changes.
7. Run relevant tests, examine CI and fix related failures. Use the lowest-cost check that can actually detect the changed behavior, and do not claim offline mocks or reused local fixtures prove live integration.
8. Make a focused Issue-linked PR targeting `dev`; direct task commits to `dev` or production `main` are prohibited. Report checks and risks. Merge autonomously only if low risk, required checks pass and auto-deploy effects are within authorization. Promote production changes only through the separate release/backport PR flow in the Git governance policy.
9. When the current Phase or milestone is actually complete, reconcile linked GitHub Project items and Issues against PR/CI/acceptance before dependent Phase work. Fix only verified drift, close only proved complete work and retain FAIL/PARTIAL blockers; unavailable Project API means PROJECT_UNVERIFIED. See [docs/milestone-reconciliation.md](../../docs/milestone-reconciliation.md). At that boundary, check whether the project's ADS submodule pin has an approved update without auto-upgrading it; use [docs/how-to-update.md](../../docs/how-to-update.md).
10. Distinguish implemented, tested, merged, deployed and live-tested in the summary. Continue working within the current session until goal completion or genuine blocker.

No compulsory per-stage approval, duplicate evidence archive or always-on maintenance scope.

## Primary provider dispatch

Read [provider selection](../../docs/git-provider.md) and validated .ads-project.json. Submit the Issue-linked PR targeting dev to the configured primary provider. In CNB Primary use current-SHA CNB review and deterministic CI, process feedback and re-review within a capped loop; NPC stays read/comment only unless separately authorized. Do not create a parallel GitHub PR. Production promotion, mirror and tags require separate authority and ref verification.
