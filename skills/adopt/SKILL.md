---
name: adopt
description: Adopt ADS in an existing project by preserving working workflows and removing unnecessary agent ceremony.
---
# Adopt into an existing repository

1. Inspect the existing `AGENTS.md`, source structure, hooks, CI, Git provider, deployment triggers and current build/tests. Do not mistake an instructional warning for an enforced security boundary.
2. Preserve working architecture and user/project choices. Install only the minimal reviewed ADS pin and short root [AGENTS.md](../../templates/AGENTS.md); update by PR, not a moving branch. Existing project-specific integrations take precedence over optional ADS examples.
3. **Do not** auto-activate strict Git, CodeGraph, RTK, lifecycle receipts, SCA/SBOM, Docker or host isolation. Existing project requirements remain as configured. Missing security-only extras are advisory, not a reason to stop ordinary feature work.
4. Remove redundant copied rules or hooks only after checking what they actually enforce. Changing a required CI check needs an authorized, reviewable update; never conceal a failed check.
5. Prove compatibility with one representative real task or affected project test, and distinguish Process/State/Outcome in the report.

Keep existing provider/remotes and deployed resources unchanged without a separate grant. Use [lite](../../docs/lite-adoption.md), [provider selection](../../docs/git-provider.md) and [scope](../../SAFETY.md).
