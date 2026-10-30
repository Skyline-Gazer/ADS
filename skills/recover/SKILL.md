---
name: recover
description: Resume an interrupted task or investigate a CI failure using Git, issues, PRs and minimal project context.
---
# Recover work without a workflow database

1. Read the current goal, git status, active branch, recent commits, open PR and relevant issues. Follow Git rules in project `AGENTS.md`; when [strict Git governance](../../profiles/strict-git-governance/README.md) is enabled or work is in ADS itself, follow [git-governance.md](../../docs/git-governance.md). Preserve uncommitted changes when moving off integration/production branches.
2. Inspect the failing CI job or last observable action. Separate source failures, credentials/environment access and advisory outages.
3. Recover expected behavior from source, tests, project AGENTS.md and accepted decisions; old session notes are secondary evidence.
4. If work was delegated, inspect actual child output, surviving branches/worktrees and CI rather than trusting the last child message. In a permission or containment failure, stop affected delegated work, preserve actual attempted/allowed tool commands, verify parent and each child's effective restrictions (including shell and absolute paths), and use serial or independently sandboxed recovery; see [docs/native-subagent-safety.md](../../docs/native-subagent-safety.md). Identify ownership/conflicts and any incomplete integration; recover useful verified work, cancel or quarantine failed concurrent edits when supported, and retry or continue serially inside the original authorization.
5. For an interrupted Phase closure or ADS update, recover actual GitHub Project item IDs and accepted version gitlink from the repository, not a stale handoff. Do not mark unverified items Done or force-reset a dirty submodule. Inspect the existing GitHub discussion and reviewable update PR if present.
6. Make the smallest scoped fix, rerun relevant checks and update existing PR.
7. If blocked, identify exact missing permission or decision. Do not fabricate successful checks or trigger destructive recovery.

Keep a concise handoff only when needed for a real session transition.
