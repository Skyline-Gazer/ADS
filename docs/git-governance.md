# Mandatory Git Development Governance

**Status: normative for the ADS repository.** Consumer projects use [lite adoption](lite-adoption.md) by default and are **not** bound by this policy unless root `AGENTS.md` enables the [strict Git governance profile](../profiles/strict-git-governance/README.md). When enabled, project-local guidance may add detail but must not silently relax these rules.

ADS maintains `dev` for general integration and may maintain `cnb/dev` for CNB-specialized CI. Task PRs targeting `cnb/dev` set `ADS_DEVELOPMENT_BRANCH=cnb/dev`. Recognized task-branch prefixes include Cloud Agent `cursor/*` in addition to the conventional `feat`/`fix`/`chore`/… set.

## Branch model

- `dev` is the required daily development and integration branch. An adopting repository without `dev` must establish it through a reviewable bootstrap/migration before normal development proceeds. Do not treat direct work on `main` as an acceptable substitute.
- `main` is the production/release branch by default. If a project uses a different production branch for a documented platform reason, configure that exact branch explicitly; `dev` remains the required development integration branch.
- Every ordinary implementation task starts from the latest `dev` and uses a short-lived, isolated task branch. This includes `feat`, `feature`, `fix`, `bugfix`, `chore`, `docs`, `refactor`, `test`, `ci`, dependency maintenance and similar work.
- Use names that make the task and preferably its Issue discoverable, for example `feat/123-user-auth`, `fix/124-timeout`, or `chore/125-dependency-update`. Do not encode secrets, personal data or machine paths in branch names.
- Do not commit ordinary task changes directly to `dev` or the production branch. Deliver them through a PR targeting `dev`.
- Do not use a shared task branch for unrelated work. Concurrent agents or contributors must use isolated branches/worktrees or explicitly disjoint write ownership; a worktree is Git isolation, not a general filesystem security boundary.

## Issue and PR traceability

- Each distinct implementation task must have a GitHub Issue with a goal and proportionate acceptance criteria, and a PR that references that Issue. Reuse an existing Issue when it already covers the work; do not create one Issue per tiny commit or split a single task into artificial tickets.
- A task branch is based on the current `dev`, unless it is a release/backport transport branch carrying already-reviewed changes rather than new independent implementation.
- Ordinary task PRs target `dev`. The PR description identifies the Issue, change summary, acceptance evidence, relevant tests, risks and deployment/release effects.
- Use a closing reference such as `Closes #123` only when that PR completes the Issue's acceptance criteria. Use `Refs #123` or equivalent non-closing references for partial work. A merged PR or closed Issue alone is not proof that the delivered behavior was verified.
- Keep the chain from Issue to branch, PR, CI run, actual merge commit/SHA and any release/deployment evidence discoverable. Report skipped, blocked and unrun checks explicitly.

## Merge and release flow

1. Start from the latest `dev`, create a task branch, implement the scoped change, run checks selected by impact, and open a PR to `dev`.
2. Merge only after the applicable CI and review/safety requirements pass. Use the repository's approved merge method; squash merge is the default for ordinary task PRs when it preserves required traceability.
3. Verify the actual merge SHA and the post-merge `dev` integration result. Clean up the merged task branch when no other work depends on it.
4. Promote `dev` to the production branch through a separate, reviewable release PR. Include release scope, verification evidence, version/changelog changes where applicable, and deployment effects. A release branch, when needed, must be cut from `dev`; release-only fixes must be carried back to `dev`.
5. Production/release authorization remains separate from ordinary coding authorization. Merging source code is not proof of deployment or production validation.

## Emergency production fixes

- The fix must be implemented from the latest `dev` on a normal task branch and tracked by an Issue. Do not independently reimplement the same fix from `main`.
- When an urgent release cannot safely include the whole `dev` tree, selectively cherry-pick the reviewed fix commit into a short-lived `hotfix/<issue>-...` branch based on the production branch, then open a separate PR to production. This is release transport of the same fix, not a second development baseline.
- Ensure the fix is also merged into `dev`, resolve any conflict explicitly, and verify both the production backport and the `dev` integration. No direct production pushes or bypass of required checks.

## CI and server-side enforcement

