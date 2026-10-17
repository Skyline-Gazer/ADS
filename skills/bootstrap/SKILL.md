---
name: bootstrap
description: Initialize a new software project with only the structure, tests, CI and guidance justified by its goals and stack.
---
# Bootstrap a new project

1. Read the user's goal, host/tool restrictions and relevant ADS version.
2. Infer runtime, package manager, deployment destination and smallest functional architecture; ask only if a consequential product or stack decision cannot be safely inferred.
3. Create a runnable minimal vertical slice with appropriate dependency lockfile and common scripts. Add only relevant unit or integration tests and simple CI commands that can really run.
4. Render the ADS template `templates/AGENTS.md` at the pinned ADS revision (repository root, not inside this skill directory) using **actual** project paths, commands, auto-deploy effects and sensitive operations. If that file is not locally readable, report the gap instead of inventing a pin. Pin an immutable ADS revision and ensure its text is accessible, not merely a private URL.
5. Add a short architecture/decisions note only for consequential lasting choices. Do not copy unused profiles, empty folders or blanket CI workflows.
6. Run feasible local validation, state what passed and what could not be tested. Avoid deploying or creating cloud resources without authorization.

Output: code-ready project and a concise summary. Do not turn bootstrapping into a multi-stage approval workflow.
