"""The VM agent: natural language -> real droplet -> real shell commands -> answer.

Hero flow: "spin up a vm and host a hello world page"
  1. provision a real droplet (s-1vcpu-1gb, ~$0.009/hr)
  2. LLM plans the shell commands for the task
  3. each command runs over SSH, output streams back to chat
  4. LLM summarizes what happened
  5. droplet is destroyed (unless the user says "keep it")
"""
import json
import os
import re

import httpx

from . import compute
from .models import resolve_model
from ..memory.store import save_message

INFERENCE_URL = os.getenv("DO_INFERENCE_URL", "https://inference.do-ai.run/v1")
INFERENCE_KEY = os.getenv("DO_INFERENCE_KEY", "")

VM_RE = re.compile(
    r"\b(spin\s*up|provision|launch|create)\b.*\b(vm|droplet|server|machine|box)\b",
    re.IGNORECASE,
)

KEEP_RE = re.compile(r"\bkeep it\b|\bdon't destroy\b|\bdont destroy\b", re.IGNORECASE)


def wants_vm(text: str) -> bool:
    return bool(VM_RE.search(text))


def extract_task(text: str) -> str:
    m = re.search(r"\band\b(.+)", text, re.IGNORECASE)
    return m.group(1).strip().rstrip(".") if m else "run a quick check"


async def _llm(messages: list[dict], timeout: int = 90) -> str:
    headers = {"Authorization": f"Bearer {INFERENCE_KEY}"} if INFERENCE_KEY else {}
    async with httpx.AsyncClient(timeout=timeout) as c:
        r = await c.post(
            f"{INFERENCE_URL}/chat/completions", headers=headers,
            json={"model": resolve_model(), "messages": messages},
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


async def plan_commands(task: str) -> list[str]:
    sys = ("You are a DevOps agent operating a fresh Ubuntu 24.04 droplet as root. "
           "Translate the user's task into shell commands. Reply with ONLY a JSON "
           "array of command strings, max 6, no explanations. Prefer non-interactive "
           "flags (-y, -q). Do not include destructive commands.")
    raw = await _llm([{"role": "system", "content": sys},
                      {"role": "user", "content": task}])
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    try:
        cmds = json.loads(m.group(0)) if m else []
        return [str(x) for x in cmds][:6]
    except Exception:
        return []


async def summarize(task: str, transcript: list[str]) -> str:
    sys = ("You are Sidekick, reporting back after running commands on a fresh "
           "cloud VM. Summarize what was done and the key result in 3 sentences "
           "max. Plain language, no fluff.")
    body = f"Task: {task}\n\n" + "\n".join(transcript[-12:])
    return await _llm([{"role": "system", "content": sys},
                       {"role": "user", "content": body}])


async def run_vm_task(text: str):
    """Async generator yielding progress events for the chat stream."""
    task = extract_task(text)
    keep = bool(KEEP_RE.search(text))
    yield {"text": f"🖥️ Spinning up a droplet for: {task}"}

    droplet = await compute.provision()
    ip, did = droplet["ip"], droplet["id"]
    yield {"text": f"Droplet live at {ip} (s-1vcpu-1gb, sfo3). Waiting for SSH…"}

    _, pem = await compute.ensure_ssh_key()
    await compute.wait_ssh(ip, pem)
    yield {"text": "SSH ready. Planning the commands…"}

    cmds = await plan_commands(task)
    if not cmds:
        cmds = ["uptime"]
    transcript = []
    for cmd in cmds:
        yield {"text": f"→ `{cmd}`"}
        res = await compute.run(ip, pem, cmd)
        if "denied" in res:
            transcript.append(f"$ {cmd}\nBLOCKED: {res['denied']}")
            yield {"text": f"⚠️ Blocked: {res['denied']}"}
            continue
        out = (res["out"] or res["err"] or "(no output)").strip()
        transcript.append(f"$ {cmd}\n{out[:1500]}")
        yield {"text": f"```\n{out[:800]}\n```"}

    summary = await summarize(task, transcript)
    if keep:
        yield {"text": f"{summary}\n\nDroplet kept alive at {ip} (id {did}). Say 'destroy it' when done."}
    else:
        await compute.destroy(did)
        yield {"text": f"{summary}\n\n✅ Droplet destroyed. Ephemeral infra — pennies, then gone."}
    await save_message("assistant", summary)
