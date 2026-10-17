# Code review options and the v0.3 decision

**Status:** evaluation record for Issue #4. No review service is installed, configured, required or deployed by this repository; v0.2 and v0.3 stay functional without any AI review integration.

## Decision

Repository-first review, using the coding agent host's built-in review capability on demand, with deterministic CI as the only blocking gate (required by convention on the repository's current plan, see below). No third-party review service was adopted, and no bespoke review orchestrator, extra agent client or mandatory per-step local review call was added. Repository-level vendors remain optional per-repository candidates with conditions, not commitments.

## Already available before choosing anything

| Capability | Evidence from this evaluation | Limits |
| --- | --- | --- |
| Host agent review subagents (quality and security review specialists) | real trial on PR #7 (below) | one host verified (OMP 18.11.3); findings are advisory and must be verified against code and tests |
| Host language-server diagnostics | device present; a diagnostics call on `scripts/check-ads.py` returned `No language server found` | unavailable for Python on this host; applies only where a server is configured |
| GitHub PR checks | `Validate ADS` runs on every pull request; `gh pr checks` reported pass for PR #7 | this private repository answers 403 for branch protection on its current plan, so CI is green-gated by convention and the owner's judgment, not by an enforced required check |
| Deterministic repository checks | `python3 -m unittest discover -s tests`, `python3 scripts/check-ads.py` | catch regressions in this repository's own artifacts only |

## Measured trial (safe, isolated, real PR)

PR #7, 2026-10-17, OMP 18.11.3, host review subagent over `origin/main...feat/v0.3-environment-first` (13 changed files: Markdown guidance, skill files, one dependency-free Python checker, an added `.gitignore` and one removed bytecode file):

- 7m47s wall time, one session, no installs, no third-party service, no repository credentials, no billed service.
- 7 findings: 3 major (fence-detection bypass, incomplete disclosure patterns, an undisclosed normative rule) and 4 minor (unpinned rules, unpinned code-region scoping, missing exit-code assertions, false positives).
- Disposition: all 7 addressed in `977e16c`; one false-positive class accepted and documented by design.
- Reviewer claims independently re-verified rather than trusted: the reviewer's 28-case escape list re-ran 28/28 as expected, a mutation harness confirmed 13/13 probe rules are pinned by tests, and the suite reached 18 passing tests before the CI run went green. Those two harnesses were session-scoped scripts and were not kept; their results are corroborated by commit `977e16c` and by the recorded row in [scenarios/environment-first.md](../scenarios/environment-first.md).
- Not exercised: other agent hosts, fork pull-request threat model, multi-repository scale.

## Alternatives considered

| Option | Access, license and cost (verified at the primary source) | Assessment |
| --- | --- | --- |
| OpenCodeReview (`alibaba/open-code-review`) | Apache-2.0 (`LICENSE`) | Rejected as a default. The observed third-party run spent 17m04s and 51,106 tokens on two selected files, both reviews timed out and produced zero findings (Issue #4). The prior design is preserved only as history in closed PR #3 |
| reviewdog | MIT (`LICENSE`) | A findings transporter, not a reviewer: it still needs a separately pinned analyzer or LLM action, its own credentials and a per-PR budget. Viable later only alongside a repository-level reviewer |
| PR-Agent (`The-PR-Agent/pr-agent`, formerly Qodo Merge) | MIT (`LICENSE`, Copyright 2026 The PR Agent); stewardship moved from Qodo to a community organization; self-hostable in Actions with your own model keys | The strongest optional candidate if a repository later wants an in-CI reviewer. Pin an exact revision, because license metadata and stewardship changed across the hand-over |
| CodeRabbit | Commercial SaaS: monthly list price — Essentials $24/user/mo, Team $48, Advanced $72, Enterprise on request; annual billing is discounted (pricing page) | Not adopted: per-seat cost plus a third-party GitHub App holding repository access, which is disproportionate for personal projects |

Criteria coverage and gaps: licensing, access model and maintenance burden were judged from primary sources, and no alternative was installed or trialled here. Inline-comment quality, per-option review latency, incremental re-review behaviour, cost per pull request and fork handling under a credentialed `pull_request_target` were therefore **not** evaluated for the alternatives; only the host review capability was measured.

## Rollout guidance (optional, advisory)

1. Default: request host review for non-trivial, security-relevant or unfamiliar diffs; keep required deterministic checks as the merge gate and treat model findings as advisory input under [QUALITY.md](../QUALITY.md).
2. Verify concrete findings against code, contracts and tests; fix real ones, answer false positives briefly. Report model or service unavailability as `review unavailable`, never as a pass, and never as an automatic blocker for unrelated low-risk changes.
3. Adding a repository-level reviewer stays a per-repository decision: rehearse on a disposable branch first, pin the action and CLI revision to a commit, keep untrusted fork content out of credentialed execution, cancel obsolete runs, cap spending and grant no merge or deploy authority. This repository does not install one now.
4. Do not add a third review system, a state store or a mandatory local review step per coding action.

## References

- [OpenCodeReview (alibaba)](https://github.com/alibaba/open-code-review)
- [reviewdog](https://github.com/reviewdog/reviewdog)
- [PR-Agent (The-PR-Agent)](https://github.com/The-PR-Agent/pr-agent)
- [CodeRabbit pricing](https://www.coderabbit.ai/pricing)

No production state, secret, IAM scope or repository configuration was changed to obtain this evaluation.
