# Agent-native smoke test protocol

**Status:** NOT RUN. This protocol is an acceptance checklist, not evidence of successful integration.

## One new-project test
Use a disposable directory with a coding-agent host that can read the selected ADS revision and invoke its native Skills discovery. Ask: "Bootstrap a small Astro website showing a list of tasks with one relevant test; use ADS bootstrap guidance, avoid databases and external services." Observe:
- Agent can locate the selected bootstrap Skill without manually pasting its complete contents.
- Generated project runs and builds under the chosen runtime.
- It creates a meaningful project-local AGENTS.md, not a bare private repository URL.
- No needless orchestrator, cloud deployment workflow or state database appears.
- Agent reports commands actually executed and limits honestly.

## One existing-project test
Use a disposable copy or branch; task: "Repair a failing relevant unit test using ADS deliver and recover." Check scope control, true CI status, and that no protected resource is modified.

## Test matrix
| Host | Skill discovery | Bootstrap | Scoped repair | Status |
| --- | --- | --- | --- | --- |
| Codex CLI | Not exercised | Not exercised | Not exercised | PENDING |
| OpenCode | Not exercised | Not exercised | Not exercised | PENDING |
| Claude Code | Not exercised | Not exercised | Not exercised | PENDING |

A platform may be unsupported by the available execution environment; report NOT TESTED rather than PASS. A successful Markdown validation workflow does not satisfy these end-to-end criteria.
