# CNB to GitHub safe release mirror

**Opt-in only; never installed as a default ADS pipeline.** The consumer's CNB dev and PR process is authoritative. Its GitHub mirror accepts only production main and an exact, approved release tag. No dev, feature, PR, or unapproved tag refs are pushed.

## Release manifest and preflight

Use [the release example](../templates/cnb-sync/release-approval.json.example) as a template for a new, separately reviewed **per-release** approval record. Set both approvals only after the owner reviewed production and push-triggered deployment effects. Obtain source main SHA and tag peeled target from actual immutable commits; verify the consumer production-boundary guard has passed against the exact release candidate. The example intentionally defaults to false and invalid placeholders.

Copy [the sync script](../scripts/sync_cnb_release.py) into a trusted release checkout as scripts/ads-sync-github.py (Python 3, git, authenticated named remotes). Run it in the **CNB main** checkout with remote origin pointing to authoritative CNB and a separate remote github pointing to the target mirror. Use protected non-printing credentials; avoid putting tokens in remote URLs, manifests or logs. Keep the mirror sync action outside PR/NPC execution contexts.

Dry-run preflight:

    python3 scripts/ads-sync-github.py --manifest APPROVED_MANIFEST.json

After the owner grants production authorization and the actual GitHub main/tag, CI, branch protections, deployment triggers and credential scope are checked, execute explicitly:

    python3 scripts/ads-sync-github.py --manifest APPROVED_MANIFEST.json --execute

The script fails closed unless CNB remote main equals approved main SHA, the CNB tag object equals local approved tag object, tag peeled commit matches approval, and GitHub existing main is an ancestor of the approved main. It rejects missing GitHub main (requires separately approved bootstrap), divergent GitHub history, tag collision, invalid tags, force-push or reverse-sync. It never writes dev or feature branches and never replaces existing tags. It verifies remote main before tag publishing and verifies both refs afterwards.

Main push and tag push are not atomic. If the connection fails between them, status is PARTIAL, **no remote rollback or force update occurs**, and the next approved run re-reads both refs and resumes safely. Do not claim the operation succeeded based on exit code alone; record actual source and destination SHAs and deployment status. GitHub Release creation remains a separate project-specific action and is not implied by pushing the Git tag.

The official CNB tencentcom/git-sync plugin can push a single branch with branch: main, force: false, push_tags: false. However omitting branch pushes ALL branches, and enabling push_tags pushes more tags than this release policy authorizes. Therefore this adapter uses explicit refspecs for main and one release tag, and intentionally does **not** install a generic auto-sync-on-every-push plugin. CNB review/plugin scopes must not read the GitHub mirror token.

Official documentation: https://cnb.cool/cnb/plugins/tencentcom/git-sync

## Acceptance and deployment boundaries

- Verify GitHub main SHAs/immutable tags after sync, not merely CNB pipeline green.
- Test isolated bare Git repositories first; then test a real CNB Consumer and isolated GitHub repository with credential/protection checks.
- Inspect GitHub Actions/Pages/Vercel deploy triggers before authorization. A main mirror update can cause live deployment even if GitHub is described as read-only.
- Never add GitHub token to CNB PR or NPC job, code, manifest, URL, or logging.
- If GitHub private plan does not support protection or integration returns 403, report the actual limitation; do not mark hard protection verified.
