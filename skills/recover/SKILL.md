---
name: recover
description: Resume an interrupted task or investigate a CI failure using Git, issues, PRs and minimal project context.
---
# Recover work without a workflow database

1. Read the current goal, git status, active branch, recent commits, open PR and relevant issues.
2. Inspect the failing CI job or last observable action. Separate source failures, credentials/environment access and advisory outages.
3. Recover expected behavior from source, tests, project AGENTS.md and accepted decisions; old session notes are secondary evidence.
4. Make the smallest scoped fix, rerun relevant checks and update existing PR.
5. If blocked, identify exact missing permission or decision. Do not fabricate successful checks or trigger destructive recovery.

Keep a concise handoff only when needed for a real session transition.
