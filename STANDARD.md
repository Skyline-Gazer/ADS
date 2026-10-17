# ADS Development Standard

Version: **0.3 candidate**. Not automatically adopted by any project. The v0.2 release remains the tag `v0.2`; this candidate adds environment-first guidance without changing v0.2 semantics.

## Priority and inheritance

Follow host safety restrictions and the user's explicit task instructions. Respect project-local factual constraints (architecture, build, API contracts and deployment effects); they may specialize ADS defaults but may not bypass safety boundaries. Surface genuine conflicts. Pin an ADS commit/release rather than a moving branch. Keep a short local AGENTS.md as the canonical repository entrypoint; platform adapters should only point there, not copy competing rules.

## Environment first, reuse first

Before choosing how to build, test or integrate, check what the host and the project already provide: agent and platform capabilities, native Skills, installed runtimes and package managers, lockfiles, caches, declared build/test commands and reachable local services. Prefer the smallest existing facility that can satisfy the task instead of installing a second runtime, rebuilding a container, provisioning cloud resources or adding another service.

Keep that scan proportional: one short read-only check for ordinary tasks; deeper investigation only for a first bootstrap, a host migration, an expensive integration or known drift. Reuse the findings for the rest of the session and re-verify stale assumptions rather than maintaining an inventory database or a mandatory discovery phase.

Probe with availability checks, versions, file metadata and repository scripts. Do not print environment variable values, tokens or credential-bearing configuration, and do not change global host settings to make a check pass. Report states distinctly: **installed**, **configured** and actually **verified**. When a capability is absent or unverified, take the smallest documented fallback or report the real blocker; never replace a required live integration with a mock.

## Agent-native goal execution

A concrete goal authorizes investigation, changes, relevant tests, task branches, commits, PRs and CI repair within its scope. Split work and use platform-native subagents when beneficial; don't build an orchestrator. Continue until completion, a real blocker or a materially new decision, within the host session's capabilities. No promise of execution after the session ends. Give concise milestone updates, not approval requests for phases.

Use **minimum sufficient implementation**: prefer existing architecture, only directly related fixes and local refactoring. Don't introduce new infrastructure, optional features or elaborate design artifacts as prerequisites. Record out-of-scope improvements as optional issues.

For significant, durable architectural choices, propose alternatives and get owner direction before a consequential change. Ordinary mature, necessary dependencies and tooling may be selected autonomously; validate compatibility and security. Use brief ADRs only when the decision must persist.

## Workflow and GitHub

Use as much planning as uncertainty merits. Small task: implement and check. Larger task: short plan, implementation, relevant verification and review. GitHub Issues/Projects can track material work; avoid a second task database, per-step journals and archival rituals. Use short accurate PR descriptions. Low-risk PRs can merge autonomously if relevant required CI passes, justified blockers are resolved and the repo's auto-deploy effects are allowed. Do not split changes to evade risk classification; see SAFETY.md.

## Recovery and completion

On test/CI failure, inspect and diagnose, fix only related issues and rerun appropriate checks. Reconstruct context from Git, Issues, PRs and essential project documents rather than requiring session history. Clearly distinguish implemented, verified, PR open, merged, deployed and production validated. Do not claim inaccessible external integration tests passed.

## Existing frameworks

Trellis, Comet, OpenSpec and hooks may be useful, but fixed mandatory stages and repeated consents are not ADS requirements. Migration must inspect executable hooks/CI as well as Markdown. Do not remove legitimate release or security controls to make a workflow seem simpler.
