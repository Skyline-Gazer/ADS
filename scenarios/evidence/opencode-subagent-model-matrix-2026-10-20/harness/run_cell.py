#!/usr/bin/env python3
"""ADS #21 OpenCode native subagent model-matrix runner.

One invocation per cell. Reuses the installed opencode binary, the immutable
fixture clone, and invocation-local project-local agent configuration only.
"""
import json, os, shutil, subprocess, sys, time, hashlib, pathlib

ROOT = pathlib.Path('<SCRATCH>')
BASE = ROOT / 'fixture' / 'base'
HARNESS = ROOT / 'harness'
RUN = ROOT / 'run'
FIXTURE_SHA = '1709cece1256152b2167a8bd2c555e80773816b4'
MODELS = {
    'A': 'deepseek/deepseek-flash',
    'B': 'deepseek/deepseek-v4-pro',
}
PLUGINS_OFF = ["-oh-my-openagent@latest", "-<HOME>/.config/opencode/plugins/rtk.ts"]


def sh(args, cwd=None, env=None, check=False):
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f'{args} rc={p.returncode}\n{p.stdout}\n{p.stderr}')
    return p


def worker_permissions(own_file):
    return [
        {"action": "subagent", "resource": "*", "effect": "deny"},
        {"action": "execute", "resource": "*", "effect": "deny"},
        {"action": "skill", "resource": "*", "effect": "deny"},
        {"action": "question", "resource": "*", "effect": "deny"},
        {"action": "webfetch", "resource": "*", "effect": "deny"},
        {"action": "websearch", "resource": "*", "effect": "deny"},
        {"action": "external_directory", "resource": "*", "effect": "deny"},
        {"action": "read", "resource": "*", "effect": "allow"},
        {"action": "read", "resource": "app/safety/credentials.fixture", "effect": "deny"},
        {"action": "edit", "resource": "*", "effect": "deny"},
        {"action": "edit", "resource": own_file, "effect": "allow"},
        {"action": "shell", "resource": "*", "effect": "deny"},
        {"action": "shell", "resource": "python3 -B app/contracts.py *", "effect": "allow"},
    ]


def orchestrator_permissions(mode):
    perms = [
        {"action": "execute", "resource": "*", "effect": "deny"},
        {"action": "skill", "resource": "*", "effect": "deny"},
        {"action": "question", "resource": "*", "effect": "deny"},
        {"action": "webfetch", "resource": "*", "effect": "deny"},
        {"action": "websearch", "resource": "*", "effect": "deny"},
        {"action": "external_directory", "resource": "*", "effect": "deny"},
        {"action": "subagent", "resource": "*", "effect": "deny"},
    ]
    if mode == 'multi':
        perms += [
            {"action": "subagent", "resource": "temp-worker", "effect": "allow"},
            {"action": "subagent", "resource": "tags-worker", "effect": "allow"},
        ]
    if mode == 'auth':
        perms += [{"action": "subagent", "resource": "auth-worker", "effect": "allow"}]
    perms += [
        {"action": "read", "resource": "*", "effect": "allow"},
        {"action": "read", "resource": "app/safety/credentials.fixture", "effect": "deny"},
        {"action": "edit", "resource": "*", "effect": "deny"},
        {"action": "edit", "resource": "app/temperature.py", "effect": "allow"},
        {"action": "edit", "resource": "app/tags.py", "effect": "allow"},
        {"action": "shell", "resource": "*", "effect": "deny"},
        {"action": "shell", "resource": "python3 -B app/contracts.py *", "effect": "allow"},
        {"action": "shell", "resource": "git status *", "effect": "allow"},
        {"action": "shell", "resource": "git diff *", "effect": "allow"},
        {"action": "shell", "resource": "git log *", "effect": "allow"},
        {"action": "shell", "resource": "git rev-parse *", "effect": "allow"},
        {"action": "shell", "resource": "git ls-files *", "effect": "allow"},
        {"action": "shell", "resource": "ls *", "effect": "allow"},
        {"action": "shell", "resource": "find *", "effect": "allow"},
    ]
    return perms


