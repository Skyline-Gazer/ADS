# Using ADS with an existing coding agent

ADS is not a daemon, CLI or centralized policy delivery service. A file existing in ADS does not make the host agent automatically discover it.

## Pin and make guidance accessible

1. Pick an approved ADS release or immutable full commit SHA.
2. Place the relevant ADS rules and selected SKILL.md content where the coding agent can actually read them: vendor a small snapshot in the project, or explicitly load the pinned files through a properly authorized GitHub connector.
3. Add a short project AGENTS.md based on templates/AGENTS.md specifying the pin, accessible location, commands, auto-deploy behavior and real operational limits. Do not point only to a private URL that the agent cannot access.
4. Expose the skill directories through that host's **documented** native discovery mechanism, or explicitly instruct the agent to read a particular SKILL.md. Test discovery with a harmless prompt. Do not assume a generic .agents/skills path works on every agent version.

5. Keep a single content source. Platform adapters should contain minimal links/pointers, not duplicated conflicting policy.
6. To upgrade, review the diff between pinned revisions and test with one scoped task; then update the pin explicitly.

Verified example (OMP): a skill is discovered natively at `<project>/.omp/skills/<name>/SKILL.md` (non-recursive; the host also scans ancestor `.omp/skills` directories and `~/.omp/agent/skills`, and has separate Claude/Codex/`.agents`/`.github` project providers). Copying `skills/bootstrap`, `skills/recover`, `skills/adopt` or `skills/deliver` there exposes it natively. ADS itself ships no host-specific skill directory, so a bare clone exposes nothing until the chosen skills are copied or linked into that path. Run a harmless discovery prompt after copying and record the host version.

## Boundaries

- A private GitHub repository requires explicit read permission, and may be inaccessible to other agents or offline hosts.
- Agents cannot continue after a session terminates unless the host platform offers persistence or scheduling.
- Native deployment integrations remain authoritative; ADS does not create another deploy controller.
- A repository's CI/security hooks can override behavior until separately migrated. Never claim adoption was successful without checking executable restrictions.
