import { execFile, spawnSync } from "node:child_process";
import { readFileSync, existsSync, appendFileSync } from "node:fs";
import { createRequire } from "node:module";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

let openclawCliPath = null;
if (typeof process.argv[1] === "string" && process.argv[1].endsWith("openclaw.mjs") && existsSync(process.argv[1])) {
  openclawCliPath = process.argv[1];
} else {
  try {
    const require = createRequire(import.meta.url);
    const pkgPath = require.resolve("openclaw/package.json");
    openclawCliPath = join(dirname(pkgPath), "openclaw.mjs");
    if (!existsSync(openclawCliPath)) openclawCliPath = null;
  } catch {
    openclawCliPath = null;
  }
}
const openclawBinPath = join(dirname(process.execPath), "openclaw");
const OPENCLAW_BIN_CANDIDATES = [
  openclawBinPath,
  "/usr/bin/openclaw",
  "/usr/local/bin/openclaw",
  join(homedir(), ".nvm", "versions", "node", "v22.22.0", "bin", "openclaw"),
];

const STATE_DIR = process.env.OPENCLAW_STATE_DIR || join(homedir(), ".openclaw");
const NODE_DIR = join(STATE_DIR, "examples", "nodes", "testnode");
const PID_FILE = join(NODE_DIR, ".testnode.pid");
const IDENTITY_FILE = join(NODE_DIR, "identity.json");
const DEBUG_LOG_FILE = join(NODE_DIR, "testnode-plugin-debug.log");

function logDebug(event, fields = {}) {
  try {
    const line = JSON.stringify({
      ts: new Date().toISOString(),
      event,
      ...fields,
    });
    appendFileSync(DEBUG_LOG_FILE, `${line}\n`, "utf-8");
  } catch {
    // Best-effort logging only; never break command flow.
  }
}

function runBash(script) {
  const startedAt = Date.now();
  return execFileAsync("bash", ["-c", script], {
    maxBuffer: 4096,
    timeout: 15000,
  })
    .then(({ stdout, stderr }) => {
      const output = (stdout + (stderr ? stderr : "")).trim();
      logDebug("runBash.ok", {
        durationMs: Date.now() - startedAt,
        output: output.slice(0, 500),
      });
      return output;
    })
    .catch((error) => {
      logDebug("runBash.error", {
        durationMs: Date.now() - startedAt,
        code: String(error?.code ?? ""),
        message: String(error?.message ?? ""),
      });
      throw error;
    });
}

function getNodeId() {
  if (!existsSync(IDENTITY_FILE)) return null;
  try {
    const raw = readFileSync(IDENTITY_FILE, "utf-8");
    const data = JSON.parse(raw);
    const nodeId = typeof data.deviceId === "string" ? data.deviceId : null;
    logDebug("getNodeId", { nodeId });
    return nodeId;
  } catch {
    logDebug("getNodeId.error");
    return null;
  }
}

async function ensureNodeRunning() {
  const script = `
NODE_DIR=${JSON.stringify(NODE_DIR)}
PID_FILE=${JSON.stringify(PID_FILE)}
if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  CMD="$(ps -p "$(cat "$PID_FILE")" -o cmd= 2>/dev/null || true)"
  if [[ "$CMD" == *"testnode.py"* ]]; then
    echo "already-running"
  else
    rm -f "$PID_FILE"
    nohup "$NODE_DIR/.venv/bin/python" -u "$NODE_DIR/testnode.py" > "$NODE_DIR/testnode.log" 2>&1 &
    echo $! > "$PID_FILE"
    echo "started:$(cat "$PID_FILE")"
    sleep 3
  fi
else
  rm -f "$PID_FILE"
  nohup "$NODE_DIR/.venv/bin/python" -u "$NODE_DIR/testnode.py" > "$NODE_DIR/testnode.log" 2>&1 &
  echo $! > "$PID_FILE"
  echo "started:$(cat "$PID_FILE")"
  sleep 3
fi
`;
  return runBash(script);
}

async function restartNode() {
  const script = `
NODE_DIR=${JSON.stringify(NODE_DIR)}
PID_FILE=${JSON.stringify(PID_FILE)}
if [[ -f "$PID_FILE" ]]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID" || true
    sleep 1
    kill -9 "$PID" 2>/dev/null || true
  fi
  rm -f "$PID_FILE"
fi
nohup "$NODE_DIR/.venv/bin/python" -u "$NODE_DIR/testnode.py" > "$NODE_DIR/testnode.log" 2>&1 &
echo $! > "$PID_FILE"
echo "restarted:$(cat "$PID_FILE")"
sleep 3
`;
  return runBash(script);
}

function isTransientNodeInvokeError(errorText) {
  return /not connected|connection|timeout|timed out|timedout|etimedout|econnrefused|ehostunreach|enetunreach|gateway closed|abnormal closure|unavailable|UNAVAILABLE/i.test(
    errorText || "",
  );
}

