# How to install and update ADS (AI-native Git Submodule)

ADS is guidance, **not an auto-updating executable**. Default [Lite adoption](lite-adoption.md) offers two valid options: a self-contained root `AGENTS.md` alone, or that same file plus an immutable pinned `.ads` Git submodule for extended rules. Neither requires copied scripts unless an optional profile is enabled. Read [SAFETY.md](../SAFETY.md) for actual authorization limits.

## Standalone Lite — no submodule

Copy [templates/AGENTS.md](../templates/AGENTS.md) to the repository root, fill in actual project facts and commit it using the project's existing branch/PR process. The copied working agreement is self-contained: no `.ads`, GitHub authentication or external policy fetch is required to begin authorized coding. Review any future template update as an ordinary change to that tracked file; do not silently overwrite project-local instructions.

## Optional pinned submodule — install once

Run in the consumer repo with an existing working Git checkout and confirmed access to ADS:

```sh
git submodule add https://github.com/Skyline-Gazer/ADS.git .ads
git -C .ads checkout v0.2
git add .gitmodules .ads AGENTS.md
git commit -m "chore: adopt ADS as pinned submodule"
```

`v0.2` above is an example **published release**, not an instruction to use the unreleased v0.3 candidate. Use the latest owner-approved released tag or SHA after checking its availability and compatibility. The Git checkout commit, not the mutable tag spelling or branch, is the effective pin. The root `AGENTS.md` must contain actual project facts and point to `.ads/STANDARD.md`, `.ads/SAFETY.md`, `.ads/QUALITY.md`, and relevant `.ads/skills/*/SKILL.md`. Populate AGENTS.md before staging; the command assumes it exists. Do not copy duplicated rules into host adapters. Native Skill discovery is host-specific: symlink/copy only selected skills into the documented path, then actually test loading after installing and after upgrading.

Because ADS may be **private**, the clone/update runner needs legitimate repository read access. Public Actions checkout credentials do not automatically grant another private repository access. Never put a PAT or secret-bearing URL into `.gitmodules`; use existing authorized credentials in the host/CI. Inaccessible submodule is a BLOCKER, not successful adoption. Existing repo with `.ads` or a different submodule? Inspect and plan a non-destructive migration instead of overwriting.

## Important: update vs upgrade

```sh
git submodule update --init --recursive
git submodule status .ads
git -C .ads rev-parse HEAD
```

These commands materialize the **already pinned gitlink**; they **do not** advance to the newest ADS release. This is intentional. Do not enable background `git submodule update --remote` against `main` as an unchecked policy upgrade.

## AI-native update check (discovery only)

**Triggers:** when explicitly asked; lightweight check at an appropriate Phase/Milestone closure before the next Phase; optionally on a new task/session if the previous check is stale; and periodic checks **only if** the project owner has explicitly configured an existing scheduler or GitHub workflow. There is no ADS daemon, global hook, hidden updater or implicit recurring task.

An agent should:

1. Identify the pinned `.ads` gitlink commit and current accessible rules. Check working tree and nested submodule cleanliness; avoid touching unrelated modifications.
2. Discover trusted published releases/tags and compare the current SHA to the selected **approved target**, using existing authorized GitHub integration or Git transport. Do not infer that a larger version string is safe; classify status as **CURRENT / UPDATE_AVAILABLE / INACCESSIBLE / DIRTY / UNKNOWN**. An unreleased candidate is not a stable default.
3. If a newer approved revision exists, review `git diff OLD_SHA..NEW_SHA` (from the ADS repository) covering `STANDARD.md`, `SAFETY.md`, `QUALITY.md`, Skills, templates and migration notes. Classify compatibility with project-specific rules, currently installed host Skills, CI/security gates and deployment effects. Summarize breaking/adaptation changes.
4. For a safe scoped change, make an isolated project branch, advance the submodule gitlink to the approved exact commit and update root AGENTS.md pin/pointers or host-native skill links only as needed. Execute targeted project tests, Skill discovery and CI; create a concise PR explaining old/new SHAs and migration effects. Never silently merge a change that alters security/production authorization or auto-deploy semantics.
5. At the relevant Phase boundary, reconcile the update Issue/Project status using [milestone-reconciliation.md](milestone-reconciliation.md). Do not confuse ADS pin change with successful adoption or production validation.

To prepare a proposed upgrade inside the consumer's task branch, after verifying the target is trusted and accessible:

```sh
git -C .ads fetch --tags origin
git -C .ads checkout APPROVED_ADS_COMMIT_SHA
git add .ads AGENTS.md
git diff --cached --submodule=log
```

Then use the consumer's existing test command, review the diff and open a PR. Only commit AGENTS.md if it actually changed. Prefer one reviewable pin change per PR. No automatic `--remote`, force checkout, destructive `submodule deinit`, or update of nested dependencies without a known effect.

## Rollback and clean setup

If an update fails before merging, return the proposed gitlink to the consumer's original recorded SHA in the task branch, restore only changes made by that update, and rerun applicable checks. After a reviewed rollback commit, collaborators run:

```sh
git submodule sync --recursive
git submodule update --init --recursive
```

The parent Git history preserves the old and new gitlinks. Do not roll back unrelated project content or rewrite published history to mask a regression.

## Existing projects at ADS v0.2/v0.3

First identify whether ADS is a vendored copy, a bare remote link, existing host Skill copy, an independent local checkout, or already a submodule. Preserve the project's existing rules and deployed behavior. Choose the path `.ads` only if it is free and compatible. Introduce `.gitmodules` and the pinned gitlink on an isolated branch; replace redundant copied files **only after** mapping current references and completing host discovery/tests. Projects cannot be silently migrated or updated merely because the ADS source repo released a new version.

## Minimal acceptance

See [submodule-update.md](../scenarios/submodule-update.md). The policy itself is documented here; a successful cross-repository checkout, private access and project-specific migration require their own real test evidence.
