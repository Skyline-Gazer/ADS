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

## Working agreement
Verification default: prefer existing hosted CI for automated checks and an isolated target-platform preview/staging environment when real runtime behavior matters. Keep local checks lightweight and optional; do not provision a full persistent local environment per project by default. Never infer production safety from a preview label, expose secrets to untrusted CI jobs or use production data for routine tests. If remote verification is unavailable, state the blocker and use the smallest useful existing fallback.

Implement minimum sufficient changes, verify relevant behavior, repair CI inside task scope and give concise milestones. Use project-specific rules for real constraints without bypassing host or ADS safety. No extra task state machine or mandatory session journal.
