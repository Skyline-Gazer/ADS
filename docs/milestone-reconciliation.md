# AI-native Phase / Milestone reconciliation

**Purpose:** close a meaningful goal or Phase against the *real* GitHub Project and delivery evidence, then begin the next dependent Phase. This is a focused completion checkpoint, not a per-commit ceremony, shadow backlog, or separate task database. Read [STANDARD.md](../STANDARD.md), [QUALITY.md](../QUALITY.md) and [SAFETY.md](../SAFETY.md).

## When to run

Run once when a named Phase, project milestone, or user goal appears complete, **before** starting a dependent Phase; also on explicit owner request and when a discrepancy in status, scope or delivered code is observed. Do not run the entire project audit after every file edit, CI run or tiny task. Use the existing GitHub Issue Milestone if one exists; it is optional and does not replace GitHub Projects.

## Discover the authoritative work graph

1. Identify the relevant repository, Project (owner/number or URL), Phase boundary, linked issue IDs, acceptance criteria and dependent items. Discover Project fields/status semantics from the live Project; don't invent a board, field name or ID.
2. Read current Project items, Issue state/labels/milestone, PR merge state and base/head, actual main commit, associated CI/check conclusions and relevant release/deploy effects. Use the connected GitHub tools or existing authenticated `gh` interface with least privilege. GitHub Projects v2 may require GraphQL/project-specific permissions; if unavailable, mark **PROJECT_UNVERIFIED**, not synchronized. Never infer Project Done from a closed issue alone.
3. Match items by canonical issue/PR URLs, repository plus item number, and Project item ID when available. Handle draft Project items separately; don't accidentally delete or close them because no Issue exists.
4. Compare expected acceptance and relationships against observable output. Distinguish merged code from deployed or production validated code; independently check security gates and the actual target SHA.

## Classification and convergence

| Class | Meaning | Action |
| --- | --- | --- |
| DONE_VERIFIED | Acceptance criteria met, PR and relevant CI/target SHA proved, with Project and Issue status aligned | Close remaining valid Issue if appropriate, move corresponding Project item to its discovered Done status, record concise evidence |
| OPEN_VALID | Unfinished, blocked or intentionally deferred; Project and Issue accurately reflect it | Keep open; carry dependency forward accurately |
| STATUS_DRIFT | Work proved done but Issue/Project says open, or status says done without matching evidence | Correct false status; do not mark unverified work complete |
| SCOPE_DRIFT | Project/Issue scope does not match actual deliverable, unexpected out-of-scope edits or newly discovered dependency | Reconcile scope through current Issue/Project; record material decisions and fix the specific mismatch |
| EVIDENCE_GAP | Acceptance or CI/merge/deployment evidence missing/contradictory | Recover evidence or reopen/keep open; do not manufacture a PASS |
| PROJECT_UNVERIFIED | Project API, access or canonical board identity unavailable | Record exact blocker; reconcile only independently confirmed Issue/PR facts; do not claim Project alignment |

For each drift: identify the smallest corrective action, amend the existing Issue/PR/Project item (not a duplicate ticket), re-read the changed state and confirm convergence. Close only when **that item's own acceptance** is independently verified. Do not close parent Phase, safety/security defects or blocked items merely because a PR merged or advisory checks passed. Historical FAIL/PARTIAL archives remain unchanged.

If a consequential architectural, credential, production or permission impact must change, get scoped authorization per SAFETY.md. If there are unresolved blocking items, the Phase is **PARTIAL/BLOCKED** and dependent work does not silently advance; unrelated independent work may continue. If Project access is unavailable, report it and request the smallest access/owner decision needed.

## End-of-Phase handoff (in existing GitHub discussion)

One compact comment on the Phase Issue/PR or existing milestone discussion—not another file, database or ritual:

- Phase / Project URL and ID / target repository and main SHA
- Items assessed and per-item status; verified closures vs carried-open, with PR/CI evidence
- Drift found and corrective actions, including a re-read confirmation
- Unresolved issues, access gaps and next dependent Phase: **GO / HOLD / PARTIAL**
- No private secrets, global host configuration, token values or fabricated Project states

## Native workflow example

An agent may use the installed `gh` CLI or a connected GitHub integration. First discover available Project identifiers and permissions, e.g.:

```sh
gh project list --owner OWNER
gh project item-list PROJECT_NUMBER --owner OWNER --format json
gh issue list --repo OWNER/REPO --state all --limit 100
gh pr list --repo OWNER/REPO --state all --limit 100
```

Use item pagination/GraphQL when necessary; default lists may omit items. Fetch details/CI for the concrete relevant IDs rather than treating every listed item as in scope. Authenticate using existing host facilities; never display tokens or create credentials just to perform a checkpoint. Changing a Project item requires known field and option IDs, preferably discovered from GitHub rather than guessing.

## Verification

Follow [phase-milestone-reconciliation.md](../scenarios/phase-milestone-reconciliation.md). This document establishes a protocol; it is **not** evidence that any real Project was reconciled.
