# ADS — Agent Development Standard

ADS is a **lightweight development convention**, not an orchestration system, approval engine, task database or OS sandbox. Its purpose is to help coding agents finish an authorized goal, verify what actually changed and avoid unnecessary development blockers.

**Version status:** [v0.7.0 Simplify to Deliver](https://github.com/Skyline-Gazer/ADS/releases/tag/v0.7.0) is **published**. [Release PR #112](https://github.com/Skyline-Gazer/ADS/pull/112) merged to `main`; the immutable release commit is `42ba05c6b6707690702689988c352d4d3a3cde6e`. Pin the published tag or full commit SHA; consumer updates remain separate reviewable changes. CNB-specific post-release guidance landed separately in [PR #118](https://github.com/Skyline-Gazer/ADS/pull/118) on `cnb/dev`.

**Default is development-first:** no Docker/VM/OS sandbox, SCA/SBOM/license inventory, security-only reassessment or extra CI is required just to develop ordinary project code. These are opt-in hardening capabilities. ADS does **not** enforce filesystem/process isolation, and an agent must still respect actual task scope, host/tool denials, secrets and consequential production/privilege/spending authorization.

**What stays:** relevant build/tests/functional CI, material code review, the project's configured Git provider/PR workflow, and truthful **Process / State / Outcome** reporting. See [STANDARD](STANDARD.md), [SAFETY](SAFETY.md), [QUALITY](QUALITY.md). Optional tooling and stricter governance are in [profiles](profiles/README.md).

**License:** [MIT](LICENSE).

## One-message agent adoption + Mission

In an existing project, send your coding agent **one request**. Replace only the last line with your goal or a reference to an existing Plan, Spec, Issue or Project; no special task format or separate ADS installer is needed:

```text
Adopt ADS Lite from https://github.com/Skyline-Gazer/ADS at its current published release.
Inspect this project first: existing AGENTS.md, source, build/tests, Git provider, PR/CI,
deployment effects and permissions. Read that ADS release's templates/AGENTS.md and
docs/lite-adoption.md. Reconcile the project's root AGENTS.md with verified facts,
preserving local rules. Prefer standalone unless this project already uses or I explicitly
request a pinned .ads submodule. Do not follow an unpinned ADS branch, change remotes,
enable optional governance/tools, or touch production as a side effect of adoption.
Then implement and verify my Mission using this project's existing workflow. Accept the
input as-is (freeform/Plan/Spec/Issue/Project), infer reversible technical details from
the repository, and do not demand another specification format. Continue through tests,
review feedback, PR and authorized merge when available. Ask only for a truly missing
owner preference or consequential authorization. If the Mission authorizes a backlog,
keep taking the next unblocked item; otherwise finish and report the actual outcome.
Mission: <my request or link to existing project requirements>
```

This is an **instruction to the agent**, not a new ADS runner. An agent that cannot read
the release or lacks a required host permission must report the specific limitation
instead of claiming that adoption or delivery succeeded.

## Start here

1. Read [Lite adoption](docs/lite-adoption.md) and use the [project AGENTS.md template](templates/AGENTS.md) to record real project facts: purpose, build/tests, Git/deploy effects and sensitive operations.
2. Choose **standalone** (commit the self-contained `AGENTS.md`, no ADS checkout) or **pinned submodule** (add `.ads` at an immutable approved SHA to load the extended rules). Both are valid Lite entries; see [bootstrap](skills/bootstrap/SKILL.md), [adopt](skills/adopt/SKILL.md) and [updates](docs/how-to-update.md). Existing projects keep their current integration unless deliberately changed.
3. Implement a real task with the existing tools and relevant functional checks. Enable only the [optional profiles](profiles/README.md) you actually need; no separate security preflight or Docker requirement.

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
