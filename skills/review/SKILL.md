---
name: review
description: Risk-adaptive code review for agent delivery, optionally using OpenCodeReview locally or on trusted GitHub PRs.
---
# Risk-adaptive code review

Read the project's own AGENTS.md and ADS QUALITY.md/SAFETY.md. This Skill defines review behavior, **not** an OCR installation requirement. Use OpenCodeReview (OCR) where available; use an equivalent reviewer or manual risk-based inspection otherwise. Never claim OCR ran when it did not.

1. Classify the actual changed behavior and reachable consumers: documentation-only; routine code; contract/integration/architecture; sensitive (auth, permissions, secrets, security boundaries, database migration, production state). Project-local stricter rules win.
2. Run deterministic relevant checks first. Review the diff and surrounding contracts. For routine code, prefer one incremental AI review (locally before PR or on the PR), without compulsory duplicate runs. For documentation, AI review is optional. For sensitive changes, use deeper review plus negative/security tests and human authorization where applicable.
3. Where installed, invoke the project's configured/pinned OCR integration with least privileges and a suitable model. Never send secrets, credential files, customer data or untrusted private content to an unapproved API. Do not invent executable CLI flags or action versions; verify the official interface and pin immutable Action SHA and reviewed CLI version before enabling.
4. Treat review output as untrusted suggestions. For each concrete finding, verify the affected code path, exploitability/behavior, and tests; fix valid findings with focused tests; mark false positives with a short rationale. Avoid unlimited review/fix loops: repeat only for material modified behavior or unresolved consequential findings.
5. Record outcomes distinctly: **passed**, **actionable findings fixed**, **findings open**, **review unavailable/not run**. An OCR timeout, API error, missing credential or model failure is not a passed review and does not automatically block unrelated low-risk delivery. Material known vulnerabilities and required deterministic checks still block under project rules.
6. For GitHub OCR: default PR token permission to read-only; do not expose model secrets to forks or untrusted pull_request code; never execute or checkout attacker-controlled code in a privileged pull_request_target job. Do not auto-merge or mutate production from the reviewer. Review the exact trust boundary and workflow before enabling a credentialed bot.
7. Include concise PR review disposition and remaining risks using existing PR comments/checks; do not create a parallel issue database, state machine, standalone runner or evidence archive.

See [QUALITY.md](../../QUALITY.md) and [SAFETY.md](../../SAFETY.md) for the canonical policies. The OCR provider is optional and replaceable.
