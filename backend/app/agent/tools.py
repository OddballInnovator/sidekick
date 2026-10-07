"""Tool interface: web_search / web_fetch.

Transport is resolved at runtime, in this order:
1. DO_ACTION_GATEWAY_MCP_URL set -> call the gateway MCP endpoint (pending
   verification of the exact endpoint shape; see docs/PLAN.md flags).
2. DEMO_MODE=1 -> deterministic fixtures for filming.
3. Otherwise -> raise, so we never silently fake a tool call.
"""
import json
import os

import httpx

DEMO_MODE = os.getenv("DEMO_MODE") == "1"
GATEWAY_MCP_URL = os.getenv("DO_ACTION_GATEWAY_MCP_URL", "")

_FIXTURES = {
    "search": [
        {"title": "AI infra week in review", "url": "https://example.com/ai-infra-1",
         "snippet": "Fixture result one."},
        {"title": "New inference pricing shakeup", "url": "https://example.com/ai-infra-2",
         "snippet": "Fixture result two."},
        {"title": "GPU capacity expands", "url": "https://example.com/ai-infra-3",
         "snippet": "Fixture result three."},
    ]
}


async def web_search(query: str, n: int = 5) -> list[dict]:
    if GATEWAY_MCP_URL:
        return await _gateway_call("web_search", {"query": query, "n": n})
    if DEMO_MODE:
        return _FIXTURES["search"][:n]
    raise RuntimeError("no tool transport configured (set DO_ACTION_GATEWAY_MCP_URL or DEMO_MODE=1)")


async def web_fetch(url: str) -> str:
    if GATEWAY_MCP_URL:
        return await _gateway_call("web_fetch", {"url": url})
    if DEMO_MODE:
        return f"Fixture article text for {url}."
    raise RuntimeError("no tool transport configured (set DO_ACTION_GATEWAY_MCP_URL or DEMO_MODE=1)")


async def _gateway_call(tool: str, args: dict):
    """MCP call over streamable HTTP. Shape TBD by console verification."""
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            GATEWAY_MCP_URL,
            json={"tool": tool, "arguments": args},
            headers={"Authorization": f"Bearer {os.getenv('DO_ACTION_GATEWAY_KEY', '')}"},
        )
        resp.raise_for_status()
        data = resp.json()
    return data.get("result", data)
