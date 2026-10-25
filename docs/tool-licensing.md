# ADS v0.4: developer-tool license and edition verification

Scope: **projects adopting ADS**, not a requirement to install developer tools in ADS itself.
This supplements [consumer developer toolchain](consumer-dev-toolchain.md) and #45/#51.

## License and use matrix (recheck at each latest-stable update)

| Dependency | Edition and components | Current license(s) | Typical internal use | Restrictions |
| --- | --- | --- | --- | --- |
| CodeGraph (`@andysom25/codegraph`) | CLI/MCP | MIT | Allowed with preservation of copyright/license notices on redistribution | Inspect the actual version's distributed LICENSE |
| RTK `rtk` | Full command filters + compression engine | Apache-2.0 for CLI/filters; BUSL-1.1 for engine | Current Additional Use Grant permits free production use as bundled by RTK AI Labs | Offering licensed engine or derivatives to third parties as a paid or hosted product/service is not granted |
| RTK `rtk-oss` | CLI/filters without compression engine | Apache-2.0 | Generally permitted under Apache-2.0 | **Not** a compliant substitute for ADS's required *full* edition |
| `rtk-proxy` | Standalone daemon; **not** included in `rtk` | BUSL-1.1 | Additional Use Grant applies | Separate component; do not infer installation |

The BUSL engine's **current** Change Date is 2030-09-09 and Change License Apache-2.0; the terms **can differ per distributed version** and may change on future latest-stable updates. BUSL is source-available, not OSI-approved. Apache-2.0 redistribution has notice obligations. An ADS consumer's independently written product does **not** inherit these tool licenses merely because its developers ran the tools.

Official primary sources:
- https://github.com/andysom25/codegraph/blob/main/LICENSE
- https://www.rtk-ai.app/docs/resources/editions/
- https://github.com/rtk-ai/rtk/blob/develop/engine/LICENSE

## Mandatory preflight and change control

1. First verify actual installed executable **and** package/edition provenance, host integration, smoke checks, and latest-stable version using the existing ADS tool preflight. `rtk --version` alone cannot establish the edition.
2. Obtain the **license files from the actual versioned distribution**, not merely a current `main`/`develop` webpage. For CodeGraph, inspect the versioned npm tarball `LICENSE`; for full RTK, inspect both `LICENSE` and `LICENSE-ENGINE` shipped alongside its versioned release binary. Keep the read-only provenance/association evidence out of Git and away from production artifacts.
3. Classify consumer use: `internal-development`, `independent-software-delivery`, `tool-redistribution`, or `hosted-rtk-service`. Do not conflate selling an independently developed website with selling RTK as a product.
4. Fill the versioned evidence object in [example](../templates/consumer-devtools/license-evidence.example.json); update observed version/source, real local license-file paths and attestation booleans **only after verification**. The example is intentionally not PASS. Run `python3 scripts/check-ads-license-compliance.py /path/to/license-evidence.json` after copying the checker from [template](../templates/consumer-devtools/check-license-compliance.py) into the consumer dev branch.
5. Any missing provenance, text/grant mismatch, license change, OSI-only corporate policy conflict, or tool redistribution/hosted exposure is **BLOCKED**, not a silent legal approval. Request a specific rights/authorization decision; never downgrade to `rtk-oss` without changing the ADS requirement through a separately reviewed policy decision.
6. When upgrading `latest-stable`, obtain newly distributed license files, compare hashes and terms with the last accepted record, and review **before** changing the installed binary. Do not silently bless a changed license just because markers still match; the offline checker verifies evidence markers, not legal identity or complete compatibility.

The offline checker does not download binaries, attest authenticity or certify legal rights. It validates locally provided evidence and recorded assertions. **Use independent installed-package verification and a review of license changes to justify those assertions.** The check must not be represented as end-to-end automation of legal clearance.

ADS itself is licensed MIT (see [root LICENSE](../LICENSE)). This does not change the license of the consumer repository or grant rights to redistribute third-party developer tools.

## v0.4 release acceptance

Repository tests and isolated consumer CI cover policy and negative fixtures. They are **not** a substitute for a real consumer installing, initializing and using the full toolchain. Keep #45 open until that bounded pilot records exact versions, host invocation/compression, CodeGraph freshness/worktree binding, negative production boundary tests, correctness and regressions. Do not claim universal host coverage.

## Owner-approved CodeGraph source fallback

If official stable npm and Releases distribution are both confirmed absent, an explicitly approved, immutable upstream source SHA may replace **only CodeGraph's distribution channel**. The source's actual versioned `LICENSE` must match MIT, the build must be reproduced from that SHA, and evidence must record `source_sha`, `source_fallback_approved: true`, `source_fallback_verified: true`, and `latest_stable_verified: false`. Record a `distribution_url` of `https://github.com/andysom25/codegraph/commit/<exact-sha>`. This source channel is not an upstream tagged stable release. The offline checker still only verifies the operator-supplied evidence; actual source/binary hashes, grant change, review and local host integration are separate required proofs.
