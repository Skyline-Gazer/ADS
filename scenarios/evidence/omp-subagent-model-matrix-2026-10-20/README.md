# OMP native subagent model matrix evidence — 2026-10-20

**Overall: PARTIAL.** Native child creation, batch fan-out and repository-relative isolation are verified; absolute-path writes escape child worktrees; efficiency is a N=1 exploratory result (multi slower). Read the [acceptance report](../../v0.3-omp-subagent-model-matrix.md) for the preserved failures, model routing findings and boundaries.

- [Machine-readable summary](summary.json): both models, serial and two-child modes, wall time, parent and child tokens, cache, host cost estimate, native session ids, overlap and every capability verdict.
- [Redacted execution archive](evidence.redacted.tar.gz): normalized OMP session records (session headers, model and thinking resolution, tool calls with arguments, assistant text, usage), isolation patch files, the exact prompts, overlays, worker agent definition, oracle and runner used.
- [SHA-256 sums](SHA256SUMS): one line per archived file, verified against the extracted archive.
- Host record `host.json` inside the archive: OMP version and binary hash, OS, fixture and ADS pins, and identical global-config hashes before and after.

Redaction removes the user home path and the scratch root, replaces the synthetic canary value, and drops model thinking blocks and system-prompt snapshots. Native ids, timestamps, tool arguments, failures and usage counters are retained, because the report's claims depend on them.

The archive holds normalized audit records rather than raw multi-megabyte session files: each JSONL line is one event reduced to the fields the report cites (`session`, `session_init`, `model_change`, `thinking_level_change`, `message`, `custom.tool_execution_start`, `custom.session_exit`). Raw sessions remain locally under the scratch root recorded in `host.json`; they are not required to check a claim in the report.

Nothing here is an ADS runner or service. No credential value, token or account identity is included, and no application code from the fixture is redistributed.
