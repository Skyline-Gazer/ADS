import fs from "node:fs";
import path from "node:path";

const AUDIT = process.env.OMP_CONTAIN_AUDIT || "";
const SHELL_BLOCK_AGENTS = (process.env.OMP_CONTAIN_SHELL_BLOCK_AGENTS || "")
  .split(",")
  .map((s) => s.trim().toLowerCase())
  .filter(Boolean);

// Least privilege for every subagent in this experiment. MCP/extension/custom
// tools are additive to explicit agent tool lists, so an allowlist is the only
// way to keep the tested boundary closed.
const ALLOWED_SUB_TOOLS = null; // no allowlist: reproduces the path-only hook

function audit(entry) {
  if (!AUDIT) return;
  try {
    fs.mkdirSync(path.dirname(AUDIT), { recursive: true });
    fs.appendFileSync(AUDIT, JSON.stringify({ ts: Date.now(), pid: process.pid, ...entry }) + "\n");
  } catch {
    // Audit logging must never become the enforcement path.
  }
}

function expandHome(p) {
  if (p === "~") return process.env.HOME || p;
  if (p.startsWith("~/")) return path.join(process.env.HOME || "", p.slice(2));
  return p;
}

// Resolve every existing symlink component, including a dangling final symlink
// whose target does not exist yet. realpath() alone leaves that final target
// unresolved.
function resolveExisting(abs, depth) {
  if (depth > 40) return { error: "symlink depth exceeded" };
  let st;
  try {
    st = fs.lstatSync(abs);
  } catch (err) {
    if (err.code !== "ENOENT" && err.code !== "ENOTDIR") return { error: String(err) };
  }
  if (st?.isSymbolicLink()) {
    let link;
    try {
      link = fs.readlinkSync(abs);
    } catch (err) {
      return { error: String(err) };
    }
    return resolveExisting(path.resolve(path.dirname(abs), link), depth + 1);
  }
  if (st) {
    try {
      return fs.realpathSync.native(abs);
    } catch (err) {
      return { error: String(err) };
    }
  }
  const parent = path.dirname(abs);
  if (parent === abs) return abs;
  const resolvedParent = resolveExisting(parent, depth + 1);
  if (typeof resolvedParent !== "string") return resolvedParent;
  return path.join(resolvedParent, path.basename(abs));
}

function canonical(target, cwd) {
  let s = expandHome(String(target).trim());
  if (!s) return null;
  if (s.startsWith("file://")) s = s.slice("file://".length);
  return resolveExisting(path.resolve(cwd, s), 0);
}

function inside(candidate, root) {
  return candidate === root || candidate.startsWith(root + path.sep);
}

function isUrl(s) {
  return /^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(s);
}

function extractTargets(toolName, input) {
  if (!input || typeof input !== "object") return [];
  const out = [];
  const add = (v) => {
    if (typeof v === "string" && v.trim()) out.push(v.trim());
  };
  if (toolName === "read" || toolName === "write" || toolName === "grep" || toolName === "glob") {
    add(input.path);
    if (toolName === "grep" && typeof input.path === "string") {
      for (const part of input.path.split(";")) add(part);
    }
  }
  return out;
}

export default function containment(pi) {
  pi.on("session_start", async (_event, ctx) => {
    audit({ event: "session_start", agent: ctx.agent, cwd: ctx.cwd });
  });

  pi.on("tool_call", async (event, ctx) => {
    if (ctx.agent?.kind !== "sub") return;

    const toolName = String(event.toolName || "");
    const agentName = String(ctx.agent?.name || "").toLowerCase();

    if (ALLOWED_SUB_TOOLS && !ALLOWED_SUB_TOOLS.has(toolName)) {
      audit({ event: "decision", agent: ctx.agent, cwd: ctx.cwd, tool: toolName, target: null, decision: "block_tool" });
      return { block: true, reason: `containment: tool ${toolName} is not allowed for subagents` };
    }

    if ((toolName === "bash" || toolName === "eval") && SHELL_BLOCK_AGENTS.includes(agentName)) {
      audit({ event: "decision", agent: ctx.agent, cwd: ctx.cwd, tool: toolName, target: null, decision: "block_shell" });
      return { block: true, reason: `containment: ${toolName} is denied for subagent ${agentName}` };
    }

    const targets = extractTargets(toolName, event.input);
    if (targets.length === 0) return;

    const cwdReal = canonical(ctx.cwd, ctx.cwd);
    const root = typeof cwdReal === "string" ? cwdReal : path.resolve(ctx.cwd);

    for (const raw of targets) {
      if (isUrl(raw)) {
        audit({ event: "decision", agent: ctx.agent, cwd: ctx.cwd, tool: toolName, target: raw, decision: "block_url" });
        return { block: true, reason: `containment: ${toolName} refuses internal/remote URL ${raw}` };
      }
      const resolved = canonical(raw, ctx.cwd);
      if (typeof resolved !== "string") {
        audit({ event: "decision", agent: ctx.agent, cwd: ctx.cwd, tool: toolName, target: raw, decision: "block_unresolvable" });
        return { block: true, reason: `containment: cannot resolve ${raw}` };
      }
      audit({ event: "decision", agent: ctx.agent, cwd: ctx.cwd, tool: toolName, target: raw, resolved, root, decision: inside(resolved, root) ? "allow" : "block_path" });
      if (!inside(resolved, root)) {
        return { block: true, reason: `containment: ${toolName} path ${raw} resolves outside ${root}` };
      }
      if (toolName === "write") {
        const rel = path.relative(root, resolved);
        if (rel === ".git" || rel.startsWith(".git" + path.sep)) {
          return { block: true, reason: "containment: git metadata is not writable" };
        }
      }
    }
    return;
  });
}
