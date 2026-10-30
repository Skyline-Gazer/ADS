# ADS — Agent Development Standard

ADS **v0.5.0 Lite is published:** [GitHub Release](https://github.com/Skyline-Gazer/ADS/releases/tag/v0.5.0) at `9bd8b115fa7a3bff19c0d69c22c0423c7141e63f`. Notes: [v0.5.0-notes.md](docs/releases/v0.5.0-notes.md). Contract: [v0.5.0.md](docs/releases/v0.5.0.md). Consumers pin tag `v0.5.0` (or that full SHA).

**In development:** [v0.6.0 Adaptive Goal Execution](docs/releases/v0.6.0.md) — execution-semantics patch on Lite (Goal / Adaptation / Outcome / Convergence). Not a published tag.

**Status:** Current released pin is **v0.5.0**. Prior **v0.4.x** tags remain immutable. Mac TUI host enforcement remains NOT_VERIFIED.

ADS is an agent-native development standard for personal software projects: **submodule + short `AGENTS.md` + core rules**, not a second app copied into your repo. It reuses the coding agent, GitHub and the host platform—no CLI, approval engine, task database, orchestrator or deployment controller.

**License:** [MIT](LICENSE) for ADS's own standard, Skills and templates.

## Start here (lite default)

1. Read [docs/lite-adoption.md](docs/lite-adoption.md) — **default** for all consumer projects.
2. New repo: [skills/bootstrap/SKILL.md](skills/bootstrap/SKILL.md). Existing repo: [skills/adopt/SKILL.md](skills/adopt/SKILL.md).
3. Copy [templates/AGENTS.md](templates/AGENTS.md) to the project root and fill in **project facts**.
4. Pin ADS as submodule `.ads`; see [docs/how-to-update.md](docs/how-to-update.md).
5. Optional extra governance or tooling: [profiles/README.md](profiles/README.md) — enable **only** by naming profiles in project `AGENTS.md`.

## Core rules

- [STANDARD.md](STANDARD.md) — autonomous execution, scope and delivery.
- [SAFETY.md](SAFETY.md) — scoped authorization and risk.
- [QUALITY.md](QUALITY.md) — adaptive testing and evidence.
- [AGENTS.md](AGENTS.md) — working **in ADS itself** (full Git governance applies here).

## Skills and profiles

- [skills/](skills/) — bootstrap, adopt, deliver, recover.
- [profiles/](profiles/) — optional strict Git, consumer toolchain, lifecycle, stack hints.

## Further reference

- [docs/agent-adoption.md](docs/agent-adoption.md) — host discovery and submodule updates.
- [docs/git-governance.md](docs/git-governance.md) — **mandatory inside ADS**; optional profile for consumers.
- [docs/host-filesystem-boundary.md](docs/host-filesystem-boundary.md) — local TUI read/write containment guidance.
- [docs/native-subagent-safety.md](docs/native-subagent-safety.md) — delegation boundaries.
- [scenarios/](scenarios/) — archived acceptance evidence (not required reading for lite adoption).

## Design principles

Goal-driven execution; minimum sufficient implementation; project-local `AGENTS.md` as entrypoint; environment-first reuse; remote-first verification when it helps; truthful verification labels; low-risk autonomous delivery inside scope; explicit approval for sensitive effects. Optional profiles add strict Git, toolchain, or lifecycle discipline—never by default.

## Migration and publication

Released baselines stay immutable; consumer ADS pin updates are separate reviewable PRs. See [docs/how-to-update.md](docs/how-to-update.md) and release notes under [docs/releases/](docs/releases/).
