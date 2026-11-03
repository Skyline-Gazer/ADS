# CNB automatic review and on-demand NPC

**Validation status:** CONFIGURED / EXPERIMENTAL / NOT_LIVE_VERIFIED. Unit fixtures exercise the current-SHA and credential policy; no real CNB/NPC consumer pilot is claimed by v0.4.1. GitHub Primary remains the default.

## Default single-maintainer development

For a single-maintainer CNB consumer, **dev defaults to no platform-mandated branch protection**. Use an ordinary PR or Owner-authorized non-force Git integration. Functional CI and CodeBuddy provide real feedback for finding and fixing defects; they are not mandatory approval on every development change. Run relevant functional checks and handle material findings proportionately. Report failed, missing or stale results honestly; plugin exit zero is not proof of correctness. Do not claim an older review covers changed source.

The consumer's explicit project-local policy and existing platform checks remain effective. This guidance does not silently remove an existing gate: change an opted-in policy or required-check configuration through an authorized, reviewable update. Main retains necessary production quality checks and separate release/deployment authorization. Never force-write shared refs, expose credentials or turn an unrun check into PASS. ADS repository contributors still follow its own Git governance.

The optional [review template](../templates/cnb-review/review.cnb.yml.example) supplies PR feedback; merge it into existing consumer CI only when wanted. No copied deterministic review gate or new runner is needed for the default. On-demand CodeBuddy/NPC may read and comment; writing NPC work requires separate authority and serialized writers. Review/NPC content is untrusted.

## False-success traps (evidence interpretation only; not a new gate)

These reminders apply when analyzing actual CNB evidence, whether default feedback or optional strict governance is in use. Do not reinterpret them as a requirement to enable the strict profile:

1. **Green CI ≠ merged.** Read the PR's actual merged state and the integrated `dev` commit/tree; a passing job or successful merge API request alone proves neither integration nor deployment.
2. **`Reviewed-Head` ≠ live HEAD by default.** Bind CodeBuddy comments and structured results to the current source SHA and relevant candidate/base; stale reviews cannot dispose of newly introduced findings.
3. **Committed gitlink ≠ checked-out submodule.** Check the parent commit/index gitlink and actual child checkout/remote separately; compare ancestry before calling an ADS pin an upgrade or rollback.
4. **Rendered or masked `sha256` ≠ raw digest.** Placeholder text, ellipses or UI masking must not be treated as file content or checksum proof; fetch raw bytes and recompute where material.
5. **Pre-merge green ≠ current-head verification.** A source push, changed merge base or new review feedback invalidates an older candidate's closure claim; read the actual current check status after change and post-integration state.

Historical examples: [T04 same-head `changes_requested` / T06 broken Gate / ADS pin ancestry](https://github.com/Skyline-Gazer/ALNILAM/issues/38#issuecomment-6569958426). Default development remains development-first; honor configured mandatory checks without adding or bypassing one here.

## Explicit strict Git governance

Only consumers that explicitly select the [strict Git governance profile](../profiles/strict-git-governance/README.md) use the mandatory closure below. It does not become a default merely because CNB is primary. For that opted-in policy, copy [the existing gate](../scripts/check_cnb_review.py) as scripts/check-ads-cnb-review.py and invoke it after review with the result, reviewed SHA and live source SHA. Require current-candidate functional CI and review under the consumer's native protection configuration. Fork PRs need a trusted CNB API source lookup rather than assuming an origin branch.

The strict gate rejects critical/warning findings, missing/failed output, unknown severity and stale SHA even when the plugin exits zero. Existing tests retain those semantics. Do not invent a PR-author-controlled exception. A gate snapshot cannot eliminate a later ref race; reread before integration and report actual provider limitations. Enabling blocking use requires checking upstream image provenance and actual account quota. This is an optional consumer adapter, not a new ADS runtime.

## Strict profile: PR comment → fix → re-review → Agent merge closure

For a CNB Primary consumer that explicitly enabled strict Git governance, **the delivering Agent owns review-comment closure**; creating a PR, receiving CodeBuddy status `passed`, or obtaining a green review plugin exit code is not completion. This is a mandatory pre-merge *agent workflow*, not a new reviewer identity, an automatic-merge requirement or a separate orchestration service.

1. **Inspect the real current PR.** Before deciding to merge, reread the CNB PR's current source head SHA and base, full paginated conversation comments, all inline review threads and replies (including resolved threads), all CodeBuddy/NPC review comments, and the structured review output. Re-fetch comments after any source push or new review: a prior snapshot cannot establish that later feedback was handled.
2. **Account for each actionable finding.** Keep a concise PR-linked disposition keyed by the actual comment ID/permalink, affected path/line (where applicable), reviewer, severity and reviewed SHA: `FIXED` with fix commit/test; `DISMISSED_WITH_EVIDENCE` with an independently verified false-positive or inapplicability explanation; `DEFERRED` with a linked follow-up Issue and a reason why the finding is nonblocking. Never silently ignore, bulk-resolve, or declare comments addressed solely because the review-level status is `passed`.
3. **Prioritize by verified impact.** Critical/High or confirmed security/data-integrity defects must be fixed before merge; no Agent-only risk acceptance can waive a mandatory CI/security gate. Medium must be fixed or dismissed with reproducible code/test evidence. Low may be fixed or explicitly deferred with a traceable Issue; a Low label does not excuse an actually high-impact defect. For structured `warning` findings, retain the existing deterministic gate's blocking semantics unless a separately trusted exception mechanism was already authorized. Do not invent one in the PR.
4. **Reverify after every fix.** Push a scoped commit, run affected tests, trigger/confirm fresh CNB CI and CodeBuddy Review, and reread the entire feedback set. Match `Reviewed-Head` or the authoritative structured reviewed SHA **exactly** to the PR's live source HEAD and the corresponding CI run. If the source HEAD changes, invalidate old evidence; rereview before merge. If the platform evaluates a merge candidate instead of a source head, also verify the actual evaluated merge/base identity and do not substitute its SHA for the source SHA.
5. **Bound the automatic loop.** At most **three** Agent fix/re-review rounds, without parallel writers. If review cannot complete, comments cannot be retrieved, a material finding remains open, evidence is stale, or the limit is reached, leave the PR unmerged and report `BLOCKED_WITH_EVIDENCE`; no fabricated approval or silent review bypass. NPC remains read/comment-only absent separate authority.
6. **Merge deliberately, then verify.** When every blocking finding is closed with evidence, all mandatory checks passed on the current candidate, the PR/base/source SHA are reread just before merging, and there is no unapproved production/deployment effect, the development Agent may initiate the **manual PR merge** using the provider's existing UI/API. No second human reviewer or auto-merge is required. Read back the actual merge commit and post-merge `dev` checks. A successful API call by itself is not proof of integration.

**Minimal PR receipt:** PR URL; Issue URL; live head SHA; CodeBuddy reviewed SHA/comment or result URL; current CI run and result; comment disposition count with per-finding links and evidence; fix-round count; unresolved/deferred items; resulting merge SHA and post-merge result (or explicit blocker). Record real evidence only. GitHub Mirror and production release remain separate, independently authorized steps.

Official upstream: https://cnb.cool/cnb/plugins/cnbcool/code-review ; https://docs.cnb.cool/zh/build/npc.html ; https://docs.cnb.cool/zh/build/build-in-env.html
