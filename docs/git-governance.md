# Mandatory Git Development Governance

**Status: normative.** This policy applies equally to the ADS repository and every project that adopts ADS. It is not an ADS-repository-only convention or an optional recommendation. Project-local guidance may add detail but must not silently relax these rules.

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
- Enable branch protection or repository Rulesets where the Git host and plan support them: require PRs and required status checks, disallow force pushes/deletion of important branches, and apply appropriate review rules. Do not assume that adding a workflow alone prevents direct pushes.
- If server-side protection cannot be enabled, report that the rule is documented/CI-checked but not server-enforced, and identify the exact platform/plan limitation. Do not claim hard enforcement when a user with write access can still bypass it.
- Do not make a fixed number of reviewers, a new workflow engine, or repeated approval stages mandatory for every low-risk change. Review rigor and test scope should match risk while preserving blocking safety/release gates.

## History, rollback and completion

- Keep commits scoped and messages meaningful. Never force-push shared `dev` or production history. Do not rewrite published history to conceal a regression.
- Prefer a revert or a new corrective PR for merged changes. A rollback must identify the affected commit/release, restore the intended behavior, run relevant checks, and preserve the audit trail.
- Treat merge, release, deployment and production validation as distinct states. Close Issues and reconcile GitHub Projects only against their own acceptance evidence and the actual delivered SHA.
- Do not commit secrets, machine-specific paths, generated CodeGraph indexes/caches, RTK binaries, or other generated build/runtime artifacts.

## Adoption and migration

- Bootstrap and adoption Skills must inspect the actual repository branches, deployment triggers, current CI, Issue/PR conventions and protection settings.
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
