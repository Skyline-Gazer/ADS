# Optional profile: strict Git governance

**Not part of lite adoption.** Enable only when the project `AGENTS.md` lists this profile.

When enabled, the consumer follows [docs/git-governance.md](../../docs/git-governance.md): `dev` integration branch, Issue-linked task branches, PRs to `dev`, separate release promotion.

Optional automation (copy via reviewable PR when the owner wants it):

- [templates/git-governance/ensure-ads-branch-protection.py](../../templates/git-governance/ensure-ads-branch-protection.py) → `scripts/ensure-ads-branch-protection.py`
- [templates/git-governance/check_git_governance.py](../../templates/git-governance/check_git_governance.py) → consumer `scripts/` if CI should enforce PR rules

Inspect real CI job names before passing `--required-check`. A `403` from `gh` is an access/plan blocker, not proof that protection is absent.
