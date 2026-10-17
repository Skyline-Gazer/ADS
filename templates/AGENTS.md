# Project Agent Instructions

## ADS adoption
Source: https://github.com/Skyline-Gazer/ADS
Pinned revision: <full immutable ADS commit SHA or release tag>
Locally available guidance: <vendored path or agent-accessible pinned source>
Primary rules: STANDARD.md, SAFETY.md, QUALITY.md at that revision.
If private content is inaccessible, report it rather than pretending these rules were loaded.

## Project facts
Purpose: <one sentence>
Source and architecture: <paths and key constraints>
Build/test: <actual commands>
Default branch and delivery: <does merging trigger production?>
Sensitive operations: <targets, data/credentials, explicit approval boundaries>

## Working agreement
Implement minimum sufficient changes, verify relevant behavior, repair CI inside task scope and give concise milestones. Use project-specific rules for real constraints without bypassing host or ADS safety. No extra task state machine or mandatory session journal.
