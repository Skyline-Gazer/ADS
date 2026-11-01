---
name: recover
description: Resume work from real repository state, take over stale task chains, and repair without drifting the Goal or widening authorization.
---
# Recover work without a workflow database

## 1. Recompute remaining work from live state

1. Restate the Goal Contract from Issue/PR/user text (Goal, Invariants, Acceptance, Scope, Stop). Do not invent a new Goal to make recovery easier.
2. Read git status, branch, recent commits, **open PRs and branches for the same Goal**, and relevant Issues. Prefer **taking over** an existing task PR/branch over opening a parallel chain.
3. Follow Git rules in project `AGENTS.md`; ADS itself / Strict Git profile: [git-governance.md](../../docs/git-governance.md). Preserve uncommitted work when leaving integration/production branches.

## 2. Diagnose with real evidence

1. Inspect the failing CI job or last observable action. Separate source defects, credentials/environment limits, and advisory outages.
2. After mid-run or partial failure, **re-read actual state** (tree, remote SHA, service health) before repairing — do not assume the last command finished or rolled back cleanly.
3. Recover expected behavior from source, tests, and project `AGENTS.md`; session notes are secondary.

## 3. Delegation and safety

If work was delegated, inspect child output, surviving worktrees/CI and actual authorization; do not trust a child's claimed success. A missing host sandbox is advisory for normal development, not a reason to abandon or repeat the task. For explicitly hardened work follow [native-subagent-safety.md](../../docs/native-subagent-safety.md).

Project-outside access remains unauthorized unless explicitly granted. Missing isolation is `ISOLATION_NOT_ENFORCED` / `NOT_VERIFIED`, never PASS and never an automatic ordinary development blocker — [host-filesystem-boundary.md](../../docs/host-filesystem-boundary.md).

## 4. Repair and converge

1. Smallest scoped fix; update the **existing** PR; rerun relevant checks.
2. Resume [deliver](../deliver/SKILL.md) convergence inside authorization: CI/review on current HEAD, authorized merge, target SHA reread, close only proved-complete Issues.
3. If blocked, name the exact missing permission or Owner action. Do not fabricate PASS, force-reset dirty submodules, deploy production, switch Provider, or bypass Review/safety gates to “finish.”

Keep a short handoff only for a real session boundary.
