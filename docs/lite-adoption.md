# Lite adoption (default)

**Status: normative default for projects adopting ADS.**

ADS is a short, agent-readable rule set—not a second application copied into your repository. The default path keeps coupling low so feature work stays on your product code.

## What lite adoption includes

1. **Pinned submodule** at `.ads` (or another free path) pointing to an approved ADS release or commit.
2. **Root `AGENTS.md`** rendered from [templates/AGENTS.md](../templates/AGENTS.md) with **project facts only**: purpose, build/test commands, deployment triggers, sensitive operations, and pointers to `.ads/STANDARD.md`, `.ads/SAFETY.md`, `.ads/QUALITY.md`.
3. **Optional native Skill exposure** by copying or linking only the ADS skills you use (`bootstrap`, `adopt`, `deliver`, `recover`) into the host's documented skill path—after a harmless discovery test.

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

## Submodule updates

Follow [how-to-update.md](how-to-update.md): one reviewable PR that advances the `.ads` gitlink when the owner approves. Do not auto-track ADS `main`. Updating ADS does not require upgrading optional profile scripts unless the owner uses those profiles.

## What lite still preserves

Lite removes unnecessary script copies and ceremony. It does **not** remove, for projects that already use them:

- Task branches, PRs, Review, CI, Agent repair, and owner-authorized merge loops
- CNB Primary CodeBuddy comment disposition, current-SHA re-review, CI, and Agent-initiated **manual** merge ([cnb-review.md](cnb-review.md))
- Host/OS safety boundaries in [SAFETY.md](../SAFETY.md) and [host-filesystem-boundary.md](host-filesystem-boundary.md)

## ADS repository itself

Contributing to ADS still follows [git-governance.md](git-governance.md) in full. The ADS repo keeps both `dev` (general) and `cnb/dev` (CNB-specialized integration) lines; Lite lands on `dev` first, then integrates into `cnb/dev` without force-overwriting CNB workflow specialty. That dual-line requirement does not automatically apply to lite consumers.

Consumers pin a **single** published release (for example v0.5.0)—there is no separate `v0.5.0-cnb` tag.
