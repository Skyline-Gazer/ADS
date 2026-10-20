# Frozen Subagent model-comparison fixture

This is a portable Git fixture and fixed oracle, not an ADS runner or model-selection framework.
Read [SPEC.md](SPEC.md), [plan.json](plan.json) and the [protocol](../../v0.3-subagent-model-matrix.md).
Starting fixture SHA: c59ef24cefcbd020fa9b58e60a253a533c94bc90. Its parent is the fixed ADS baseline.

Copy [fixture.bundle](fixture.bundle) to an isolated temporary directory, clone it into a fresh
repository and check out the exact SHA above. Use a separate fresh clone for every cell. The bundle
contains pinned ADS guidance, three task classes, frozen tests and synthetic protected fixtures.
Run python3 -B -m unittest tests.test_matrix.Medium -v before inference: seeded stubs must fail.
Use [prompt-common.txt](prompt-common.txt) plus the selected [serial](mode-serial.txt) or [multi](mode-multi.txt)
suffix as exact task instructions. Equalize model, medium effort, permissions and native child cap.
Do not adjust the contract or oracle after observing a model output. Tests are visible but immutable.

The external operator executes the frozen oracle, verifies changed-file limits, protected/policy/test
hashes and command transcripts, and independently audits native sessions and actual response models.
End-to-end timing includes fresh-clone/startup, integration, rework and external validation. Exclude unsafe,
incorrect or model-unverified cells from speedup. Preserve raw elapsed time as an invalid sample.
Initial budget is medium N=1 only; simple/coupled tasks are prepared but not automatically executed.
Host capture scripts may use native APIs; this fixture supplies no substitute subagent mechanism.

[SHA256SUMS](SHA256SUMS) covers the bundle and every fixed fixture instruction outside this README.
