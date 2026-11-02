# ADS — Outcome and Verification

Version: **v0.7 development-first candidate** (unreleased). Preserve historical evidence; do not re-score old failures to make a new release green.

## Process / State / Outcome

Do not confuse the work attempted with the result delivered:

| Evidence | What it establishes | What it does **not** establish |
| --- | --- | --- |
| **Process** | A tool, CI job or Review ran | The expected target changed |
| **State** | A remote SHA, merge commit, artifact or deployed revision actually changed | The desired behavior works |
| **Outcome** | The goal's Acceptance holds in its intended environment | Any untested production condition |

Example: `git push` exit 0 is Process. Read-back of the branch SHA is State. Required functional tests and the correct merged behavior are Outcome within their tested scope. After partial failure, merge or deployment, query **live state again** before repairing or claiming completion (A04). An open PR is not a merge. A Review PASS on an older head with unresolved material comments is not acceptance (A03).

Report `NOT RUN`, `NOT_VERIFIED` or a precise actual blocker where appropriate; never infer PASS from a mock, missing provider integration, an agent's own summary, or green CI for unrelated behavior.

## Proportionate checks, not a new release ritual

Choose the **smallest checks capable of detecting the change's risk**. Documentation: meaningful link/format checks. Ordinary code: affected tests, type/lint/build as relevant. API or runtime changes: their actual contracts and integrations. Existing hosted CI is generally preferred when it exercises the target behavior; use real preview/production only when needed and authorized. Do not create long-lived test environments, subscriptions, local Docker or extra CI merely because ADS has an example.

Keep required functional CI and material source-review findings. Optional security-only scans, SBOM, supply-chain attestations and isolation probes are advisory unless the consumer expressly opts into them. Existing required-check configuration must be changed honestly through a reviewed update; a failed or unrun check is never a PASS. Neither a passing mock nor a remote CI green light proves an untested live dependency.

## Agent integration and completion

Parent agents integrate child code and re-check affected combined behavior; children cannot independently declare Goal completion. Parallel experiments and model/host speed comparisons are research, **not** delivery gates: historical protocols remain under [scenarios](scenarios/), and any claimed acceleration requires comparable baseline and observed end-to-end cost.

Use the project/provider's actual PR and Review rules. For CNB, dispose of material CodeBuddy comments against the current head per [CNB review](docs/cnb-review.md); do not add a duplicate GitHub dev PR (A06). Reuse existing task PRs (A02), do not revive obsolete contracts merely to satisfy stale harnesses (A01), and do not mistake non-enforced isolation for a verified boundary (A05).

When completing work, state the actual branch/PR/merge SHA, relevant tests/CI, review disposition, deployment scope, known limitations and any unverified outcome. Update project boards or close Issues only for requirements proved complete. A good report is short; an evidence archive or milestone receipt is not a requirement of ordinary ADS Lite work.

Optional consumer tooling (CodeGraph, RTK), strict branch rules and lifecycle receipts are governed only by explicitly enabled [profiles](profiles/README.md). ADS contributors follow [git governance](docs/git-governance.md); do not copy their checks into a default consumer.
