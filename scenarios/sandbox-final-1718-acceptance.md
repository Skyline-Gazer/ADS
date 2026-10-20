# Issues #17/#18 — isolated Sandbox final acceptance

Run: 2026-10-20, Asia/Shanghai. **ADS_BASELINE_SHA:** `c24d0b8edc1e56ee4464d107c5257722c3683a8f`.
This is a new live trial; the [historical PARTIAL report](issues-17-18-native-acceptance.md) and its evidence remain unchanged.

| Decision | Result | Meaning |
| --- | --- | --- |
| ISSUE_17_RESULT | **PASS** | Actual Project drift, acceptance-backed closure, false Done/security hold, false Open, draft scope repair and independent reread verified in the authorized fixtures |
| ISSUE_18_RESULT | **PARTIAL** | Remote install/upgrade PRs, local lifecycle, native discovery, consumer tests and recovery verified; hosted private submodule checkout fails |
| FINAL_DECISION | **PARTIAL / HOLD for #18** | Recommend owner closure of #17 after reviewing this evidence; keep #18 open. Do not merge the ADS report PR or release ADS |

## Scope, tools and evidence

Only [ADS-Acceptance-Sandbox](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox), Sandbox Issues #1/#2/#3 and this run's four [Project #9](https://github.com/orgs/Skyline-Gazer/projects/9) Items were mutated. ADS receives only this task-branch report PR. Neither official Issue was closed by this run. The final independent read shows ADS main still at the fixed baseline and #17/#18 both OPEN. No KIRARI, AiringCal, Project 1, credentials, organization Secrets, production or release operation was performed.

Read the baseline's milestone/update guides, both corresponding scenarios, STANDARD, SAFETY, QUALITY and adopt/deliver/recover Skills. Reused Git, authenticated `gh`, Python unittest and **Codex CLI 0.163.0**. Native discovery uses the documented [repository skill locations](https://learn.chatgpt.com/docs/build-skills) and [app-server skills/list](https://learn.chatgpt.com/docs/app-server). A real read-only, ephemeral `codex exec` turn also loaded the consumer's deliver Skill, read its local rules, checked the rollback pin and passed its three tests. The whole GitHub exercise was driven by this host agent using Git/gh and temporary evidence helpers; it was not all delegated to that CLI smoke turn.

Durable evidence: [directory](evidence/sandbox-final-1718-2026-10-20/README.md), [summary](evidence/sandbox-final-1718-2026-10-20/summary.json), [full redacted command/API/CI archive](evidence/sandbox-final-1718-2026-10-20/evidence.redacted.tar.gz), [SHA256SUMS](evidence/sandbox-final-1718-2026-10-20/SHA256SUMS). The archive has a second internal SHA-256 manifest, inert operator source, command arguments/exits and native CLI events. Paths/emails are redacted; stable IDs, full SHAs and exact errors are preserved. This is evidence, not a new ADS runner, tracker or scheduler.

## Phase A — Project convergence

**PROJECT_ID:** `PVT_kwDOEwGMMc4Bn1h-`. GraphQL discovered 13 fields, all options and all Items; pagination was exhausted. The Project initially had **zero Items**, so no pre-existing unrelated Item was changed. Only the following four created IDs were admitted to the mutation helper.

Status field: `PVTSSF_lADOEwGMMc4Bn1h-zhmYUtk`. Discovered options: Todo `f75ad846`, In Progress `47fc9ee4`, Done `98236657`. There is no Blocked option; unresolved work uses the actual Todo option. No field/option configuration was changed or copied from a different Project.

| Fixture / stable Project Item ID | Initial state after addition | Drift actually observed | Final independently read state |
| --- | --- | --- | --- |
| #1 `PVTI_lADOEwGMMc4Bn1h-zhCAgcI` | Todo / OPEN | PR creation corresponded to In Progress; merged PR automatically closed Issue while Project stayed In Progress | **Done / CLOSED** |
| #2 `PVTI_lADOEwGMMc4Bn1h-zhCAgdM` | Todo / OPEN | Injected Done / OPEN despite unresolved security; later observed **Done / CLOSED** while safety CI failed | **Todo / OPEN** |
| #3 `PVTI_lADOEwGMMc4Bn1h-zhCAgeQ` | Todo / OPEN | Distinct task merged with passing CI, deliberately still Todo / OPEN | **Done / CLOSED** |
| Draft `PVTI_lADOEwGMMc4Bn1h-zhCAgfQ` | Todo / no Issue | Injected stale completed-#1 scope while actual dependency was unresolved #2 | **Todo / no Issue**, corrected canonical dependency; same Item and draft content IDs |

