# Repository-first OpenCodeReview integration

ADS v0.2 recommends **repository-level** AI PR reviews rather than compulsory agent-side review calls. Use the [optional GitHub Actions example](../templates/github/ocr-review.yml.example) only after verification. The project remains functional without OCR; do not make ADS depend on a model, MCP server or dedicated runner.

## Configure a project

1. Select a reviewed official `alibaba/open-code-review` release and resolve the tag to its **full immutable commit SHA**. Pin both the Action SHA and its `ocr_version` input; a pinned Action with `latest` CLI is not reproducible. Never use `@main` in a credentialed workflow.
2. Copy the example as `.github/workflows/ocr-review.yml`, replace the action pin placeholder, and ensure the entrypoint and input names match that precise upstream Action commit. The .example extension intentionally prevents automatic activation.
3. Set `OCR_LLM_URL` and `OCR_LLM_AUTH_TOKEN` in GitHub Actions Secrets. For multiple projects prefer **Organization Secrets** restricted to selected repositories, not all repositories. Set `OCR_LLM_MODEL` as a repository variable; set `OCR_LLM_USE_ANTHROPIC=false` for an OpenAI-compatible API such as OpenRouter.
4. Enable only after confirming repository policies, API data-disclosure approval, fork handling, `pull_request_target` threat model, and the actual OCR Action implementation. The action reads the PR diff with credentialed access; untrusted text may still be prompt injection, even when not executed.
5. PR review should run independently of required deterministic CI. Set concurrency to cancel obsolete in-progress runs for the same PR. Do not let review jobs merge, deploy, run code from a fork, or use self-hosted runners for untrusted forks.
6. Only configured trusted PR events should spend LLM budget. No untrusted comment/review commands by default. Disable raw artifact uploading unless needed; protect findings and LLM output if sensitive.
7. Make AI review advisory. Distinguish service failure or missing variables from clean findings; protect required deterministic CI and real security boundaries. Investigate concrete findings rather than blindly obeying a model.

## Performance

Run PR OCR on opened, synchronize, reopened and ready_for_review. Prefer a single incremental pass using the official Action's checkpoint or incremental settings once verified against the pinned version; do not chain review after CI. Reduce OCR effort/concurrency/budget as appropriate while preserving useful coverage. Avoid re-reviewing documentation-only edits when explicitly safe for the project. The GitHub-hosted runner still incurs startup and model latency; MCP would not eliminate model latency and is not required for repository-driven review.

## Rollout

Initially install and test on one low-risk repository; verify successful PR comment, changed-code findings, missing-token and error reporting, fork isolation, and rerun-on-push behavior. Then optionally adopt in KIRARI/AiringCal with their own protections and approval. This repository does **not** deploy OCR into either target.

## Official references

- https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/README.md
- https://github.com/alibaba/open-code-review/blob/main/action.yml
- https://github.com/alibaba/open-code-review/releases
