import { execFile, spawn } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { promisify } from "node:util";
import { pathToFileURL } from "node:url";

const execFileAsync = promisify(execFile);
const profileName = process.env.QUANTBRIEF_OPENCLAW_PROFILE || "quantbrief";
const homeDir = process.env.USERPROFILE || process.env.HOME;

if (!homeDir) {
  throw new Error("Could not resolve the user home directory for OpenClaw state.");
}

const stateDir =
  process.env.OPENCLAW_STATE_DIR || path.join(homeDir, `.openclaw-${profileName}`);
const configPath =
  process.env.OPENCLAW_CONFIG_PATH || path.join(stateDir, "openclaw.json");
const appData = process.env.APPDATA;

if (!appData) {
  throw new Error("APPDATA is required to locate the OpenClaw installation.");
}

const openclawCmd =
  process.platform === "win32"
    ? path.join(appData, "npm", "openclaw.cmd")
    : "openclaw";

process.env.OPENCLAW_STATE_DIR = stateDir;
process.env.OPENCLAW_CONFIG_PATH = configPath;
process.env.OPENCLAW_PROFILE = process.env.OPENCLAW_PROFILE || profileName;

const distDir = path.join(appData, "npm", "node_modules", "openclaw", "dist");
const distEntries = await fs.readdir(distDir);
const loginQrEntry = distEntries.find((entry) => /^login-qr-.*\.js$/i.test(entry));

if (!loginQrEntry) {
  throw new Error("Could not find the OpenClaw WhatsApp login module.");
}

const { startWebLoginWithQr, waitForWebLogin } = await import(
  pathToFileURL(path.join(distDir, loginQrEntry)).href
);

const projectDir = process.cwd();
const qrPath = path.join(projectDir, "quantbrief-whatsapp-qr.png");
const statusPath = path.join(projectDir, "quantbrief-whatsapp-login-status.json");
const maxSessionMs = 15 * 60 * 1000;
const maxQrAttempts = 5;

async function writeStatus(stage, message, extra = {}) {
  const payload = {
    stage,
    message,
    profile: profileName,
    stateDir,
    configPath,
    qrPath,
    updatedAt: new Date().toISOString(),
    ...extra,
  };
  await fs.writeFile(statusPath, JSON.stringify(payload, null, 2), "utf8");
  return payload;
}

function decodeQrPng(dataUrl) {
  const prefix = "data:image/png;base64,";
  if (!dataUrl.startsWith(prefix)) {
    throw new Error("Unexpected QR payload format from OpenClaw.");
  }
  return Buffer.from(dataUrl.slice(prefix.length), "base64");
}

async function stopQuantbriefGateway() {
  if (process.platform !== "win32") return;
  const script = `
Get-CimInstance Win32_Process |
Where-Object { $_.CommandLine -like '*--profile ${profileName} gateway*' } |
ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
`;
  try {
    await execFileAsync("powershell.exe", ["-NoProfile", "-Command", script], {
      timeout: 15000,
      windowsHide: true,
    });
  } catch {
    // Best effort only. We do not want a stop failure to block relinking.
  }
}

function startQuantbriefGateway() {
  try {
    const child = spawn(openclawCmd, ["--profile", profileName, "gateway"], {
      detached: true,
      stdio: "ignore",
      windowsHide: true,
    });
    child.unref();
  } catch {
    // Non-fatal: the user can still start the gateway manually.
  }
}

function isRetryableLoginMessage(message) {
  const lower = message.toLowerCase();
  return (
    lower.includes("408") ||
    lower.includes("timed out") ||
    lower.includes("restart required") ||
    lower.includes("expired") ||
    lower.includes("qr refs attempts ended")
  );
}

function isFatalLoginMessage(message) {
  const lower = message.toLowerCase();
  return (
    lower.includes("logged out") ||
    lower.includes("unauthorized") ||
    lower.includes("connection failure") ||
    lower.includes("no active whatsapp login")
  );
}

