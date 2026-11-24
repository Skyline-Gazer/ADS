# Working on ADS itself

ADS is a lightweight standard, not a new execution framework. Read README.md, STANDARD.md, SAFETY.md, QUALITY.md and [docs/lite-adoption.md](docs/lite-adoption.md) before structural changes. Keep capabilities agent-native: SKILL.md files, concise templates and optional profiles. Do not add a CLI, runner, state machine, duplicate tracker or deployment system unless separately authorized.

**Consumer defaults are lite.** CodeGraph/full RTK, strict Git scripts and lifecycle receipts are optional profiles for adopters—do not reintroduce them as mandatory defaults. Do not install CodeGraph/RTK in the ADS repository as part of consumer policy.

Preserve project-local limits. Prefer remote CI and target-platform previews when relevant; if absent, autonomously provision a minimal task-scoped remote environment within existing authorization. Ask the user only for the exact missing owner action when a real boundary is reached. Keep local validation lightweight.

ADS itself must follow [docs/git-governance.md](docs/git-governance.md): ordinary task branches from latest `dev`, Issue reference, PR to `dev`—never push task commits directly to `dev` or `main`. Treat `main` promotion as a separate release PR. Cloud Agent `cursor/*` branches are recognized task branches. ADS maintains one canonical normative source on `dev`/`main` with conditional provider capabilities; the former `dev`-to-`cnb/dev` synchronization strategy is superseded and `cnb/dev` is a preserved historical retirement candidate (do not push new normative work to it or delete it without separate authorization).

Provider-aware adoption: [docs/git-provider.md](docs/git-provider.md). ADS itself remains GitHub Primary unless separately authorized to migrate. Mode B stays cancelled. Exact-SHA Mode A mirror and consumer GitHub sync-branch PR flows are **not** interchangeable ([docs/cnb-sync.md](docs/cnb-sync.md)).

Keep released v0.4.x history immutable. Single published consumer tag for v0.5.0 (no `v0.5.0-cnb`).
