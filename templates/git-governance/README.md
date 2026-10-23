# Git governance templates

These files help an ADS consumer apply the mandatory policy in [the canonical Git governance standard](../../docs/git-governance.md). They do not create server-side branch protection by themselves.

## Install

1. Copy `check_git_governance.py` into the consumer repository as `scripts/check-ads-git-governance.py`.
2. Copy `git-governance.yml` into `.github/workflows/ads-git-governance.yml` and keep its development branch set to `dev`. If the production branch is not `main`, update `ADS_PRODUCTION_BRANCH` and the workflow's PR branch filter.
3. Optionally copy `pull_request_template.md` into `.github/pull_request_template.md`.
4. Ensure the repository has `dev`, and inspect actual deployment triggers before changing branch setup. Existing consumers need a reviewable migration rather than a silent rewrite.
5. Run the checker tests when adapting it, then verify the workflow on a real PR.
6. Configure GitHub branch protection/Rulesets separately where the repository plan permits. The workflow reports PR policy violations; it does not prevent a user with write access from directly pushing to an unprotected branch.

The check validates the PR's base, head branch type, and an explicit Issue reference in the PR body. It checks reference syntax; it does not claim to verify Issue existence or acceptance completion.
