# Project-only filesystem reads for local TUI Agents

ADS Issue [#72](https://github.com/Skyline-Gazer/ADS/issues/72) covers an observed macOS TUI exploration of personal directories (for example `~/Music`) outside an authorized project. **Reading, listing, searching, hashing, indexing or opening any personal-directory entry is access.** A restriction on **writes** is not a restriction on **reads**. Neither AGENTS.md, Git worktrees, CodeGraph's project index, Git ignore rules nor ordinary ADS CI can enforce a running TUI's OS-level file access.

## Default authorization boundary

The Owner's project/task grant is the only starting point: files within the canonical project workspace, read-only *minimal system/runtime* tools required to run the task, and separately approved external sources with exact real paths and purpose. Other user home directories, sibling projects, removable volumes and connected app/MCP files are **denied by default** for reads AND writes, even if a command or file search would be convenient. External access requires an **explicit narrowly scoped grant** and the runtime's enforceable policy must reflect it. No project instructions, Agent self-promise, subagent prompt or untrusted tool output grants access. If an internal dependency cannot run with the restricted profile, report the minimum precise exception instead of making all of `$HOME` readable.

This applies to the **main TUI Agent, its native child Agents, shell/Python/Ruby/node commands, search/glob tools, CodeGraph/RTK invocations, native filesystem APIs, MCP servers, and background commands**. A permitted shell that can bypass a forbidden file-tool Read is not containment. Native MCP connectors or an unsandboxed service may have different permissions; evaluate them separately. Avoid launching from `~`, `~/Desktop` or a parent containing unrelated personal data. Check actual session CWD and effective workspace roots.

### Mac and host adapter selection

**Codex CLI with filesystem permission profiles (beta):** See [official permission profiles](https://learn.chatgpt.com/docs/permissions). On a supporting macOS Codex build, use a named **workspace-only** profile with `":root" = "deny"` plus `":minimal" = "read"`; keep the workspace writable and unnecessary `/tmp` reading disabled. A version-gated example is at [templates/host-access/codex-workspace-only.toml](../templates/host-access/codex-workspace-only.toml). Test its actual application to the TUI and to the commands the TUI runs: a project config can be ignored for untrusted workspaces or overridden by other CLI flags; `sandbox_mode` / `--sandbox` **selects the legacy mode instead of** `default_permissions`. **Do not combine the two systems.** Legacy `workspace-write` does not establish no-read-outside, even though it prevents ordinary external writes. Do not use `danger-full-access`, bypass flags or extra writable roots to get a green test. `codex sandbox macos --permissions-profile ads-project-only ...` can test a contained command, but a passing command probe does not prove native TUI/file-search/MCP accesses have the same policy.

**Claude Code:** Verify active `/sandbox` and `/permissions` configuration. Host Read/Glob/Grep denial syntax is version-dependent; this ADS repository has already observed that a seemingly accepted single-slash `Read(/absolute/path/**)` deny did not block a read in Claude Code 2.1.304 ([native subagent findings](native-subagent-safety.md)). Deny shell escape routes, indirect file paths, inherited child permissions and MCP access as well as direct `Read`. Test OS-level enforcement using an explicit project-only read+write restriction, or isolate the entire Claude process in a dedicated container/VM. A tool-level deny alone is not a general OS read sandbox. Do not edit `~/.claude` or global settings automatically.

**Other hosts:** Establish an equivalent OS-enforced read AND write boundary. If unavailable, mark `PROMPT_ONLY` / `BLOCKED`, use a separate isolated VM/container with no mounted user-home directories, or suspend tasks needing isolation. Host extensions and external filesystem/search MCPs are separate attack surfaces, not covered automatically by a shell sandbox.

## Read-only preflight at Bootstrap / Adopt / Deliver / resume

1. Identify the executing host/version and current **real** repo root and actual working directory. Verify that the TUI is started from the intended repo, not a parent directory; capture only sanitized metadata.
2. Inspect the active effective permissions / sandbox profile, all extra directory grants, connected filesystem/search/indexer/MCP mounts and child grants without dumping credentials or global configuration values. Detect legacy Codex sandbox mode when a modern profile was intended.
3. Prepare disposable synthetic files at an authorized test workspace and a separate Owner-approved *synthetic* sibling path (NOT `~/Music`, not real Documents/Downloads/SSH files). Keep probe locations outside Git and avoid copying source data.
4. Run **within the actual host-enforced command sandbox** the [filesystem probe](../scripts/host_filesystem_probe.py) with exactly two synthetic file paths, one allowed and one denied; see usage below. Verify inside reads succeed; outside `open`, `os.listdir`, `cat`, `shasum` and a workspace symlink into the denied synthetic file fail specifically with an access-denied result. A missing command or nonexistent denied file is **not** proof of denial. The probe emits result labels only, never canary contents. Independently verify fixtures exist/read correctly *outside* the tested sandbox.
5. Run equivalent negative attempts through **the native TUI Read, Glob, Grep, Shell, CodeGraph/RTK indexer, each connected filesystem MCP and each subagent** when those capabilities have access. A shell-only probe is not sufficient proof of these tool paths.
6. Report `VERIFIED_BOUNDED` only for paths, host version, policy, tool routes and vectors actually tested. A successful unauthorized synthetic read/list/hash is `UNSAFE`; merely documented restrictions are `PROMPT_ONLY`; missing verified policy/host/test is `BLOCKED` or `NOT_TESTED`. For sensitive work an unresolved read escape **blocks task execution**; for ordinary work, disclose limitation and use a truly isolated environment instead of claiming safety.
7. Re-check when the TUI version, profile, subagent, directory grants or MCP inventory changes. Never give the Agent authority to widen its own profile to make tests pass.

### Synthetic probe command

The user / independent verifier prepares two harmless text files in *disposable* directories, with the **exact basenames** `ADS_ALLOWED_PROBE.txt` within the real project workspace and `ADS_DENIED_PROBE.txt` in a separate synthetic sibling directory outside the workspace. The allowed file contains `ADS_ALLOWED_PROBE_V1`; the forbidden file can contain arbitrary synthetic text. Add an optional symlink named `ADS_OUTSIDE_LINK` inside the workspace pointing to the denied synthetic file.

Run the command **through the actual host's constrained command-runner**, for example:

```sh
# Substitute ONLY owner-created synthetic probe paths and the verified host profile.
codex sandbox macos --permissions-profile ads-project-only python3 scripts/host_filesystem_probe.py --inside ./ADS_ALLOWED_PROBE.txt --outside ../ads-synthetic-private/ADS_DENIED_PROBE.txt --link ./ADS_OUTSIDE_LINK
```

The parent-directory test area must be authorized by the Owner and must not be a real personal folder. Inspect JSON verdict. An `UNSAFE` outcome should stop this host's sensitive workflow immediately. Delete synthetic fixtures only under the exact authorized disposable test path. Never run probe operations against actual `~/Music`, private SSH files or other user content.

**Limitations:** Neither this probe nor its unit tests is an OS sandbox; they are a test instrument. The sandbox must be selected in the *launching host*. Runtime permission profiles are beta and need version-specific validation. Recording no leaked text is not proof that no read occurred. Live macOS TUI verification remains `NOT_TESTED` until independently executed on that machine.

