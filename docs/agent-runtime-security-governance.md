# Agent Runtime Security Governance

Scope: all ADS Consumers and ADS itself. Every agent runtime — CLI/TUI, desktop GUI (Codex Desktop), IDE extension, remote/cloud agent, MCP server, delegated subagent — must be evaluated under one contract. The enforcement technology is host-specific; the **contract is not**.

## Four decoupled layers

1. **Security Contract (normative, runtime-agnostic).** Least privilege for filesystem reads/writes, subprocess inheritance, MCP surface, credentials, and network. Deny-by-default; every allow is named, scoped to a canonical absolute path or capability, and auditable. A runtime that cannot *prove* enforcement is UNVERIFIED; one that fails a synthetic probe is UNSAFE; both fail closed for sensitive-data tasks.
2. **Host Discovery.** Before any work, identify the actual executing host: product, version, executable path, execution location (local/remote runner/container), runtime form (main agent vs delegated worker vs MCP child), and the permissions actually inherited. Discovery output feeds the Preflight; it is evidence input, not evidence of enforcement.
3. **Enforcement Adapter.** Host-specific mechanism that implements the contract: macOS CLI → Seatbelt launcher (`templates/host-security/gen_project_sandbox.py`); Codex CLI → native permission profiles; GUI → App Sandbox + XPC/Helper boundary of the **agent worker process** (never the GUI shell); IDE extension → the extension host's child-process policy; remote → runner/container isolation + workspace mounts + credential scope. Adapters implement the interface below; no runtime is required to launch through a specific command.
4. **Evidence & Verification.** Synthetic canary probes only (never real private files), run against the *actual executing process*, recorded as structured evidence. A PASS is the observed denial of every forbidden vector plus the success of every legitimate vector, bound to host version + adapter version + profile identity.

## Primary-vs-worker separation

GUI and IDE hosts must distinguish the **main process** (window, UI, orchestration) from the **agent worker** that actually executes code and filesystem calls. Isolation of the shell is irrelevant; only the worker's effective privileges count. The same applies to MCP servers and subagents: verify the process that touches the filesystem.

## Fail-closed gate

- `VERIFIED_BOUNDED`: real-enforcement evidence complete for the vectors claimed, at a named host/adapter/profile version.
- `PROMPT_ONLY`: restrictions documented but not proven.
- `UNVERIFIED`: adapter exists, evidence absent (no claims allowed).
- `UNSAFE`: any forbidden synthetic vector succeeded.
- `BLOCKED`: host unavailable or adapter not implementable.

Sensitive-data tasks require `VERIFIED_BOUNDED` (or a genuinely isolated environment). Everything else may proceed with a disclosed limitation, never claiming support.

## Adapter interface

Adapters are declarative JSON (`templates/host-security/adapters/<name>.json`) plus optional scripts. Required fields:

| Field | Meaning |
| --- | --- |
| `adapter` | stable id, e.g. `macos-cli-seatbelt` |
| `runtime_kinds` | subset of `cli`, `gui`, `ide`, `remote`, `mcp`, `subagent` |
| `discovery` | how to detect host+version+exec path (commands, files) |
| `enforce` | mechanism description; command if applicable |
| `verify` | probe entry point (`scripts/verify-sandbox.sh` for the CLI adapter) |
| `evidence` | where results are recorded; schema version |
| `status` | `supported`, `planned`, `blocked` — with reason |

Contract: an adapter MUST NOT claim `supported` without a recorded passing verification; adding an adapter never weakens another adapter's profile.

## Support matrix (authoritative at merge time)

| Runtime | Enforcement | Status | Evidence |
| --- | --- | --- | --- |
| omp / macOS CLI | Seatbelt launcher (deny-default profile) | supported | `scripts/verify-sandbox.sh` 39/39, macOS 27.0.1, live agent run |
| Codex CLI | native permission profiles | planned (beta profile exists at `templates/host-access/codex-workspace-only.toml`) | none — UNVERIFIED |
| Codex Desktop (GUI) | worker-process audit | planned | none — UNVERIFIED |
| Claude Code | sandbox/permissions audit | planned | none — UNVERIFIED (2.1.304 deny bypass observed) |
| IDE extension | extension-host child policy | planned | none — UNVERIFIED |
| Remote/Cloud agent | runner/container isolation audit | planned | CNB runner container evidence exists (Issue #63) but not bound to this contract |
| MCP servers / subagents | inherit launcher profile (CLI) | verified for CLI children | included in verify-sandbox.sh vectors |
| Network isolation | none in current adapters | blocked pending design | out of scope of FS evidence |

Rules: statuses change only with evidence attached here; "supported" is per runtime kind, not per product family.

## Owner authorization boundary

No global alias, GUI app, IDE setting, or system security policy is modified by this governance; runtime-specific activation (e.g. making a sandboxed launcher the default) is a separate owner-approved action per runtime.

## Version boundary (2026-10-28)

- **Mode A (CNB Primary → GitHub Mirror) is part of the published, immutable v0.4.2** and has passed isolated live acceptance — consumers may pin v0.4.2 for Mode A adoption.
- **The macOS CLI Seatbelt hardening (PR #83) is merged to `dev` only** and is NOT part of any published release; it is a candidate for a future version. Do not attribute OS-level sandbox enforcement to a v0.4.2 pin.
- **Per-runtime support statuses above are independent**: the macOS CLI Seatbelt verification must not be generalized to GUI, desktop, IDE or remote runtimes; each requires its own evidence.
- Consumer cutovers (including ALNILAM) remain separately authorized; task tracking stays on GitHub regardless of provider mode.
