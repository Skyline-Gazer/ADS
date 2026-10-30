# Consumer-project developer toolchain: CodeGraph + full RTK

**Optional profile — not [lite adoption](lite-adoption.md).** Enable only when the project `AGENTS.md` lists [profiles/consumer-devtoolchain/README.md](../profiles/consumer-devtoolchain/README.md).

**Scope:** This policy applies to consumer repositories that opted in. It does **not** require CodeGraph or RTK in the ADS standards repository itself.

## Required outcome (when profile enabled)

The consumer project must use both tools during development:

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
- CodeGraph stable package version: official npm `latest` dist-tag at https://registry.npmjs.org/@andysom25%2Fcodegraph/latest **when published**. In its verified absence, use the explicitly approved source SHA fallback instead of pretending that npm 404 is a stable release.
- Full RTK: https://github.com/rtk-ai/rtk
- RTK edition/licensing details: https://github.com/rtk-ai/rtk/blob/develop/docs/guide/resources/editions.md

## Controlled official CodeGraph source fallback (owner-approved for v0.4)

**Default remains latest official stable distribution.** When official CodeGraph npm `latest` returns a genuine HTTP 404 *and* its official GitHub Releases collection is empty, an explicitly authorized, reviewed immutable SHA of `andysom25/codegraph` may be used as `SOURCE_FALLBACK`. This channel is **not** a published stable release; never print `LATEST` or `latest_stable_verified=true` for it.

- Use `check-codegraph-channel.py` to observe official npm, release list, exact upstream SHA and versioned `package.json`/MIT metadata; network failures, suspicious metadata and release-channel presence must fail closed.
- Install/build from a detached, verified full SHA using Node 22 and `npm ci --ignore-scripts && npm run build`; verify actual executable, included assets and license. Do not run unreviewed upstream install scripts; never treat `package.json` version alone as the stable channel.
- Before installing or changing global settings, obtain explicit user approval. Record the approved commit SHA, build output, source license, version, chosen host installation path, and independent hash/provenance attestation; untracked evidence stays off production.
- If official stable distribution returns, prioritize it during the next authorized upgrade and retire source fallback. If upstream HEAD changes, keep the previously reviewed immutable pin; **do not silently upgrade**: require review of actual diff, new SHA and license, then revalidate the project and host integration. Do not weaken full RTK requirements.
- For consumers using this fallback, include `check-codegraph-channel.py` beside `check-consumer-devtools.py` and `check-latest-releases.py`, and use `--codegraph-source-sha <approved-full-sha>` to select the previously reviewed immutable pin during preflight. An observed version match is not full provenance or agent-MCP verification.

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

When this profile is enabled together with strict Git governance, prefer keeping CodeGraph/RTK configuration on the development integration branch and its task branches. Regardless of Git profile, CodeGraph/RTK project configuration must not enter the consumer's production `main` branch or production release/deployment artifacts.

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

Read [the mandatory tool-license policy](tool-licensing.md) and verify edition, actual distributed-version license files, install provenance, usage classification, and license/grant changes *before* upgrading or claiming tool readiness. The [offline evidence checker](../templates/consumer-devtools/check-license-compliance.py) blocks incomplete or incompatible attestations; it does not establish legal authorization or binary authenticity by itself.


CodeGraph's upstream repository currently declares MIT; recheck upstream metadata during validation. Full RTK includes BUSL-1.1 and Apache-2.0 components; follow the current upstream terms and do not silently switch editions. The full and OSS editions use the same binary name, so `rtk --version` alone does not prove the edition. Verify package/install provenance (for example, a checksum-verified official full archive plus its Apache and engine licenses, bound to the actual PATH executable) or mark the edition UNVERIFIED and request permission to install the full edition from its official source. This is implementation guidance, not a legal opinion.

For each adoption, preserve concise evidence for:
- upstream latest stable release and URL;
- installed executable paths and versions;
- project initialization and host integration smoke tests;
- CodeGraph sync/status after a real source change;
- branch-boundary negative/positive tests;
- checks actually run, failures, fallbacks and unverified areas.

Do not report PASS just because the tools are installed.

## Executable adoption and session preflight (v0.4.1)

