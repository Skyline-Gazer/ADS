---
name: deliver
description: Execute an approved software goal through implementation, relevant testing, PR and permitted merge without repeated phase approval.
---
# Goal-driven delivery

1. Define observable success and scope. Inspect local project rules and actual merge-to-production implications.
2. Run one short capability check before implementing: existing runtimes and package managers, the project's declared build/test command, reusable fixtures and already available host Skills or subagents. Reuse those findings for the whole task; repeat only a check of stale assumptions, not a full environment audit.
3. For simple changes implement directly; for large or uncertain work use one concise plan and platform-native workers where helpful.
4. Treat multi-agent as an efficiency choice, not a required number of workers. If the host's native subagents are actually available and bounded independent tasks exist, delegate with a compact contract (goal, dependencies, permitted paths and operations, verification, output). Prefer read-only parallel exploration or disjoint writes in isolated worktrees; otherwise work serially. No child may exceed the parent's explicit authorization or authorize peers.
5. Main agent owns integration: inspect child results/diffs, resolve conflicts, re-run relevant combined tests and distinguish independently observed results from agent claims. If a worker fails, times out or lacks safe isolation, retry narrowly or fall back to serial work without widening scope.
6. Prefer existing architecture and minimum sufficient implementation; reuse existing test facilities, caches and lockfiles before adding frameworks, containers or services. Use necessary mature dependencies; escalate consequential architecture changes.
7. Run relevant tests, examine CI and fix related failures. Use the lowest-cost check that can actually detect the changed behavior, and do not claim offline mocks or reused local fixtures prove live integration.
8. Make a focused PR or use the repository's authorized direct-commit path; report checks and risks. Merge autonomously only if low risk, required checks pass and auto-deploy effects are within authorization.
9. When the current Phase or milestone is actually complete, reconcile linked GitHub Project items and Issues against PR/CI/acceptance before dependent Phase work. Fix only verified drift, close only proved complete work and retain FAIL/PARTIAL blockers; unavailable Project API means PROJECT_UNVERIFIED. See [docs/milestone-reconciliation.md](../../docs/milestone-reconciliation.md). At that boundary, check whether the project's ADS submodule pin has an approved update without auto-upgrading it; use [docs/how-to-update.md](../../docs/how-to-update.md).
10. Distinguish implemented, tested, merged, deployed and live-tested in the summary. Continue working within the current session until goal completion or genuine blocker.

No compulsory per-stage approval, duplicate evidence archive or always-on maintenance scope.
