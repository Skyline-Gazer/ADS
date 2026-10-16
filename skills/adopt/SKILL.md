---
name: adopt
description: Adopt ADS in an existing codebase or simplify legacy Trellis, Comet, OpenSpec and agent workflows without weakening real safeguards.
---
# Adopt ADS safely

1. Inventory AGENTS.md, agent-specific instructions, hooks, CI workflows, issue/PR conventions, ADRs and actual deployment triggers.
2. Separate executable controls from Markdown descriptions. Identify redundant consent phases, session journals and evidence duplication; also identify legitimate security and production gates.
3. Propose a minimal diff that keeps project architecture, tests, data contracts, secrets controls and release behavior. Do not disable safeguards to force a green build.
4. Add a project-local AGENTS.md referencing an immutable accessible ADS revision. Treat it as canonical; other agent adapters should contain only short pointers.
5. Remove or adjust obsolete mandatory hooks/CI **only** after understanding their operational effect. Preserve history through Git and existing Issues/PRs.
6. Validate with one small real task or an isolated rehearsal and report remaining workflow conflicts.

Never silently rewrite production configs, rotate credentials or merge a high-risk migration without scoped authorization.
