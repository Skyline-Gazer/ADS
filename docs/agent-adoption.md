# Using ADS with an existing coding agent

ADS is not a daemon, CLI or centralized policy delivery service. A file existing in ADS does not make the host agent automatically discover it.

## Mandatory Git workflow

Before ordinary work, apply the [mandatory Git governance policy](git-governance.md). The consumer must have a `dev` integration branch; create it through a reviewable migration if absent. Every feature/fix/chore/docs/refactor/test/CI task starts from the latest `dev`, references an Issue, and is delivered by a PR to `dev`. Production changes use a separate release PR; emergency fixes are developed from `dev` and selectively backported as the same reviewed change. During adoption, inspect actual CI check names and branch protection with authenticated `gh`; if classic protection is absent/incomplete, run `templates/git-governance/ensure-ads-branch-protection.py` from the consumer repository with exact `--required-check` names, then verify the API result. A `403` is an access/plan blocker, not evidence that protection is absent. Existing consumers are migrated through scoped PRs, not silently rewritten.

## Pin and make guidance accessible

1. Pick an approved ADS release or immutable full commit SHA.
2. **Default for new consumers:** add ADS as a pinned Git submodule at `.ads` following [how-to-update.md](how-to-update.md), using a published approved tag/full SHA and authorized clone access. Existing vendored or connector-based consumers may migrate on an isolated branch, after inspecting existing files and deploy rules; don't destructively overwrite an existing `.ads` path. If submodules are genuinely unsupported, document the fallback and keep one immutable, locally readable rule snapshot.
3. Add a short project AGENTS.md based on [templates/AGENTS.md](../templates/AGENTS.md) specifying the **actual consumer gitlink SHA**, `.ads` rule paths, build commands, auto-deploy behavior and real operational limits. Root AGENTS.md remains necessary: an agent will not automatically load nested submodule policies. Do not point only to a private URL that the agent cannot access.
4. Expose the skill directories through that host's **documented** native discovery mechanism, or explicitly instruct the agent to read a particular SKILL.md. Test discovery with a harmless prompt. Do not assume a generic .agents/skills path works on every agent version.

5. Keep a single content source. Platform adapters should contain minimal links/pointers, not duplicated conflicting policy.
6. At an explicit request, a Phase/Milestone checkpoint or an owner-configured periodic trigger, check approved upstream releases without changing the consumer gitlink. To upgrade, compare exact old/new SHAs, review guideline and host Skill changes, advance the submodule on a task branch, test a scoped task and send a PR. `git submodule update --init --recursive` only materializes the parent-recorded pin and does not fetch the latest version automatically; see [how-to-update.md](how-to-update.md).

Verified example (OMP): a skill is discovered natively at `<project>/.omp/skills/<name>/SKILL.md` (non-recursive; the host also scans ancestor `.omp/skills` directories and `~/.omp/agent/skills`, and has separate Claude/Codex/`.agents`/`.github` project providers). Copying `skills/bootstrap`, `skills/recover`, `skills/adopt` or `skills/deliver` there exposes it natively. ADS itself ships no host-specific skill directory, so a bare clone exposes nothing until the chosen skills are copied or linked into that path. Run a harmless discovery prompt after copying and record the host version.

## Boundaries

- A private GitHub repository requires explicit read permission, and may be inaccessible to other agents or offline hosts.
- Agents cannot continue after a session terminates unless the host platform offers persistence or scheduling.
- Native deployment integrations remain authoritative; ADS does not create another deploy controller.
- `actions/checkout` of a private consumer does not itself guarantee access to a different private ADS repository; provide only authorized checkout credentials in existing secure CI configuration.
- Phase closure and GitHub Project status alignment follow [milestone-reconciliation.md](milestone-reconciliation.md); unqueried Project fields never count as verified alignment.
- A repository's CI/security hooks can override behavior until separately migrated. Never claim adoption was successful without checking executable restrictions.
