# Lifecycle Drift Convergence & Remote-Heavy Execution

**Optional profile — not [lite adoption](lite-adoption.md).** Enable when project `AGENTS.md` lists [profiles/strict-lifecycle/README.md](../profiles/strict-lifecycle/README.md). Mandatory for contributors working **in the ADS repository**. Read [STANDARD](../STANDARD.md), [Phase reconciliation](milestone-reconciliation.md), [remote-first verification](../scenarios/remote-first-verification.md), and [Provider selection](git-provider.md).

## Execution placement: local-light, remote-heavy

At session/task recovery, read actual Provider, repository/branch SHA, remote CI/preview, CI triggers, production side effects, quotas, existing evidence and local sandbox. Prefer **existing authorized remote execution** before creating any new runner.

| Workload | Default executor | Local policy |
| --- | --- | --- |
| Editing, Git, formatting, short deterministic tests | Local or safe remote worktree | Allowed within actual read/write sandbox |
| Docker build / Compose E2E | Hosted CI / isolated runner | Heavy local fallback requires scoped exception + remote failure evidence |
| Chromium/Playwright, screenshots, CLS, Lighthouse | Hosted CI / isolated preview | Do not silently install local browsers or start heavy local services |
| SCA, full matrix, cross-platform E2E | Trusted CI / isolated target | Local mock is not real-platform acceptance |
| Staging/release | Authorized remote Provider | No implicit production access or provider switching |

**A Dockerfile or Compose recipe is a deployable product output, not proof that the Mac needs Docker.** Do not silently install Docker Desktop, launch its daemon, pull images or run heavyweight E2E locally when usable remote CI exists. Remote failure must be observed, not assumed; heavy local execution needs explicit task-scoped authorization and does not close remote-platform evidence gaps.

## Contract migrations: protect the gate without freezing an obsolete contract

When a consumer intentionally replaces an interface/schema (for example, Site TOML → YAML-only), first compare the accepted Issue and candidate schema against **both** the target-owned CI harness and the candidate tests. A target/base harness importing an obsolete business-contract implementation is **version skew**, not evidence that the candidate must restore deprecated support. Fix the smallest affected test/fixture path within the existing PR and rerun authoritative remote CI. Do not build a second legacy compatibility layer, duplicate end-to-end framework, or new approval service just to satisfy the old harness.

Keep the trusted control plane privileged only for immutable PR identity, isolation and receipt verification. Test the candidate's current contract **inside its existing low-privilege, credential-free environment**; have trusted code validate outcomes and source/merge SHAs. Never import or execute candidate-authored modules in a privileged gate or silently weaken an existing blocker. If the mismatch cannot safely be repaired in scope, report the exact failing CI run and blocker rather than manufacturing a green result. Prefer the already available remote CI to repeated heavyweight local debugging; bounded local deterministic feedback is optional and cannot substitute for remote acceptance.

Examine the concrete workflow before triggering it: some GitHub `dev` push events deploy Workers or run remote D1 migrations. Use safe PR CI, disposable fixtures or approved remote execution; do not push production-capable branches merely to start tests. Keep secrets out of PR/NPC contexts; respect budget and isolation. Record tested SHA, run URL, runner, relevant image digest, artifact and cleanup evidence.

## Lifecycle drift checkpoints

| Checkpoint | Mandatory reconciliation |
| --- | --- |
| Session resume | Proportional read-only comparison of actual dev/PR/Issue/Provider/CI with prior Handoff; preserve uncommitted Owner changes |
| Task / PR preflight | Issue scope, Phase dependency, dev ancestry, source/target, remote executor and deploy triggers |
| Pre-merge | Current source/target/merge-base, review and actual CI; no new production authority |
| **Post-merge** | Read back target SHA, real merge result, affected Issue/Project/doc/CI state; repair only proved drift |
| Phase / milestone exit | Existing live Project/Issue reconciliation, dependency gate, unresolved acceptance and history preserved |
| Release / Provider cutover | Freeze actual refs, writer authority, protection, mirror/tag ancestry, deploy effects and rollback; hold conflicting states |

Classify `STATUS_DRIFT` (tracker vs code), `SCOPE_DRIFT` (requirement vs diff), `EVIDENCE_GAP`, `PROVIDER_DRIFT` (conflicting writers/old decisions), and `RELEASE_DRIFT` (mirror/tag/deployment). Preserve historical superseded plans while labeling the current authoritative decision. Correct existing records and **re-read** to verify; do not create shadow issues, modify unrelated tickets or claim aligned Project V2 status from Issue/Markdown alone. If Project access is missing record `PROJECT_UNVERIFIED`, keep dependent Phase gates on hold and allow unrelated tasks to continue. Cutover and production writes always require separate authorization.

## Minimal machine-checkable receipt

For significant post-merge, Phase exit, release and Provider cutover checkpoints, attach concise JSON to existing PR/Issue or CI artifact. No per-file ritual. Run `python3 scripts/check_lifecycle_receipt.py receipt.json --expected-head <FULL_SOURCE_SHA>` where the actual SHA is substituted by the caller.

```json
{
  "schema_version": 1,
  "checkpoint": "POST_MERGE",
  "repository": "example/project",
  "provider": "github-primary",
  "source_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "target_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "observed_target_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "project_state": "PROJECT_UNVERIFIED",
  "verdict": "PARTIAL",
  "workloads": [
    {"kind": "container_e2e", "executor": "github-actions", "status": "PASS",
     "tested_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
     "evidence_url": "https://github.com/example/project/actions/runs/123"}
  ],
  "drift": [
    {"kind": "EVIDENCE_GAP", "status": "BLOCKED",
     "issue_url": "https://github.com/example/project/issues/1"}
  ]
}
```

The checker only verifies **structure and internal consistency of untrusted declarations**. It does not query GitHub/CNB or establish that Project, approval, remote CI, sandbox or deployment facts are true. A structurally valid receipt is NOT a live acceptance PASS; independently read the real Provider state and archive traceable links.

## Rollout / test consumers

- AiringCal: retain deploy/v3 Dockerfile + Compose; reuse existing GitHub Actions `v3_compose_e2e` and `v3_operator_smoke`. GitHub dev-push may deploy Cloudflare/D1: do not trigger it as a test shortcut. Its CNB migration #139 is project-local and independent of this ADS PR.
- ALNILAM: GitHub Primary during historical P1 was a time-scoped baseline, not a permanent Provider decision. For later phases read the project's current approved Provider manifest, live CNB/GitHub refs and latest Owner handoff; use hosted CI for full build/browser acceptance. Preserve existing Core/Site history and pinned ADS until separately reviewed.
- Consumers do not auto-upgrade to unpublished ADS development commits. Revalidate on adoption at exact SHA and keep old accepted releases available.
