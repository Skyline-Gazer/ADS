# Claude Code native multi-agent evidence — 2026-10-20

**FAIL overall; native Subagents VERIFIED. N=1 per mode.** Read the [complete acceptance report](../../v0.3-claude-multi-agent-acceptance.md) for the forbidden synthetic credential read, global configuration drift, preserved wrong-baseline preflight, cost boundaries and untested areas.

- [Machine-readable summary](summary.json): all five serial/multi cases, actual native child IDs/windows, elapsed time, tokens and host estimates.
- [Redacted execution archive](evidence.redacted.tar.gz): original CLI invocations, native parent/sidechain work records, tool requests/results, patches, seeded/final tests, permission inventories, independent audits, failures and collector source snapshots.
- [Archive provenance](archive.json) and [SHA-256 sums](SHA256SUMS): original local archive checksum, exported archive checksum and verified member hashes.
- [Delivery checks](delivery.json): final local documentation/regression checks and branch scope.

The archive contains `RAW-MANIFEST.json` and `EXPORT-MANIFEST.json`, pairing original and exported file checksums. Redaction removes user home paths, model thinking/signatures, system prompt snapshots, unrelated plugin/Skill metadata and non-project instruction content. It preserves native IDs, timestamps, real work, permission settings, failures and usage counters. The synthetic canary value and common credential patterns are checked before export.

Originals remain locally at `/private/tmp/ads-claude-ma-20261019/evidence/`; the local-only source fixture is `/private/tmp/ads-claude-ma-20261019/fixture.local.bundle`. The complete raw archive is `/private/tmp/ads-claude-ma-20261019/raw-evidence.local.tar.gz` (checksum in `archive.json`). The parent directory is mode 0700 and the raw archive mode 0600. No actual credential file contents are copied. These are evidence artifacts, not an ADS runner or service.

Host `total_cost_usd` has unknown cost basis; real spend is NOT OBSERVED. Authorization correctness failures and global drift are retained and excluded from speedup claims. No PR merge, release, production change or dependency installation is part of this acceptance.
