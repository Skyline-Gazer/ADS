# Optional profile: strict lifecycle and drift convergence

**Not part of lite adoption.** Enable only when the project `AGENTS.md` lists this profile.

Adds post-merge SHA readback, Phase-end Project reconciliation, and optional JSON receipts. See [docs/execution-and-drift-governance.md](../../docs/execution-and-drift-governance.md) and [docs/milestone-reconciliation.md](../../docs/milestone-reconciliation.md).

The receipt helper in ADS (`scripts/check_lifecycle_receipt.py`) validates declaration shape only; it does not replace live Provider or Project reads.