await writeStatus(
  "preparing",
  "Pausing the QuantBrief gateway so WhatsApp relinking can happen without session races.",
  { linked: false, qrReady: false }
);
await stopQuantbriefGateway();

const deadline = Date.now() + maxSessionMs;
let lastMessage = "WhatsApp login did not start.";

for (let attempt = 1; attempt <= maxQrAttempts && Date.now() < deadline; attempt += 1) {
  await writeStatus(
    "starting",
    attempt === 1
      ? "Booting the QuantBrief WhatsApp login flow."
      : `Refreshing the WhatsApp QR automatically (attempt ${attempt}/${maxQrAttempts}).`,
    { attempt, maxAttempts: maxQrAttempts, linked: false, qrReady: false }
  );

  const loginStart = await startWebLoginWithQr({
    accountId: "default",
    timeoutMs: 60_000,
    force: true,
    verbose: true,
  });

  lastMessage = loginStart.message || "Failed to start WhatsApp login.";
  if (!loginStart.qrDataUrl) {
    await writeStatus("error", lastMessage, {
      attempt,
      maxAttempts: maxQrAttempts,
      linked: false,
      qrReady: false,
    });
    console.error(lastMessage);
    if (attempt >= maxQrAttempts) {
      startQuantbriefGateway();
      process.exit(1);
    }
    continue;
  }

  await fs.writeFile(qrPath, decodeQrPng(loginStart.qrDataUrl));
  await writeStatus("qr_ready", loginStart.message || "Scan the QR in WhatsApp -> Linked Devices.", {
    attempt,
    maxAttempts: maxQrAttempts,
    linked: false,
    qrReady: true,
  });
  console.log(`QR ready: ${qrPath}`);
  console.log(`Scan it in WhatsApp -> Linked Devices. Attempt ${attempt}/${maxQrAttempts}.`);

  let refreshQr = false;
  while (Date.now() < deadline) {
    const remainingMs = deadline - Date.now();
    const waitResult = await waitForWebLogin({
      accountId: "default",
      timeoutMs: Math.min(30_000, remainingMs),
    });

    lastMessage = waitResult.message || "Still waiting for the QR scan.";
    if (waitResult.connected) {
      await writeStatus("linked", waitResult.message || "WhatsApp linked successfully.", {
        attempt,
        maxAttempts: maxQrAttempts,
        linked: true,
        qrReady: false,
      });
      console.log(waitResult.message || "Linked.");
      startQuantbriefGateway();
      process.exit(0);
    }

    if (isRetryableLoginMessage(lastMessage)) {
      refreshQr = true;
      await writeStatus(
        "refreshing",
        `WhatsApp asked for a fresh QR. Regenerating automatically. Last message: ${lastMessage}`,
        {
          attempt,
          maxAttempts: maxQrAttempts,
          linked: false,
          qrReady: false,
        }
      );
      console.warn(lastMessage);
      break;
    }

    if (isFatalLoginMessage(lastMessage)) {
      await writeStatus("error", lastMessage, {
        attempt,
        maxAttempts: maxQrAttempts,
        linked: false,
        qrReady: false,
      });
      console.error(lastMessage);
      startQuantbriefGateway();
      process.exit(1);
    }

    await writeStatus("waiting", lastMessage, {
      attempt,
      maxAttempts: maxQrAttempts,
      linked: false,
      qrReady: true,
    });
    console.log(lastMessage);
  }

  if (!refreshQr) {
    break;
  }
}

const timeoutState = await writeStatus(
  "timeout",
  `WhatsApp did not link after ${maxQrAttempts} QR attempts. Last message: ${lastMessage}`,
  {
    linked: false,
    qrReady: false,
    maxAttempts: maxQrAttempts,
  }
);
console.error(timeoutState.message);
startQuantbriefGateway();
process.exit(2);
