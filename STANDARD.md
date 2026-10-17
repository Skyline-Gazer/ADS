# ADS Development Standard

Version: **0.2 candidate**. Not automatically adopted by any project.

## Priority and inheritance

Follow host safety restrictions and the user's explicit task instructions. Respect project-local factual constraints (architecture, build, API contracts and deployment effects); they may specialize ADS defaults but may not bypass safety boundaries. Surface genuine conflicts. Pin an ADS commit/release rather than a moving branch. Keep a short local AGENTS.md as the canonical repository entrypoint; platform adapters should only point there, not copy competing rules.

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
