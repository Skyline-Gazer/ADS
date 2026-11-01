---
name: recover
description: Continue an interrupted task from live repository facts without starting a duplicate task chain.
---
# Recover and finish

1. Recover the actual Goal and Acceptance from the user request, Issue, open PRs, commits, workspace and CI. Reuse the existing task branch/PR rather than opening a parallel chain.
2. After a partial command, broken CI or interrupted merge, **reread real state** before a repair. Identify whether the cause is source behavior, stale tests, missing integration access or an advisory service failure. Do not restore retired behavior to satisfy an old fixture.
3. Repair the smallest related fault, rerun relevant checks and continue review/authorized merge on the current SHA. Resolve actual material review comments; distinguish unmerged code, merged code and deployed behavior.
4. For delegated work, inspect integrated changes rather than trusting child reports. Git worktrees do not enforce filesystem boundaries, but absent host isolation never blocks ordinary authorized project coding. Disclose `ISOLATION_NOT_ENFORCED` or `NOT_VERIFIED` without claiming PASS.
5. Stop only the action crossing an actual authorization or required functional acceptance boundary. No automatic production deployment, privilege escalation, branch force reset, provider change or fabricated successful test.

Keep a short handoff only when a real session ends. [Deliver](../deliver/SKILL.md) governs continued task convergence; [SAFETY](../../SAFETY.md) governs consequential operations.
