# Repository-first review acceptance scenarios

These scenarios are specifications, not claims that OCR has run.

1. **Docs-only:** relevant deterministic checks pass without compulsory local/PR model invocation.
2. **Ordinary code PR:** optional repository OCR posts incremental findings; required CI runs independently, never waits for OCR.
3. **False positive:** agent inspects real code/tests, replies with a concise rationale and does not change correct code merely to satisfy a model.
4. **Model outage:** missing secret, LLM 401/429 or timeout is disclosed as unavailable, not passed; unrelated low-risk PR is not automatically blocked.
5. **Sensitive PR:** focused security review and negative tests apply; confirmed consequential flaw still blocks under project policy.
6. **Fork threat model:** `pull_request_target` credentialed job must not checkout/execute fork head or fetch untrusted scripts/config into privileged execution. Ensure PR content is treated only as untrusted review input.
7. **Pinned action:** verify complete 40-character official Action commit plus exact CLI version, upstream implementation and relevant security advisories before copying template into active workflow.
8. **Resource controls:** obsolete PR pushes cancel older OCR job; comment-triggered model spending is disabled by default; no review-triggered merge/deploy.
9. **Local policy:** stricter project rules supersede ADS defaults. Review Skill is optional assistance for triaging PR feedback.
10. **Integration rollout:** exercise a real PR in an approved test repository; verify comments, error reporting, fork/permission boundaries and no credentials in logs.

**Status:** documentary design only; no authenticated OCR/CLI or integration tests have run here.
