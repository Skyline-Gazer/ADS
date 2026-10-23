# Project Agent Instructions

## ADS adoption
Source: https://github.com/Skyline-Gazer/ADS
Pinned revision: <full immutable ADS commit SHA recorded by the consumer gitlink>
Locally available guidance: .ads/ (Git submodule; use another explicit path if already occupied)
Primary rules: .ads/STANDARD.md, .ads/SAFETY.md, .ads/QUALITY.md at that revision.
Install/update guide: .ads/docs/how-to-update.md; use approved release diff + tested gitlink PR, never an unchecked moving-branch update.
Phase checkpoint: .ads/docs/milestone-reconciliation.md; reconcile real GitHub Project issues/items/PR/CI when a Phase or goal ends.
If private content is inaccessible, report it rather than pretending these rules were loaded.

## Project facts
Purpose: <one sentence>
Source and architecture: <paths and key constraints>
Build/test: <actual commands>
Default branch and delivery: <does merging trigger production?>
Sensitive operations: <targets, data/credentials, explicit approval boundaries>

## Mandatory consumer developer toolchain

Follow the policy at `.ads/docs/consumer-dev-toolchain.md` (or the actual configured ADS submodule path) for CodeGraph and the full RTK edition. These tools are required for development in this consumer repository, not production runtime dependencies. Check latest stable versions and project/host initialization during adoption and relevant development-session preflight. Initialize project integration only on development branches. Keep tool-specific manifests, host integration and generated tool artifacts out of the consumer's production `main`; install the generic production-boundary guard and run it on PRs targeting that branch. After source changes, explicitly run CodeGraph sync/status before relying on graph-based impact analysis. Ask before installing missing binaries or changing global host settings.

## Working agreement
Verification default: prefer remote CI and target-platform preview/staging when relevant. If no suitable remote facility exists, create the smallest task-scoped hosted workflow or ephemeral environment autonomously when existing credentials, permissions, quotas, budget and user authorization allow it. Ask only for a genuine blocker outside that scope, naming the exact provider setting/permission/secret or owner action required; continue independent safe work. Use local checks as a fallback only when remote verification is unnecessary or cannot be provisioned within scope. Never infer production safety from a preview label, expose secrets to untrusted CI jobs, use production data for routine tests, or silently incur new recurring spend, broaden IAM or create long-lived infrastructure.

Implement minimum sufficient changes, verify relevant behavior, repair CI inside task scope and give concise milestones. Use project-specific rules for real constraints without bypassing host or ADS safety. No extra task state machine or mandatory session journal.
