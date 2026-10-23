# Consumer-project developer toolchain: CodeGraph + full RTK

**Scope:** This policy applies to software projects that adopt ADS. It does **not** require CodeGraph or RTK to be installed or initialized in the ADS standards repository itself.

## Required outcome

Every ADS consumer project must use both tools during development:

- **CodeGraph** for code navigation and impact analysis.
- **Full RTK** for supported command-output compression. Do not substitute `rtk-oss`.

The tools are required capabilities, not optional recommendations. They are developer-environment tools, not production runtime dependencies.

## When to check

Run the preflight when:

1. bootstrapping a new consumer project;
2. adopting ADS into an existing repository;
3. starting a development session that will inspect or change source code;
4. switching to a different consumer repository or development worktree;
5. a tool's availability/version was previously blocked or may have changed.

For each tool, distinguish **installed**, **latest stable**, **project initialized**, **host integration active**, and **verified**. Record the executable path, actual version, official upstream release URL, project status, and smoke-test result. Never treat installation alone as successful adoption.

Official sources:
- CodeGraph: https://github.com/andysom25/codegraph
- Full RTK: https://github.com/rtk-ai/rtk
- RTK edition/licensing details: https://github.com/rtk-ai/rtk/blob/develop/docs/guide/resources/editions.md

## Latest stable is a moving requirement

Use the latest stable upstream release every time the tool is installed or updated. Do not permanently pin an old CodeGraph or RTK version in consumer-project configuration.

- Query the official upstream release source during bootstrap/adoption and before relying on the tools.
- If a tool is missing, ask the user before installing it. State the proposed latest stable version, official source, installation method, license implications, and whether the change is global or project-local.
- If installed but outdated, update to latest stable only within existing authorization. Ask for the exact approval needed if the update requires a global configuration change, elevated privileges, or another action outside scope.
- After installation/update, verify the actual executable version and run a smoke test.
- If the upstream source cannot be reached, mark freshness `UNVERIFIED` or `BLOCKED`. A cached version or an old manifest is not evidence that a tool is latest.
- Exclude prerelease/nightly builds unless separately authorized.

The latest-version check is dynamic. Record observed versions in run evidence, but do not turn them into a permanent version pin.

## Consumer branch boundary — mandatory

The consumer must follow the mandatory [Git governance policy](git-governance.md): `dev` is the required development/integration branch, and every ordinary task branch starts from the latest `dev`. CodeGraph/RTK project configuration may exist on `dev` and its task branches, but must not enter the consumer's production `main` branch or production release/deployment artifacts. If the consumer has no `dev`, establish it through a reviewable migration before normal implementation.

1. Identify the consumer's actual production branch from repository facts; use `main` when that is the project's production branch.
2. Initialize CodeGraph and configure the host's RTK integration only in a consumer development checkout. Do not perform first-time project initialization on production `main`.
3. Keep the consumer manifest (normally `.ads-devtools.json`), CodeGraph/RTK integration files, host-specific developer hooks, and tool-specific project configuration on development branches only.
4. Before merging any consumer PR into production `main`, check the exact candidate tree and distributable artifacts. Fail closed if any tool configuration or generated artifact would enter production.
5. Keep a generic production-boundary guard and its CI workflow in the consumer repository if needed. The guard is policy enforcement, not a CodeGraph/RTK integration; it may remain on `main`.
6. Do not commit generated CodeGraph databases/indexes, caches, RTK binaries, transient session/telemetry data, secrets, or machine-specific absolute paths to any branch. Keep reproducible project integration/configuration in Git only on the consumer development branch.

ADS itself may publish this normative document, Skills, generic templates, and policy tests. Those are not the consumer project's actual tool configuration or generated tool artifacts.

## Consumer manifest

The template [`.ads-devtools.json.example`](../templates/consumer-devtools/.ads-devtools.json.example) is a starting point. Copy it to `.ads-devtools.json` **only on the consumer development branch**. It must declare the latest-stable policy rather than a fixed version. Populate `dev_only_paths` with the exact host configuration files that were modified for these tools.

The manifest is intentionally absent from production `main`. A production-boundary checker must reject the manifest itself and any existing path listed in `dev_only_paths`. If `.gitignore` is modified to ignore CodeGraph-generated data, that modification is also development-only and must be listed in `dev_only_paths`.

## CodeGraph initialization and freshness lifecycle