function isGatewayRestartLikeError(errorText) {
  return /gateway closed|abnormal closure|no close frame|ETIMEDOUT|ECONNREFUSED|EHOSTUNREACH|ENETUNREACH/i.test(
    errorText || "",
  );
}

async function runOpenclawInvoke(nodeId, paramsJson) {
  const args = [
    "nodes",
    "invoke",
    "--node",
    nodeId,
    "--command",
    "testnode.echo",
    "--params",
    paramsJson,
  ];
  const opts = { encoding: "utf-8", timeout: 20000, env: process.env, cwd: homedir(), killSignal: "SIGTERM" };
  const startedAt = Date.now();
  let result = null;
  let launch = "";
  const runExec = async (file, fileArgs) => {
    try {
      const { stdout = "", stderr = "" } = await execFileAsync(file, fileArgs, opts);
      return { status: 0, signal: null, stdout, stderr, error: null };
    } catch (error) {
      return {
        status: typeof error?.code === "number" ? error.code : null,
        signal: error?.signal ?? null,
        stdout: String(error?.stdout ?? ""),
        stderr: String(error?.stderr ?? ""),
        error:
          typeof error?.code === "string" || error?.message
            ? { code: String(error?.code ?? ""), message: String(error?.message ?? "") }
            : null,
      };
    }
  };

  if (openclawCliPath) {
    launch = `node ${openclawCliPath}`;
    result = await runExec(process.execPath, [openclawCliPath, ...args]);
  } else {
    // Prefer deterministic absolute binaries over PATH resolution.
    for (const bin of OPENCLAW_BIN_CANDIDATES) {
      if (!existsSync(bin)) continue;
      launch = bin;
      result = await runExec(bin, args);
      if (!(result.error?.code === "ENOENT" || result.status === 127)) break;
    }
    // Last resort: resolve via login shell and invoke absolute path if found.
    if (!result || result.error?.code === "ENOENT" || result.status === 127) {
      const which = spawnSync("bash", ["-lc", "command -v openclaw || true"], {
        encoding: "utf-8",
        timeout: 5000,
        env: process.env,
        cwd: homedir(),
      });
      const resolved = String(which.stdout || "").trim().split("\n").at(-1)?.trim() || "";
      if (resolved && existsSync(resolved)) {
        launch = resolved;
        result = await runExec(resolved, args);
      } else {
        launch = "openclaw";
        result = await runExec("openclaw", args);
      }
    }
  }
  logDebug("runOpenclawInvoke.done", {
    launch,
    nodeId,
    durationMs: Date.now() - startedAt,
    status: result.status ?? null,
    signal: result.signal ?? null,
    errorCode: String(result.error?.code ?? ""),
    errorMessage: String(result.error?.message ?? ""),
    stdout: String(result.stdout ?? "").trim().slice(0, 500),
    stderr: String(result.stderr ?? "").trim().slice(0, 500),
  });
  return result;
}

async function invokeEcho(nodeId, messageText) {
  logDebug("invokeEcho.start", { nodeId, text: messageText.slice(0, 200) });
  const paramsJson = JSON.stringify({ text: messageText });
  const result = await runOpenclawInvoke(nodeId, paramsJson);
  const stdout = (result.stdout || "").trim();
  const stderr = (result.stderr || "").trim();
  const combined = stdout || stderr;
  // Spawn timeout or missing CLI: surface so handler can retry or user can fix
  if (result.error) {
    const why =
      result.error.code === "ENOENT"
        ? "openclaw CLI not found (PATH/absolute lookup failed)."
        : String(result.error.code ?? result.error.message);
    const out = { ok: false, error: why };
    logDebug("invokeEcho.result", out);
    return out;
  }
  if (result.status !== 0 && !combined) {
    const out = { ok: false, error: "openclaw CLI failed (no output)." };
    logDebug("invokeEcho.result", out);
    return out;
  }
  if (result.status !== 0 && combined) {
    const errMsg = stderr ? `${stdout ? stdout + "\n" : ""}${stderr}` : combined;
    try {
      const parsed = JSON.parse(combined);
      const err = parsed.error || parsed.message || errMsg;
      const out = { ok: false, error: typeof err === "string" ? err : JSON.stringify(err) };
      logDebug("invokeEcho.result", out);
      return out;
    } catch {
      const out = { ok: false, error: errMsg.slice(0, 500) };
      logDebug("invokeEcho.result", out);
      return out;
    }
  }
  try {
    const parsed = JSON.parse(combined);
    if (parsed.ok && (parsed.payload != null || parsed.payloadJSON != null)) {
      const payload =
        parsed.payload != null
          ? parsed.payload
          : (() => {
              try {
                return JSON.parse(parsed.payloadJSON);
              } catch {
                return null;
              }
            })();
      const msg = payload?.message ?? payload?.payloadJSON;
      const out = { ok: true, message: typeof msg === "string" ? msg : JSON.stringify(payload ?? parsed) };
      logDebug("invokeEcho.result", { ok: true, message: String(out.message).slice(0, 300) });
      return out;
    }
    const err = parsed.error || parsed.message || combined;
    const out = { ok: false, error: typeof err === "string" ? err : JSON.stringify(err) };
    logDebug("invokeEcho.result", out);
    return out;
  } catch {
    const out = { ok: false, error: combined || "Invalid response from node invoke." };
    logDebug("invokeEcho.result", out);
    return out;
  }
}

