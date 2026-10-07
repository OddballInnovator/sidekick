"""Ephemeral compute: provision a real DigitalOcean droplet, run shell commands
over SSH, then tear it down. This is what makes Sidekick an agent, not a chatbot.

Safety rails (v1):
- Only the smallest droplet size (s-1vcpu-1gb, ~$0.009/hr).
- Single region (sfo3, same as the app).
- Command denylist blocks destructive patterns.
- Droplets are tagged sidekick-ephemeral and destroyed after the task.
"""
import asyncio
import io
import os
import time

import httpx
import paramiko

DO_TOKEN = os.getenv("DIGITALOCEAN_TOKEN", "")
DO_API = "https://api.digitalocean.com/v2"

DROPLET_SIZE = "s-1vcpu-1gb"
DROPLET_REGION = "sfo3"
DROPLET_IMAGE = "ubuntu-24-04-x64"
DROPLET_TAG = "sidekick-ephemeral"
SSH_KEY_NAME = "sidekick-agent"

# Patterns that are never allowed through, even on the user's own droplet.
DENY = [
    "rm -rf /", "rm -rf /*", "mkfs", "dd if=", ":(){", "shutdown",
    "reboot", "halt", "poweroff", "> /dev/sd", "chmod -R 777 /",
]


def _headers():
    return {"Authorization": f"Bearer {DO_TOKEN}", "Content-Type": "application/json"}


def _denied(cmd: str) -> str | None:
    low = cmd.lower()
    for pat in DENY:
        if pat in low:
            return pat
    return None


async def _api(method: str, path: str, body: dict | None = None):
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.request(method, DO_API + path, headers=_headers(), json=body)
        r.raise_for_status()
        return r.json() if r.text else {}


# ---------------------------------------------------------------- SSH keys

async def ensure_ssh_key() -> tuple[str, str]:
    """Return (key_id, private_key_pem). Creates the sidekick-agent key once."""
    keys = await _api("GET", "/v2/account/keys")
    for k in keys.get("ssh_keys", []):
        if k["name"] == SSH_KEY_NAME:
            # Private half lives in Valkey; fetch it.
            from ..memory.cache import get as cache_get
            pem = await cache_get("ssh:private_pem")
            if pem:
                return str(k["id"]), pem
    # Generate a fresh Ed25519 keypair.
    key = paramiko.Ed25519Key.generate()
    buf = io.StringIO()
    key.write_private_key(buf)
    pem = buf.getvalue()
    pub = f"{key.get_name()} {key.get_base64()} {SSH_KEY_NAME}"
    created = await _api("POST", "/v2/account/keys",
                         {"name": SSH_KEY_NAME, "public_key": pub})
    from ..memory.cache import set as cache_set
    await cache_set("ssh:private_pem", pem)
    return str(created["ssh_key"]["id"]), pem


# ---------------------------------------------------------------- droplets

async def provision(name: str = "sidekick-task") -> dict:
    """Create the droplet. Returns {id, ip} once active with an IP."""
    key_id, _ = await ensure_ssh_key()
    d = await _api("POST", "/v2/droplets", {
        "name": name,
        "region": DROPLET_REGION,
        "size": DROPLET_SIZE,
        "image": DROPLET_IMAGE,
        "ssh_keys": [key_id],
        "tags": [DROPLET_TAG],
    })
    droplet_id = d["droplet"]["id"]
    # Poll until active with a public IPv4.
    for _ in range(40):
        await asyncio.sleep(10)
        cur = await _api("GET", f"/v2/droplets/{droplet_id}")
        dd = cur["droplet"]
        if dd["status"] == "active":
            v4 = [n["ip_address"] for n in dd["networks"]["v4"]
                  if n["type"] == "public"]
            if v4:
                return {"id": droplet_id, "ip": v4[0]}
    raise TimeoutError("droplet did not become active in time")


async def destroy(droplet_id: int | str):
    await _api("DELETE", f"/v2/droplets/{droplet_id}")


# ---------------------------------------------------------------- SSH exec

def _ssh_run(ip: str, pem: str, command: str, timeout: int = 120) -> tuple[str, str, int]:
    """Blocking SSH run; called in a thread."""
    key = paramiko.Ed25519Key.from_private_key(io.StringIO(pem))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username="root", pkey=key, timeout=30,
                   banner_timeout=30, auth_timeout=30)
    try:
        _, stdout, stderr = client.exec_command(command, timeout=timeout)
        rc = stdout.channel.recv_exit_status()
        return stdout.read().decode(errors="replace"), \
            stderr.read().decode(errors="replace"), rc
    finally:
        client.close()


async def wait_ssh(ip: str, pem: str, tries: int = 24):
    for _ in range(tries):
        try:
            await asyncio.to_thread(_ssh_run, ip, pem, "echo ok", 15)
            return
        except Exception:
            await asyncio.sleep(10)
    raise TimeoutError("SSH never came up")


async def run(ip: str, pem: str, command: str, timeout: int = 120) -> dict:
    """Run one shell command. Returns {out, err, rc} or {denied}."""
    hit = _denied(command)
    if hit:
        return {"denied": f"blocked pattern: {hit}"}
    out, err, rc = await asyncio.to_thread(_ssh_run, ip, pem, command, timeout)
    return {"out": out[-4000:], "err": err[-2000:], "rc": rc}
