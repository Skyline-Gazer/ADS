# CNB Development + GitHub Release Gate pilot

**DRAFT / NOT_READY.** Follow-up to [Issue #63](https://github.com/Skyline-Gazer/ADS/issues/63), evaluated during [ALNILAM P0 #85](https://github.com/Skyline-Gazer/ALNILAM/pull/85). This is a proposed governance extension and safety correction, not an available provider mode, live-platform PASS or part of released ADS v0.4.

## Evidence and incompatibility

Stable v0.4 is `2af17d9e1d816844c49835ae91b784405765ad46`. Candidate `13c50f072d3f2b6aa95ca7387a8cff3dc0b606a1` includes #64/#65/#66: provider schema, current-source-SHA review and bounded forward main/tag mirror. The candidate's `check_repository_provider.py` only accepts GitHub Primary or CNB Primary + GitHub Mirror. `sync_cnb_release.py` writes CNB-authoritative main to GitHub main. Neither implements the authority direction below. Keep both modes and their rejection semantics intact.

ALNILAM GitHub dev/main have active PR-only, non-fast-forward-protected rulesets, required `verify`, and no bypass actor. Direct mirror pushes to either protected branch are incompatible. A failing mirror cannot be repaired with forced pushes, bypass credentials, disabled checks or branch protection removal.

## Proposed authorities and sequence

CNB dev owns daily integration. GitHub Issues/Project retain product tracking. GitHub dev owns release-candidate integration, GitHub main the sole production release authority, CNB main the read-only published-release copy. Greptile independently reviews GitHub release PRs; it does not replace CNB daily review.

1. CNB task branch -> PR -> dev: automatic review, on-demand read-only NPC, at most three serial fix rounds, native CI and review bound to the current source SHA. Never expose mirror credentials to PR/NPC jobs.
2. Create an independent release-preparation branch from the approved CNB dev SHA; remove dev-only configuration only there. CNB dev continuously retains its development configuration. Do not merge these removals into dev. Freeze the clean branch SHA and rerun production-boundary checks; no source mutation after freeze.
3. Import that SHA only into a nonprotected GitHub `release/cnb-<full-SHA>` transfer branch. A reviewed **merge commit** PR joins GitHub dev. A separate reviewed **merge commit** dev -> main PR requires CI, security/license/boundary evidence, current-SHA Greptile and explicit Owner release approval. Squash/rebase would sever the ancestry expected by this pilot and is not allowed for these transfers.
4. Copy the exact GitHub release SHA and each explicitly approved annotated tag object to CNB main with ordinary fast-forward explicit ref updates. Reread both providers before and after a write, reject drift/divergence/tag collision, and make interrupted retry idempotent. Preserve exact tag object and peeled target. Never push wildcard tags or mirror every ref.
5. Reconcile the published GitHub release into CNB dev through a reviewed merge PR before the next cycle. Its merge result must preserve dev-only paths from the pre-merge dev tree while retaining published-release ancestry. Do not delete tooling from dev and restore it in a later commit; only each independent release-preparation branch strips it.
6. Configure explicit one-way events: CNB dev review never triggers production-copy, GitHub approved release-copy never re-triggers candidate import, and CNB release-copy/reconciliation never republishes. Store an immutable processed release identity and reject duplicate or stale events. No automatic bidirectional sync is authorized.

## Required schema / implementation before activation

A separate versioned provider mode must represent development, issue and release authority independently; explicit transfer prefixes; production branches; both native review/check identities; max fix rounds; no-force policy; processed-release identity; exact approved source/tag; and deploy effects. Keep old mirror schema backward compatible. Do not simply set CNB primary with a reverse mirror direction.

Separate trusted import and release-copy adapters need dry-run by default, explicit apply authorization, validated canonical repositories, least-privilege credentials, protected trusted policy, source/destination rereads, ancestry checks and fail-closed recovery. Review evidence must identify the true trusted App and current candidate SHA; PR-authored JSON is insufficient. Greptile comments/score cannot substitute for a deterministic required check.

**Unresolved native protection decision:** if CNB only allows merge commits into protected main, its main SHA will differ from the GitHub release SHA. Exact-copy cannot be claimed then. Choose a verified native fast-forward-only copy mechanism or explicitly model the extra commit and downstream reconciliation; do not grant an unreviewed bypass.

## Acceptance oracle and current results

ALNILAM's historical `scripts/tests/release_dag_test.py` executes two consecutive rounds with two local bare remotes: feature/preparation/import/release/reconcile merge ancestry, frozen/release tree equality, actual production-boundary guard, exact annotated tag identity, repeated-copy idempotence, interruption between branch/tag, rejected backward branch update and rejected tag replacement. That historical fixture deleted/restored development configuration on dev; it is not the lifecycle specified here and must not be treated as this mode's acceptance. Its result is **offline Git mechanics PASS only**. It does not execute ADS's existing mirror script, platform review, native branch protection, credential containment or event-loop controls.

Before enabling this mode, independently rerun that oracle against new adapters and a specifically authorized isolated CNB/GitHub repository pair. Add stale-review/source-drift, untrusted-policy, force/tag collision, interrupted writes, retry limits, pipeline-loop, unauthorized-credential and two-round/no-reimport negative cases. Verify both production trees contain no dev tooling. Compare Tree and Commit SHAs with explicit explanations. Keep every real-platform item NOT_RUN/BLOCKED until observed.

Greptile App installation, paid plans, secret provisioning, IAM changes, production Rulesets and provider cutover each retain their own Owner authorization boundary. No P0 evidence or green CI implies cutover approval.

## Version-title correction

Released v0.4's STANDARD/SAFETY/QUALITY headers still said 0.3 candidate. Correct only this development branch's headers; never move or rewrite the v0.4 tag. Consumers continue pinning the released commit until a separately reviewed upgrade.

## Dedicated variant source implementation — 2026-10-27

The Owner-authorized [CNB variant](cnb-variant.md) now provides a separate schema v2 and import/publication adapter with supplementary two-round bare-Git tests. The earlier draft remains historical design evidence. This does not make generic v0.4.1 Mode B-capable, prove native branch protection/review, or authorize Consumer cutover. Native acceptance is still separately required.
