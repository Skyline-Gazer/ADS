# ADS — Agent Development Standard

**Status:** ADS v0.3 is released at tag `v0.3`, pointing to `1e07d6c4bbd296b7d37dcd31934cfc70426f73ac`. See [release notes](docs/releases/v0.3-notes.md) and [release decision](docs/releases/v0.3.md).

ADS is an agent-native, minimal-ceremony development standard for personal software projects. It reuses the coding agent, GitHub and the host platform rather than introducing a CLI, approval engine, task database, orchestrator or deployment controller.

## Start here

1. For a new repository, read [skills/bootstrap/SKILL.md](skills/bootstrap/SKILL.md).
2. For an existing repository, read [skills/adopt/SKILL.md](skills/adopt/SKILL.md).
3. Use [templates/AGENTS.md](templates/AGENTS.md) as a short project-local entrypoint.
4. Prefer a pinned ADS Git submodule at `.ads` in each consumer repository. The root AGENTS.md points to its actual checked-out content. See [docs/how-to-update.md](docs/how-to-update.md). A private URL without authorized clone access is **not** effective policy.
5. Keep the project's own architecture, tests and production boundaries. ADS is opt-in and never automatically rewrites other repositories.

## Reference

- [STANDARD.md](STANDARD.md): autonomous execution, scope and delivery.
- [SAFETY.md](SAFETY.md): scoped operational authorization and risk.
- [QUALITY.md](QUALITY.md): adaptive testing, review and evidence.
- [AGENTS.md](AGENTS.md): instructions for working **in ADS itself**.
- [skills/](skills/): opt-in agent-native capabilities.
- [profiles/](profiles/): optional stack hints, not mandatory architectures.
- [scenarios/](scenarios/): acceptance scenarios.
- [docs/how-to-update.md](docs/how-to-update.md): AI-native submodule-first adoption, update triggers, review and rollback.
- [docs/native-subagent-safety.md](docs/native-subagent-safety.md): verified child permission ceilings, command/file-system containment and lifecycle preflight; preserves observed host failures.
- [docs/milestone-reconciliation.md](docs/milestone-reconciliation.md): Phase-end GitHub Project/Issue/PR/CI drift convergence.
- [docs/agent-adoption.md](docs/agent-adoption.md): practical, pinned adoption and skill discovery.
- [docs/git-governance.md](docs/git-governance.md): mandatory Issue/branch/PR/CI/release governance for ADS itself and all adopting projects.
- [docs/consumer-dev-toolchain.md](docs/consumer-dev-toolchain.md): mandatory latest-stable CodeGraph + full RTK for consumer projects, development-branch-only integration and production-boundary guard.
- [docs/code-review-options.md](docs/code-review-options.md): v0.3 review-option decision and the native review trial evidence.
- [scenarios/migration-recon.md](scenarios/migration-recon.md): read-only findings for KIRARI and AiringCal (not a passed migration).
- [scenarios/v0.3-multi-agent-acceptance.md](scenarios/v0.3-multi-agent-acceptance.md): v0.3 native Multi-Agent protocol; Codex PARTIAL and Claude FAIL archived, not a blanket compatibility PASS.
- [scenarios/v0.3-subagent-model-matrix.md](scenarios/v0.3-subagent-model-matrix.md): controlled host/model/serial-vs-parallel matrix, workload sizing and budgeted independent safety validation (new runs NOT TESTED).
- [scenarios/subagent-permission-containment.md](scenarios/subagent-permission-containment.md): isolated negative read/write/escape/permission-inheritance test (OpenCode 2.0.32: default/broad UNSAFE; narrow exact-path scoped pass; model matrix NOT RUN).
- [scenarios/phase-milestone-reconciliation.md](scenarios/phase-milestone-reconciliation.md): Phase closure and drift acceptance protocol (live Project not tested).
- [scenarios/submodule-update.md](scenarios/submodule-update.md): consumer adoption/update/rollback acceptance protocol (live consumer not tested).
- [scenarios/environment-first.md](scenarios/environment-first.md): environment-first probe, local reuse and fallback evidence.
- [scenarios/remote-first-verification.md](scenarios/remote-first-verification.md): remote-first verification with autonomous in-scope provisioning, exact user-action escalation, local-light fallback and evidence labels.
- [scenarios/v0.3-omp-acceptance.md](scenarios/v0.3-omp-acceptance.md): OMP 18.11.3 v0.3 acceptance archive.
- [scenarios/v0.3-opencode-acceptance.md](scenarios/v0.3-opencode-acceptance.md): OpenCode v2.0.32 v0.3 acceptance archive.
- [scenarios/v0.3-codex-acceptance.md](scenarios/v0.3-codex-acceptance.md): historical Codex CLI 0.163.0 first run, PARTIAL due to restored global-config drift.
- [scenarios/v0.3-codex-closure.md](scenarios/v0.3-codex-closure.md): Codex CLI 0.163.0 complete retest PASS; global policy content unchanged, HTTP contained in the native sandbox, historical writer still unattributed.
- [scenarios/v0.3-claude-code-acceptance.md](scenarios/v0.3-claude-code-acceptance.md): Claude Code 2.1.292 native acceptance PASS; permission-handling deviations and untested areas retained.
- [scenarios/auth-scope-regression.md](scenarios/auth-scope-regression.md): authorization-scope regression (path attributes are not authorization).
- [scenarios/v0.2-acceptance.md](scenarios/v0.2-acceptance.md): real-host acceptance protocol before release; OCR deferred to v0.3.

## Design principles

Goal-driven execution; phase-end GitHub Project milestone convergence; review-gated ADS submodule updates; environment-first reuse of existing host and project capability; remote-first verification with local-light execution; minimum sufficient implementation; a single canonical rule source; project-local operational constraints; adaptive multi-agent collaboration; truthful, layered verification; low-risk autonomous delivery; explicit approval for sensitive effects. Provide concise milestone reporting; do not gate on paperwork or per-stage owner confirmation.

## Migration and publication

The v0.2 release baseline is tag `v0.2` (merged PRs #2 and #5); v0.3 is in release-candidate closeout. Isolated GitHub Actions KIRARI/AiringCal compatibility and *real private* ADS Submodule consumer CI are separate release gates listed in [the v0.3 release decision](docs/releases/v0.3.md). Those projects do not adopt ADS merely because this repository is updated.
