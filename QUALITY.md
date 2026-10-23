# ADS Quality and Layered Verification

Version: **0.3 candidate**.

Choose checks from changed behavior, impact and consumers—not a mandatory test count. Docs: meaningful formatting/links. Ordinary code: impacted tests, types/lint/build as relevant. API/refactor: contract and integration tests. Sensitive changes: negative/security and recovery tests. Don't mask transitive impact with path filters.

## Environment and verification reuse

Reuse the project's existing runtimes, declared test commands, fixtures and caches before adding a framework, container or service for the same purpose. Pick the lowest-cost check that can actually detect the changed behavior: one existing targeted test or scoped real run usually suffices, while an unbounded integration re-run adds cost without adding evidence.

Keep evidence classes distinct and report the one actually performed: local deterministic tests, reuse of an existing test facility, isolated live exercise against real dependencies and production validation are not interchangeable. Reusing a local facility never stands in for an unperformed live integration, and a missing capability is a stated boundary rather than an implicit pass.

## Remote-first execution and verification

For projects with existing hosted CI, make that CI the primary authoritative automated check instead of requiring every agent session to recreate the full test environment locally. Use isolated target-platform preview/staging environments only when the changed behavior depends on the real runtime, bindings or external integration. Keep quick local checks optional; reuse an already-installed facility and do not provision a persistent per-project local stack by default.

Choose checks by changed behavior and cost, not by an assumption that every test must run remotely. A remote CI pass does not prove an unexercised target-platform integration; a preview deployment does not prove production behavior; a local mock does not prove a live dependency. Keep commit SHA, workflow run, deployment revision, test data boundary and cleanup evidence traceable. Use synthetic data and least-privilege credentials, preserve required gates, and never run destructive tests against production by default. If remote access or platform capability is unavailable, state the exact blocker and use only the smallest useful fallback already available; do not invent evidence or silently create long-lived infrastructure. Start CI early and work on independent tasks while it runs to reduce perceived latency.

See [scenarios/remote-first-verification.md](scenarios/remote-first-verification.md) for decision order and acceptance cases.

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

## CI and review

Keep relevant required checks and material safety regressions blocking. Don't disable failing checks merely to turn CI green. Advisory AI reviews and irrelevant external review-service outages are not automatic blockers. Increase review rigor with change risk; routine low-risk code need not have two independent reviewers. Choose review tooling only after inspecting existing host capability; the v0.3 decision record is [docs/code-review-options.md](docs/code-review-options.md) and no third-party review service is required. Resolve concrete blocking findings, accurately report known limitations, then deliver under STANDARD.md and SAFETY.md.
