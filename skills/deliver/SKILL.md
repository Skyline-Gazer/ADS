---
name: deliver
description: Finish a scoped software goal using existing tools, relevant functional checks and real-state verification.
---
# Deliver a goal

## Understand and act

Reuse the user's request or Issue/PR for the Goal, invariants, Acceptance, scope and real stop conditions. State a short session-local version only when complexity warrants it; do not create a mandatory contract file. Inspect the actual repository, open PRs, tools and tests, then make the **smallest change** that achieves the result. An obsolete fixture never licenses restoring a retired feature merely to green CI (A01).

Adapt the implementation path when it fails, not the Goal. Start relevant hosted CI early when available; use native subagents for independent work only when useful. Their worktree is not an OS sandbox, their claims are not verification and their delegation cannot broaden authorization.

## Default is development-first

ADS is **not** a sandbox. No Docker daemon, host isolation, negative probe, SCA/SBOM or security-only review is required for ordinary authorized coding, PRs or merges. Report unavailable isolation as `ISOLATION_NOT_ENFORCED` / `NOT_VERIFIED`, never PASS or an automatic `BLOCKED`. Avoid unapproved external paths, secrets, production changes and spending. Apply stricter isolation only when the project expressly enables it.

## Verify, converge and report

1. Run checks relevant to changed behavior and respect the **project's existing** functional CI and Review rules. A green tool exit is Process, a live remote SHA is State, and verified Acceptance is Outcome ([QUALITY](../../QUALITY.md)).
2. Find and take over the existing branch/PR for the same goal before opening another (A02). Resolve material review comments against the current head, not an older Review PASS (A03).
3. After failed partial operations, pushes, reviews and merges, reread actual remote state before proceeding (A04). Use the configured provider's native process; CNB Primary and GitHub Mirror are not duplicate development PRs (A06).
4. Merge only within the actual grant and configured required checks; production deploy, provider cutover, elevated IAM, secrets and remote destruction require separate authorization. Close Issues only when Acceptance is proved.
5. Report what truly happened: implemented, tests, PR link/current SHA, merged/not merged, deployed/not deployed, verified/unverified target. Do not stop at PR creation if a permitted next step remains.

See [SAFETY](../../SAFETY.md), [CNB review](../../docs/cnb-review.md) when applicable and [optional profiles](../../profiles/README.md). No second tracker or review ceremony.
