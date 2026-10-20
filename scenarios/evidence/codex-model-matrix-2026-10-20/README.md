# Codex model-matrix preflight evidence

See [the report](../../v0.3-codex-model-matrix-2026-10-20.md) and the
[portable fixture](../../fixtures/subagent-model-matrix/README.md).
This is a stopped preflight: N=0; no actual model, native child or timing comparison is claimed.

[Summary](summary.json), [catalog](models-catalog.json), [Oracle self-check](oracle-selfcheck.json) and
[actual host policy delta](host-policy-delta.json) are directly inspectable.
The [redacted archive](evidence.redacted.tar.gz) contains captured baseline failures, reference/negative
Oracle results, executable/OS metadata, native schema excerpts and metadata failure, host approval event,
policy fingerprints, validation and inert one-shot preparation sources. No execution framework is installed.
Paths/emails are redacted; full SHAs and the exact added rule remain. No raw global config or credentials.

[SHA256SUMS](SHA256SUMS) covers this directory except itself. The archive has an internal
MANIFEST.sha256 covering every payload. Fixture hashes live with the separately frozen bundle.
