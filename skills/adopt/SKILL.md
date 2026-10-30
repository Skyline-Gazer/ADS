---
name: adopt
description: Adopt ADS in an existing codebase or simplify legacy Trellis, Comet, OpenSpec and agent workflows without weakening real safeguards.
---
# Adopt ADS safely

Default path: [lite adoption](../../docs/lite-adoption.md). Do not auto-change Provider, remotes, or the ADS gitlink.

1. Inventory existing AGENTS.md, hooks, CI, deployment triggers and issue/PR habits. Separate executable controls from Markdown-only descriptions.
2. On local TUI adoption, apply [host filesystem boundary](../../docs/host-filesystem-boundary.md) before sensitive discovery when personal data could be exposed.
3. Inspect host-native Skills, runtimes and working test commands; reuse before replacing.
4. Prefer a pinned ADS submodule at `.ads`; migrate from vendored copies on an isolated branch ([how-to-update.md](../../docs/how-to-update.md)).
5. Render or update root `AGENTS.md` from [templates/AGENTS.md](../../templates/AGENTS.md) with project facts and `.ads` rule pointers.
6. Enable optional profiles **only** when the owner names them in `AGENTS.md` ([profiles/README.md](../../profiles/README.md)): strict Git, consumer toolchain, strict lifecycle.
7. Remove obsolete mandatory hooks or duplicated policy **only** after understanding operational effect; preserve legitimate security and release gates.
8. Validate with one small real task or rehearsal; report checks not run.

Never silently rewrite production configs, rotate credentials, or merge high-risk migrations without scoped authorization.

## Provider note

Read [provider selection](../../docs/git-provider.md). CNB adoption follows [CNB review](../../docs/cnb-review.md) only when the owner configured CNB Primary.
