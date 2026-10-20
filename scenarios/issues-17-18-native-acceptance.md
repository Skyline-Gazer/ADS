# Issues #17 / #18 — AI-native integration acceptance

Run: 2026-10-20, Asia/Shanghai. Fixed ADS baseline and approved upgrade target: `b33b41f5c15c0ebac40e25882de81f0b383bc81b`. Refs [#17](https://github.com/Skyline-Gazer/ADS/issues/17), [#18](https://github.com/Skyline-Gazer/ADS/issues/18). **Both Issues remain unaccepted; dependent Phase: HOLD.** The existing closed state of #17 is a finding, not a passed acceptance.

| Item | Result | Verified boundary | Remaining acceptance |
| --- | --- | --- | --- |
| #17 Phase / Milestone reconciliation | **PARTIAL** | Actual Project v2 fields and all 33 items; ADS Issues, PR, exact main SHA and hosted CI; premature closure detected | Authorized isolated Project repair/closure/re-read; false Open/Done, failed-security and draft/split-item exercises |
| #18 submodule adoption / upgrade | **PARTIAL** | **PASS for local lifecycle:** actual private ADS source, two consumer checkouts, immutable gitlinks, native discovery, dirty/access/target failures and rollback | Remote isolated consumer upgrade PR and hosted consumer CI; whole-task no-global-write condition has a host-approval deviation |

The canonical protocols remain [Phase acceptance](phase-milestone-reconciliation.md) and [submodule acceptance](submodule-update.md). Their historical NOT TESTED labels are not rewritten into global PASS claims.

## Actual scope and authority

- GitHub repository read: private `Skyline-Gazer/ADS`; Issues #17/#18; merged PR #19; its head and merge-SHA check runs/Actions; current default-branch SHA.
- Project read only: [markd3ng Project 1](https://github.com/users/markd3ng/projects/1), ID `PVT_kwHODRFUbM4BlFsV`. Discovered 16 fields and 33 Issue items, with all requested connection pages exhausted. Queried IDs, types, archive flags, Issue states and field values, without unrelated Issue titles/bodies. Before/after Project response objects are identical.
- No isolated test Project was designated or granted write authority. No Project mutation or Issue state change was performed. An optional request for isolated-test authority received no grant during execution; the run continued within the read-only boundary. Production board identity was never treated as a test authorization.
- Local consumers only: `$RUN/consumer`, `$RUN/checkout`, `$RUN/private-checkout` and local bare `$RUN/consumer.git`, where `$RUN` was `/private/tmp/ads-1718-acceptance-C6V37r`. No real consumer project or remote consumer repository was modified. The original ADS checkout stayed on its existing clean task branch; report work uses a separate worktree/branch based on the fixed baseline.
- Reused installed Git, `gh` 2.102.0, Python 3.9.6 and Codex CLI 0.163.0. No dependency/runtime installation, credential inspection, credential rotation, deployment or recurring scheduler setup.

## #17: observed facts, classification and missing trials

Project GraphQL reads **succeeded**. ADS has zero repository-associated Projects, and #17/#18 have no Project items. Therefore **PROJECT_UNVERIFIED applies to the intended acceptance board**: its canonical isolated identity and write grant are missing. There was no API permission denial; reporting this as a missing-token or Projects-permission error would be inaccurate. A denied-Project-access negative trial was not performed.

The existing board's discovered Status field is `PVTSSF_lAHODRFUbM4BlFsVzhjz3Ow`; options were Todo (`bf63282d`), In Progress (`70fa65c2`), In Review (`07196ee1`), Blocked (`bfd7f099`) and Done (`bc11403b`). Other actual fields include Phase, Priority and Roadmap Status. These observed IDs were not used for mutations or assumed to apply to another board. All 33 observed items are Issues; there was no draft-item fixture.

| Classification | Actual observation and disposition |
| --- | --- |
| STATUS_DRIFT | #17 was CLOSED at `2026-10-20T02:10:09Z`; its close event identifies PR #19. PR #19's `closingIssuesReferences` still includes #17. Its body says neither Issue should close automatically, and #17's later comment explicitly says live Project work was not tested and the Issue should stay open. Closure is not supported by its acceptance evidence. |
| Scope / evidence coverage | PR #19 delivered normative guidance; #17 requires real drift repair and acceptance-backed closure. This deliverable/acceptance mismatch is recorded without shrinking #17's scope. It does **not** prove the separate outdated/split Project-item SCOPE_DRIFT scenario. |
| EVIDENCE_GAP | No authorized test item status write, correct closure, false Open repair, failed-CI/security false Done fixture, draft handling or post-write re-read. No DONE_VERIFIED classification is assigned to #17. |
| OPEN_VALID | #18 is OPEN with remaining remote consumer PR/CI acceptance. Local successes do not remove that boundary. |
| PROJECT_UNVERIFIED | Canonical isolated acceptance board and write authorization absent; actual existing-board read access is verified. |

PR #19 merged as the exact fixed baseline. Its head `3c08d04e5684151e79c192fe29e23d9a0bcfc47f` has successful [Validate ADS run 39357382242](https://github.com/Skyline-Gazer/ADS/actions/runs/39357382242); the merge SHA has successful [run 39357447498](https://github.com/Skyline-Gazer/ADS/actions/runs/39357447498). The workflow runs unit/documentation/Skill checks, not live Project mutation or consumer integration. Thus green CI does not fill the missing acceptance.

**Disposition:** do not recommend closing #17; its owner should reopen the premature closure until the missing trials pass. This run did not reopen it because Issue state mutation was restricted to authorized isolated test Issues. Existing Project states were unchanged. Before/after reads establish snapshot equality, not the absence of all possible intermediate external activity.

Evidence: [initial Project response](evidence/issues-17-18/production-project-readonly-page-1.json), [final response](evidence/issues-17-18/final-read/production-project-readonly-page-1.json), [close event](evidence/issues-17-18/issue-17-close-event.json), [PR closing references](evidence/issues-17-18/final-read/pr19-closing-references.json), [PR metadata](evidence/issues-17-18/pr-19.json), [final Issue #17](evidence/issues-17-18/final-read/issue-17.json), [summary](evidence/issues-17-18/acceptance-summary.json).

## #18: real local Git lifecycle

Published old pin `v0.2` resolved to `ed4a6118254dfa88b7ba957d8ffb4e2b2b3c0b2f`. The owner-approved candidate was the full fixed baseline above; approval for this trial does not make v0.3 a published release.

| Check | Result and directly observed evidence |
| --- | --- |
| Install and root references | HTTPS submodule add from the real private ADS repository succeeded using existing host access. `.gitmodules` contains the source URL without credentials. Root AGENTS.md pins the full SHA, points to the three rules and selected Skill, and states fixture tests/local-only delivery and operational limits. Referenced checked-out files were byte-compared to Git objects. |
| Recorded gitlink / checkout | `git ls-tree` records mode `160000` and the full old SHA. A second clone with recursive submodules checks out exactly that SHA. `submodule update --init --recursive` preserves it while fetched `origin/main` is the newer approved candidate. |
| Approved upgrade | Reviewed the actual upstream rule/Skill/template diff. On a consumer task branch only `.ads` and necessary AGENTS.md pin text change. The gitlink and nested HEAD both become the approved full SHA. A second checkout reproduces it. The fixture health contract stays identical and its test passes. |
| Native Skill discovery | Committed `.agents/skills/deliver` symlink resolves into `.ads`. Codex native `skills/list` returns enabled `scope=repo` after install, upgrade and rollback; an unrelated negative directory returns no repository deliver Skill. The indexed file was actually read and hashed: old/rollback `1e0c5c93bc44272ebc3fdf4f62990cb28d9c48d87c85d0284ed7ae63dfb0799f`; upgrade `55ed390a5db0a8b23d494f29912de2039b508441c7790ee40d450c80bd02c874`. This proves native indexing and full file readability, not a separate model turn executing every Skill instruction. |
| Dirty protection | Added both a tracked rule edit and an untracked nested file. The update check returns DIRTY before checkout; parent/nested status, HEAD and both dirty-file hashes remain identical. Restored only the driver's own injected bytes. This is an agent procedure rehearsal, not an ADS runtime guard. |
| Unavailable target | Real `cat-file` lookup of an absent 40-character target fails with exit 128; classified UNKNOWN with no checkout or pin change. |
| Incompatible proposal | Executed a negative compatibility assertion simulating a consumer that permits published releases only. The actual candidate README fails it with HOLD/exit 1. No merge occurs; old main pin and both history states remain. This tests a stated synthetic compatibility restriction, not an undiscovered real consumer conflict. |
| Private access failure | ADS privacy was independently read as `isPrivate=true`. A child Git process with isolated configuration/home, no credential helper and prompting disabled fails real HTTPS access, then an actual new consumer submodule initialization fails after Git's two clone attempts. Exact failure: `fatal: unable to get password from user`. Classified INACCESSIBLE; gitlink stays old and guidance is absent. Real credentials/global auth configuration were untouched. |
| Rollback | A new rollback commit restores the old gitlink and AGENTS.md without rewriting history. The second checkout runs submodule sync/update and returns to the exact old SHA. Both parent/nested worktrees are clean; contract tests pass; native Skill discovery returns the old content. |
| Update triggers | This explicit request caused the check. No scheduler, unattended remote update or auto-merge was configured. Actual scheduled execution and automatic Phase/task-start triggering were not tested. |
| Consumer PR / hosted CI | **NOT TESTED.** Consumer branches were pushed only to the local bare repository. The ADS evidence PR is not a consumer upgrade PR, and ADS documentation CI is not consumer CI. |

Consumer history is retained in the [Git bundle](evidence/issues-17-18/consumer.bundle), independently verified as complete:

| Checkpoint | Consumer commit | Recorded ADS gitlink |
| --- | --- | --- |
| Installed / local main | `416b72770715a166463e6f395730d8f37011f8e7` | `ed4a6118254dfa88b7ba957d8ffb4e2b2b3c0b2f` |
| Upgrade proposal | `30e0056bc544538e85a27fade933ac132008d4a1` | `b33b41f5c15c0ebac40e25882de81f0b383bc81b` |
| Rollback | `a9f96d36eb86a3912cffc3501374437ee40b83fe` | `ed4a6118254dfa88b7ba957d8ffb4e2b2b3c0b2f` |

The bundle contains consumer history only; materializing `.ads` still requires legitimate private ADS access. It contains no consumer `.git/config` or credential store.

Evidence: [105 lifecycle commands](evidence/issues-17-18/submodule-commands.json), [independent Git/content/contract checks](evidence/issues-17-18/independent-verification.json), [consumer proposal diff](evidence/issues-17-18/consumer-upgrade.json), [upstream guidance diff](evidence/issues-17-18/upstream-guidance.json), [native upgrade index](evidence/issues-17-18/upgraded-native.json), [dirty before](evidence/issues-17-18/dirty-before-git.json), [dirty after](evidence/issues-17-18/dirty-after-git.json), [private initialization failure](evidence/issues-17-18/private-submodule-failure.json), [lifecycle summary](evidence/issues-17-18/submodule-summary.json).

## Integrity, deviations and delivery checks

No agent command changed global configuration or credentials. Native app-server trust was an invocation-local configuration argument. Selected global policy files were hashed before/after the formal lifecycle and were identical. **The wider task was not globally write-free:** the host approval mechanism reported saving command allow rules; a later snapshot confirms `$USER_HOME/.codex/rules/default.rules` changed outside the formal lifecycle window. This tool-managed deviation is retained in [host policy delta](evidence/issues-17-18/host-approval-policy-delta.json); it is not attributed to an ADS rule or silently removed. These selected-file inventories are not a complete filesystem audit.

The safe source change is this report, its scenario-index pointer and evidence. No ADS executable, CLI, runner, scheduler, policy rewrite or automatic migration is added. No normative source defect was established; the concrete false-close defect is GitHub delivery metadata/state. No PR is merged and no release is proposed.

Local checks: ADS checker passes links/relative paths/Skill frontmatter/unsafe examples; all 30 existing unit tests pass; whitespace check and archived evidence SHA-256 verification pass. Consumer contract checks run at install, upgrade, replay and rollback, followed by independent Git/byte/contract verification. The first staged whitespace check flagged space-only context lines in raw patch artifacts; JSON wrapping now preserves the exact diff text without introducing whitespace errors. Its failed exit is retained in the evidence. Expected negative exits are preserved and never counted as successful commands. Hosted checks on the report PR are recorded separately in GitHub.

Durable evidence is [this directory](evidence/issues-17-18/), indexed by [SHA-256 manifest](evidence/issues-17-18/manifest.sha256). It contains redacted API responses, exact command exits, before/after states and [one-shot operator sources](evidence/issues-17-18/operator-sources.txt) as non-executable evidence. Personal home/temporary paths are replaced with `$USER_HOME`/`$RUN`; native IDs, source/consumer SHAs and exact errors remain. Raw working evidence and temporary drivers also remain locally under `$RUN`; temporary retention is not required to review the committed evidence.

Not verified: authorized Project writes/test Issue closure, denied-Project permission/draft/split-item cases, remote consumer PR/CI, separate model Skill execution, other hosts/versions and production behavior. **Keep #18 open; do not accept #17's existing closure.** Obtain a designated isolated Project and an explicitly authorized isolated remote consumer before completing those remaining acceptance criteria.
