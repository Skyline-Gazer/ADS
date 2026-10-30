# Using ADS with an existing coding agent

ADS is not a daemon, CLI or centralized policy delivery service. A file existing in ADS does not make the host agent automatically discover it.

## Default: lite adoption

Follow [lite-adoption.md](lite-adoption.md):

1. Pick an approved ADS release or immutable full commit SHA.
2. Add ADS as a pinned Git submodule at `.ads` ([how-to-update.md](how-to-update.md)), with authorized clone access.
3. Render [templates/AGENTS.md](../templates/AGENTS.md) at the repository root with **project facts** and pointers to `.ads/STANDARD.md`, `.ads/SAFETY.md`, `.ads/QUALITY.md`.
4. Expose needed skills through the host's documented discovery path; test with a harmless prompt.

Do **not** copy ADS scripts, governance checkers, or toolchain preflights unless the owner enables an [optional profile](../profiles/README.md) in `AGENTS.md`.

## Submodule updates

At owner request or a configured periodic trigger, compare approved upstream releases to the recorded gitlink without changing it. Upgrades are isolated PRs that advance the gitlink after review ([how-to-update.md](how-to-update.md)). `git submodule update --init` only materializes the existing pin.

## Optional profiles

| Profile | When to enable |
| --- | --- |
| [Strict Git governance](../profiles/strict-git-governance/README.md) ([git-governance.md](git-governance.md)) | Owner wants `dev`, Issue-linked PRs, optional branch-protection helper |
| [Consumer developer toolchain](../profiles/consumer-devtoolchain/README.md) | Owner wants CodeGraph + full RTK and production-boundary guards |
| [Strict lifecycle](../profiles/strict-lifecycle/README.md) | Owner wants drift receipts and strict post-merge reconciliation |

## Boundaries

- Private ADS requires explicit read permission for each host and CI job that needs it.
- Agents cannot continue after session end unless the host offers persistence.
- Native deployment integrations remain authoritative; ADS does not add a deploy controller.
- Never claim successful adoption without checking executable restrictions the project actually uses.

## Provider note

Read [provider selection](git-provider.md) before GitHub-specific `gh` steps. CNB Primary consumers use CNB-native PR/CI; do not require duplicate GitHub PRs unless configured.
