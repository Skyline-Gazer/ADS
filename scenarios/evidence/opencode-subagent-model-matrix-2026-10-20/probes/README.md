# Mechanism probes

These probes establish host behaviour; they are not the measured workload cells.

| Directory | What it shows |
| --- | --- |
| `background-disposal/` | Two `background: true` subagent calls create two real child sessions, then the parent ends its turn; `opencode run` exits and both children stay at zero tokens with no work. Preserved FAIL. |
| `per-child-model-and-shell-bypass/` | Parent and two children resolve the per-agent configured models (parent `deepseek-flash`, child A `deepseek-flash`, child B `deepseek-v4-pro`); an `edit` deny does **not** stop a shell redirection, so `zeta.txt` was created by a child whose edit permission was restricted to `beta.txt`. |
| `child-permissions-not-subset/` | Parent is denied `read creds.txt`; an unconfigured child reads it successfully. A restricted sibling is blocked from the same read and from shell writes. Child permissions are independent, not a subset. |
| `agent-flag-does-not-select-model/` | With `--agent orchestrator` but no `--model`, the session ran `magpie/group/free-deepseek` from global config, not the agent's `deepseek/deepseek-flash`. Discarded cell, kept as evidence. |
| `path-escape-blocked/` | With `external_directory: deny`, a child allowed to edit anything inside the project is blocked from both `/tmp/.../escape-absolute.txt` and `../escape-relative.txt` by `permission.rejected: external_directory`; a project-relative write succeeds. Verified against the filesystem. |
| `unavailable-model/` | Requesting a nonexistent model fails explicitly with `provider.no-route`, exit code 1; no silent fallback. |
