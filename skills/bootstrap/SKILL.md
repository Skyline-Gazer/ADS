---
name: bootstrap
description: Initialize a new software project with only the structure, tests, CI and guidance justified by its goals and stack.
---
# Bootstrap a new project

1. Read the user's goal, host/tool restrictions and relevant ADS version.
2. Discover what already exists before choosing a stack or tool: the platform agent's native Skills, `command -v` and version checks for candidate runtimes and package managers, repository scripts, lockfiles and any reachable local service or cache. Record what is **installed**, **configured** and actually **verified**, and keep the scan to a few read-only commands.
3. Infer runtime, package manager, deployment destination and smallest functional architecture from those findings; ask only if a consequential product or stack decision cannot be safely inferred. Reuse an installed supported runtime and its test facility; if a preferred one is absent, take the smallest documented fallback or report the blocker instead of installing global tooling.
4. Create a runnable minimal vertical slice with appropriate dependency lockfile and common scripts. Add only relevant unit or integration tests and simple CI commands that can really run.
5. By default, add ADS as a pinned Git submodule at `.ads` (or an available project-compatible path), choosing an approved published release or immutable SHA and verifying authorized read access. See [docs/how-to-update.md](../../docs/how-to-update.md) at the repository root. An inaccessible private submodule is a blocker, not installed guidance; do not embed credentials in `.gitmodules`.
6. Render the ADS template `templates/AGENTS.md` at the pinned ADS revision (repository root, not inside this skill directory) using **actual** project paths, commands, auto-deploy effects and sensitive operations. If that file is not locally readable, report the gap instead of inventing a pin. Pin an immutable ADS revision and ensure its text is accessible, not merely a private URL.
7. Add a short architecture/decisions note only for consequential lasting choices. Do not copy unused profiles, empty folders or blanket CI workflows.
8. Validate with the cheapest credible facility: reuse existing hosted CI first, and use an isolated target-platform preview only when runtime/binding behavior needs it. Lightweight local checks are optional; do not install a second runtime or create a persistent local stack merely to reproduce existing CI. If remote capability is unavailable, state the blocker and use the smallest useful existing fallback. Avoid deploying or creating cloud resources without authorization.

Output: code-ready project and a concise summary. Do not turn bootstrapping into a multi-stage approval workflow.
