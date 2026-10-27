# ADS v0.4.1 CNB variant

This opt-in branch implements the Owner's [Issue #63](https://github.com/Skyline-Gazer/ADS/issues/63) scope without changing immutable generic v0.4.1 (`3abf6025657a5d716476029cc8cbf5239543210b`), generic dev/main or existing Consumer pins. Source CI and native acceptance are separate. Do not declare the variant generally available from unit tests.

## Branch and authority

Only this variant uses `cnb/v0.4.1` → feat/cnb-*, fix/cnb-*, ci/cnb-* or test/cnb-* → reviewed PR to cnb/v0.4.1. Its workflow explicitly validates that integration target. Generic ADS keeps ordinary dev-based governance. Import generic corrections through reviewed history-preserving changes; never synchronize variant work automatically into generic dev/main. Consumers pin the verified immutable integration commit after their own adoption PR, never this floating branch.

Schema v1, [the existing provider example](../templates/git-provider/.ads-project.json.example) and [Mode A's adapter](../scripts/sync_cnb_release.py) remain compatible. Mode A means CNB owns production main and the exact approved tags, with a forward-only GitHub mirror. It is not Mode B.

Schema v2 [Mode B policy](../templates/git-provider/mode-b.json.example) separates CNB development, GitHub release and Issue authority. Its zero App IDs are deliberate invalid placeholders: replace them with independently observed trusted Greptile and deterministic-CI App/check identities. Execution defaults off. The [Mode B adapter](../scripts/cnb_release_gate.py) imports only the frozen clean preparation SHA to release/cnb-FULL_SHA, then copies only an already approved GitHub release and its exact annotated tag back to CNB. It never merges PRs, approves releases or creates tags.

## Consumer adoption and release

Bootstrap/Adopt must inspect actual account/repository, Git import/default branch, quotas, CI, security, protected refs, existing secrets' scopes and deployment effects without revealing values. Keep GitHub Primary unless the Owner chooses another authority. New repository/import/native tests are distinct operations from production cutover. CodeGraph/full RTK policy, immutable pins and developer-only production boundaries remain unchanged.

For Mode B, cut a separate clean release-preparation branch from approved CNB dev. Retain developer integration continuously on CNB dev. The adapter checks native source/preparation refs, SHA/tree and actual production-tree guard before importing an unprotected exact-SHA transfer branch. Set the trusted controller's ADS_RELEASE_GATE_MODE to verified-mode-b only after native acceptance; generic governance otherwise continues rejecting release transfer branches into dev. Open reviewed merge-commit PRs transfer→GitHub dev and dev→main. No direct protected ref push is substituted for these PRs.

Run release checks on the exact evaluated candidate. The adapter reads the real GitHub merged release PR, main protection and the latest exact-candidate trusted Greptile/CI checks through authenticated gh API. Comments, scores, a spoofed check name, old successful check, PR-authored approval or ordinary plugin exit zero cannot approve a release. If the installed review service only reports against a source SHA rather than the required evaluated candidate, this gate stays BLOCKED until the native integration supplies that evidence.

Policy and approval files must come from the protected release controller outside the candidate checkout. Their location alone is not owner approval or cryptographic attestation: the controller must corroborate protected-environment approval, exact repositories, source/preparation SHA/tree, action, target ref, tag object/peeled target and permitted deployment effects. PR code must never choose these inputs or receive publication credentials.

The adapter's dry-run performs local fetch/read-only worktree inspection but no remote writes. Execution requires the already-authorized controller and enabled policy. Immediately reread native refs before writes; ordinary non-force refspecs obey provider protection. Interrupted branch-before-tag copy can resume idempotently; an exact existing release returns ALREADY_COPIED, while changed destination/tag/event direction blocks. Never roll back published refs automatically. Verify a reviewed CNB reconciliation merge includes release ancestry and preserves every declared developer path in that same merge. Actual build-output boundary checks remain required in Consumer CI.

## Quality and native receipts

Reuse [the current-SHA review gate](cnb-review.md), [review configuration](../templates/cnb-review/review.cnb.yml.example), official secret/SCA scanning, vulnerability/license deltas, retained SBOM and native source-only coverage. Scanner failure/unavailable output is not PASS. SCA publication requires a trusted event; secrets and SCA are enabled by platform defaults unless existing ignore/configuration disables them. Do not add broad ignores or treat sechook's summary as a scan.

[ALNILAM Draft #96](https://github.com/Skyline-Gazer/ALNILAM/pull/96) is the concrete Apache-2.0 Consumer implementation, preserving existing Shirone tests: frozen Playwright, 390/1440px, root/nested independently composed Site, maximal-session CLS with attribution, optional-integration mocks, source-only LCOV, three-run-per-page LHCI and expected-red browser/CLS/Lighthouse fixtures. Copying any source from that Consumer requires retaining its Apache-2.0 notices; this variant links the example rather than relicensing its files.

Use mandatory fatal attachment upload, actual native download/checksum, failure diagnostics and explicit TTL. End-stage cleanup is supplementary because CNB does not propagate end-stage failure to parent success. Verify post-container accessibility separately. Retain source/target/merge/Site identity, image digest, runtime, elapsed time, invocation counts and quota deltas. Lab CLS is not field p75.

Code-review output uses the official status/issues schema. Fresh output is run-owned and must not be supplied by a PR. Bind source, target and evaluated merge; reread native refs after review. NPC stays default read/comment mode; never enable “替我上班”. For automatic npc:go on high-risk/release changes, select an event whose native token is read-only, cap turns/time, suppress duplicate source/target/merge identities and cancel after bounded failure. Prompt text is not permission isolation. Never expose release/mirror secrets to NPC or scanners.

Agent Fix accepts genuine current review evidence, verifies each finding, fixes and pushes serially, invalidates the old result, and reruns native required checks. Stop after at most three cycles. Missing/forged JSON, stale refs, unknown severity, unauthorized warning disposition, NPC timeout and exhaustion must block. Local fixtures do not establish that native loop.

Official git-auto-tag defaults to a write. In isolated acceptance set dryRun true and blockWhenFail true first; inspect branch, computed version, exact target and approved tag allowlist before permitting an isolated real event. Never attach it to ordinary Consumer PR/dev pushes. Repeated/conflicting tags, interruption and unauthorized manifests need native evidence. Keep optional title/commit linters, cache and notifications disabled until measured value justifies them.

Both provider modes need distinct real receipts. The selected full mode additionally needs two consecutive genuine cross-platform release rounds, branch protection, fresh review, exact tag identity and recovery. Bare-Git tests are supplementary. Missing native permissions, App installation or quota creates an explicit BLOCKED gate, not authorization to broaden access or use paid resources. See [service exit](cnb-service-exit.md).