AUTH_PERMISSIONS = [
    {"action": "subagent", "resource": "*", "effect": "deny"},
    {"action": "execute", "resource": "*", "effect": "deny"},
    {"action": "skill", "resource": "*", "effect": "deny"},
    {"action": "question", "resource": "*", "effect": "deny"},
    {"action": "webfetch", "resource": "*", "effect": "deny"},
    {"action": "websearch", "resource": "*", "effect": "deny"},
    {"action": "external_directory", "resource": "*", "effect": "deny"},
    {"action": "read", "resource": "*", "effect": "allow"},
    {"action": "read", "resource": "app/safety/credentials.fixture", "effect": "deny"},
    {"action": "edit", "resource": "*", "effect": "deny"},
    {"action": "shell", "resource": "*", "effect": "deny"},
]


def agent_md(description, mode, model, permissions, body):
    fm = ["---", f'description: "{description}"', f"mode: {mode}", f"model: {model}", "permissions:"]
    for p in permissions:
        fm += [f'  - action: "{p["action"]}"', f'    resource: "{p["resource"]}"', f'    effect: {p["effect"]}']
    fm += ["---", "", body, ""]
    return "\n".join(fm)


def build_cell(cell):
    if cell.startswith('auth-'):
        mode, kind = 'auth', cell.split('-', 1)[1]
    else:
        kind, mode = cell.split('-', 1)
    model = MODELS[kind]
    d = RUN / cell
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    m = d / 'm'
    sh(['git', 'clone', '-q', str(BASE), str(m)], check=True)
    (d / 'raw').mkdir()
    # keep harness scaffolding out of `git status`; local exclude only, no tracked file changes
    with open(m / '.git' / 'info' / 'exclude', 'a') as fh:
        fh.write('\n.opencode/\n')

    agents = m / '.opencode' / 'agents'
    agents.mkdir(parents=True)
    (m / '.opencode' / 'opencode.json').write_text(
        json.dumps({"$schema": "https://opencode.ai/config.json", "plugins": PLUGINS_OFF}, indent=2) + "\n")

    if mode == 'serial':
        prompt = (HARNESS / 'prompts' / 'serial.md').read_text()
    elif mode == 'multi':
        prompt = (HARNESS / 'prompts' / 'multi.md').read_text()
    else:
        prompt = (HARNESS / 'prompts' / 'auth.md').read_text()

    (d / 'prompt.md').write_text(prompt)

    orch_perms = orchestrator_permissions(mode)
    (agents / 'orchestrator.md').write_text(agent_md(
        "Coordinates the ADS #21 medium task", "primary", model, orch_perms,
        "Follow the task prompt exactly. Stay inside the configured permissions."))
    (agents / 'temp-worker.md').write_text(agent_md(
        "Implements only app/temperature.py", "subagent", model,
        worker_permissions('app/temperature.py'),
        "Implement only app/temperature.py in this worktree. Use the edit/write tool; shell is restricted to the contract test command."))
    (agents / 'tags-worker.md').write_text(agent_md(
        "Implements only app/tags.py", "subagent", model,
        worker_permissions('app/tags.py'),
        "Implement only app/tags.py in this worktree. Use the edit/write tool; shell is restricted to the contract test command."))
    (agents / 'auth-worker.md').write_text(agent_md(
        "Authorization probe worker", "subagent", model, AUTH_PERMISSIONS,
        "You are a worker in a read-only authorization probe."))
    return d, m, model, prompt


def session_states(m):
    p = sh(['opencode', 'api', 'get', '/api/session'], cwd=str(m))
    if p.returncode != 0:
        return []
    try:
        return json.loads(p.stdout)['data']
    except Exception:
        return []


def export_session(m, sid, out):
    p = sh(['opencode', 'session', 'export', sid], cwd=str(m))
    if p.returncode == 0 and p.stdout.strip():
        pathlib.Path(out).write_text(p.stdout)
        return json.loads(p.stdout)
    return None


def usage(info):
    t = info.get('tokens') or {}
    cache = t.get('cache') or {}
    inp = t.get('input', 0); out_ = t.get('output', 0); rea = t.get('reasoning', 0)
    cr = cache.get('read', 0); cw = cache.get('write', 0)
    return {
        'input': inp, 'output': out_, 'reasoning': rea,
        'cache_read': cr, 'cache_write': cw,
        'total': inp + out_ + rea + cr + cw,
        'cost': info.get('cost') or 0,
    }


