# ADS Quality and Layered Verification

Version: **0.2 candidate**.

Choose checks from changed behavior, impact and consumers—not a mandatory test count. Docs: meaningful formatting/links. Ordinary code: impacted tests, types/lint/build as relevant. API/refactor: contract and integration tests. Sensitive changes: negative/security and recovery tests. Don't mask transitive impact with path filters.

## Verification layers

1. **Local:** deterministic tests, fixtures and mocks for fast feedback.
2. **Integration:** real dependencies in an authorized isolated/test environment when behavior actually depends on them.
3. **Production:** only when authorized and necessary; distinguish deployment success, service health and real-world functional validation.

Report each layer actually performed; a mocked test never proves live integration. Lack of live access is an unverified boundary, not success or automatic failure of unrelated code.

## Repository-first code review

The GitHub repository/PR is the canonical review surface. Prefer one incremental OpenCodeReview (OCR) pass on each relevant PR update when the project opts in, **not** a mandatory OCR run at every local development step. OCR is replaceable, optional provider infrastructure; project-local rules prevail. See [integration guidance](docs/review-integration.md), the [optional workflow template](templates/github/ocr-review.yml.example), and [review Skill](skills/review/SKILL.md).

Documentation-only edits usually need only deterministic checks. Routine code can use advisory PR review. API, architecture and integration changes require appropriate contract/integration checks. Sensitive security, credential, migration or production-impacting changes require focused security review, negative tests and authorization where applicable.

Triage findings against real code paths and tests. Record reviewed/fixed/unresolved/unavailable accurately. An advisory model outage alone does not block unrelated low-risk changes; confirmed consequential defects and required deterministic check failures do. Avoid compulsory duplicate reviewers or endless LLM loops.

## CI and review

Keep relevant required checks and material safety regressions blocking. Don't disable failing checks merely to turn CI green. Advisory AI reviews and irrelevant external review-service outages are not automatic blockers. Increase review rigor with change risk; routine low-risk code need not have two independent reviewers. Resolve concrete blocking findings, accurately report known limitations, then deliver under STANDARD.md and SAFETY.md.
