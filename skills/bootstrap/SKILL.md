---
name: bootstrap
description: Initialize a new software project with only the structure, tests, CI and guidance justified by its goals and stack.
---
# Bootstrap a new project

1. Read the user's goal, host/tool restrictions and relevant ADS version.
2. Discover what already exists before choosing a stack or tool: the platform agent's native Skills, `command -v` and version checks for candidate runtimes and package managers, repository scripts, lockfiles and any reachable local service or cache. Record what is **installed**, **configured** and actually **verified**, and keep the scan to a few read-only commands.
3. Infer runtime, package manager, deployment destination and smallest functional architecture from those findings; ask only if a consequential product or stack decision cannot be safely inferred. Reuse an installed supported runtime and its test facility; if a preferred one is absent, take the smallest documented fallback or report the blocker instead of installing global tooling.
4. Create a runnable minimal vertical slice with appropriate dependency lockfile and common scripts. Add only relevant unit or integration tests and simple CI commands that can really run.
5. Render the ADS template `templates/AGENTS.md` at the pinned ADS revision (repository root, not inside this skill directory) using **actual** project paths, commands, auto-deploy effects and sensitive operations. If that file is not locally readable, report the gap instead of inventing a pin. Pin an immutable ADS revision and ensure its text is accessible, not merely a private URL.
6. Add a short architecture/decisions note only for consequential lasting choices. Do not copy unused profiles, empty folders or blanket CI workflows.
7. Validate with the project's own test command before adding a harness. Run feasible local validation, state what passed and what could not be tested. Avoid deploying or creating cloud resources without authorization.

Output: code-ready project and a concise summary. Do not turn bootstrapping into a multi-stage approval workflow.
