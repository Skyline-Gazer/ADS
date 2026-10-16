# ADS Quality and Layered Verification

Version: **0.2 candidate**.

Choose checks from changed behavior, impact and consumers—not a mandatory test count. Docs: meaningful formatting/links. Ordinary code: impacted tests, types/lint/build as relevant. API/refactor: contract and integration tests. Sensitive changes: negative/security and recovery tests. Don't mask transitive impact with path filters.

## Verification layers

1. **Local:** deterministic tests, fixtures and mocks for fast feedback.
2. **Integration:** real dependencies in an authorized isolated/test environment when behavior actually depends on them.
3. **Production:** only when authorized and necessary; distinguish deployment success, service health and real-world functional validation.

Report each layer actually performed; a mocked test never proves live integration. Lack of live access is an unverified boundary, not success or automatic failure of unrelated code.

## Risk-adaptive code review

Review changed behavior and its consumers, not just changed lines. Documentation-only edits need relevant deterministic checks; AI review is optional. Ordinary code benefits from one incremental review where configured. API/architecture/integration changes warrant contract-oriented review and tests. Authentication, authorization, secrets, migrations and production-impacting changes need security-focused review, negative tests and scoped authorization as applicable.

[The review Skill](skills/review/SKILL.md) describes the process. OpenCodeReview is a preferred optional implementation, **not** a required ADS dependency or a substitute for deterministic verification. A project's stricter local requirements take precedence. Avoid duplicate mandatory reviews and endless model-driven fix loops.

Triage findings by concrete impact and evidence; verify AI suggestions before modifying code. Classify results honestly as reviewed, fixed, unresolved or not run/unavailable. Model/API failures are not success, but advisory outages do not automatically block unrelated low-risk work. Confirmed material defects and required check failures must not be suppressed.

## CI and review

Keep relevant required checks and material safety regressions blocking. Don't disable failing checks merely to turn CI green. Advisory AI reviews and irrelevant external review-service outages are not automatic blockers. Increase review rigor with change risk; routine low-risk code need not have two independent reviewers. Resolve concrete blocking findings, accurately report known limitations, then deliver under STANDARD.md and SAFETY.md.
