# PAS — Personal Agent Development Standard

A lightweight, tool-neutral standard for personal projects developed with AI coding agents. The objective is reliable software delivery with minimal ceremony, not a new agent framework.

**Status: v0.1 draft.** No other project adopts these rules automatically.

## Documents

- [STANDARD.md](STANDARD.md): Agent autonomy, ordinary development flow, Git and PR policy.
- [SAFETY.md](SAFETY.md): Risk and operational authorization boundaries.
- [QUALITY.md](QUALITY.md): Tests, CI, review, and truthful delivery claims.
- [templates/AGENTS.md](templates/AGENTS.md): Minimal project adoption template.

## Agreed decisions

Low-risk PRs may be merged autonomously after relevant CI succeeds and no justified blocker remains, provided the repository's deployment policy permits it. Review effort is risk-based; ordinary work does not need double review. Trellis, Comet and OpenSpec remain optional tools, not mandatory approval stages.

## Adoption after approval

Pin a specific PAS revision. Add a short local AGENTS.md identifying the project's architecture, test commands, merge-to-production effects and sensitive actions. Audit and adjust enforcement hooks, CI and agent instructions: merely linking PAS cannot remove old hard gates. Try the revised flow on a small task first.

Initial research reviewed KIRARI, AiringCal and CFWorker4AliCDT. InfraTools was inaccessible and is not claimed as audited.