- If the CodeGraph executable exists but the consumer project is not initialized, initialize it in the development checkout and verify that its index is usable. Do not ask the user to perform safe project-local initialization that the agent can do.
- Prefer CodeGraph's native file watcher/auto-sync and connect-time reconciliation. Do not run `codegraph sync` after every source edit or every Git operation when automatic synchronization is healthy.
- Before relying on graph-based navigation or impact analysis, verify the applicable index state with `codegraph status`, confirm that the monitor/sync path is healthy, and check that the active MCP session points to the correct checkout and index.
- After a relevant source-changing batch or Git operation, ensure automatic synchronization has caught up before using graph results. If a query reports stale data, wait for reconciliation or read the affected source directly; do not treat stale graph results as authoritative.
- Run explicit `codegraph sync` and then `codegraph status` when automatic sync is disabled/unhealthy, pending updates persist, a relevant checkout/merge/rebase/reset was not reconciled, or results are demonstrably inconsistent. If recovery fails, disclose that graph-assisted analysis is unavailable and fall back to direct source inspection.
- Each independently indexed Git worktree must have its own index. Never share one mutable CodeGraph index between distinct worktrees, and verify MCP is bound to the current worktree rather than a stale checkout.
- Use full reindexing only for initial construction, indexing-configuration changes that require it, corruption recovery, or another documented upstream requirement. Do not schedule or trigger a full rebuild for ordinary source edits.
- Keep generated index/database/cache files untracked and ignored. CodeGraph's current upstream README documents `.codegraph/` as its per-project generated index directory; use the [development-only ignore snippet](../templates/consumer-devtools/gitignore.append) on the consumer development branch. Verify any additional generated paths against the installed latest version before adding them.

## Full RTK initialization and verification

- If the `rtk` executable is absent, ask permission before installation. Do not silently install `rtk-oss` as a substitute.
- If full RTK is installed but the consumer host integration is absent, initialize the project-level integration in the development branch and verify it.
- Test the actual active host, not only the binary: run a safe representative command and confirm the host's tool output passes through RTK and is compressed as expected.
- Preserve command exit codes, failure diagnostics and a way to retrieve raw output. Output compression must not hide test failures or security-relevant information.
- Do not silently modify global host settings or global hooks. If the supported integration requires a global change, ask permission for that specific change.
- If the host does not support a project-local adapter, report the exact limitation and request only the missing user action; do not claim the integration is active merely because an instruction file exists.

## Production boundary guard

Copy [`check-production-boundary.py`](../templates/consumer-devtools/check-production-boundary.py) to the consumer repository as `scripts/check-ads-devtools-boundary.py` and [`production-boundary.yml`](../templates/consumer-devtools/production-boundary.yml) to `.github/workflows/ads-devtools-boundary.yml` as a generic merge guard. If the consumer's production branch is not named `main`, update the workflow's branch trigger and `PRODUCTION_BRANCH` value. These guard files may be installed on the consumer's `main`; they do not install or configure either tool.

The guard must run against PR merge candidates targeting the production branch and on pushes to that branch. It checks for the consumer manifest, known generated index/database/cache paths, RTK binaries, and CodeGraph/RTK integration in common host configuration files. Customize the scan for the actual host files used by the project, without allowing the tool integration itself onto production `main`.

Run the guard once with a negative fixture containing a forbidden manifest/artifact (must fail), once with a development-branch target (must permit dev-only placement), and once against a clean production tree (must pass).

## Remote-first validation

Prefer the consumer project's existing GitHub Actions and short-lived test fixtures. Do not create a persistent service or a separate full local environment per project just for these tools.

At adoption and before use, query current upstream releases and check local binaries. For remote release metadata, copy [`check-latest-releases.py`](../templates/consumer-devtools/check-latest-releases.py) to the consumer development branch as `scripts/check-ads-devtools-latest.py` and [`latest-release-check.yml`](../templates/consumer-devtools/latest-release-check.yml) to `.github/workflows/ads-devtools-latest.yml`. This workflow checks the official latest stable release on pushes to development/task branches, PRs targeting `dev`, and manual dispatch; it does not install tools or prove which edition is installed. The local `check-consumer-devtools.py` compares installed versions and package provenance. Do **not** put the tool-specific workflow on production `main` just to enable a schedule: GitHub scheduled workflows normally run only from the default branch. Session preflight plus development-branch remote checks are the default; use a central monitor only if one is actually configured and authorized.

## Licensing and evidence

CodeGraph's upstream repository currently declares MIT; recheck upstream metadata during validation. Full RTK includes BUSL-1.1 and Apache-2.0 components; follow the current upstream terms and do not silently switch editions. The full and OSS editions use the same binary name, so `rtk --version` alone does not prove the edition. Verify package/install provenance (for example, Homebrew formula metadata) or mark the edition UNVERIFIED and request permission to install the full edition from its official source. This is implementation guidance, not a legal opinion.

For each adoption, preserve concise evidence for:
- upstream latest stable release and URL;
- installed executable paths and versions;
- project initialization and host integration smoke tests;
- CodeGraph sync/status after a real source change;
- branch-boundary negative/positive tests;
- checks actually run, failures, fallbacks and unverified areas.

Do not report PASS just because the tools are installed.
