# Using ADS with an existing coding agent

ADS is not a daemon, CLI or centralized policy delivery service. A file existing in ADS does not make the host agent automatically discover it.

## Default: lite adoption

Follow [lite-adoption.md](lite-adoption.md) and choose **one** entry intentionally; existing projects keep their current integration unless deliberately changed:

1. Pick an approved ADS release or immutable full commit SHA.
2. **Standalone:** copy [templates/AGENTS.md](../templates/AGENTS.md) to the repository root, fill in real project facts and commit it. The copied working agreement is self-contained; record the adopted ADS full source commit SHA (required) — plus the release tag when the copy came from a tagged release — at the `Source:` line. No `.ads` checkout, clone access or external rule fetch is required.
3. **Pinned:** add ADS as a Git submodule at `.ads` at that exact approved SHA ([how-to-update.md](how-to-update.md)), with authorized clone access, then render the same template with real project facts and pointers to `.ads/STANDARD.md`, `.ads/SAFETY.md` and `.ads/QUALITY.md`. Never follow a moving branch.
4. Expose needed skills through the host's documented discovery path; test with a harmless prompt. Native Skill discovery is host-specific: when it is unavailable, keep the explicit document-pointer route instead of inventing an ADS-specific installer or loading protocol.

Do **not** copy ADS scripts, governance checkers, or toolchain preflights unless the owner enables an [optional profile](../profiles/README.md) in `AGENTS.md`.

## Submodule updates

At owner request or a configured periodic trigger, compare approved upstream releases to the recorded gitlink without changing it. Upgrades are isolated PRs that advance the gitlink after review ([how-to-update.md](how-to-update.md)). `git submodule update --init` only materializes the existing pin.

## Optional profiles

| Profile | When to enable |
| --- | --- |
| [Strict Git governance](../profiles/strict-git-governance/README.md) ([git-governance.md](git-governance.md)) | Owner wants `dev`, Issue-linked PRs, optional branch-protection helper |
| [Consumer developer toolchain](../profiles/consumer-devtoolchain/README.md) | Owner wants CodeGraph + full RTK and production-boundary guards |
| [Strict lifecycle](../profiles/strict-lifecycle/README.md) | Owner wants drift receipts and strict post-merge reconciliation |

## Optional third-party Skills (advisory, never required)

Skill files follow the open [Agent Skills specification](https://github.com/agentskills/agentskills) (`SKILL.md` + frontmatter, progressive disclosure: metadata catalog → body on match → bundled references on demand); ADS's own Skills conform to it. ADS adds **no** loading protocol, registry, lockfile schema or router of its own.

- **Install (optional):** copy the skill folder into a host-discoverable project path yourself, or use a mature existing installer such as the `skills` CLI (vercel-labs/skills, MIT; `1.9.0` verified on 2026-11-25 — a point-in-time observation, not a permanent ADS tool policy) with telemetry disabled (`DISABLE_TELEMETRY=1`). Its `skills-lock.json` records the source commit SHA and content hash; a plain copy with a source URL + full SHA + license note is equally valid. Nothing here is mandatory, and no upstream script is executed on install without review.
- **Evidence ladder — report each level separately:** installation → host discovery → explicit read → recommendation applied → behavioral adoption. Installation never proves discovery; adoption requires observed task outcomes; an absent optional Skill degrades to ordinary authorized work, never a false PASS.
- **Host interop:** the CLI supports many per-host directory sets (Claude, Codex, Cursor, CodeBuddy and more — see its own agent docs for the exact path per host). **OMP is not in its host list:** it benefits only **passively**, because the CLI's universal flat `.agents/skills/<name>/SKILL.md` layout is exactly what `omp/19.1.1` was observed to discover non-recursively — passive interop, not native support. Nested installer layouts may not be discovered at all; verify one harmless prompt per host after any change.
- **Effective external references:** when reproducibility is intended, pin what the Skill *reads or fetches at use time* too (guideline docs, remote checklists): record the immutable revision, integrity and applicable license, and verify material dependencies at adoption. A pinned Skill file alone does not pin its external rule references.
- **ADS-owned Skills boundary:** the relative links inside `.ads/skills/*/SKILL.md` resolve only within a pinned or fully vendored ADS tree, so those Skills load **as published** under the pinned entry or after complete vendoring with rewritten links. Standalone adoption carries the needed guidance through the self-contained root `AGENTS.md`; copying an ADS Skill file into a standalone project is an ordinary vendored project edit that requires fixing its relative links — do not claim standalone installation of ADS's own Skills as published.

## Boundaries

- Private ADS requires explicit read permission for each host and CI job that needs it.
- Agents cannot continue after session end unless the host offers persistence.
- Native deployment integrations remain authoritative; ADS does not add a deploy controller.
- Never claim successful adoption without checking executable restrictions the project actually uses.

## Provider note

Read [provider selection](git-provider.md) before GitHub-specific `gh` steps. CNB Primary consumers use CNB-native PR/CI; do not require duplicate GitHub PRs unless configured.
