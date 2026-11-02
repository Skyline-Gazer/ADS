# Lite adoption (default)

**Status: normative default for projects adopting ADS.**

ADS is lightweight agent guidance, not a separate application. **Either a self-contained project-root `AGENTS.md` or a project-root `AGENTS.md` plus a pinned `.ads` submodule is a valid Lite entry.** Choose one intentionally; neither requires new tooling, a Docker host or a security preflight.

## What lite adoption includes

1. **Standalone:** copy [templates/AGENTS.md](../templates/AGENTS.md) to project root, fill real project facts, commit the file. Its working agreement is self-contained; no `.ads` directory or further rule files are needed for ordinary development. The project's own Git commit is the immutable version of the copied instructions.
2. **Pinned:** use the same root template plus an optional `.ads` submodule at an approved immutable ADS commit/tag. The template then points to `STANDARD.md`, `SAFETY.md`, `QUALITY.md` inside that exact gitlink. No auto-update.
3. **Optional native Skills:** expose only needed Skills (`bootstrap`, `adopt`, `deliver`, `recover`) through the host's supported discovery path. Neither entry requires native Skills or a package installation.

That is sufficient for autonomous agent development on most personal projects.

## What lite adoption does *not* require

Do **not** copy these into a consumer repository unless the owner explicitly enables the matching [optional profile](../profiles/README.md):

- CodeGraph / RTK preflight scripts or manifests ([consumer developer toolchain profile](../profiles/consumer-devtoolchain/README.md))
- `ensure-ads-branch-protection.py`, consumer `check_git_governance.py`, or other governance scripts ([strict Git governance profile](../profiles/strict-git-governance/README.md))
- Lifecycle drift receipts or post-merge SHA reconciliation rituals ([strict lifecycle profile](../profiles/strict-lifecycle/README.md))
- Phase-end GitHub Project reconciliation (only when the owner tracks Phases in Project)

## Git workflow under lite adoption

Use whatever branch and PR habit the **project `AGENTS.md`** declares. Lite template does **not** mandate a `dev` branch, Issue-per-task, or copied branch-protection helpers.

If the owner wants ADS-style `dev` + Issue-linked PRs, enable the [strict Git governance profile](../profiles/strict-git-governance/README.md) in `AGENTS.md`—do not infer it from ADS alone.

## Updates

Standalone: update the project-root `AGENTS.md` through an ordinary reviewed project change, comparing relevant new guidance with the project's existing requirements. No external ADS fetch is needed to keep working on the current copy.

Pinned submodule: follow [how-to-update.md](how-to-update.md): one reviewable PR advancing the `.ads` gitlink when the owner approves. Do not auto-track ADS `main`. Optional profile scripts update only if those profiles are enabled.

## What lite still preserves

Lite removes unnecessary script copies and ceremony. It does **not** remove, for projects that already use them:

- Task branches, PRs, Review, CI, Agent repair, and owner-authorized merge loops
- CNB Primary CodeBuddy comment disposition, current-SHA re-review, CI, and Agent-initiated **manual** merge ([cnb-review.md](cnb-review.md))
- Actual authorization limits in [SAFETY.md](../SAFETY.md). Host/OS isolation in [host-filesystem-boundary.md](host-filesystem-boundary.md) is optional, not a prerequisite for ordinary coding or PRs.

## ADS repository itself

Contributing to ADS still follows [git-governance.md](git-governance.md) in full. The ADS repo keeps both `dev` (general) and `cnb/dev` (CNB-specialized integration) lines; Lite lands on `dev` first, then integrates into `cnb/dev` without force-overwriting CNB workflow specialty. That dual-line requirement does not automatically apply to lite consumers.

Pinned consumers use one approved immutable release/commit (never a floating `cnb/dev` tag); standalone consumers version their copied `AGENTS.md` in the project itself. CNB specialization is integrated into the shared ADS rules, not released as a separate tag.
