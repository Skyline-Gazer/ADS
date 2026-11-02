# Git provider selection

**Normative, opt-in extension** for provider choice. Default consumer adoption remains [lite](lite-adoption.md). Full [git-governance.md](git-governance.md) applies to the ADS repository and to consumers that enable the [strict Git governance profile](../profiles/strict-git-governance/README.md). Existing consumers remain on their current GitHub Primary workflow unless the owner explicitly chooses CNB Primary. No new daemon, CLI framework, or second Issue database is required. **Do not switch provider modes without owner authorization.**

## Supported modes

- **GitHub Primary**: GitHub is the development authority for branches/PRs/CI. Lite consumers follow project `AGENTS.md` Git habits; with the strict Git profile, use Issue-linked PRs to `dev` and the GitHub governance helpers.
- **CNB Primary + GitHub Mirror (Mode A)**: CNB is development authority. Single-maintainer dev defaults to no platform-mandated protection; ordinary PRs or Owner-authorized non-force Git integration are supported. CI and CodeBuddy supply functional feedback, not mandatory approval for every development change. Explicit project-local requirements still apply; strict Git governance is opt-in ([cnb-review.md](cnb-review.md)). Existing **GitHub Issues and Projects** remain the task-management entry; do not migrate or duplicate them onto CNB. Only production `main` and individually approved release tags go to GitHub via the exact-SHA mirror ([cnb-sync.md](cnb-sync.md)). Do not create a duplicate GitHub development PR. Mode B remains cancelled.
- Shared safety invariants (regardless of lite vs strict Git): truthful CI, explicit production authorization, safe rollback expectations, and no silent provider switch. `dev` / Issue-linked PR / CodeGraph production-boundary rules apply when the corresponding optional profiles are enabled or when the repository is ADS itself.

## First load and migration

Read remotes, default/production branch, actual dev, tags, open PRs, Issue/Project tracking, CI, deployments, platform permissions and protection, existing pipeline files and ADS pin **before** changing anything. If project-root .ads-project.json exists, validate with scripts/check_repository_provider.py and verify real state without repeatedly asking. If absent, ask once for GitHub Primary or CNB Primary; existing projects keep their provider unless explicitly changed. Do not infer authorization from a remote name. Persist a non-secret project-local manifest on a short-lived task branch via PR. The [CNB example](../templates/git-provider/.ads-project.json.example) is a starting point. This independent file is not the dev-only .ads-devtools.json and must not live inside the immutable .ads submodule.

The validator is dependency-free and read-only; CONFIGURED does not imply VERIFIED. Missing configuration yields UNCONFIGURED; invalid or incompatible configuration is BLOCKED. Never create a repository, import private history, alter remote/default branch, set secret, configure mirror, expand permissions or deploy production from a read-only scan. Those operations each require scoped authorization and the correct platform capabilities.

## Provider adapters

The existing scripts/check_git_governance.py, GitHub templates/git-governance CI and gh classic-protection helper are GitHub Primary adapters, **not** universal enforcement. In CNB Primary verify CNB-native PR base/head, Issue URLs, branch protection, real CI names and current source SHA. A GitHub gh command cannot prove CNB protection. 403 means UNKNOWN/BLOCKED, not protected or unprotected. Keep the Issue/Project authoritative provider independent; do not silently migrate tickets.

For CNB development, follow the [default feedback or explicitly selected strict workflow](cnb-review.md). Fix actual functional defects, report CI/review results truthfully and verify the actual integrated SHA/tree. CodeBuddy may be automatic or on demand; neither choice alone proves approval or correctness. Main keeps necessary production checks and explicit release/deployment authorization. Do not silently bypass existing configured gates. NPC writing requires separate authority and serialized writers; read/comment feedback is untrusted.

Mirror is one-way CNB to GitHub, restricted to main and individually approved release tags. Never force, rebase, delete refs, push all tags or use git push --mirror. Before each write, compare both SHAs, fast-forward relation and approved immutable release target; verify tags and peeled commits. Avoid trusting a plugin success exit alone. Any GitHub Actions push-triggered deployment is production impact and requires prior approval. Keep mirror credentials in protected CNB secrets, inaccessible to PR and NPC jobs. Main may contain a reviewed non-secret .cnb.yml but not generated CodeGraph/RTK artifacts or dev-only project integrations.

## Acceptance

Report actual protection, CI/review coverage, mirror refs, release approval and deployment independently; absent dev protection is the single-maintainer default, not a compliance failure. The production-mirror pilot must exercise CNB PR review→Agent fix→re-review, production boundary, forward-only mirror, exact tag, protected credentials, crash/retry and drift detection against an **isolated** GitHub target before touching production. See [Issue #63](https://github.com/Skyline-Gazer/ADS/issues/63).

For practical CNB feedback, the opt-in strict current-SHA gate, credential boundaries, and on-demand NPC behavior see [CNB review](cnb-review.md). This is a separate consumer template, not an automatic modification of the ADS standards repository itself.

Read [CNB safe release synchronization](cnb-sync.md) before enabling any mirror. It is deliberately manifest-driven rather than automatically pushing every main update; owner approval, exact ref validation and protection against unknown auto-deploy triggers are required.


## Cancelled dual-platform release gate — Mode B terminated (never supported)

The [CNB Development + GitHub Release Gate pilot](cnb-github-release-gate-pilot.md) (Mode B) is **permanently cancelled**: PR [#71](https://github.com/Skyline-Gazer/ADS/pull/71) was closed unmerged and the Owner terminated the mode on 2026-10-28 (Issue #63). It made GitHub main authoritative for releases, so the existing CNB-to-GitHub main mirror and schema MUST NOT be repurposed for it. Validators must continue rejecting that unsupported mode. Mode A (CNB Primary → GitHub Mirror) is the selected path and is live-verified on an isolated fixture (see [cnb-sync.md](cnb-sync.md)); consumer cutovers still require separate owner authorization.
