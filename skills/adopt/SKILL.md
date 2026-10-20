---
name: adopt
description: Adopt ADS in an existing codebase or simplify legacy Trellis, Comet, OpenSpec and agent workflows without weakening real safeguards.
---
# Adopt ADS safely

1. Inventory AGENTS.md, agent-specific instructions, hooks, CI workflows, issue/PR conventions, ADRs and actual deployment triggers.
2. Inspect what the host agent and machine already provide — native Skills, subagent or review capabilities, installed runtimes, existing scripts and fixtures — before proposing any replacement service. Reuse working facilities instead of adding a second one, and distinguish installed, configured and verified capabilities.
3. Before adopting a multi-agent pattern, identify existing host-native delegation, **effective per-child read/edit/shell permissions**, writable shared directories, absolute-path/parent-worktree escape behavior and hooks. A separate child worktree may not be a filesystem sandbox, and a parent permission deny may not propagate. Check relevant safe negative controls under [docs/native-subagent-safety.md](../../docs/native-subagent-safety.md) before sensitive delegation. Keep project-local permission/CI/deployment rules authoritative for every child; prefer existing native capability over additional task orchestration.
4. Separate executable controls from Markdown descriptions. Identify redundant consent phases, session journals and evidence duplication; also identify legitimate security and production gates.
5. Propose a minimal diff that keeps project architecture, tests, data contracts, secrets controls and release behavior. Do not disable safeguards to force a green build.
6. Prefer a pinned ADS Git submodule at `.ads` for new adoption and a carefully reviewed migration from old vendored/pointer approaches. Inspect existing `.ads`, `.gitmodules`, current host Skill copies and deployment behavior first; never force overwrite. Follow [docs/how-to-update.md](../../docs/how-to-update.md), verify private repository access and submodule gitlink visibility.
7. Add a project-local AGENTS.md referencing an immutable accessible ADS revision. Treat it as canonical; other agent adapters should contain only short pointers.
8. Remove or adjust obsolete mandatory hooks/CI **only** after understanding their operational effect. Preserve history through Git and existing Issues/PRs.
9. Validate with one small real task or an isolated rehearsal and report remaining workflow conflicts.

Never silently rewrite production configs, rotate credentials or merge a high-risk migration without scoped authorization.
