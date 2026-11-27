# ADS — Development Standard

Version: **v0.8.1 Refine, Don't Reinvent** — [published release](https://github.com/Skyline-Gazer/ADS/releases/tag/v0.8.1), the final frozen framework version ([release notes](docs/releases/v0.8.1.md)). Existing tags remain immutable; consumer updates require a deliberate pin change.

## Purpose and precedence

ADS is a lightweight convention for **finishing authorized software goals**, not an agent runner, OS sandbox, task database or replacement for a project's own rules. Follow host/tool restrictions and the user's actual grant. Project `AGENTS.md` owns project facts: architecture, test commands, Git provider, review policy, deployment effects and sensitive operations. Do not copy rival instruction stacks or create new governance infrastructure.

## Goal-driven work

- Identify the **Goal**, what must remain true, relevant **Acceptance**, authorized **Scope** and genuine **Stop** conditions. Reuse the user's request or Issue/PR; for complex work, summarize these briefly in the session, not a mandatory new file.
- Inspect existing code, toolchain, lockfiles, Skills, CI and open task branches/PRs. Reuse what already works; do not install a second runtime, Docker or remote service merely for ADS compliance.
- Implement the smallest necessary change. When a plan fails, diagnose and adapt the method without silently changing the Goal or lowering Acceptance. An outdated test harness is not authority to restore a deliberately retired feature (A01).
- Continue independently through code, relevant tests, functional review repairs and authorized Git delivery. Avoid per-phase approval prompts. Do not assume work will continue after the session ends.
- Stop only for a genuine unavailable dependency required for Acceptance, an actual host denial, a consequential decision or an operation outside authorization. Name the precise blocker and continue unrelated authorized work. A missing optional check or tool is not a blocker.

**Requirement authority and supervision.** A Mission may be expressed in an Issue, plan, spec, roadmap or forwarded report, but its format does not authorize every requirement inside it. When a material obligation, acceptance criterion or gate would expand or conflict with the granted goal, check its basis in actual Owner direction, delegated engineering scope or an applicable legal, security or data-integrity obligation; Agent recommendations, forwarded reports and repeated historical claims are not new Owner authorization, and a report being reviewed or forwarded does not approve its proposals. Symmetrically, do not silently drop Owner-approved scope in the name of Lite or minimality. Planning, review and other supervisory agents derive Acceptance from the authorized objective, challenge unsupported or disproportionate work before enforcing it, and reuse sufficient existing evidence instead of re-running it; routine authorized repair proceeds inside the same grant rather than returning to the Owner as a scheduler. The latest actual Owner scope decision supersedes conflicting active plans: retire the rejected obligation from current acceptance and gate status, preserve the historical record, and keep genuine product, security and required-CI obligations.

## Development-first security boundary

**ADS provides no filesystem/process isolation.** An `AGENTS.md` restriction, working directory, Git worktree or clean diff cannot enforce read/write containment. Never claim a verified boundary without evidence. Do not deliberately read unrelated private files, disclose secrets, delete outside the granted target or expand privileges.

**Ordinary project work continues without Docker, VM, sandbox, negative probes, SCA, SBOM, license inventory, supply-chain attestations or security-only re-review.** Missing isolation is `ISOLATION_NOT_ENFORCED` / `NOT_VERIFIED` (advisory), not a default `BLOCKED`. Do not provision isolation solely to satisfy ADS. Existing required functional CI and actual project/provider protections remain in force; make any authorized change to a required-check configuration through a reviewable change, never by inventing PASS.

Consumers may expressly select hardened isolation or other audits for sensitive work; only then apply [host isolation](docs/host-filesystem-boundary.md), [subagent containment](docs/native-subagent-safety.md) and the project's stated stop conditions. Security opt-out does **not** grant production, credential, IAM, destructive resource or spending authority. See [SAFETY.md](SAFETY.md).

## Native agents and efficient execution

Use current host-native Skills, tools and subagents when they help. Parallelize independent read-only checks or disjoint project edits when speedup exceeds coordination cost; run tightly coupled work serially. Give children a scoped task, owner for modified files, tests and report expectations; parent owns integration and outcome.

**Delegation never expands the parent's authorization.** Child permission policy might differ, and worktrees only separate Git changes, not OS file access. Do not mistake a child summary for verification. Without an opted-in isolation policy, normal authorized project coding continues; avoid only operations needing additional authority.

Choose the execution route by task fit, availability, cost and required independence rather than host lock-in: the host's native capability commonly wins, and an alternative harness or model may be chosen directly when it materially fits, without forcing a native failure first or adding a discovery ritual. When a model, subagent or tool route is unavailable, prefer the host's **already-authorized native recovery** — configured retry/fallback, model switch, cancelling a stalled child — then re-delegate or take the work over; do not wait indefinitely or keep re-sending the same failing request unchanged, and stop that path after at most three unsuccessful related attempts (retrying earlier only when a new diagnostic or change justifies it) while continuing independent authorized work. Do not add a router, scheduler or runner because the host already provides the capability. A substitution never widens authorization and never substitutes for a required independent review; when a preferred reviewer or tool is unavailable, sufficient equivalent independent evidence may complete ordinary work, while a genuine mandatory gate stays binding. Report a child by its actual terminal result — finished is not succeeded.

## Git, provider and delivery

- Honor the **consumer project's declared** Git/CI/review workflow. Lite does not require a new `dev` branch, Issue-per-change, branch-protection scripts, or CodeGraph/RTK. Strict Git, lifecycle and developer-toolchain policies apply only when the project explicitly selects their existing [profiles](profiles/README.md).
- ADS **itself** follows [Git governance](docs/git-governance.md): task branch from canonical `dev`, Issue-linked PR, relevant checks, reviewed integration; release to `main` is separate. Avoid force-writing integration/release branches.
- Activate provider capabilities conditionally from project configuration, verified live state, task relevance and authorization. GitHub Primary is the default; CNB Primary (Lite or explicit strict opt-in) and CNB+GitHub Mode A release mirror apply only when configured and authorized—never auto-switch providers from a remote name or add a duplicate GitHub dev PR. See [provider](docs/git-provider.md) and [CNB review](docs/cnb-review.md).
- **Reuse an existing PR for the same goal** instead of opening a second chain (A02). Resolve actionable material comments on the current head, not an older Review PASS (A03). Start relevant CI early; repair related faults only. A passing command or CI run alone does not prove a merge or target behavior.
- After a push, failed partial operation, review, merge or deploy-shaped action, **re-read the actual remote state** before reporting or trying again (A04). Merge only when already authorized and the repository's real checks/review and side effects permit it. Production deployment, provider switching, secrets, paid infrastructure and high-impact actions need their own grants.
- Close Issues/Projects based on proven completion, not a pushed branch. Reconcile tracked milestones proportionately; missing optional audits do not freeze unrelated feature work. Report clearly: implemented / tested / PR open / merged / deployed / behavior verified. See [QUALITY.md](QUALITY.md).

## Adoption and recovery

Use one short project-root [AGENTS.md template](templates/AGENTS.md); add an immutable ADS pin (typically the `.ads` submodule) only when the project chooses the extended-rules entry; optional Skills are [bootstrap](skills/bootstrap/SKILL.md), [adopt](skills/adopt/SKILL.md), [deliver](skills/deliver/SKILL.md), [recover](skills/recover/SKILL.md). Never silently update consumer pins, copy governance scripts, change the Git provider or modify production. On interruption, reconstruct truth from Git, PRs, Issues and tests rather than session history. A GitHub PR, a CNB PR and a deployment are different states (A06); verify the one that matters.
