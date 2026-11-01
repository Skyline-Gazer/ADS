# ADS — Development Standard

Version: **v0.7 development-first candidate** (unreleased). Existing tags remain immutable; consumer updates require a deliberate pin change.

## Purpose and precedence

ADS is a lightweight convention for **finishing authorized software goals**, not an agent runner, OS sandbox, task database or replacement for a project's own rules. Follow host/tool restrictions and the user's actual grant. Project `AGENTS.md` owns project facts: architecture, test commands, Git provider, review policy, deployment effects and sensitive operations. Do not copy rival instruction stacks or create new governance infrastructure.

## Goal-driven work

- Identify the **Goal**, what must remain true, relevant **Acceptance**, authorized **Scope** and genuine **Stop** conditions. Reuse the user's request or Issue/PR; for complex work, summarize these briefly in the session, not a mandatory new file.
- Inspect existing code, toolchain, lockfiles, Skills, CI and open task branches/PRs. Reuse what already works; do not install a second runtime, Docker or remote service merely for ADS compliance.
- Implement the smallest necessary change. When a plan fails, diagnose and adapt the method without silently changing the Goal or lowering Acceptance. An outdated test harness is not authority to restore a deliberately retired feature (A01).
- Continue independently through code, relevant tests, functional review repairs and authorized Git delivery. Avoid per-phase approval prompts. Do not assume work will continue after the session ends.
- Stop only for a genuine unavailable dependency required for Acceptance, an actual host denial, a consequential decision or an operation outside authorization. Name the precise blocker and continue unrelated authorized work. A missing optional check or tool is not a blocker.

## Development-first security boundary

**ADS provides no filesystem/process isolation.** An `AGENTS.md` restriction, working directory, Git worktree or clean diff cannot enforce read/write containment. Never claim a verified boundary without evidence. Do not deliberately read unrelated private files, disclose secrets, delete outside the granted target or expand privileges.

**Ordinary project work continues without Docker, VM, sandbox, negative probes, SCA, SBOM, license inventory, supply-chain attestations or security-only re-review.** Missing isolation is `ISOLATION_NOT_ENFORCED` / `NOT_VERIFIED` (advisory), not a default `BLOCKED`. Do not provision isolation solely to satisfy ADS. Existing required functional CI and actual project/provider protections remain in force; make any authorized change to a required-check configuration through a reviewable change, never by inventing PASS.

Consumers may expressly select hardened isolation or other audits for sensitive work; only then apply [host isolation](docs/host-filesystem-boundary.md), [subagent containment](docs/native-subagent-safety.md) and the project's stated stop conditions. Security opt-out does **not** grant production, credential, IAM, destructive resource or spending authority. See [SAFETY.md](SAFETY.md).

## Native agents and efficient execution

Use current host-native Skills, tools and subagents when they help. Parallelize independent read-only checks or disjoint project edits when speedup exceeds coordination cost; run tightly coupled work serially. Give children a scoped task, owner for modified files, tests and report expectations; parent owns integration and outcome.

**Delegation never expands the parent's authorization.** Child permission policy might differ, and worktrees only separate Git changes, not OS file access. Do not mistake a child summary for verification. Without an opted-in isolation policy, normal authorized project coding continues; avoid only operations needing additional authority.

## Git, provider and delivery

- Honor the **consumer project's declared** Git/CI/review workflow. Lite does not require a new `dev` branch, Issue-per-change, branch-protection scripts, or CodeGraph/RTK. Strict Git, lifecycle and developer-toolchain policies apply only when the project explicitly selects their existing [profiles](profiles/README.md).
- ADS **itself** follows [Git governance](docs/git-governance.md): task branch from `dev` (or CNB specialty `cnb/dev`), Issue-linked PR, relevant checks, reviewed integration; release to `main` is separate. Avoid force-writing integration/release branches.
- Use the configured primary Git provider. CNB Primary uses native PR/CodeBuddy and manual Agent-initiated merge after effective review; GitHub mirror is not a duplicate development lane. See [provider](docs/git-provider.md) and [CNB review](docs/cnb-review.md).
- **Reuse an existing PR for the same goal** instead of opening a second chain (A02). Resolve actionable material comments on the current head, not an older Review PASS (A03). Start relevant CI early; repair related faults only. A passing command or CI run alone does not prove a merge or target behavior.
- After a push, failed partial operation, review, merge or deploy-shaped action, **re-read the actual remote state** before reporting or trying again (A04). Merge only when already authorized and the repository's real checks/review and side effects permit it. Production deployment, provider switching, secrets, paid infrastructure and high-impact actions need their own grants.
- Close Issues/Projects based on proven completion, not a pushed branch. Reconcile tracked milestones proportionately; missing optional audits do not freeze unrelated feature work. Report clearly: implemented / tested / PR open / merged / deployed / behavior verified. See [QUALITY.md](QUALITY.md).

## Adoption and recovery

Use one short project-root [AGENTS.md template](templates/AGENTS.md) and an immutable ADS pin (typically `.ads` submodule); optional Skills are [bootstrap](skills/bootstrap/SKILL.md), [adopt](skills/adopt/SKILL.md), [deliver](skills/deliver/SKILL.md), [recover](skills/recover/SKILL.md). Never silently update consumer pins, copy governance scripts, change the Git provider or modify production. On interruption, reconstruct truth from Git, PRs, Issues and tests rather than session history. A GitHub PR, a CNB PR and a deployment are different states (A06); verify the one that matters.