Keep the existing helpers together on the consumer development branch: `check-consumer-devtools.py`, `check-codegraph-channel.py`, and `check-license-compliance.py`. Fill the existing [license evidence template](../templates/consumer-devtools/license-evidence.example.json) using independently observed distribution/checkout/checksum evidence. Each tool now needs its actual resolved `executable` and `executable_sha256`; matching version strings or a Homebrew formula elsewhere on PATH cannot establish provenance. These hashes bind a reviewed installation record to the active file; operator attestations still do not cryptographically establish source-to-binary correspondence.

For an already installed, authorized toolchain, run from the consumer development checkout with a known source symbol:

```sh
python3 scripts/check-consumer-devtools.py --root . --evidence /path/to/installation-evidence.json --query KnownSourceSymbol --initialize --rtk-host codex
```

Only an explicitly reviewed CodeGraph source fallback adds `--codegraph-source-sha FULL_REVIEWED_SHA`. The helper rechecks official-channel absence and reads metadata at that immutable SHA; new upstream HEAD does not upgrade it. A stable package must match the official package name and exact tarball origin. Missing tools stop with an installation consent requirement; no command installs or upgrades global binaries. The currently supported source-fallback recipe requires the direct `dist/bin/codegraph.js` entry in the reviewed official checkout, with its hash attested before execution; npm shims/wrappers are rejected. Child CodeGraph commands set the official `CODEGRAPH_NO_DOWNLOAD=1` guard. This does not attest every dependency or arbitrary bundled distributions.

`--initialize` initializes an absent current-worktree CodeGraph index and, for the explicit Codex adapter, runs project-local `rtk init --codex`. It rejects escaping symlinks and refuses to overwrite an existing unreviewed `RTK.md`. There is no implicit bare `rtk init` host guess. Other hosts must use their own documented project-local integration and record its exact verification; this helper reports unsupported adapters rather than claiming cross-host readiness. Global adapters retain their separate authorization boundary.

CodeGraph uses JSON status, validates checkout and index ownership, rejects pending/reindex states, and queries the requested source symbol. Healthy sessions never reinitialize or mechanically sync. After native reconciliation fails, explicitly add `--recover` for one bounded sync/status retry. Check native MCP binding after worktree creation/switch and reconnect it to that checkout; never copy or share indexes between worktrees. Remove temporary indexes with their disposable worktree, without deleting another checkout's index.

Exit `1` means BLOCKED; exit `3` means `CLI_PASS_HOST_UNVERIFIED`, not overall PASS. The script proves project status/query, full-edition evidence, representative compression and failure exit/diagnostic preservation. It cannot prove native Agent Host interception. Before declaring adoption verified, use the active host's CodeGraph tool to find the same symbol in this checkout and execute a representative command through its RTK hook, recording actual host, worktree, tool route and results. CI stdio MCP probes prove protocol behavior only. Do not use fixture attestations to turn this state into a real user Host PASS.

## Release preparation and build-output checks

Keep reproducible developer configuration continuously on `dev`. Cut an independent release-preparation branch from an approved dev SHA and remove developer configuration only there. Reconcile release ancestry back into dev while preserving its pre-merge developer files in the merge result; never delete from dev and restore in a later commit. Generated databases/caches remain untracked everywhere; `.git/info/exclude` can avoid tracked production ignore-rule contamination.

A stripped production tree no longer carries `.ads-devtools.json`, so supply the trusted development manifest from outside that tree to retain custom-path policy. Invoke the same guard after the consumer's real build, using its actual extracted output directory:

```sh
python3 scripts/check-ads-devtools-boundary.py --root /path/to/release-candidate --target-branch main --dev-only-manifest /path/to/trusted-dev-manifest.json --artifact-root /path/to/built-output
```

Missing output directories fail closed. Artifact scans include dependency/cache directories, reject unverified symlinks, and run even when the source branch is dev. An archive must first be safely extracted by the consumer's build process. Wire this command into the existing build job after output creation; the generic source guard alone cannot certify a build artifact. Run clean and deliberately contaminated tree/output fixtures. ADS's own normative templates are publishable standards, not installed consumer integration.
