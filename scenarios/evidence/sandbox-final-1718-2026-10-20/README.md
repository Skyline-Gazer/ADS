# Sandbox final acceptance evidence

ADS baseline: `c24d0b8edc1e56ee4464d107c5257722c3683a8f`. Run: 2026-10-20.

See [the report](../../sandbox-final-1718-acceptance.md) and [summary](summary.json).
[Before](project-before.json), [injected](project-injected.json), [false Done](project-false-done-closed.json),
[false Open](project-false-open.json), [after](project-after.json) and [independent reread](project-independent-reread.json)
are direct GitHub responses. [Policy delta](host-policy-delta.json) and [deviations](execution-deviations.json)
preserve execution limits and host approval-rule writes.

The [redacted archive](evidence.redacted.tar.gz) contains every captured command/exit, GraphQL mutation and read,
PR/CI/jobs/log response, upstream diff, gitlink/content/contract check, native discovery, actual CLI turn,
dirty/unknown/incompatible/rollback evidence and one-shot operator sources as inert text.
Its internal `MANIFEST.sha256` covers every payload file. [SHA256SUMS](SHA256SUMS) covers all files in this directory
except itself. Home/run paths and email addresses are redacted; stable GitHub IDs, full SHAs and failure messages remain.
No credential files or raw global configuration were read into the archive. Policy config is hashed only.
These temporary acceptance helpers are not installed ADS capabilities or a new execution framework.
