# Using ADS with an existing coding agent

ADS is not a daemon, CLI or centralized policy delivery service. A file existing in ADS does not make the host agent automatically discover it.

## Pin and make guidance accessible

1. Pick an approved ADS release or immutable full commit SHA.
2. **Default for new consumers:** add ADS as a pinned Git submodule at `.ads` following [how-to-update.md](how-to-update.md), using a published approved tag/full SHA and authorized clone access. Existing vendored or connector-based consumers may migrate on an isolated branch, after inspecting existing files and deploy rules; don't destructively overwrite an existing `.ads` path. If submodules are genuinely unsupported, document the fallback and keep one immutable, locally readable rule snapshot.
3. Add a short project AGENTS.md based on [templates/AGENTS.md](../templates/AGENTS.md) specifying the **actual consumer gitlink SHA**, `.ads` rule paths, build commands, auto-deploy behavior and real operational limits. Root AGENTS.md remains necessary: an agent will not automatically load nested submodule policies. Do not point only to a private URL that the agent cannot access.
4. Expose the skill directories through that host's **documented** native discovery mechanism, or explicitly instruct the agent to read a particular SKILL.md. Test discovery with a harmless prompt. Do not assume a generic .agents/skills path works on every agent version.

5. Keep a single content source. Platform adapters should contain minimal links/pointers, not duplicated conflicting policy.
6. At an explicit request, a Phase/Milestone checkpoint or an owner-configured periodic trigger, check approved upstream releases without changing the consumer gitlink. To upgrade, compare exact old/new SHAs, review guideline and host Skill changes, advance the submodule on a task branch, test a scoped task and send a PR. `git submodule update --init --recursive` only materializes the parent-recorded pin and does not fetch the latest version automatically; see [how-to-update.md](how-to-update.md).

Verified example (OMP): a skill is discovered natively at `<project>/.omp/skills/<name>/SKILL.md` (non-recursive; the host also scans ancestor `.omp/skills` directories and `~/.omp/agent/skills`, and has separate Claude/Codex/`.agents`/`.github` project providers). Copying `skills/bootstrap`, `skills/recover`, `skills/adopt` or `skills/deliver` there exposes it natively. ADS itself ships no host-specific skill directory, so a bare clone exposes nothing until the chosen skills are copied or linked into that path. Run a harmless discovery prompt after copying and record the host version.

## Mandatory consumer developer-toolchain

For the consumer repository being adopted, complete the required CodeGraph + full RTK preflight described in [consumer-dev-toolchain.md](consumer-dev-toolchain.md). This applies to the consumer, not to ADS itself.

- Check the latest stable upstream release, installed binary version, project initialization and actual host integration separately.
- Ask before installing a missing tool or changing global configuration. If the binaries already exist, initialize the consumer project's integration on a development branch without asking the user to repeat safe project-local work.
- Keep the consumer manifest, host integration and tool-specific configuration off the consumer's production `main`; install the generic branch-boundary guard before enabling the development-only integration.
- Explicitly sync and verify CodeGraph after source changes before using graph output for impact analysis.

## Boundaries

- A private GitHub repository requires explicit read permission, and may be inaccessible to other agents or offline hosts.
- Agents cannot continue after a session terminates unless the host platform offers persistence or scheduling.
- Native deployment integrations remain authoritative; ADS does not create another deploy controller.
- `actions/checkout` of a private consumer does not itself guarantee access to a different private ADS repository; provide only authorized checkout credentials in existing secure CI configuration.
- Phase closure and GitHub Project status alignment follow [milestone-reconciliation.md](milestone-reconciliation.md); unqueried Project fields never count as verified alignment.
- A repository's CI/security hooks can override behavior until separately migrated. Never claim adoption was successful without checking executable restrictions.
