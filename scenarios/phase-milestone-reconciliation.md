# Phase/Milestone checkpoint — acceptance

Status: **PROTOCOL ONLY — live GitHub Project check NOT TESTED.** Follow [the canonical guide](../docs/milestone-reconciliation.md).

Use one disposable GitHub Project or an explicitly authorized existing test Project with representative linked Issues, and a test repo/branch with genuine PR/CI evidence. Do not mutate production projects without permission.

1. **Correct closure:** verified merged PR, expected SHA/CI and full item acceptance → update discovered Project Done status and close only the matched Issue; re-read confirms aligned state.
2. **False Done:** Project Done but PR open/CI failed/security evidence unresolved → correct the Project status or hold it without falsely closing the Issue.
3. **False Open:** verified task completed but Issue and/or Project still open → mark consistent and close, retaining evidence.
4. **Scope drift:** Project item points to outdated work or a split Issue; reconcile canonical identity and dependencies without duplicating a tracker.
5. **Missing Project permission / draft item:** fail open as PROJECT_UNVERIFIED; report the precise access gap and keep unresolved tasks open.
6. **Prior FAIL/PARTIAL:** merge of a historical evidence PR is not authorization to mark acceptance PASS. A known unsafe or blocked task stays open until its own acceptance evidence is verified.

Evidence: Project item IDs and actual field/option names, linked Issue numbers, commit+PR+CI, before/after state, action performed and final GO/HOLD/PARTIAL. A check is **not** passed if it only compares markdown checklists or reads GitHub Issue state without querying the intended Project.
