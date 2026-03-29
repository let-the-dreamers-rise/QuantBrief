from __future__ import annotations

import json
import shutil
import socket
from pathlib import Path
from typing import Any


WINDOWS_OPENCLAW_CMD = Path.home() / "AppData" / "Roaming" / "npm" / "openclaw.cmd"
GLOBAL_OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
PROFILE_NAME = "quantbrief"
PROFILE_OPENCLAW_CONFIG = Path.home() / f".openclaw-{PROFILE_NAME}" / "openclaw.json"
PROFILE_STATE_DIR = Path.home() / f".openclaw-{PROFILE_NAME}"
WHATSAPP_CREDS_PATH = PROFILE_STATE_DIR / "credentials" / "whatsapp" / "default" / "creds.json"
DEFAULT_GATEWAY_PORT = 18789


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _has_payload(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_has_payload(item) for item in value.values())
    if isinstance(value, list):
        return any(_has_payload(item) for item in value)
    return value not in (None, "", False)


def _port_is_open(port: int, host: str = "127.0.0.1", timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _status_label(reachable: bool, configured: bool) -> str:
    if reachable:
        return "ready"
    if configured:
        return "setup"
    return "offline"


def _file_has_payload(path: Path) -> bool:
    try:
        return path.exists() and path.stat().st_size > 0
    except Exception:
        return False


def _telegram_is_configured(channels_config: dict[str, Any]) -> bool:
    telegram = channels_config.get("telegram")
    if not isinstance(telegram, dict):
        return False
    return bool(
        telegram.get("token")
        or telegram.get("botToken")
        or telegram.get("bot_token")
    )


def get_openclaw_status(project_dir: Path) -> dict[str, Any]:
    project_dir = project_dir.resolve()
    workspace_config = _load_json(project_dir / "openclaw.json")
    profile_config = _load_json(PROFILE_OPENCLAW_CONFIG)
    global_config = profile_config or _load_json(GLOBAL_OPENCLAW_CONFIG)
    active_config_path = PROFILE_OPENCLAW_CONFIG if profile_config else GLOBAL_OPENCLAW_CONFIG

    gateway_config = global_config.get("gateway") if isinstance(global_config.get("gateway"), dict) else {}
    auth_config = gateway_config.get("auth") if isinstance(gateway_config.get("auth"), dict) else {}
    agents_defaults = (((global_config.get("agents") or {}).get("defaults")) or {})
    default_model = (((agents_defaults.get("model") or {}).get("primary")) or "Not configured")
    default_workspace = str(agents_defaults.get("workspace") or "").strip()
    workspace_mcp = (((workspace_config.get("mcpServers") or {}).get("quantbrief")) or {})
    skills = workspace_config.get("skills") or []

    port = int(gateway_config.get("port") or DEFAULT_GATEWAY_PORT)
    gateway_reachable = _port_is_open(port)
    gateway_configured = bool(gateway_config)
    installed = bool(shutil.which("openclaw") or WINDOWS_OPENCLAW_CMD.exists())

    channels_config = global_config.get("channels") if isinstance(global_config.get("channels"), dict) else {}
    login_status = _load_json(project_dir / "quantbrief-whatsapp-login-status.json")
    whatsapp_login_stage = str(login_status.get("stage") or "").strip().lower()

    whatsapp_configured = _has_payload(channels_config.get("whatsapp"))
    whatsapp_linked = _file_has_payload(WHATSAPP_CREDS_PATH)
    telegram_configured = _telegram_is_configured(channels_config)

    workspace_ready = bool(workspace_config) and bool(workspace_mcp)
    skill_ready = any(str(item).startswith("./skills") or str(item).endswith("/skills") for item in skills)
    default_workspace_matches = default_workspace.lower() == str(project_dir).lower()
    profile_prefix = f"openclaw --profile {PROFILE_NAME}" if active_config_path == PROFILE_OPENCLAW_CONFIG else "openclaw"

    ask_command = (
        f'Set-Location "{project_dir}"; '
        '$env:PYTHONIOENCODING="utf-8"; '
        f'{profile_prefix} agent --local --session-id qb --message "How does my portfolio look?"'
    )
    channel_setup_command = f"{profile_prefix} configure --section channels"
    gateway_run_command = f"{profile_prefix} gateway"
    gateway_probe_command = f"{profile_prefix} gateway probe"
    whatsapp_login_command = f'Set-Location "{project_dir}"; node scripts/openclaw_whatsapp_login.mjs'

    if gateway_reachable and whatsapp_linked:
        headline = "QuantBrief is live in OpenClaw and WhatsApp is linked as the chat front door."
    elif gateway_reachable and whatsapp_login_stage in {"qr_ready", "waiting"}:
        headline = "QuantBrief is live in OpenClaw and the WhatsApp QR is waiting for your scan."
    elif gateway_reachable:
        headline = "QuantBrief is live in OpenClaw, but messaging channels still need to be linked."
    else:
        headline = "QuantBrief is OpenClaw-ready, but the gateway and mobile channels need more setup."

    workspace_note = (
        f"QuantBrief is using the dedicated OpenClaw profile '{PROFILE_NAME}', so it stays isolated from your other workspaces."
        if active_config_path == PROFILE_OPENCLAW_CONFIG
        else (
            "OpenClaw's global default workspace points somewhere else, so launch QuantBrief from this folder to guarantee the right MCP tools."
            if default_workspace and not default_workspace_matches
            else "This project already ships its own OpenClaw workspace file, MCP registration, and skill."
        )
    )
    config_note = f"Profile config: {active_config_path}" if active_config_path == PROFILE_OPENCLAW_CONFIG else "Using the default OpenClaw home."

    summary_bits = [
        f"Gateway on port {port}" if gateway_configured else "Gateway not configured",
        f"model {default_model}" if default_model else "model not configured",
        "WhatsApp linked" if whatsapp_linked else "WhatsApp awaiting scan" if whatsapp_login_stage in {"qr_ready", "waiting"} else "WhatsApp configured" if whatsapp_configured else "WhatsApp not configured",
        "Telegram configured" if telegram_configured else "Telegram not configured",
    ]

    surfaces = [
        {
            "id": "local-agent",
            "label": "Local Agent",
            "status": "ready" if installed and workspace_ready else "setup",
            "detail": "Ask QuantBrief directly from OpenClaw CLI with this project's MCP tools and skill loaded.",
            "meta": "Best for fast portfolio questions from the terminal.",
            "actionLabel": "Copy CLI prompt",
            "command": ask_command,
        },
        {
            "id": "gateway",
            "label": "Gateway",
            "status": _status_label(gateway_reachable, gateway_configured),
            "detail": (
                f"Gateway is listening on ws://127.0.0.1:{port} and ready for local OpenClaw clients."
                if gateway_reachable
                else f"Gateway is configured for loopback on port {port}, but it is not fully healthy right now."
            ),
            "meta": f"Auth mode: {auth_config.get('mode', 'unknown')}. Bind: {gateway_config.get('bind', 'loopback')}.",
            "actionLabel": "Copy probe command" if gateway_reachable else "Copy gateway run",
            "command": gateway_probe_command if gateway_reachable else gateway_run_command,
        },
        {
            "id": "whatsapp",
            "label": "WhatsApp",
            "status": "ready" if whatsapp_linked else "setup" if whatsapp_configured else "offline",
            "detail": (
                "WhatsApp is linked and ready to act as QuantBrief's primary chat front door."
                if whatsapp_linked
                else "The WhatsApp QR is live right now. Scan it in WhatsApp -> Linked Devices to finish linking QuantBrief."
                if whatsapp_login_stage in {"qr_ready", "waiting"}
                else "WhatsApp channel is configured in the QuantBrief profile and can become the primary chat front door once you scan the QR."
                if whatsapp_configured
                else "WhatsApp is not configured yet. Use the QuantBrief OpenClaw profile to connect it and make QuantBrief feel chat-first."
            ),
            "meta": (
                f"Ideal for quick retail-investor check-ins and push-style decision briefs. QR file: {login_status.get('qrPath')}."
                if login_status.get("qrPath")
                else f"Ideal for quick retail-investor check-ins and push-style decision briefs. {config_note}"
            ),
            "actionLabel": "Copy WhatsApp login",
            "command": whatsapp_login_command,
        },
        {
            "id": "telegram",
            "label": "Telegram",
            "status": "ready" if telegram_configured else "setup",
            "detail": (
                "Telegram channel is already configured in OpenClaw and can deliver the same QuantBrief agent experience."
                if telegram_configured
                else "Telegram is not configured yet. Use the same OpenClaw channel wizard to turn it on."
            ),
            "meta": "Useful when you want a cleaner bot flow than the CLI.",
            "actionLabel": "Copy channel setup",
            "command": channel_setup_command,
        },
    ]

    return {
        "status": "ok",
        "headline": headline,
        "summary": " | ".join(summary_bits),
        "workspaceNote": workspace_note,
        "installed": installed,
        "model": default_model,
        "gateway": {
            "configured": gateway_configured,
            "reachable": gateway_reachable,
            "port": port,
            "mode": gateway_config.get("mode", "local"),
            "bind": gateway_config.get("bind", "loopback"),
            "authMode": auth_config.get("mode", "unknown"),
        },
        "workspace": {
            "configured": bool(workspace_config),
            "mcpRegistered": bool(workspace_mcp),
            "skillRegistered": skill_ready,
            "projectPath": str(project_dir),
            "defaultWorkspace": default_workspace,
            "matchesProject": default_workspace_matches,
            "mcpCwd": str(workspace_mcp.get("cwd") or ""),
        },
        "channels": {
            "whatsappConfigured": whatsapp_configured,
            "whatsappLinked": whatsapp_linked,
            "whatsappLoginStage": whatsapp_login_stage,
            "telegramConfigured": telegram_configured,
        },
        "commands": {
            "ask": ask_command,
            "channels": channel_setup_command,
            "whatsappLogin": whatsapp_login_command,
            "gateway": gateway_run_command,
            "probe": gateway_probe_command,
        },
        "surfaces": surfaces,
    }