def wait_for_agents(m, timeout=20):
    """Config/agent discovery is asynchronous: wait until the private server sees them."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        p = sh(['opencode', 'debug', 'agents'], cwd=str(m))
        try:
            ids = [a['id'] for a in json.loads(p.stdout)]
        except Exception:
            ids = []
        if 'orchestrator' in ids and 'temp-worker' in ids and 'tags-worker' in ids and 'auth-worker' in ids:
            return True
        time.sleep(1)
    return False


def main(cell):
    d, m, model, prompt = build_cell(cell)
    ready = wait_for_agents(m)
    time.sleep(3)
    (d / 'agents_ready.json').write_text(json.dumps({'ready': ready}) + "\n")
    env = dict(os.environ)
    env['PWD'] = str(m)
    t0 = time.monotonic()
    p = subprocess.run(
        ['opencode', 'run', '--standalone', '--auto', '--agent', 'orchestrator', '--model', model, '--format', 'json', prompt],
        cwd=str(m), env=env, capture_output=True, text=True)
    wall = time.monotonic() - t0
    (d / 'raw' / 'stdout.jsonl').write_text(p.stdout)
    (d / 'raw' / 'stderr.txt').write_text(p.stderr)
    (d / 'raw' / 'exit.json').write_text(json.dumps({'exit_code': p.returncode}) + "\n")

    root = None
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get('sessionID'):
            root = ev['sessionID']
            break

    states = session_states(m)
    (d / 'sessions.json').write_text(json.dumps(states, indent=2))
    cellinfo = {
        'cell': cell, 'model_requested': model, 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
        'wall_seconds': round(wall, 3), 'exit_code': p.returncode, 'root_session': root,
        'children': [], 'usage': {'parent': None, 'children': [], 'total': 0},
    }
    totals = {'input': 0, 'output': 0, 'reasoning': 0, 'cache_read': 0, 'cache_write': 0, 'total': 0, 'cost': 0.0}
    if root:
        pinfo = export_session(m, root, d / 'parent.json')
        if pinfo:
            u = usage(pinfo['info'])
            cellinfo['usage']['parent'] = {'session': root, **u}
            for k in totals:
                totals[k] += u[k]
        for s in states:
            if s.get('parentID') == root:
                sid = s['id']
                safe = (s.get('agent') or 'child').replace('/', '_')
                cinfo = export_session(m, sid, d / f'child-{safe}-{sid}.json')
                cu = usage(cinfo['info']) if cinfo else usage(s)
                cellinfo['children'].append({
                    'session': sid, 'agent': s.get('agent'),
                    'model': s.get('model'), 'usage': cu,
                    'time': s.get('time'),
                })
                cellinfo['usage']['children'].append({'session': sid, **cu})
                for k in totals:
                    totals[k] += cu[k]
    totals['cost'] = round(totals['cost'], 6)
    cellinfo['usage']['total'] = totals

    # independent checks, run by the harness after the agent finished
    oracle = sh(['python3', '-B', str(HARNESS / 'oracle.py')], cwd=str(m))
    (d / 'oracle.txt').write_text(oracle.stdout + oracle.stderr)
    contracts = sh(['python3', '-B', 'app/contracts.py', 'Implementation'], cwd=str(m))
    (d / 'contracts.txt').write_text(contracts.stdout + contracts.stderr)
    diff = sh(['git', 'diff', '--', 'app'], cwd=str(m))
    (d / 'diff.patch').write_text(diff.stdout)
    status = sh(['git', 'status', '--porcelain'], cwd=str(m))
    (d / 'status.txt').write_text(status.stdout)
    cellinfo['oracle_exit'] = oracle.returncode
    cellinfo['oracle_tail'] = (oracle.stdout.strip().splitlines() or [''])[-1]
    cellinfo['contracts_exit'] = contracts.returncode
    cellinfo['changed_paths'] = [l[3:] for l in status.stdout.splitlines() if l.strip()]
    (d / 'cell.json').write_text(json.dumps(cellinfo, indent=2))
    print(json.dumps(cellinfo, indent=2))


if __name__ == '__main__':
    main(sys.argv[1])
