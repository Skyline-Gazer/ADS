# Read-only adoption reconnaissance — 2026-10-16

This is an observation, **not** a completed ADS adoption or successful live migration. No target repository was changed.

## KIRARI
- Branch: main. AGENTS.md blob: `7dbb112a24bffaf755ebb810676ee185eb0feacf`.
- The entrypoint still instructs agents to initialize Trellis context, inspect its specs and follow task records.
- .trellis/workflow.md blob: `b475fbaa6dfde84bfecb954efbd57d66fc41928c`. It describes per-task directories with task.json and planning artifacts.
- Migration requirement: inspect CI, hooks and deployment consequences before attempting to remove mandatory Trellis stages. Preserve functional tests and real security gates.

## AiringCal
- Branch: dev. AGENTS.md blob: `ff70d6e53200f33bc588969378c63c1df7dedfd5`.
- The entrypoint mandates docs synchronization and references Comet phase rules.
- .claude/rules/comet-phase-guard.md blob: `8f6afdc0f55420d4e8d2dd4049ba3b09b5ea7227`. It describes enforced phases and a separate comet-hook-guard.sh hard gate.
- Migration requirement: find actual hook triggers and preserve API, documentation correctness, data safety and release controls. Merely changing Markdown is insufficient.

## Next experiments
In isolated disposable branches: run a simple bugfix under the existing policy and under the proposed ADS adaptation; record number of required owner interactions, relevant tests, behavior and unresolved operational concerns. Do not change production environments or merge target repository PRs as part of the rehearsal.

**Status:** `RECON_ONLY`. No evidence of successful bootstrap, multi-agent execution, CI recovery or production integration from this read-only exercise.
