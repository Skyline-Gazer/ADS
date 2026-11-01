---
name: bootstrap
description: Initialize a new software project with only the structure, tests, CI and guidance justified by its goals and stack.
---
# Bootstrap a new project

Follow [lite adoption](../../docs/lite-adoption.md) unless the owner already enabled optional profiles in `AGENTS.md`.

1. Read the user's goal, host restrictions and chosen ADS pin. Do not copy ADS governance or toolchain scripts by default.
2. Honor the actual project access grant. [Host filesystem containment](../../docs/host-filesystem-boundary.md) is optional and is not a preflight for ordinary development. Never probe private folders to claim a sandbox pass.
3. Discover what exists: native Skills, installed runtimes, lockfiles, declared scripts. Record **installed**, **configured**, **verified** with a short read-only scan.
4. Infer the smallest runnable stack from findings; ask only for consequential product decisions.
5. Create a minimal vertical slice with lockfile, build/test scripts, and CI only if it materially improves verification.
6. Add ADS as a pinned submodule at `.ads` ([how-to-update.md](../../docs/how-to-update.md)); verify clone access without embedding secrets in `.gitmodules`.
7. Render [templates/AGENTS.md](../../templates/AGENTS.md) at the repository root with actual commands, deploy effects and sensitive-operation boundaries.
8. Copy optional profile assets **only** when listed in the rendered `AGENTS.md` ([profiles/README.md](../../profiles/README.md)).
9. Validate with the lowest-cost checks that detect real behavior; prefer existing remote CI when available ([remote-first verification](../../scenarios/remote-first-verification.md)).

Output: code-ready project and a concise summary. No multi-stage approval workflow.

## Provider note

Read [provider selection](../../docs/git-provider.md) before GitHub-specific automation. Preserve existing remotes unless the owner chooses otherwise.
