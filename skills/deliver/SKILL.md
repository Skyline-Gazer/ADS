---
name: deliver
description: Execute an approved software goal through implementation, relevant testing, PR review triage and permitted merge without repeated phase approval.
---
# Goal-driven delivery

1. Define observable success and scope. Inspect local project rules and actual merge-to-production implications.
2. For simple changes implement directly; for large or uncertain work use one concise plan and platform-native workers where helpful.
3. Prefer existing architecture and minimum sufficient implementation. Use necessary mature dependencies; escalate consequential architecture changes.
4. Run relevant deterministic tests and examine CI; fix related failures. Do not claim mocks prove cloud integration.
5. Submit a focused PR or use the authorized direct-commit path. If configured, consume the repository's OCR PR review, verify findings and fix real issues; [review Skill](../review/SKILL.md) explains optional local assistance and triage. Never mandate OCR before every commit. Disclose unavailable reviews and material risks.
6. Merge autonomously only if low risk, required checks pass and auto-deploy effects are within authorization. Distinguish implemented, tested, reviewed, merged, deployed and live-tested in the summary. Continue within the current session until completion or genuine blocker.

No compulsory per-stage approval, duplicate evidence archive or always-on maintenance scope.