export default function (api) {
  api.registerCommand({
    name: "testnode",
    description: "Start/stop the Testnode or send it a message (testnode.echo).",
    acceptsArgs: true,
    handler: async (ctx) => {
      const raw = (ctx.args ?? "").trim();
      const lower = raw.toLowerCase();
      logDebug("handler.start", { raw: raw.slice(0, 200), channel: String(ctx?.channel ?? "unknown") });
      let action;
      if (raw === "" || lower === "on" || lower === "start") action = "start";
      else if (lower === "off" || lower === "stop") action = "stop";
      else if (lower === "restart") action = "restart";
      else action = "echo";

      if (action === "start") {
        const script = `
NODE_DIR=${JSON.stringify(NODE_DIR)}
PID_FILE=${JSON.stringify(PID_FILE)}
if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Testnode is already running (PID: $(cat "$PID_FILE"))."
else
  nohup "$NODE_DIR/.venv/bin/python" -u "$NODE_DIR/testnode.py" > "$NODE_DIR/testnode.log" 2>&1 &
  echo $! > "$PID_FILE"
  echo "Testnode started (PID: $(cat "$PID_FILE"))."
fi
`;
        const out = await runBash(script);
        logDebug("handler.start.done", { out: out.slice(0, 300) });
        return { text: `Checking if testnode is running…\n\n${out}` };
      }

      if (action === "stop") {
        const script = `
NODE_DIR=${JSON.stringify(NODE_DIR)}
PID_FILE=${JSON.stringify(PID_FILE)}
if [[ ! -f "$PID_FILE" ]]; then
  echo "Testnode is not running (no PID file found)."
else
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "Testnode stopped (PID: $PID)."
  else
    echo "Testnode was not running (stale PID: $PID)."
  fi
  rm -f "$PID_FILE"
fi
`;
        const out = await runBash(script);
        logDebug("handler.stop.done", { out: out.slice(0, 300) });
        return { text: `Stopping testnode…\n\n${out}` };
      }

      if (action === "restart") {
        const script = `
NODE_DIR=${JSON.stringify(NODE_DIR)}
PID_FILE=${JSON.stringify(PID_FILE)}
if [[ -f "$PID_FILE" ]]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "Testnode stopped (PID: $PID)."
  fi
  rm -f "$PID_FILE"
fi
nohup "$NODE_DIR/.venv/bin/python" -u "$NODE_DIR/testnode.py" > "$NODE_DIR/testnode.log" 2>&1 &
echo $! > "$PID_FILE"
echo "Testnode restarted (PID: $(cat "$PID_FILE"))."
`;
        const out = await runBash(script);
        logDebug("handler.restart.done", { out: out.slice(0, 300) });
        return { text: `Restarting testnode…\n\n${out}` };
      }

      // echo: ensure node running, then invoke testnode.echo
      const nodeId = getNodeId();
      if (!nodeId) {
        logDebug("handler.echo.noNodeId");
        return {
          text: "Testnode has not been started yet. Run /testnode on first, then try again.",
        };
      }
      const ensureOut = await ensureNodeRunning();
      logDebug("handler.echo.ensureNodeRunning", { out: ensureOut.slice(0, 300) });
      let result = await invokeEcho(nodeId, raw);
      if (!result.ok && isTransientNodeInvokeError(result.error)) {
        if (isGatewayRestartLikeError(result.error)) {
          // During /restart windows, gateway handover can exceed one invoke timeout.
          logDebug("handler.echo.gatewayRecoveryWait", { error: result.error });
          await new Promise((r) => setTimeout(r, 8000));
          result = await invokeEcho(nodeId, raw);
        }
        if (!result.ok && isTransientNodeInvokeError(result.error)) {
          // A stale but running process can still fail invoke; hard restart once, then retry.
          const restartOut = await restartNode();
          logDebug("handler.echo.restartAfterTransient", { out: restartOut.slice(0, 300), error: result.error });
          await new Promise((r) => setTimeout(r, 2000));
          result = await invokeEcho(nodeId, raw);
        }
      }
      if (result.ok) {
        return {
          text: `Ensuring testnode is running and sending your message…\n\n${result.message ?? "Done."}`,
        };
      }
      return {
        text: `Ensuring testnode is running and sending your message…\n\nTestnode echo failed: ${result.error ?? "unknown error"}. Ensure testnode.echo is in gateway.nodes.allowCommands and the gateway is running.`,
      };
    },
  });
}
