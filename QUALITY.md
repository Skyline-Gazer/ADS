# ADS Quality and Layered Verification

Version: **development after v0.4**. Released v0.4 remains immutable; unreleased extensions require separate consumer review.

Choose checks from changed behavior, impact and consumers—not a mandatory test count. Docs: meaningful formatting/links. Ordinary code: impacted tests, types/lint/build as relevant. API/refactor: contract and integration tests. Sensitive changes: negative/security and recovery tests. Don't mask transitive impact with path filters.

## Environment and verification reuse

Reuse the project's existing runtimes, declared test commands, fixtures and caches before adding a framework, container or service for the same purpose. Pick the lowest-cost check that can actually detect the changed behavior: one existing targeted test or scoped real run usually suffices, while an unbounded integration re-run adds cost without adding evidence.

Keep evidence classes distinct and report the one actually performed: local deterministic tests, reuse of an existing test facility, isolated live exercise against real dependencies and production validation are not interchangeable. Reusing a local facility never stands in for an unperformed live integration, and a missing capability is a stated boundary rather than an implicit pass.

## Remote-first execution and verification

For projects with existing hosted CI, make that CI the primary authoritative automated check instead of requiring every agent session to recreate the full test environment locally. Use isolated target-platform preview/staging environments only when the changed behavior depends on the real runtime, bindings or external integration. Keep quick local checks optional; reuse an already-installed facility and do not provision a persistent per-project local stack by default.

Choose checks by changed behavior and cost, not by an assumption that every test must run remotely. A remote CI pass does not prove an unexercised target-platform integration; a preview deployment does not prove production behavior; a local mock does not prove a live dependency. Keep commit SHA, workflow run, deployment revision, test data boundary and cleanup evidence traceable. Use synthetic data and least-privilege credentials, preserve required gates, and never run destructive tests against production by default.

When a needed remote environment is absent, do not stop at reporting the gap: provision the smallest fit-for-purpose hosted CI or ephemeral preview/test environment autonomously when the existing credentials, permissions, quotas, budget and task authorization permit it. Prefer repo-native CI and provider-native preview capabilities over a new permanent service. If creation crosses a real authorization boundary (new recurring spend, plan upgrade, elevated IAM, missing owner-only credentials, production access or long-lived infrastructure), request only the specific missing user action, keep working on independent safe tasks, and report what remains unverified. Use local fallback only when remote execution is not needed or cannot be provisioned within scope. Start CI early and work on independent tasks while it runs to reduce perceived latency.

See [scenarios/remote-first-verification.md](scenarios/remote-first-verification.md) for decision order and acceptance cases.

## Consumer developer-toolchain and production-boundary checks

For every project adopting ADS, validate CodeGraph and the full RTK edition as required development capabilities. Check the official latest stable releases dynamically; do not treat an old pinned version as current. The consumer project must initialize the tools on a development branch and prove the active host integration works. Prefer CodeGraph native auto-sync, verify index freshness before graph-dependent analysis, and use explicit sync/status for recovery or when automatic reconciliation is unhealthy. A deterministic guard must reject consumer tool configuration, generated indexes/caches and binaries from the production branch and release artifacts. The generic guard itself may remain on production main because it does not configure either tool. These requirements apply to ADS consumers, not to the ADS standards repository. See [consumer-dev-toolchain.md](docs/consumer-dev-toolchain.md).

## Multi-agent integration and efficiency evidence

A child agent's summary, self-tested branch or reviewer finding is input to the main agent, not final verification. The main agent checks the combined diff, re-runs affected contract/integration checks after merging independent changes and reports skipped or unavailable checks. A delegated security review cannot widen authorization, and an AI-only review is not a substitute for deterministic CI. Before accepting safety claims for native Subagents, verify actual child read/edit/shell permissions, canonical path and absolute-path escape containment, and lifecycle waiting with the [targeted negative oracle](scenarios/subagent-permission-containment.md). Independent passing application tests do not erase an observed forbidden read or write. Worktrees alone do not prove containment; missing tool/OS restrictions are reported as unsafe or unverified.