- Validate PR base branches and Issue references automatically where deterministic. Ordinary task branches may target `dev`; production PRs may come from `dev` for a release or from an approved release/hotfix branch for controlled promotion/backport. Reject ordinary feature/fix/chore PRs targeting production.
- Run the repository's relevant CI on PR candidates and on pushes to `dev` and the production branch. A passing PR check must correspond to the actual candidate SHA; after merge, verify the target branch SHA and integration result.
- During adoption/bootstrap, inspect the actual `dev` and production branches and their server-side protection before declaring the repository compliant. Use an authenticated GitHub CLI (`gh`) session with repository-admin permission. A `404` from the classic branch-protection endpoint means that classic rule is absent; a `403` means the state could not be inspected and must not be interpreted as unprotected.
- If classic protection is absent or incomplete, run the shipped `scripts/ensure_branch_protection.py` helper. It uses `gh api` to enable/strengthen protection, requires exact CI check names supplied with repeated `--required-check` arguments, requires PRs and up-to-date required checks, enforces rules for admins, dismisses stale approvals, preserves stronger existing review thresholds/restrictions/checks, and disables force pushes and branch deletion. It re-reads the settings and fails if verification does not pass. It does not create branches or change the default branch.
- Example for ADS itself (use the exact check names observed in the current CI): `python3 scripts/ensure_branch_protection.py --repo Skyline-Gazer/ADS --branches dev main --required-check validate --required-check "Isolated consumer / AiringCal" --required-check "Isolated consumer / KIRARI"`. For an adopting repository using the provided workflow, use `--required-check branch-policy` and add the consumer's other stable blocking check names. Do not guess check names; inspect actual PR checks first.
- The consumer template includes the same helper at `templates/git-governance/ensure-ads-branch-protection.py`; copy it into the consumer repository and run it during adoption/bootstrap after `dev`, the production branch, and the governance workflow exist. Use `--dry-run` to inspect planned changes before applying them when desired.
- The helper manages classic branch protection through the REST API. If a repository relies on Rulesets, inspect their actual matching rules separately; do not claim compliance based only on the classic endpoint.
- Enabling server-side protection requires repository-admin access and a GitHub plan that supports protected branches. GitHub Free supports this for public repositories; private repositories require an eligible paid plan. If a `403` or plan restriction blocks configuration, report the exact failure and request the minimum owner action (grant admin access or change plan/visibility). Never claim hard enforcement when protection cannot be verified.
- Do not make a fixed number of reviewers, a new workflow engine, or repeated approval stages mandatory for every low-risk change. Review rigor and test scope should match risk while preserving blocking safety/release gates.

## History, rollback and completion

- Keep commits scoped and messages meaningful. Never force-push shared `dev` or production history. Do not rewrite published history to conceal a regression.
- Prefer a revert or a new corrective PR for merged changes. A rollback must identify the affected commit/release, restore the intended behavior, run relevant checks, and preserve the audit trail.
- Treat merge, release, deployment and production validation as distinct states. Close Issues and reconcile GitHub Projects only against their own acceptance evidence and the actual delivered SHA.
- Do not commit secrets, machine-specific paths, generated CodeGraph indexes/caches, RTK binaries, or other generated build/runtime artifacts.

## Adoption and migration

- Bootstrap and adoption Skills must inspect actual branches, deployment triggers, current CI, Issue/PR conventions and protection settings; after ensuring `dev` exists, automatically attempt to enable/strengthen missing classic branch protection with the `gh` helper and verify the result.
- If `dev` does not exist, establish it from the appropriate current baseline using the smallest reviewable migration. Verify that the production branch and deployment triggers remain unchanged. Do not silently change the repository default branch or production behavior.
- Existing consumers are not rewritten automatically. Create a scoped migration Issue/PR, migrate their rules and CI, and report any enforcement limitation. Until migrated, describe the gap honestly rather than claiming full ADS compliance.
- If repository permissions or the Git host prevent the required branch/CI setup, continue independent safe work and ask only for the exact owner action needed. The required branch model is not silently waived.

## Minimum acceptance

- A normal task starts from `dev`, has an Issue reference, and its PR targets `dev`.
- A normal feature/fix/chore PR targeting production is rejected by the automated policy check.
- A `dev`-to-production release PR and a production hotfix backport PR are accepted only in their defined forms and still require the applicable checks.
- Missing Issue references and unsupported target branches fail the policy check.
- CI runs on `dev` pushes and PRs; server-side protection state is separately verified and reported.
- ADS itself and consumer templates, Skills and bootstrap/adoption guidance all describe the same mandatory policy.

## Provider-aware interpretation (Issue #63)

The mandatory branch / Issue-linked PR / review / release invariants apply on the primary Git provider. Existing references to GitHub Issue, GitHub PR and gh protection describe the GitHub Primary adapter only. CNB Primary needs CNB-native PR and branch protection checks; do not create a duplicate GitHub PR just to satisfy GitHub tooling. Existing Issues and Projects may stay on GitHub with canonical cross-provider issue URLs. See [provider selection](git-provider.md). The baseline remains unchanged for existing consumers.

## Consumer release-preparation lifecycle

Consumer dev continuously retains reproducible developer integration. Strip it only on an independent release-preparation branch cut from the approved dev SHA. Supply the development manifest externally to the production guard so custom paths remain checked after removal, and scan actual build outputs. Reconcile published-release ancestry through a reviewed merge whose result preserves pre-merge dev-only files; do not delete from dev and restore in a later commit. Use merge commits where ancestry-preserving release transport requires them; no force-push or published-history rewrite.
