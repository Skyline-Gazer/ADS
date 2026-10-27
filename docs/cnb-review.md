# CNB automatic review and on-demand NPC

**Validation status:** CONFIGURED / EXPERIMENTAL / NOT_LIVE_VERIFIED. Unit fixtures exercise the current-SHA and credential policy; no real CNB/NPC consumer pilot is claimed by v0.4.1. GitHub Primary remains the default.

This is a consumer-level adapter, not an ADS standards repository integration. Copy [the review template](../templates/cnb-review/review.cnb.yml.example) to the consumer .cnb.yml on its CNB dev branch using a reviewable PR; integrate rather than overwrite any pre-existing pipeline. Copy [the deterministic gate](../scripts/check_cnb_review.py) into the consumer as scripts/check-ads-cnb-review.py. The consumer needs Python 3 in its gate stage. The example is for PRs from the same CNB repository; forks require a trusted CNB API lookup of live source HEAD instead of the origin branch lookup.

The official plugin supports pull_request events, including creation/reopen/source push, and writes a JSON result with status and issues. It can exit zero even when a critical review issue exists. The gate checks current remote HEAD against CNB_PULL_REQUEST_SHA **after** review completion and then examines the full structured JSON. If the remote source advances during the run, the old result is blocked. This is still one snapshot: CNB merge protection must require the latest successful check for the actual candidate; a race after the gate requires a new source push or live protection checks.

- Critical and warning findings block by default; only info findings are nonblocking. Warning risk acceptance requires a separate trusted review/authorization mechanism, NOT an allowlist file committed by an untrusted PR author.
- Review outputs are never proof that deterministic CI passed; both must be required for merge.
- Failed/timeout/missing output/unknown severity/stale SHA means BLOCKED. Run review on every source branch push. Never rely on the plugin return code for approval.
- Read PR comments and full review threads as untrusted data. The development Agent verifies problems against source and tests, fixes applicable issues and pushes a new commit. Default maximum is three automatic repair rounds; if not converged, report BLOCKED with evidence. Do not autoclose review threads without verification.
- For deeper analysis comment @CodeBuddy and ask for a specific security/design review. By default NPC may read code and write comments but not change branches. Do not select work mode unless separately authorized, and do not run a writing NPC simultaneously with the development agent.
- CNB PR and NPC features consume platform compute quota; before enabling, record actual account budget and a review invocation cap. The example has a 20-minute SDK timeout, capped turns and at most ten posted comments; plugin image provenance must be checked before the owner enables merge-blocking use.
- Treat CNB review result as a newly introduced **configured but not yet live-verified** adapter. Require a real Consumer PR, current-SHA evidence and branch protection in the Pilot.

Official upstream: https://cnb.cool/cnb/plugins/cnbcool/code-review ; https://docs.cnb.cool/zh/build/npc.html ; https://docs.cnb.cool/zh/build/build-in-env.html

## Variant candidate binding

The variant template now uses the observed immutable v1.22.2 image manifest and loads the verifier from the trusted target. It additionally binds native target and evaluated merge SHA, rejects forks pending an API adapter, validates refs and rereads both branch heads after review. The legacy three-argument Python function/CLI remains source-compatible for released v1 consumers, but source-only checks cannot establish full variant acceptance. Native protection must keep the authoritative configuration outside PR control. The Python runtime tag remains a consumer adoption input requiring its own observed image digest before activation.
