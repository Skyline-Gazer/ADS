# Read-only adoption reconnaissance — 2026-10-16

This is an observation, **not** a completed ADS adoption or successful live migration. No target repository was changed.

## KIRARI
- Branch: main at `219bd26fa6024876fc8a1ba9b334936d04b844e3`. AGENTS.md blob: `e62b592fcb56355a0ae8a4ed4741e09785067649` (recorded 2026-10-16 blob `7dbb112a…` differs only by the added `@kirari/edge-gateway-core` boundary row).
- The entrypoint still instructs agents to initialize Trellis context, inspect its specs and follow task records.
- .trellis/workflow.md blob: `b475fbaa6dfde84bfecb954efbd57d66fc41928c`. It describes per-task directories with task.json and planning artifacts.
- Migration requirement: inspect CI, hooks and deployment consequences before attempting to remove mandatory Trellis stages. Preserve functional tests and real security gates.
- Executable control: `scripts/check-trellis-adapter-sync.mjs` (`pnpm trellis:check`, also in CI) requires byte-equivalent skill mirrors across `.agents/`, `.opencode/` and `.reasonix/`. No deploy controller lives in Actions; deployment is provider-native.
- Rehearsal 2026-10-17 (disposable clone, branch `rehearsal/ads-minimal`, never pushed): rewrote AGENTS.md with the ADS pin, removed the Trellis skill mirrors, the sync script, its test, the CI test entry and `trellis:check`. Result: CI gate tests 50/50 pass, `pnpm check` passes end-to-end. No production resource or provider called. Removing the sync gate is required because it enforces the duplication ADS replaces; ordinary CI gates were kept.

## AiringCal
- Branch: dev. AGENTS.md blob: `ff70d6e53200f33bc588969378c63c1df7dedfd5`.
- The entrypoint mandates docs synchronization and references Comet phase rules.
- .claude/rules/comet-phase-guard.md blob: `8f6afdc0f55420d4e8d2dd4049ba3b09b5ea7227`. It describes enforced phases and a separate comet-hook-guard.sh hard gate.
- Migration requirement: find actual hook triggers and preserve API, documentation correctness, data safety and release controls. Merely changing Markdown is insufficient.

- Active change `adopt-d1-r2-incremental-sync` is `phase: build`, so deleting the guard now would violate its own gate. Rehearsal 2026-10-17 (disposable clone, branch `rehearsal/ads-minimal`, never pushed): added the ADS pin to AGENTS.md, made CLAUDE.md a pointer, kept the Comet hook and rules intact. `pnpm typecheck`, `pnpm test` (25/25) and `pnpm build:check` (wrangler dry run) all pass; the hook still evaluates normally.

## Next experiments
In isolated disposable branches: run a simple bugfix under the existing policy and under the proposed ADS adaptation; record number of required owner interactions, relevant tests, behavior and unresolved operational concerns. Do not change production environments or merge target repository PRs as part of the rehearsal.

**Status:** `RECON_AND_REHEARSAL`. Both isolated rehearsals validated the minimal diff without touching production repositories or credentials. Not covered: a real merged migration, live deployment, or owner acceptance of dropping Trellis duplication. AiringCal's Comet guard and rules were preserved, not migrated.
