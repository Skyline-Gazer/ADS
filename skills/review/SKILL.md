---
name: review
description: Optional local review assistance and GitHub PR findings triage under ADS repository-first code review policy.
---
# Repository-first code review

Read project-local AGENTS.md, ADS QUALITY.md, and [review integration](../../docs/review-integration.md). The **repository PR** is the primary source of truth. GitHub OpenCodeReview is an optional implementation; ADS does not require each coding agent to run a local reviewer.

1. Implement and run relevant deterministic tests before submitting a PR. Do **not** insert a compulsory OCR invocation at each coding step.
2. If the repository has OCR, read its PR findings after review completes. Verify concrete claims against code, contracts and tests; fix valid findings, explain false positives briefly and report unresolved material concerns.
3. If OCR has not completed or its model/secret is unavailable, accurately report `review unavailable/not run`. Do not report a pass. Advisory OCR outages are not automatically merge blockers for unrelated low-risk changes; follow stricter local policy for sensitive code.
4. Local CLI / Agent review is optional on-demand, especially for large or sensitive changes. Do not run duplicate OCR passes solely to satisfy ADS.
5. Do not bypass required CI, use elevated review privileges, run untrusted PR code with secrets, or authorize deploy/merge outside project rules.
6. Minimize review cycles and model spend; retain concise decisions in PR comments and existing checks rather than a separate evidence archive.

This Skill is **not** an MCP adapter, GitHub workflow runner, or mandatory developer-side hook.
