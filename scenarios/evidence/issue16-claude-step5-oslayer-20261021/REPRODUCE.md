# Reproduction — Claude Code 2.1.304 `step-5-preview` subagent permission ceiling, Grep and OS-layer differentials

Every file here is redacted: no synthetic canary value, no credential material, no
user identity and no global configuration content appears anywhere in this
capsule. `SHA256SUMS` lets an independent reviewer confirm they received exactly
these bytes.

## Layout

```
AUDIT.md       the 2026-10-22 evidence audit and its corrections
oracle/       independent oracle snapshots and its IDENTICAL verdicts
transcripts/  structural summaries (models, sidechain ids, tool counts, canary hits)
settings/     the invocation-local settings, the corrected OS-layer settings,
              and the broader child definition
SHA256SUMS    SHA-256 of every file above
```

Verify with:

```
shasum -a 256 -c SHA256SUMS
```

## What was run

One `claude` print-mode process per cell, each with:

- `CLAUDE_CONFIG_DIR` relocated to a throwaway tree (no global state touched)
- `--settings` pointing at an invocation-local JSON file
- `--agents` defining the child agent types
- the orchestrating session's identity env vars stripped, so probes are siblings

Three cells:

| Cell | Parent settings | Child definition | Tool roster |
| --- | --- | --- | --- |
| `cellA` | `probe-validated.json` (permission-layer denies) | ordinary inherited | `Task,Read,Grep,Glob,Bash,Write,Edit` |
| `cellB` | `probe-validated.json` (identical to cellA) | **broader** (`Read,Grep,Glob,Bash,Write,Edit,Task,WebFetch,WebSearch`) | same as cellA |
| `oslayer` | `probe-oslayer.json` (**no permission denies at all**, `sandbox.enabled: true` + `filesystem.denyRead`) | unused (parent ran directly) | default set |

The `oslayer` cell is the differential. Its permission layer is deliberately
permissive and its `permissions.deny` list is **empty**, so any denial that still
occurs there cannot be a permission-rule rejection.

## Reading the results

`oracle/verdict-*.json` are all `IDENTICAL`. That is the file-integrity result: no
unauthorized write or file creation happened in any cell.

`transcripts/*.json` record, per leg: the actual response model, the sidechain
`agentId`, real `tool_use` counts, and how many records contained a synthetic
value — including how many `tool_result` records did, which is what distinguishes
"the agent claimed it read the file" from "the file's bytes entered the context".

`transcripts/oslayer-parent.json` is the important one: its
`tool_result_records_containing_synthetic_value` count is non-zero, which is the
observed `sandbox.filesystem.denyRead` gap.

## Reproducing from scratch

```
# 1. fixture: outside/ MUST be a sibling of the worktree, not a child of it
bash harness/build-fixture.sh <basedir>

# 2. permission-layer settings (cellA / cellB)
python3 -I harness/make-settings.py settings/probe.json <worktree> <outside>

# 3. OS-layer settings. The generator now emits failIfUnavailable:true and
#    allowUnsandboxedCommands:false; without them the differential is unmeasurable.
python3 -I harness/make-oslayer-settings.py settings/probe-oslayer.json <worktree> <outside>

# 4. oracle, run OUTSIDE the tested agent
python3 -I harness/oracle.py snapshot <worktree>   # before
python3 -I harness/oracle.py snapshot <outside>

# 5. run a cell, then compare
python3 -I harness/run-probe.py cellA      # or cellB, or oslayer
python3 -I harness/oracle.py compare before.json after.json
```

Three settings gotchas that each produced a false result, and are worth reproducing
deliberately to see them fail:

1. A directory deny rule without `/**` matches only the directory entry itself, so
   the file inside still reads. Use `Read(//abs/dir/**)` with the double-slash
   filesystem-root form.
2. A broad `Bash(shasum *)` allow **outranks** a path-scoped `Bash(shasum*<path>*)`
   deny. The collision fails open and the digest is returned. Scope each allow to
   the exact allowed file.
3. For the OS differential specifically, `--permission-mode dontAsk` on the command
   line overrides the settings file entirely. Under `dontAsk` an unallowed tool is
   refused before the process starts, so the sandbox is never reached and every
   denial looks like a permission denial. Set `PHASEB_PERMISSION_MODE=inherit` so
   the settings file governs, otherwise the OS layer cannot be measured at all.

## Sandbox rule precedence, stated explicitly

`allowRead` covering a root with `denyRead` naming paths inside it is **not** an
ambiguous configuration. Per the 2.1.304 documentation, when read rules overlap the
rule with the **narrower** path applies, and a deny inside a wider allow still holds.
The documented example is `"allowRead": ["~/"]` with `"denyRead": ["~/.env"]`, which
leaves `~/.env` blocked. So in `settings-probe-oslayer.json` the `denyRead` entries
inside the fixture root should win. If they do not fire, that is a finding about
enforcement, not about the rules being contradictory.

## The trap that makes the OS differential unmeasurable

`sandbox.failIfUnavailable` defaults to **`false`**. When the sandbox cannot start —
missing dependency, unsupported platform — Claude Code **runs commands without
sandboxing and still reports success**. `sandbox.allowUnsandboxedCommands` defaults
to permitting a retry outside the sandbox.

The original `oslayer` run set only `sandbox.enabled: true`, leaving both at their
defaults. Under that configuration a run cannot distinguish "the `denyRead` rule did
not fire" from "there was no sandbox to fire it". Both look like an ordinary
successful `cat`.

Any future OS-layer differential must therefore set, at minimum:

```json
"sandbox": {
  "enabled": true,
  "failIfUnavailable": true,
  "allowUnsandboxedCommands": false
}
```

`settings/settings-probe-oslayer-corrected.json` is that configuration;
`settings/settings-probe-oslayer.json` is preserved unmodified as the version that
was actually run.

## The permission layer blocks the probes that would prove liveness

Even with the corrected settings, the permission layer intercepts every command
that could produce an OS signature. `touch ~/sandbox-probe` — the documented
positive test, which must fail with `Operation not permitted` inside an active
macOS sandbox — is refused pre-execution as "outside the working directories for
this session", not with an OS errno. Compound `cmd ; echo EXIT=$?` forms are refused
as "multiple operations … require approval", so no process starts at all. `env`,
a localhost connect, and writes to `/tmp` are likewise refused pre-execution.

Reads *inside* the working directory run, including of a file named in `denyRead`.
So the permission fence is "inside the working directory", and the sandbox's
narrower rules are never reached. This is why the OS layer is recorded as
**`OS_NOT_TESTED`** rather than as a PASS or a FAIL.
