---
name: deliver
description: Execute an approved software goal through implementation, relevant testing, PR and permitted merge without repeated phase approval.
---
# Goal-driven delivery

1. Define observable success and scope. Inspect local project rules and actual merge-to-production implications.
2. Run one short capability check before implementing: existing runtimes and package managers, the project's declared build/test command, reusable fixtures and already available host Skills or subagents. Reuse those findings for the whole task; repeat only a check of stale assumptions, not a full environment audit.
3. For simple changes implement directly; for large or uncertain work use one concise plan and platform-native workers where helpful.
4. Prefer existing architecture and minimum sufficient implementation; reuse existing test facilities, caches and lockfiles before adding frameworks, containers or services. Use necessary mature dependencies; escalate consequential architecture changes.
5. Run relevant tests, examine CI and fix related failures. Use the lowest-cost check that can actually detect the changed behavior, and do not claim offline mocks or reused local fixtures prove live integration.
6. Make a focused PR or use the repository's authorized direct-commit path; report checks and risks. Merge autonomously only if low risk, required checks pass and auto-deploy effects are within authorization.
7. Distinguish implemented, tested, merged, deployed and live-tested in the summary. Continue working within the current session until goal completion or genuine blocker.

No compulsory per-stage approval, duplicate evidence archive or always-on maintenance scope.
