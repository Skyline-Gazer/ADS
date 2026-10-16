# ADS — Agent Development Standard

**Status:** v0.2 development candidate (not released or adopted).

ADS is an agent-native, minimal-ceremony development standard for personal software projects. It reuses the coding agent, GitHub and the host platform rather than introducing a CLI, approval engine, task database, orchestrator or deployment controller.

## Start here

1. For a new repository, read [skills/bootstrap/SKILL.md](skills/bootstrap/SKILL.md).
2. For an existing repository, read [skills/adopt/SKILL.md](skills/adopt/SKILL.md).
3. Use [templates/AGENTS.md](templates/AGENTS.md) as a short project-local entrypoint.
4. Pin an immutable ADS commit or release; make the chosen guidance locally accessible to the agent. A private URL without connector access is **not** an effective policy.
5. Keep the project's own architecture, tests and production boundaries. ADS is opt-in and never automatically rewrites other repositories.

## Reference

- [STANDARD.md](STANDARD.md): autonomous execution, scope and delivery.
- [SAFETY.md](SAFETY.md): scoped operational authorization and risk.
- [QUALITY.md](QUALITY.md): adaptive testing, review and evidence.
- [AGENTS.md](AGENTS.md): instructions for working **in ADS itself**.
- [skills/](skills/): opt-in agent-native capabilities.
- [profiles/](profiles/): optional stack hints, not mandatory architectures.
- [scenarios/](scenarios/): acceptance scenarios.
- [docs/agent-adoption.md](docs/agent-adoption.md): practical, pinned adoption and skill discovery.
- [scenarios/migration-recon.md](scenarios/migration-recon.md): read-only findings for KIRARI and AiringCal (not a passed migration).

## Design principles

Goal-driven execution; minimum sufficient implementation; a single canonical rule source; project-local operational constraints; adaptive multi-agent collaboration; truthful, layered verification; low-risk autonomous delivery; explicit approval for sensitive effects. Provide concise milestone reporting; do not gate on paperwork or per-stage owner confirmation.

## Migration and publication

This branch is a development candidate. Existing draft PR #1 and main remain separate. Validate in isolated KIRARI and AiringCal trials before release. Those projects do not adopt ADS merely because this repository is updated.