The draft content ID is `DI_lADOEwGMMc4Bn1h-zgLbEx8`. It was updated in place and was neither converted to an Issue, deleted, archived nor marked Done. This exercises stale-scope repair; it is not a split-Issue or parent/child topology test.

For #1, [PR #4](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/pull/4) added a regression proving independent health response objects without changing the public schema. Its explicit `Closes #1` exercised real GitHub automatic Issue closure. Closure alone was insufficient: merged state, actual merge commit and its main CI were checked before setting Project Done.

For #3, [PR #5](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/pull/5) added a separate JSON round-trip contract test. Its overlap with #4 was resolved by an ordinary merge preserving both tests; updated-head CI passed before merging. The subsequent snapshot proves merged code with Issue OPEN and Project Todo. Only then were completion and closure reconciled.

For #2, [PR #6](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/pull/6) contains an intentionally failing unresolved-security-acceptance assertion. Its [real hosted run](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39364685944) failed. It remains OPEN/unmerged; green unrelated PRs did not satisfy its gate. This is a synthetic missing security verdict, not a claim of a production vulnerability.

The Done mutation initially reread as OPEN, but the next read found #2 CLOSED. No agent close request for #2 preceded that observation. Its timeline records actor `markd3ng`, null commit ID; the sequence is consistent with Project automation, but the exact workflow/writer was not independently attributed. The agent changed **only #2's test Item** to Todo, reopened #2 and queried both again. This transient false closure and its repair are retained rather than hidden behind the final OPEN state.

| PR | Final head SHA | Actual merge SHA | Hosted evidence |
| --- | --- | --- | --- |
| #4 | `18451fec6dd78695d290d06d7be975013112e397` | `97f492060062aba2a9294a78a811a7a325ab1d44` | [PR CI](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39364674562) and [merge CI](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39364830858) passed |
| #5 | `23228827f5325377a0ba4caf8558ffef40d2ee53` | `d3ec6db3189db85f74a8963fc6360a5f960ba275` | [updated-head CI](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39364842743) and [merge CI](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39364902641) passed |
| #6 | `6ce07b781e89d7e325fa9bdd8db4a50df4b7902b` | **Unmerged** | Intended security-negative failure; no completion classification |

The API's pre-merge `merge_commit_sha` can identify a temporary test merge. The table uses post-merge facts. Raw pre-merge values and Actions checkout logs remain in the archive; they were not substituted for actual merged commits.

Classification: #1/#3 **DONE_VERIFIED**, #2 **OPEN_VALID** after **STATUS_DRIFT/EVIDENCE_GAP** repair, Draft **OPEN_VALID** after **SCOPE_DRIFT** repair. The intentionally unresolved negative fixture remains carried forward; it is not a blocker to exercising the independent submodule trial.

Snapshots: [before](evidence/sandbox-final-1718-2026-10-20/project-before.json), [injected](evidence/sandbox-final-1718-2026-10-20/project-injected.json), [false Done/closed](evidence/sandbox-final-1718-2026-10-20/project-false-done-closed.json), [false Open](evidence/sandbox-final-1718-2026-10-20/project-false-open.json), [after](evidence/sandbox-final-1718-2026-10-20/project-after.json). A [second independent GraphQL query](evidence/sandbox-final-1718-2026-10-20/project-independent-reread.json) used `node(id:)` and `fieldValueByName`, independently confirming all four IDs, actual options, Issue states and PR/main facts. **PROJECT_DRIFT_FOUND / REPAIRED / REREAD: YES / YES / YES.**

NOT TESTED: Project-specific missing-scope denial, renamed Status/custom-option layouts, split Issues and parent/child topology. Live field discovery, this board's different option set, Draft handling, actual writes, failed safety CI, PR auto-close and post-write independent reads were tested. #17 PASS is limited to the stated fixture acceptance and this environment; it is not universal Project-layout coverage.

