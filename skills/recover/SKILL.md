---
name: recover
description: Resume an interrupted task or investigate a CI failure using Git, issues, PRs and minimal project context.
---
# Recover work without a workflow database

1. Read the current goal, git status, active branch, recent commits, open PR and relevant issues.
2. Inspect the failing CI job or last observable action. Separate source failures, credentials/environment access and advisory outages.
3. Recover expected behavior from source, tests, project AGENTS.md and accepted decisions; old session notes are secondary evidence.
4. If work was delegated, inspect actual child output, surviving branches/worktrees and CI rather than trusting the last child message. Identify ownership/conflicts and any incomplete integration; recover useful verified work, cancel or quarantine failed concurrent edits when supported, and retry or continue serially inside the original authorization.
5. Make the smallest scoped fix, rerun relevant checks and update existing PR.
6. If blocked, identify exact missing permission or decision. Do not fabricate successful checks or trigger destructive recovery.

Keep a concise handoff only when needed for a real session transition.
