# ADS submodule lifecycle — acceptance

Status: **PROTOCOL ONLY — consumer repository live trial NOT TESTED.** Follow [the update guide](../docs/how-to-update.md).

1. In a disposable consumer repository, initialize `.ads` submodule from an accessible published ADS release, and verify root `AGENTS.md` resolves checked-out `.ads` rules; verify at least one host's selected Skill discovery.
2. Clone the consumer with `--recurse-submodules` or run `git submodule update --init --recursive` and prove checked-out ADS SHA equals the parent's recorded gitlink. Check that the latter does **not** advance to upstream HEAD.
3. Publish/discover an **approved** newer ADS revision, produce an actual upstream diff, and safely advance only the gitlink and necessary entrypoint/Skill pointers on a consumer task branch. Run project tests and a native Skill discovery smoke, then open an upgrade PR. Do not merge into auto-deploying main as a test.
4. Simulate an incompatible update: hold merge; preserve project-local rules, immutable old pin and rollback path. After rollback, demonstrate the checkout SHA returns to the prior pin.
5. Verify dirty `.ads` workspace, inaccessible private ADS repo and unavailable target: report DIRTY/INACCESSIBLE/UNKNOWN without force checkout, credentials printed or fabricated update success.
6. Confirm trigger semantics: owner request / Phase end prompts a lightweight check; recurring scheduler is opt-in and does not silently merge or advance ADS.

Evidence: old and candidate full SHAs; `.gitmodules` and gitlink; authorized source and tag/release; `git diff --submodule`, skill discovery, tests/CI, PR state, exact failure and recovery results. Check actual consumers, not only the ADS source repository.