## Phase B — remote consumer submodule lifecycle

**SUBMODULE_OLD_SHA:** `ed4a6118254dfa88b7ba957d8ffb4e2b2b3c0b2f` (remote published tag `v0.2`).
**SUBMODULE_NEW_SHA:** `c24d0b8edc1e56ee4464d107c5257722c3683a8f` (explicitly approved unreleased test candidate).

[Install PR #7](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/pull/7), head `626c65f7e0ab9102126654090141397ab472ce6d`, introduced `.gitmodules`, mode-160000 `.ads` gitlink, a concise root AGENTS.md and `.agents/skills/deliver` symlink targeting `../../.ads/skills/deliver`. The source URL is HTTPS without credentials. All guidance pointers resolve into actual checked-out submodule files, byte-compared against the pinned Git objects; the root keeps the Python schema, tests and isolated-resource limits authoritative.

The existing [PR contract CI](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39364987979) passed before the authorized Sandbox merge. Actual merge SHA: `d56db0b469792da9bc42a9a09b5a966d881b3945`; [main CI](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39365095358) passed. Its default `actions/checkout@v4` does **not** initialize submodules: green CI proves three Python consumer tests, not hosted ADS availability.

A fresh remote clone with recursive submodules succeeded using existing legitimate host access, matching the old gitlink and checked-out SHA. A subsequent ordinary `submodule update --init --recursive` preserved that old pin although remote ADS main was the newer candidate. Both release and main refs, actual upstream diff and all command exits are archived.

Reviewed the old/new STANDARD, SAFETY, QUALITY, Skills, templates and adoption/update guidance. The candidate adds environment-first reuse, scoped/delegated safety, native coordination, reconciliation and immutable update guidance; it remains unreleased. No fixture runtime API changed and no project-local deployment/security scope was widened. No scheduler, background update or mutable-main upgrade was installed.

[Upgrade PR #8](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/pull/8), head `79b5a4e6c8a2dbd67875502dcf14783222f993ca`, is a **new task branch from merged v0.2 main**. It changes only the gitlink, necessary root pin text and a directly relevant hosted guidance-checkout job. Local and second-checkout gitlinks, nested HEADs, guidance bytes, unchanged health source/test hashes and three consumer tests pass at the candidate. The PR remains **OPEN and unmerged**.

### What hosted CI actually executed

[Upgrade Actions run 39365129536](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/actions/runs/39365129536) is **FAILURE**:

| Job / step | Observed result |
| --- | --- |
| Existing `contract` job | SUCCESS; default checkout without submodules; all three Python health tests ran |
| New `guidance` checkout | FAILURE; `submodules: recursive` attempted an actual private ADS clone twice |
| Pin/actual-checkout/Skill-path assertions | SKIPPED after checkout failure |
| Consumer tests with materialized guidance | SKIPPED after checkout failure |

Exact failure: `remote: Repository not found.` and `fatal: repository 'https://github.com/Skyline-Gazer/ADS.git/' not found`. ADS privacy was independently read as true. This proves default hosted checkout access is insufficient in this environment, not that the repository does not exist. No organization Secrets, credentials, token scope or access policy was changed. The failed job and skipped steps remain visible; no gate was disabled to make it green.

The job checked GitHub's temporary PR merge ref `dde382002e3a6854f50c17d700c2a796458309ee`; that is not an actual merged upgrade. `actions/checkout@v4` internally uses a force flag in its fresh runner. No agent operation forced or cleaned a dirty local consumer.

### Native discovery, negative cases and rollback

| Acceptance | Observed evidence / result |
| --- | --- |
| Native Skill discovery | CLI `app-server` `skills/list` reports one enabled repo deliver Skill after install, upgrade, rollback and each replay. It resolves through the committed symlink; full file content was read and hashed. An unrelated negative directory has no repo deliver Skill |
| Skill identity | Old/rollback SHA-256 `1e0c5c93bc44272ebc3fdf4f62990cb28d9c48d87c85d0284ed7ae63dfb0799f`; candidate `55ed390a5db0a8b23d494f29912de2039b508441c7790ee40d450c80bd02c874` |
| Actual CLI turn | Read-only ephemeral `codex exec` loads the rollback consumer Skill and local rules, proves HEAD/index gitlinks equal nested old HEAD, passes three tests, and reports clean parent/nested status; exit 0 |
| Dirty guard | Both parent and tracked/untracked nested changes injected; classification DIRTY before any checkout. Before/after status, HEAD and all dirty-file hashes match. Only the exact test-owned bytes were restored afterward; no force/clean |
| Missing target | Actual Git lookup of an absent full SHA fails, classified UNKNOWN; no checkout or pin change |
| Incompatible update | Synthetic release-only consumer rejects the unreleased candidate with failing assertion/HOLD. No actual application incompatibility is claimed |
| Recovery | A new ordinary rollback commit restores the old gitlink, root AGENTS.md and update-added workflow changes. Upgrade remains an ancestor; rollback tree equals consumer main; no published history rewrite |
| Second rollback checkout | Fetch rollback branch, sync/update submodules; actual nested SHA returns to old pin; contract and native Skill checks pass |
| Trigger | Explicit owner request exercised. Recurring scheduler/task-start/automatic Phase trigger NOT TESTED; none was configured |

Rollback commit: [`08c3be7c667a1551f7e74f3e5e670b9430390e26`](https://github.com/Skyline-Gazer/ADS-Acceptance-Sandbox/commit/08c3be7c667a1551f7e74f3e5e670b9430390e26), preserved on `test/ads-update-rollback`. Consumer main stays at merged v0.2 install `d56db0b469792da9bc42a9a09b5a966d881b3945`. Local recovery success does not remove the hosted private-access blocker. **Keep #18 OPEN/HOLD.** Successful hosted recursive checkout and the subsequent checks require a separate owner decision on legitimate CI read access; this run did not expand its authority to provide that access.

## Phase C — integrity, deviations and delivery boundary

Historical PARTIAL records and protocol NOT TESTED labels are preserved; this report adds a dated result. The ADS change is only this report, its evidence and the scenario-index link. ADS main is not edited directly, the report PR must remain unmerged, and no release is created.

The host reported saving command-prefix approvals. Actual selected-file comparison confirms `config.toml` is unchanged (`756c6de2a4f1453f901577caafd394e632882b4edf23c51331fcf5bb19c45295`); `default.rules` changed from `e2015d98899d4533026bce54262abac8ca7aabc8793db5abf4d8ca0a6f87d4ce` to `d287c3fb38dc3dff7f7af40cce0e677a6925d95d1974034203d4e1f2beec4221`, adding five host-saved prefixes. The [exact redacted diff](evidence/sandbox-final-1718-2026-10-20/host-policy-delta.json) is retained; it was not silently restored. Native discovery calls and the actual CLI turn have unchanged policy hashes within their execution windows. This selected-file audit does not prove the whole host filesystem was write-free.

[Execution deviations](evidence/sandbox-final-1718-2026-10-20/execution-deviations.json) retain the initial old checkout, sandbox network/.git restrictions and approved retries, temporary helper naming failure before any API call, log-escape capture failure/retry, ordinary test merge conflict, transient #2 closure and its attribution limit, synthetic negative limits, and the native read-only sandbox's denied xcrun cache writes. All CLI verification commands still exited zero; warnings are not hidden.

Local ADS validation uses the existing checker for Markdown links, relative paths and Skill frontmatter, its 30 existing unit tests, staged whitespace checks and both evidence manifests. Consumer tests, actual remote CI and real Project writes are separate evidence classes; passing report/documentation CI cannot satisfy #18's remaining integration acceptance. At initial delivery of [report PR #23](https://github.com/Skyline-Gazer/ADS/pull/23), both the Actions run query and PR/check-run queries returned no hosted report checks: **NOT OBSERVED, not PASS**. The captured head and query time are retained in the evidence; consult the PR for any later delivery checks. No extra workflow dispatch or workflow change was made in ADS.

Remaining unverified boundaries: successful hosted materialization of private ADS and following checks; the specific optional Project scenarios listed above; other agents/versions and production. Final decision: **#17 acceptance supported; #18 PARTIAL; overall HOLD for dependent #18 work.**
