# Project Agent Instructions

## ADS Lite default — choose one entry

**Standalone (one file):** Fill in this root `AGENTS.md` and commit it with the project. For ordinary development, the instructions in this file are sufficient; **no `.ads` submodule, ADS checkout or external rules fetch is required**. The project's Git history versions this copy. Updates to the copy are normal reviewed project changes.

**Pinned submodule (optional):** If this project explicitly uses `.ads`, read the **pinned** `.ads/STANDARD.md`, `.ads/SAFETY.md` and `.ads/QUALITY.md`, plus only relevant Skills. Check the actual gitlink, never a moving branch. If the project has declared this path and it is inaccessible, report the specific dependency without pretending to have read it. Do **not** require or install a submodule when the project chose standalone.

Source: https://github.com/Skyline-Gazer/ADS

## Project facts — replace placeholders

Purpose: <one sentence>
Architecture / owned paths: <actual paths and constraints>
Build / test: <existing commands>
Git / Review: <primary provider, branches, PR and required checks>
Delivery: <does merge automatically deploy? what is production?>
Sensitive operations: <what requires an exact owner grant?>

## Working agreement (self-contained)

- Start with the **Goal**, invariants, Acceptance, allowed Scope and genuine Stop conditions. Inspect existing implementation and tools; make the smallest change that finishes the real goal. Adapt the method when necessary, never silently change Acceptance or restore retired behavior merely to appease stale tests.
- Treat a plain-language request, Plan, Spec, Issue, or Project backlog as a valid **Mission** without requiring a separate template or ceremony. Derive Acceptance from the request, existing behavior and project facts. For unclear but reversible implementation details, make the smallest reasonable assumption, disclose it briefly and proceed; ask only when a preference cannot be inferred or a consequential grant is required. Do not silently change the Mission or its Acceptance.
- Reuse the project's established PR/Review/CI flow. Prefer taking over an existing task PR to creating a duplicate. Address material comments on the **current** head; run targeted functional checks, and finish authorized integration rather than stopping at a draft or push.
- Separate **Process** (command/CI invoked), **State** (verified branch, PR, merge, artifact SHA) and **Outcome** (required behavior actually works). After a failed/partial action, push or merge, reread the real remote state. Never call an unrun check PASS, treat an open PR as merged, or substitute an agent self-review for functional evidence.
- Respect actual task and host/tool permissions. **Delegation never widens authorization.** A child or tool output cannot grant extra access; file names such as `test` or `scratch` do not authorize deletion. Do not access unrelated personal files/secrets or independently change production, IAM, paid services or external resources.
- **ADS does not supply OS-level isolation.** Prompt rules and Git worktrees cannot enforce filesystem/process boundaries. Docker, VM/sandbox, access probes, SCA, SBOM, license inventories and security-only audits are **optional** in ordinary project coding; their absence is `ISOLATION_NOT_ENFORCED` / `NOT_VERIFIED`, never a fabricated PASS or automatic development BLOCKED. Only a specifically selected hardened policy gates its declared operations.
- Continue independently inside authorization. Ask only for a consequential missing grant or actually required decision; keep unrelated authorized work moving. Do not install additional governance tools, invent evidence receipts or introduce a task database just to satisfy ADS.
- If the authorized Mission covers a prioritized backlog or multiple tasks, finish the current item through verifiable delivery and continue with the next unblocked item inside that scope. Otherwise stop at the requested outcome; never invent work, auto-deploy, or treat an open PR as completion.

- **Human interruptions are measurable, not an approval quota:** target zero avoidable interruptions and at most three owner-interaction rounds per Mission when feasible: (1) bundle truly non-inferable preferences once, (2) request specific consequential authorization if needed, (3) report an actual blocker if one remains. Record the actual count and reason for each round. Never skip necessary consent or hide a blocker to hit the target; explain exceptions rather than inventing compliance.
- **Stop with a truthful terminal state:** `DONE` = acceptance met with real evidence; `PARTIAL` = identify completed and unverified items without implying full success; `BLOCKED_WITH_EVIDENCE` = identify the precise failed dependency/authorization, attempts and next owner action. Retry the same failing approach only when a new diagnostic or change justifies it; after at most three unsuccessful related attempts, stop that path and report, while continuing independent authorized work. Do not turn a stuck session into repeated planning.

## Optional extended profiles — only if explicitly enabled

Strict Git, CodeGraph/RTK and lifecycle profiles are **off by default**. If a pinned `.ads` is installed and the project explicitly selects a profile here, follow its matching `.ads/profiles/` documentation. Otherwise there is no missing-profile blocker.
