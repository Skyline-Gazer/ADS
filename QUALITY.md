# Quality and Verification

Version: 0.1-draft — proposal.

Quality checks should prevent real defects, not create paperwork. Preserve the affected contracts, architecture and security protections.

## Match verification to impact
- Documentation changes: relevant format/link checks.
- Routine source changes: affected tests, type/lint checks and build as appropriate.
- Features or refactors: impacted integration, browser and API validation.
- Sensitive changes: negative/security cases and practical recovery assessment.

Test selection must account for shared dependencies and transitive consumers. Never use path filters to hide a relevant failure.

## CI
Keep relevant build, type and security-boundary regression checks blocking. Distinguish informational audits and AI reviews from hard requirements. Run expensive platform-specific suites where they add value, not automatically on every small change. Never disable necessary tests merely for green CI.

## Review
Low-risk work does not require two independent reviews. Escalate review for sensitive areas and consequential architecture changes. Blocking findings should identify concrete, supportable problems; advisory tool failures are not themselves defects.

## Completion
PRs briefly describe what changed, which checks actually ran and remaining risks. Prefer commits, PR discussion and CI logs as evidence, not duplicate evidence documents. Distinguish implementation, testing, merging, deployment and real production validation. Update user/operational docs when observable behavior, interfaces or procedures change.
