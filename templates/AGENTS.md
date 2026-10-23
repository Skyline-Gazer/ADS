# Project Agent Instructions

## ADS adoption
Source: https://github.com/Skyline-Gazer/ADS
Pinned revision: <full immutable ADS commit SHA recorded by the consumer gitlink>
Locally available guidance: .ads/ (Git submodule; use another explicit path if already occupied)
Primary rules: .ads/STANDARD.md, .ads/SAFETY.md, .ads/QUALITY.md at that revision.
Install/update guide: .ads/docs/how-to-update.md; use approved release diff + tested gitlink PR, never an unchecked moving-branch update.
Git governance: follow .ads/docs/git-governance.md. `dev` is the required development/integration branch; start each task branch from latest `dev`, reference an Issue, and deliver via PR to `dev`. Promote to production only through a separate release PR. If `dev` is absent, establish it through a reviewable migration before normal work. During adoption, inspect branch protection with `gh`; if classic protection is absent/incomplete, run `scripts/ensure-ads-branch-protection.py` with exact CI check names to apply and verify protection. A `403` means the state/action is inaccessible, not that protection is absent; report admin/plan blockers and do not claim enforcement.
Phase checkpoint: .ads/docs/milestone-reconciliation.md; reconcile real GitHub Project issues/items/PR/CI when a Phase or goal ends.
If private content is inaccessible, report it rather than pretending these rules were loaded.

## Project facts
Purpose: <one sentence>
Source and architecture: <paths and key constraints>
Build/test: <actual commands>
Default branch and delivery: <does merging trigger production?>
Sensitive operations: <targets, data/credentials, explicit approval boundaries>

## Working agreement
Verification default: prefer remote CI and target-platform preview/staging when relevant. If no suitable remote facility exists, create the smallest task-scoped hosted workflow or ephemeral environment autonomously when existing credentials, permissions, quotas, budget and user authorization allow it. Ask only for a genuine blocker outside that scope, naming the exact provider setting/permission/secret or owner action required; continue independent safe work. Use local checks as a fallback only when remote verification is unnecessary or cannot be provisioned within scope. Never infer production safety from a preview label, expose secrets to untrusted CI jobs, use production data for routine tests, or silently incur new recurring spend, broaden IAM or create long-lived infrastructure.

Implement minimum sufficient changes, verify relevant behavior, repair CI inside task scope and give concise milestones. Use project-specific rules for real constraints without bypassing host or ADS safety. No extra task state machine or mandatory session journal.
