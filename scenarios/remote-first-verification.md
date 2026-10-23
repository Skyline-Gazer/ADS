# Remote-first verification and autonomous environment provisioning

**Status:** Proposed ADS v0.3 acceptance scenario. This document defines a default workflow; it is not evidence that every consumer's CI or deployment platform has been exercised.

## Goal

Prefer remote verification and the actual target runtime over creating and maintaining a full local environment for every project. If no suitable remote environment exists, autonomously create the smallest task-scoped one when the existing authorization, credentials, permissions, quotas and budget permit it. Keep local execution optional and lightweight where practical. Remote-first is not a requirement to deploy every change or to send every test to production.

## Decision order

Choose the lowest-cost facility that can credibly detect the changed behavior, in this order:

1. **Reuse existing hosted CI.** Inspect repository workflows and required checks. Push the scoped branch/PR and run the relevant existing workflow. Prefer targeted jobs when their coverage is reliable; keep material security, contract and integration gates intact.
2. **Reuse existing target-platform previews or test environments.** For example, use an already-configured Cloudflare Workers preview, Vercel Preview Deployment, or a task-scoped environment created by existing CI when real runtime, bindings, routing, authentication, cache or external integration matters.
3. **If the needed remote facility is absent, create it autonomously when authorized.** Add the smallest repo-native hosted CI workflow or configure an ephemeral provider-native preview/test environment using existing authorized credentials and capabilities. Check permissions, quotas, cost, data isolation and cleanup before provisioning. Prefer temporary resources with bounded lifetime; don't build a permanent platform just to satisfy one test. Do not assume credentials or permissions exist—inspect the available capability first.
4. **Ask only for a genuine authorization or access blocker.** If creation needs an owner-only integration, unavailable secret/permission, new spend or plan upgrade, broader IAM, production access, or another action outside the current grant, give the user exact provider-specific steps and the minimum required permission/setting. Continue independent safe work; do not claim the remote check passed.
5. **Use existing local capabilities as a bounded fallback.** Static inspection, formatting, tiny deterministic checks and already-installed test commands are acceptable if remote verification is unnecessary or cannot be provisioned within scope. Do not install a second runtime or create a duplicate local stack merely to reproduce existing CI.
6. **Production validation is exceptional.** Use it only when explicitly authorized and genuinely required. A successful production deployment is not proof of correct application behavior; prefer isolated staging/preview and synthetic data.

This ordering is not blind: documentation-only changes may need only hosted documentation CI, not a deployed preview. Conversely, if a defect depends on the target platform, a local mock or unit test cannot close that evidence gap.

## Isolation and safety requirements

- Prefer ephemeral PR/task-scoped resources, CI service containers, preview deployments and synthetic fixtures. Reuse shared remote infrastructure only with isolated data, namespaces, identities and cleanup boundaries.
- Never point automated destructive tests at production data or production bindings by default. Do not infer authorization from a resource being named preview, test, staging or temporary.
- Use least-privilege credentials only in trusted workflows. Do not expose secrets to untrusted fork PRs, print credentials, embed tokens in URLs, or copy production data into test environments.
- Avoid provisioning a dedicated always-on environment for each repository unless an explicit, measured need justifies its cost and maintenance. Reuse runner caches and supported shared facilities without sharing mutable test state.
- Clean up resources created by the task when safe and authorized. If cleanup fails, report the resource and residual cost/risk; do not hide it.
- Provisioning should be autonomous only within the current grant and established budgets/quotas. Do not silently incur new recurring charges, upgrade a plan, broaden IAM, expose secrets, change production, use customer data or create long-lived infrastructure outside scope.
- If a user action is necessary, specify the provider, exact permission/integration/secret/variable or budget decision, secure setup steps, and the verification that will resume afterward. Never request that the user repeat a step the agent can perform.
- If remote access, secrets, quotas or platform features remain unavailable after safe provisioning options are checked, report the exact boundary. Do not claim that remote verification passed.

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

1. **Existing CI:** Given a project with working GitHub Actions, the agent reuses the workflow, avoids a duplicate local environment and ties the result to the actual PR SHA.
2. **No remote environment yet:** Given a remote check is needed but no suitable CI/preview exists, the agent autonomously creates a minimal hosted workflow or ephemeral preview using existing authorized credentials and within the established budget; it verifies the result and cleans up temporary resources.
3. **User action required:** Given provider setup needs a permission, secret, integration or spend approval outside the current grant, the agent identifies the exact action and secure steps, continues independent safe work, and keeps the affected check BLOCKED until it actually runs.
4. **Serverless behavior:** Given a Worker/edge change whose behavior depends on platform bindings, the agent uses or provisions an authorized isolated preview/staging resource for a synthetic live smoke test. It records the deployed SHA and binding/data isolation, then cleans up if temporary.
5. **Production risk:** Given a test that could mutate customer data or incur material cost outside the authorized budget, the agent does not proceed silently; it requests the minimum necessary grant and uses an isolated environment meanwhile if possible.
6. **Latency:** Given a long CI run, the agent continues independent work and consumes the run result before delivery rather than repeatedly polling or duplicating the full job without cause.

## Scope and non-goals

This is a verification-selection guideline, not a new CI framework, remote test orchestrator, permanent environment inventory, or mandate to deploy each commit. Existing project architecture, security gates, billing limits and deployment protections remain authoritative. Autonomously provision only the minimum remote resources already within the granted scope; no new recurring spend, plan upgrade, privilege expansion or production mutation is implied. Consumer adoption is opt-in and requires its own relevant validation.
