# CNB to GitHub safe release mirror

**Validation status:** LIVE_VERIFIED (isolated fixture, 2026-10-28) — real CNB protected `dev`/`main`, owner-approved fixture release `dev→main`, dry-run then authorized `--execute` mirror to a disposable GitHub target with exact SHA/tag readback; negative gates verified: non-ff/drift refusal, tag-collision refusal, unapproved-manifest refusal, credential/unreachable fail-closed, main-pushed/tag-failed recovery, idempotent re-run. See ADS Issue #63 for run evidence.

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


## Live acceptance findings (2026-10-28)

- **Empty-mirror bootstrap is fail-closed by design.** The sync refuses an uninitialized GitHub mirror (`missing GitHub main: bootstrap mirror separately with approval`). Bootstrap once by pushing the approved `main` SHA, then run the sync.
- **Mirror pushes trigger inherited workflows.** The mirrored `main` tree carries the consumer's `.github/workflows/`; GitHub fires them on every mirror push (observed live: `Deploy`/boundary workflows ran and failed on a fixture). Before enabling mirror writes, consumers MUST audit and disable/guard (paths, conditions, or `workflow_dispatch`-only) any workflow that deploys production — e.g. ALNILAM's `deploy.yml` triggers on `push` to `main` and deploys GitHub Pages.
- **Branch protection on the GitHub mirror:** the classic protection API is plan-gated for private repos (HTTP 403). Mirror write authorization therefore rests on token scope and owner identity unless the mirror repo is public or the plan supports protection. Record the actual state in the consumer's Mode A acceptance.

## Compatibility note: GitHub sync-branch PR vs exact-SHA mirror (NOT interchangeable)

ADS Mode A mirror (`sync_cnb_release.py`) requires **byte-identical commit SHA** on GitHub `main` (and approved tags) matching the authorized CNB production SHA. A consumer workflow that lands CNB production onto GitHub via a **`sync/*` (or similar) branch + ordinary GitHub PR merge** produces a **different merge commit SHA** on GitHub `main`. That path may be useful for PR/CI review on the mirror, but it is **not** the same as ADS exact-SHA mirror acceptance and must **not** be labeled LIVE_VERIFIED Mode A, PASS for `cnb-sync.md`, or a substitute for the manifest-driven sync.

- Do not rewrite this document to treat sync-branch PR merge as the approved Mode A mirror.
- Do not claim ALNILAM (or any consumer) has completed strict SHA mirror acceptance solely because a GitHub sync PR merged.
- Reconciling PR-merge SHAs with exact-SHA mirror policy is a **separate** mirror-system change; it is **out of scope** for ADS v0.5.0 Lite.

## Acceptance and deployment boundaries

- Verify GitHub main SHAs/immutable tags after sync, not merely CNB pipeline green.
- Test isolated bare Git repositories first; then test a real CNB Consumer and isolated GitHub repository with credential/protection checks.
- Inspect GitHub Actions/Pages/Vercel deploy triggers before authorization. A main mirror update can cause live deployment even if GitHub is described as read-only.
- Never add GitHub token to CNB PR or NPC job, code, manifest, URL, or logging.
- If GitHub private plan does not support protection or integration returns 403, report the actual limitation; do not mark hard protection verified.
