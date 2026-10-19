# ADS Quality and Layered Verification

Version: **0.3 candidate**.

Choose checks from changed behavior, impact and consumers—not a mandatory test count. Docs: meaningful formatting/links. Ordinary code: impacted tests, types/lint/build as relevant. API/refactor: contract and integration tests. Sensitive changes: negative/security and recovery tests. Don't mask transitive impact with path filters.

## Environment and verification reuse

Reuse the project's existing runtimes, declared test commands, fixtures and caches before adding a framework, container or service for the same purpose. Pick the lowest-cost check that can actually detect the changed behavior: one existing targeted test or scoped real run usually suffices, while an unbounded integration re-run adds cost without adding evidence.

Keep evidence classes distinct and report the one actually performed: local deterministic tests, reuse of an existing test facility, isolated live exercise against real dependencies and production validation are not interchangeable. Reusing a local facility never stands in for an unperformed live integration, and a missing capability is a stated boundary rather than an implicit pass.

## Multi-agent integration and efficiency evidence

A child agent's summary, self-tested branch or reviewer finding is input to the main agent, not final verification. The main agent checks the combined diff, re-runs affected contract/integration checks after merging independent changes and reports skipped or unavailable checks. A delegated security review cannot widen authorization, and an AI-only review is not a substitute for deterministic CI.

For multi-agent efficiency claims, compare against a **single-agent baseline** with the same goal, pinned code, test criteria and reasonably comparable host/model/tool permissions. Measure end-to-end wall time (including startup, integration, reruns and recovery), observable tokens/cost, independently verified outcome, retries and merge conflicts. Separate independent subtasks from coupled negative cases. Record missing metering as **NOT OBSERVED**, and absent or unexercised native capabilities as **NOT TESTED**, never zero cost or PASS. Compare multiple trials where practical and do not assert a universal speedup from one fixture. The acceptance protocol is [scenarios/v0.3-multi-agent-acceptance.md](scenarios/v0.3-multi-agent-acceptance.md).



1. **Local:** deterministic tests, fixtures and mocks for fast feedback.
2. **Integration:** real dependencies in an authorized isolated/test environment when behavior actually depends on them.
3. **Production:** only when authorized and necessary; distinguish deployment success, service health and real-world functional validation.

Report each layer actually performed; a mocked test never proves live integration. Lack of live access is an unverified boundary, not success or automatic failure of unrelated code.

## CI and review

Keep relevant required checks and material safety regressions blocking. Don't disable failing checks merely to turn CI green. Advisory AI reviews and irrelevant external review-service outages are not automatic blockers. Increase review rigor with change risk; routine low-risk code need not have two independent reviewers. Choose review tooling only after inspecting existing host capability; the v0.3 decision record is [docs/code-review-options.md](docs/code-review-options.md) and no third-party review service is required. Resolve concrete blocking findings, accurately report known limitations, then deliver under STANDARD.md and SAFETY.md.
