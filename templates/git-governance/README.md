# Git governance templates

These files help an ADS consumer apply the mandatory policy in [the canonical Git governance standard](../../docs/git-governance.md). They do not create server-side branch protection by themselves.

## Install

1. Copy `check_git_governance.py` into the consumer repository as `scripts/check-ads-git-governance.py`.
2. Copy `git-governance.yml` into `.github/workflows/ads-git-governance.yml` and keep its development branch set to `dev`. If the production branch is not `main`, update `ADS_PRODUCTION_BRANCH` and the workflow's PR branch filter.
3. Optionally copy `pull_request_template.md` into `.github/pull_request_template.md`.
4. Ensure the repository has `dev`, and inspect actual deployment triggers before changing branch setup. Existing consumers need a reviewable migration rather than a silent rewrite.
5. Run the checker tests when adapting it, then verify the workflow on a real PR.
6. Inspect exact blocking check names from the consumer's real CI/PR runs. Then run the branch-protection helper using an authenticated `gh` CLI session with repository-admin access:

   `python3 scripts/ensure-ads-branch-protection.py --repo OWNER/REPO --branches dev main --required-check branch-policy`

   Repeat `--required-check "EXACT CHECK NAME"` for every other stable blocking check. The helper checks current classic protection, enables or strengthens it when needed, preserves existing stricter settings, and re-reads the API to verify. Use `--dry-run` to preview. Ensure both branches already exist; the helper does not create `dev` or change the default branch.

7. If the API returns `403`, do not interpret that as an unprotected branch. Verify the `gh` account has repository-admin permission and the GitHub plan supports protection. GitHub Free supports protected branches for public repositories; private repositories require an eligible paid plan. If blocked, record the exact owner action. The workflow itself cannot prevent direct pushes.

The check validates the PR's base, head branch type, and an explicit Issue reference in the PR body. In GitHub Actions, the read-only token verifies that each referenced number resolves to an Issue in the same repository and rejects references that resolve to pull requests. Without a token/repository context, local invocation checks syntax only. Neither mode proves that the Issue's acceptance criteria are complete.
