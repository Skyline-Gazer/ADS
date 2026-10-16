---
name: deliver
description: Execute an approved software goal through implementation, relevant testing, risk-adaptive code review, PR and permitted merge without repeated phase approval.
---
# Goal-driven delivery

1. Define observable success and scope. Inspect local project rules and actual merge-to-production implications.
2. For simple changes implement directly; for large or uncertain work use one concise plan and platform-native workers where helpful.
3. Prefer existing architecture and minimum sufficient implementation. Use necessary mature dependencies; escalate consequential architecture changes.
4. Run relevant deterministic tests and examine CI; apply [risk-adaptive review](../review/SKILL.md) at a level appropriate to actual impact. Verify review findings and fix real defects. Distinguish review failure/unavailability from a successful review; do not let an advisory model outage automatically block unrelated low-risk work.
5. Make a focused PR or use the repository's authorized direct-commit path; report checks, review disposition and remaining risks. Merge autonomously only if low risk, required checks pass and auto-deploy effects are within authorization.
6. Distinguish implemented, tested, reviewed, merged, deployed and live-tested in the summary. Continue working within the current session until goal completion or genuine blocker.

No compulsory per-stage approval, duplicate evidence archive or always-on maintenance scope.
