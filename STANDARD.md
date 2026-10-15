# Personal Agent Development Standard

Version: **0.1-draft** · Status: **proposal, not yet adopted**

## Purpose and priority
PAS defines lightweight defaults for personal projects developed with AI coding agents. It is not an orchestration framework, approval engine, or replacement for GitHub. Platform safety requirements and explicit user instructions take precedence. Project-specific technical and operational safety controls remain effective; conflicts must be surfaced rather than silently ignored.

## Default execution
A clear request to implement, fix, or refactor authorizes work within its stated scope: read code, investigate, plan as needed, edit, test, create branches/worktrees, commit, push task branches, open/update PRs, and repair CI/review findings. Do not request a separate approval merely to create a task, write a plan, or enter a new workflow stage. Ask only when an essential product choice cannot be inferred or an operation exceeds the authorization boundary in [SAFETY.md](SAFETY.md).

Default flow: **Requirement → Implementation → Relevant verification → PR → Merge**. Minor changes need no mandatory PRD/design/implementation templates. Large or uncertain changes may benefit from one concise design note; do not require multiple artifacts just to satisfy a framework.

## Git, issues and PRs
Use an isolated task branch/worktree where appropriate, meaningful commits, and a concise PR describing behavior, actual verification and known limitations. No forced commit after every edit, mandatory multi-section commit body, duplicate task tracker, or journal/archive commits. Use GitHub Issues/Projects if already in use; creating an Issue for every small task is optional.

**Low-risk PRs may be merged by the agent** when the relevant required CI passes, no substantiated blocking finding remains, the change is within scope, and any automatically triggered deployment is allowed by the project's existing deployment policy. High-risk changes require explicit Owner merge authorization, even when CI passes. Never split work artificially to circumvent risk classification. A clear project-specific merge policy can be stricter where justified; absence of a policy is not permission to risk production changes. See [SAFETY.md](SAFETY.md).

## Frameworks and context
Trellis, Comet, OpenSpec, and other agent frameworks are optional tools for knowledge and coordination. Their required phases, task-creation consent, handoff documents, per-session journals, archives and repetitive approval checkpoints are **not PAS defaults**. Remove or reconfigure enforcing hooks when adopting PAS; a Markdown override alone is insufficient. Load only relevant current code, project instructions and references. Historical plans and session notes are evidence, not unquestioned requirements.

## Documentation and completion
Update docs when changes affect public behavior, configuration, APIs, operations or important architecture/security decisions. Do not create reports that duplicate PRs, tests and CI logs.

At completion state **implemented**, **verified**, **merged**, **deployed** and **live-tested** separately and truthfully. Report the actual checks and outstanding risks briefly. Green CI or a Preview is not proof of Production.

## Adoption
This draft does not automatically override other repositories. Each repository deliberately adopts a pinned PAS revision through a short local `AGENTS.md` and removes conflicting executable gates after review. No runtime network fetch of a moving policy is required.
