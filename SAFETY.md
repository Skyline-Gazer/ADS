# Safety and Authorization

Version: 0.1-draft — proposal, not yet adopted.

## Judge risk independently from complexity
Assess code impact, external operations and deployment effects separately. A large UI change may have low operational risk; a small change to infrastructure controls can be high-risk.

## Authorized ordinary development
A clear development request permits investigation, scoped code changes, local tests, branches, commits, pushing task branches and opening PRs. Low-risk PR merging follows STANDARD.md and the repository's documented deployment policy.

## Owner approval boundaries
Require specific authorization before operations or merges that materially affect production data or migrations, secrets, identity and access permissions, payment/billing behavior, externally controlled resources, service availability or security controls. Work on source code and isolated tests may proceed without executing these operations.

A native Git auto-deploy is not blanket authorization for risky changes. An existing low-risk auto-release policy must explicitly cover the change.

## Minimum protections
Never disclose secrets in source, PRs or logs. Apply least privilege. Validate untrusted data. Avoid unreviewed remote code execution. Do not claim checks or deployments that did not occur. Evaluate actual applicability of security findings instead of either suppressing all alerts or blocking indefinitely on advisory labels.

## Pause only on genuine blockers
Stop an affected action only for insufficient authorization, consequential ambiguity, unresolved material safety risk or a required check that cannot safely pass. Report the specific decision needed and continue unrelated safe work when possible.

Project-specific stricter controls are legitimate when they protect a specific real operation. Generic framework stages do not themselves justify a safety gate.
