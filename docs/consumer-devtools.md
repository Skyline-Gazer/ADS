# Consumer project developer-tool baseline: CodeGraph + full RTK

This policy applies to **repositories that adopt ADS**, not to the ADS standards repository itself. ADS defines the rules; consumer projects initialize and use the tools on their development branches.

## Required outcome

Every ADS consumer project must detect, initialize, verify, and maintain both CodeGraph and the **full `rtk` edition** as mandatory developer capabilities. They are not production dependencies.

- CodeGraph: https://github.com/andysom25/codegraph
- RTK: https://github.com/rtk-ai/rtk
- RTK edition policy: use full `rtk`, not `rtk-oss`, subject to its applicable BUSL-1.1 / Apache-2.0 terms. Do not silently substitute editions.

## 1. Preflight every consumer project

Run this during new-project bootstrap, existing-project adoption, and before a task relies on either tool. For each tool report separately:

- executable path and installed version;
- latest stable upstream version and official release/source URL;
- project initialization status;
- operational smoke-test result;
- status: `PASS`, `MISSING`, `NEEDS_INIT`, `OUTDATED`, `INCOMPATIBLE`, or `BLOCKED`.

Installed, configured, current, and operational are distinct states. Never infer one from another. Do not use stale caches or prerelease/nightly builds to claim latest stable.

## 2. Installation and latest-stable policy

The desired version is always the latest stable upstream release, not a fixed historical version.

- If a binary is missing, ask the user before installing it. State the proposed version, official source, installation method, licensing implications, and whether installation changes user-wide state.
- If installed but outdated, update it within the current authorization scope, then verify the real binary version and smoke test. Ask only when elevated privileges, global configuration, or another genuine authorization boundary requires user action.
- If the upstream source cannot be queried, report `BLOCKED/UNVERIFIED`; do not claim the installed version is latest.
- Add a scheduled remote check (for example GitHub Actions) to report upstream stable-version changes. It must not install tools on user machines, change production branches, auto-merge, or deploy production.
- Document an AI-native update procedure in the consumer repository so any coding agent can repeat the check/update safely.

## 3. Initialize project integration automatically when tools are installed

If a tool is present but the consumer project is not initialized, perform the project-local setup within the authorized development branch and verify it. Do not ask the user to do work the agent can safely perform.

### CodeGraph

- Initialize the project graph when absent using the current supported CLI (verify the current CLI's syntax rather than assuming an old command contract).
- After each source-changing implementation batch and after relevant checkout, merge, rebase, reset, or generated-source changes, explicitly run `codegraph sync` and check `codegraph status` before relying on graph-based impact analysis or review.
- A watcher is not a substitute for the explicit ADS checkpoint.
- If sync/status fails or the index is stale, label graph results unavailable and fall back to native source inspection; do not claim a successful graph review.

### Full RTK

- Initialize the project integration and the active host's supported adapter; prove that the host actually invokes RTK using a safe smoke test.
- Verify compressed output, preserved exit codes and error diagnostics, and a documented way to retrieve raw output.
- Do not silently edit global agent configuration or install global hooks. If the chosen host integration requires a global change, ask permission for that specific change.
- If the active host cannot use the selected adapter, report the exact limitation and do not mark RTK operational merely because the binary exists.

## 4. Git branch boundary: development only

This is a **consumer repository branch rule**, not just a packaging rule.

- Project-specific CodeGraph/RTK configuration, host adapters, developer-only hooks, manifests, instructions, and update workflows may be tracked on development branches (for example `dev`).
- None of those project integration files or generated artifacts may be present in the consumer's production `main` branch.
- Before merging to `main`, compare the candidate tree and enforce a deterministic denylist/manifest-based check. If a forbidden path or integration payload would enter `main`, block the merge; do not rely on `.gitignore`.
- The guard itself may be present on `main`, but tool-specific project config and artifacts may not.
- Add negative fixtures proving the guard fails when a forbidden file is present on candidate `main`, and passes when the integration exists only on the development branch.
- Keep production runtime, Docker images, Worker bundles, application packages, deployment output, and release assets free of these tools.

Never commit generated graph databases/indexes, caches, RTK binaries, transient telemetry/session data, secrets, or machine-specific absolute paths to any branch. Track only reproducible project integration/configuration on development branches.

## 5. Latest-version monitoring and update workflow

Each consumer project must have an agent-readable update guide and a remote recurring check:

1. Query official upstream release metadata for both tools.
2. Compare with the installed tool version when running locally, or report the latest upstream version in hosted CI.
3. If a newer stable version exists, produce an actionable result and update the developer environment only with appropriate authorization.
4. Re-run project initialization/smoke checks after an update.
5. Run CodeGraph sync/status after source or index-schema changes.
6. Record versions, release URLs, check time, smoke results, and any blocker.
7. Never commit generated indexes/binaries or propagate dev-only configuration to production `main`.

The recurring workflow must be remote-first, low-cost, and non-mutating by default. It reports; it does not silently change user machines or production state.

## 6. Remote-first acceptance

Prefer GitHub Actions and ephemeral consumer fixtures. Do not provision a permanent service or require a full separate local environment per project. Use local execution only when remote validation cannot exercise the relevant behavior, and record why.

Acceptance must cover:

1. Fresh-project bootstrap and existing-project adoption both enforce preflight.
2. Missing-tool tests prove install requires consent and is not attempted without it.
3. Installed-but-uninitialized tests prove project setup is performed automatically and verified.
4. Latest-stable checks detect an outdated version and handle upstream unavailability honestly.
5. Fresh-clone tests prove project integration is reproducible on a development branch while generated files and binaries remain untracked.
6. CodeGraph sync/status is executed after a source edit and stale index data is not trusted.
7. Full RTK is operational in the selected host; compression works, errors/exit codes are preserved, and raw output is recoverable.
8. A negative branch-gate test rejects CodeGraph/RTK integration/configuration/artifacts from production `main`.
9. CI/release artifact inspection confirms no tool binaries, indexes, caches, or dev-only payloads leak into production.
10. A bounded real consumer pilot reports tool calls/file reads, Token where observable, elapsed time, correctness oracle, and regressions. Do not equate command-output reduction with equal percentage savings on total model spend.

Do not mark acceptance complete solely because both binaries are installed. Project initialization, operational smoke tests, latest-stable verification, branch exclusion, CodeGraph lifecycle, and remote evidence are all required.

## Scope reminder

ADS itself remains a standards/Skills repository. Do not install CodeGraph/RTK or add their consumer-project configuration/artifacts to ADS as part of this policy. The rules in this document are applied when an agent uses ADS in a separate consumer project.
