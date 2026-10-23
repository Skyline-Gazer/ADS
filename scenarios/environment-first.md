# Environment-first probe, reuse and fallback evidence

**Status:** PARTIALLY RUN on one host (OMP 18.11.3, macOS arm64, 2026-10-17). Proportional probe, fresh isolated reuse task, repeat recheck, missing-capability fallback and probe-disclosure regression were executed. Other hosts and clean-machine bootstrap remain NOT TESTED.

This is the compact optional example for the [STANDARD.md](../STANDARD.md) "Environment first, reuse first" principle and the [QUALITY.md](../QUALITY.md) "Environment and verification reuse" section. It intentionally creates no inventory artifact, CLI, daemon, state store or mandatory phase. Remote-first selection is specified separately in [remote-first-verification.md](remote-first-verification.md); the local-host evidence below does not claim remote CI or target-platform validation.

## One proportional probe

Availability, version and repository-declared command checks only. No environment values, tokens or credential files are read; the documentation checker in `scripts/check-ads.py` rejects code blocks containing disclosing commands, and such prohibitions must be written in prose rather than as negative examples in code.

```sh
command -v python3 node bun uv gh
python3 -m unittest discover -s tests
git status --short --branch
```

## Report states, not a boolean

| State | Meaning | Observed on this host |
| --- | --- | --- |
| absent | not on `PATH`; do not install silently | `deno` |
| installed | present, may be unrelated or unused for this task | `uv`, `docker`, `wrangler` |
| configured | present and set up for the intended use | `gh` (authenticated; only masked status inspected) |
| verified | actually exercised for the task | `python3` 3.9.6 with stdlib `unittest`, `node` v22.23.2 |

## Proportionality

- Ordinary task: run the probe above once, reuse the findings for the rest of the session.
- Deeper investigation only for a first bootstrap, a host migration, an expensive integration or known drift.
- Re-verify a stale assumption with one command instead of keeping an environment database.

## Recorded results

| Case | Command and result | Outcome |
| --- | --- | --- |
| Fresh isolated reuse task | Disposable Git repo with one module and stdlib tests: `python3 -m unittest discover -s tests -v` → rc 0, 2 tests pass | PASS: reused the installed `python3` and the repository's existing `unittest discover` convention; no package manager ran and no second runtime was added |
| No second framework | `python3 -m pytest --version` → rc 1, `No module named pytest` | PASS: absence confirms no test framework was installed for the task |
| Repeat recheck | `command -v python3` → rc 0 | PASS: one command re-verified the earlier finding; no re-scan of the environment |
| Missing capability | `command -v deno` → rc 1, absent; fallback `node -e` → rc 0 | PASS: genuine absence reported as a boundary and satisfied by the smallest installed fallback |
| Probe disclosure | The documentation check rejects disclosing probe commands in fenced, blockquoted and 4-space-indented code regions: `printenv`, bare `env`/`set`, `export -p`, `declare -x`, `compgen -v`, `os.environ`/`os.getenv`, `--env-file`, reads or transfers of credential and `.env` files, GitHub token commands, CI secret contexts and credential-named variable interpolation; it also reports an unterminated fence. Prose prohibition is not flagged. Documented false-positive class: a credential-named variable is flagged whenever it is interpolated, even for a name-only use; `.env.example`-style templates and `id_rsa.pub` are exempt | PASS: one fixture test per rule (13/13 caught by mutation), 28-case coverage check, clean repo-wide scan |
| Host capability discovery | Read-only: OMP 18.11.3; native Skills `bootstrap`, `adopt`, `deliver`, `recover`; Python 3.9.6, Node v22.23.2, git, gh, make, docker present; `deno` absent | DISCOVERED: no capability was installed or reconfigured to obtain this |

## Boundaries

- OMP 18.11.3 on macOS arm64 was exercised in this environment-first scenario. Separate operator-reported acceptance runs are archived for [OpenCode v2.0.32](v0.3-opencode-acceptance.md), [Codex CLI 0.163.0](v0.3-codex-closure.md) and [Claude Code 2.1.292](v0.3-claude-code-acceptance.md). Those acceptance results do not turn this specific scenario into a multi-host environment-first test; clean-machine bootstrap and cross-host reuse remain unverified.
- No container, cloud resource, global package or credential was created, modified or required.
- A hosted CI run is separate evidence from these local runs; report both distinctly.
