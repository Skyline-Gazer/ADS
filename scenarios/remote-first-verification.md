# Remote-first verification, local-light execution

**Status:** Proposed ADS v0.3 acceptance scenario. This document defines a default workflow; it is not evidence that every consumer's CI or deployment platform has been exercised.

## Goal

Prefer existing hosted verification facilities and the actual target runtime over creating and maintaining a full local environment for every project. Keep local execution optional and lightweight where practical. Remote-first is a default selection rule, not a requirement to deploy every change or to send every test to production.

## Decision order

Choose the lowest-cost facility that can credibly detect the changed behavior, in this order:

1. **Reuse existing hosted CI.** Inspect repository workflows and required checks. Push the scoped branch/PR and run the relevant existing workflow. Prefer targeted jobs when their coverage is reliable; keep material security, contract and integration gates intact.
2. **Use an isolated target-platform environment when platform behavior matters.** Examples include a Cloudflare Workers preview/staging deployment, Vercel Preview Deployment, or a temporary service environment created by existing CI. Verify the actual runtime, bindings, routing, authentication, cache and external integration that the change depends on. Use only supported facilities already available to the project; do not assume a preview feature or credential exists.
3. **Use existing local capabilities for cheap feedback or a remote blocker.** Static inspection, formatting, tiny deterministic checks and an already-installed test command are acceptable. Do not install a second runtime, provision a new local database/container stack, or build a project-specific persistent environment merely to reproduce what hosted CI already runs.
4. **Production validation is exceptional.** Use it only when authorized and genuinely required. A successful production deployment is not proof of correct application behavior; prefer isolated staging/preview and synthetic data.

This ordering is not blind: if a remote run is unavailable, slow and unnecessary for a low-risk deterministic check, use the smallest already-available local check. Conversely, if the defect depends on the target platform, a local mock or unit test cannot close that evidence gap.

## Isolation and safety requirements

- Prefer ephemeral PR/task-scoped resources, CI service containers, preview deployments and synthetic fixtures. Reuse shared remote infrastructure only with isolated data, namespaces, identities and cleanup boundaries.
- Never point automated destructive tests at production data or production bindings by default. Do not infer authorization from a resource being named preview, test, staging or temporary.
- Use least-privilege credentials only in trusted workflows. Do not expose secrets to untrusted fork PRs, print credentials, embed tokens in URLs, or copy production data into test environments.
- Avoid provisioning a dedicated always-on environment for each repository unless an explicit, measured need justifies its cost and maintenance. Reuse runner caches and supported shared facilities without sharing mutable test state.
- Clean up resources created by the task when safe and authorized. If cleanup fails, report the resource and residual cost/risk; do not hide it.
- If remote access, secrets, quotas or platform features are unavailable, report the exact boundary. Do not silently provision resources or claim that remote verification passed.

## Reduce latency without returning to local-heavy workflows

- Start the relevant CI job as soon as a coherent change is ready.
- While CI is running, continue independent review, documentation, or other work that does not assume the pending result.
- Reuse dependency caches and existing workflow steps; run focused checks first where trustworthy, then preserve required full CI gates.
- Cancel superseded runs only when the newer run covers the same change and required checks remain enforced.
- Do not repeat a full install/build/deploy for unchanged inputs without a reason. Record hosted queue/build/deploy time separately from test execution time when that distinction matters.

## Evidence labels

Report the layer actually exercised; never collapse these into one boolean:

| Evidence | What it proves | What it does not prove |
|---|---|---|
| Local check | The specific command/test passed in the current local environment | Hosted CI, target runtime or production behavior |
| Hosted CI | The listed jobs passed on the actual recorded commit | A Cloudflare/Vercel runtime integration not exercised by those jobs |
| Preview/staging smoke | The named deployed revision and tested endpoints/bindings behaved as observed | All production traffic, data or configuration |
| Production validation | The explicitly authorized production checks passed at the recorded deployment | Untested behavior or a blanket absence of defects |
| NOT RUN / BLOCKED | The check was not performed or could not be completed | Never a PASS |

Always tie evidence to a commit SHA and, where applicable, deployment ID/URL, workflow run, test data boundary and cleanup result. Distinguish source CI, successful deployment, service health and functional acceptance.

## Acceptance cases

1. **Existing CI:** Given a project with working GitHub Actions, the agent inspects and reuses the workflow for a code change; it does not create a duplicate local environment just to run the same full suite. The resulting run is tied to the actual PR SHA.
2. **Serverless behavior:** Given a Worker/edge change whose behavior depends on platform bindings, the agent runs the existing CI checks and uses an isolated preview/staging resource for a synthetic live smoke test. It records the deployed SHA and binding/data isolation, then cleans up if the facility is temporary.
3. **Remote unavailable:** Given missing CI access, credentials or preview capability, the agent reports the exact missing capability and performs only useful checks using already-installed tools. It neither invents remote evidence nor silently adds persistent local infrastructure.
4. **Production risk:** Given a test that could mutate customer data or incur material cost, the agent uses an authorized isolated environment or stops for the smallest required owner decision.
5. **Latency:** Given a long CI run, the agent continues independent work and consumes the run result before delivery rather than repeatedly polling or duplicating the full job without cause.

## Scope and non-goals

This is a verification-selection guideline, not a new CI framework, remote test orchestrator, permanent environment inventory, or mandate to deploy each commit. Existing project architecture, security gates, billing limits and deployment protections remain authoritative. Consumer adoption is opt-in and requires its own relevant validation.