For multi-agent efficiency claims, compare against a **single-agent baseline** with the same goal, pinned code, test criteria and reasonably comparable host/model/tool permissions. Measure end-to-end wall time (including startup, integration, reruns and recovery), observable tokens/cost, independently verified outcome, retries and merge conflicts. Separate independent subtasks from coupled negative cases. Record missing metering as **NOT OBSERVED**, and absent or unexercised native capabilities as **NOT TESTED**, never zero cost or PASS. Compare multiple trials where practical and do not assert a universal speedup from one fixture. The native acceptance protocol is [scenarios/v0.3-multi-agent-acceptance.md](scenarios/v0.3-multi-agent-acceptance.md). To attribute efficiency to model choice, use the [controlled host/model matrix](scenarios/v0.3-subagent-model-matrix.md): verify the *actual* model used by the parent and every child, hold the host/fixture/sandbox constant for within-host contrasts, then attempt matched cross-host routes only if objectively available. Historical cross-host runs using different models are not a model-controlled comparison; unsafe or incorrect samples cannot establish speedup.



1. **Local:** deterministic tests, fixtures and mocks for fast feedback.
2. **Integration:** real dependencies in an authorized isolated/test environment when behavior actually depends on them.
3. **Production:** only when authorized and necessary; distinguish deployment success, service health and real-world functional validation.

Report each layer actually performed; a mocked test never proves live integration. Lack of live access is an unverified boundary, not success or automatic failure of unrelated code.

## Milestone and ADS upgrade verification

At Phase closure compare actual GitHub Project item fields and linked Issues against PR/CI, target commit and relevant contract/security evidence. Correct Project status drift only on verified facts, and distinguish historical acceptance FAIL/PARTIAL from evidence archived successfully. If the Project cannot be queried, record PROJECT_UNVERIFIED rather than silently declaring alignment.

A consumer ADS submodule upgrade requires validating the old and new recorded gitlink commits, the upstream guideline diff, local AGENTS.md and native Skill discoverability, plus tests relevant to behavioral/safety changes. A passing ADS source repository CI cannot by itself prove that the consumer's upgraded project works. See [docs/milestone-reconciliation.md](docs/milestone-reconciliation.md) and [docs/how-to-update.md](docs/how-to-update.md).

## Git governance and delivery evidence

Follow the mandatory [Git development governance policy](docs/git-governance.md) in ADS itself and every adopting project. Normal task branches originate from the latest `dev` and PRs target `dev`; production promotion uses a separate release PR. Validate PR base/branch type and explicit Issue references where deterministic, run checks against the actual candidate SHA, and verify the merged target SHA after integration. Issue closure, PR merge, deployment and production validation are distinct evidence states. A workflow run is not server-side branch protection: verify required-check and protection settings separately, and disclose when the host/plan cannot enforce them.


## CI and review

Keep relevant required checks and material safety regressions blocking. Don't disable failing checks merely to turn CI green. Advisory AI reviews and irrelevant external review-service outages are not automatic blockers. Increase review rigor with change risk; routine low-risk code need not have two independent reviewers. Choose review tooling only after inspecting existing host capability; the v0.3 decision record is [docs/code-review-options.md](docs/code-review-options.md) and no third-party review service is required. Resolve concrete blocking findings, accurately report known limitations, then deliver under STANDARD.md and SAFETY.md.

Consumer toolchain acceptance must cover missing tools without installation, uninitialized and healthy repeat sessions, controlled stale-index recovery, wrong edition/provenance, wrong worktree, source-channel failure, and clean/contaminated production trees and actual outputs. Fixed historical consumer snapshots test compatibility only; latest official releases are observed dynamically. Never label CI stdio MCP as native Agent Host verification.
