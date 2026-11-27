# ADS — Agent Development Standard

ADS is a **lightweight development convention**, not an orchestration system, approval engine, task database or OS sandbox. Its purpose is to help coding agents finish an authorized goal, verify what actually changed and avoid unnecessary development blockers.

**Version status:** [v0.8.1 Refine, Don't Reinvent](https://github.com/Skyline-Gazer/ADS/releases/tag/v0.8.1) is the **published, final framework release** (annotated tag `v0.8.1`, commit `d19bacb2725975d69b13a9e77efeb7ddc31ef790`, [release notes](docs/releases/v0.8.1.md), Release PR #148); the ADS framework is frozen at this version. The previous baseline, [v0.8.0 Personal Engineering Glue](https://github.com/Skyline-Gazer/ADS/releases/tag/v0.8.0), remains immutable at `178212c41cce8fbf9354d4066e0f77341f6f23c4`. Pin a published tag or full commit SHA; consumer updates remain separate reviewable changes.

## Status — the active deliverable is personal instructions

The only actively maintained deliverable is [personal/AGENTS.md](personal/AGENTS.md): one short file, independent of host, stack and provider, installed as your global agent instructions. A project's own `AGENTS.md` then adds only that project's real facts and constraints, versioned by its ordinary Git history.

Install it by copying `personal/AGENTS.md` into the host's global instruction file (for example `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`), keeping any host-specific imports around it. It changes through ordinary reviewed commits — no release, tag or benchmark cycle. How a host loads instructions is up to that host; the file is plain Markdown and asserts no host-specific guarantee.

Everything else here — `STANDARD.md`, `SAFETY.md`, `QUALITY.md`, the Skills, the optional profiles, the governance scripts and the consumer adoption framework — is published reference material for the frozen v0.8.1 framework. It stays accurate, immutable in history and usable by projects that already adopted it; it is not extended further.

**Default is development-first:** no Docker/VM/OS sandbox, SCA/SBOM/license inventory, security-only reassessment or extra CI is required just to develop ordinary project code. These are opt-in hardening capabilities. ADS does **not** enforce filesystem/process isolation, and an agent must still respect actual task scope, host/tool denials, secrets and consequential production/privilege/spending authorization.

**What stays:** relevant build/tests/functional CI, material code review, the project's configured Git provider/PR workflow, and truthful **Process / State / Outcome** reporting. See [STANDARD](STANDARD.md), [SAFETY](SAFETY.md), [QUALITY](QUALITY.md). Optional tooling and stricter governance are in [profiles](profiles/README.md).

**License:** [MIT](LICENSE).

## Frozen framework — one-message adoption (historical)

This flow belongs to the frozen v0.8.1 framework and is no longer the recommended default; new work should start from `personal/AGENTS.md` above. It remains valid for projects that deliberately choose the full standard.

In an existing project, send your coding agent **one request**. Replace only the last line with your goal or a reference to an existing Plan, Spec, Issue or Project; no special task format or separate ADS installer is needed:

```text
Adopt ADS Lite from https://github.com/Skyline-Gazer/ADS at its current published
release, unless this request names an exact ADS commit SHA for a pilot. Do not substitute
a moving branch or the published release when an exact pilot SHA is specified.
Inspect this project first: existing AGENTS.md, source, build/tests, Git provider, PR/CI,
deployment effects and permissions. Read that exact ADS revision's templates/AGENTS.md and
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

For a pre-release cold-start pilot, append `ADS candidate SHA: <full commit SHA>` to the same request; the Agent must fetch that exact revision and must not claim it is a published release. Count actual owner-interaction rounds, not just the questions asked within a round.

This is an **instruction to the agent**, not a new ADS runner. An agent that cannot read
the release or lacks a required host permission must report the specific limitation
instead of claiming that adoption or delivery succeeded.

## Frozen framework reference

1. Read [Lite adoption](docs/lite-adoption.md) and use the [project AGENTS.md template](templates/AGENTS.md) to record real project facts: purpose, build/tests, Git/deploy effects and sensitive operations.
2. Choose **standalone** (commit the self-contained `AGENTS.md`, no ADS checkout) or **pinned submodule** (add `.ads` at an immutable approved SHA to load the extended rules). Both are valid Lite entries; see [bootstrap](skills/bootstrap/SKILL.md), [adopt](skills/adopt/SKILL.md) and [updates](docs/how-to-update.md). Existing projects keep their current integration unless deliberately changed.
3. Implement a real task with the existing tools and relevant functional checks. Enable only the [optional profiles](profiles/README.md) you actually need; no separate security preflight or Docker requirement.

## Frozen framework — core rules

- [STANDARD.md](STANDARD.md) — autonomous execution, scope and delivery.
- [SAFETY.md](SAFETY.md) — scoped authorization and risk.
- [QUALITY.md](QUALITY.md) — adaptive testing and evidence.
- [AGENTS.md](AGENTS.md) — working **in ADS itself** (full Git governance applies here).

## Skills and profiles

- [skills/](skills/) — bootstrap, adopt, deliver, recover.
- [profiles/](profiles/) — optional strict Git, consumer toolchain, lifecycle.

## Further reference

- [docs/agent-adoption.md](docs/agent-adoption.md) — dual-entry adoption, host Skill discovery and submodule updates.
- [docs/git-governance.md](docs/git-governance.md) — **mandatory inside ADS**; optional profile for consumers.
- [docs/host-filesystem-boundary.md](docs/host-filesystem-boundary.md) — local TUI read/write containment guidance.
- [docs/native-subagent-safety.md](docs/native-subagent-safety.md) — delegation boundaries.
- [scenarios/](scenarios/) — archived acceptance evidence (not required reading for lite adoption).

## Framework design principles (historical)

Goal-driven execution; minimum sufficient implementation; project-local `AGENTS.md` as entrypoint; environment-first reuse; remote-first verification when it helps; truthful verification labels; low-risk autonomous delivery inside scope; explicit approval for sensitive effects. Optional profiles add strict Git, toolchain, or lifecycle discipline—never by default.

## Migration, publication and maintenance

Released baselines stay immutable; consumer ADS pin updates are separate reviewable PRs. See [docs/how-to-update.md](docs/how-to-update.md) and release notes under [docs/releases/](docs/releases/).

ADS framework development ended at v0.8.1. Maintenance is limited to `personal/AGENTS.md` and factual corrections to this frozen reference material; the repository's existing required Git/CI rules still apply to those changes.
