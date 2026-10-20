# OpenCode native subagent model matrix evidence — 2026-10-20

**Overall: PASS on capability and correctness, exploratory SLOWER on efficiency.** Two observed DeepSeek models each completed the same medium fixture task serially and with two real native child sessions; all four cells passed both the fixture suite and an independent 17-check oracle. Multi-agent was slower and used 2.0–2.3× the tokens at N=1. Read the [acceptance report](../../v0.3-opencode-subagent-model-matrix.md) for the preserved host failures and boundaries.

- [Machine-readable summary](summary.json): per-cell wall time, observed models, parent and child token usage, cache, host cost estimate, native child ids, overlap, verdicts and excluded runs.
- [Redacted execution archive](evidence.redacted.tar.gz): per-cell session exports, raw JSON event streams, prompts, generated agent definitions, diffs, oracle output, mechanism probes and the harness used.
- [SHA-256 sums](SHA256SUMS): one line per archived file, verified against the extracted archive.
- Host record `host.json` inside the archive: OpenCode version and binary hash, OS, ADS and fixture pins, global configuration hashes before and after, and the project-local isolation choices.

Redaction replaces the user home path and the scratch root with `<HOME>` and `<SCRATCH>` and drops nothing else. No credential value is in the archive; the credentials fixture is represented only by its SHA-256. Native ids, timestamps, tool arguments, permission rejections and usage counters are retained because the report's claims depend on them.

The archive holds normalized session exports (`opencode session export`) plus the raw `--format json` event stream per cell, not the multi-megabyte session database. Nothing here is an ADS runner or service. No application code from the fixture is redistributed.
