"""Tool interface: web_search / web_fetch via DigitalOcean Action Gateway.

Real transport (verified 2026-10-06):
1. Create a session: POST https://api.digitalocean.com/v2/action-gateway/sessions
   with the DO PAT -> returns sessionUrn + mcpUrl.
2. Invoke tools over Streamable HTTP MCP at the mcpUrl:
   JSON-RPC tools/call -> action_invoke with
   {"tools": [{"tool": "exa_web_search", "arguments": {...}}]}.
   Headers: Authorization Bearer <PAT>, X-Session-Id <urn>, X-Actor-Id,
   MCP-Protocol-Version 2025-06-18.

Resolution order:
1. DO_AG_MCP_URL (+ DO_AG_SESSION_URN) set -> use that session.
2. DIGITALOCEAN_TOKEN set -> create a session, cache it.
3. DEMO_MODE=1 -> deterministic fixtures for filming.
4. Otherwise -> raise, so we never silently fake a tool call.
"""
import itertools
import json
import os

import httpx

DEMO_MODE = os.getenv("DEMO_MODE") == "1"
ACTOR_ID = os.getenv("DO_AG_ACTOR_ID", "sidekick")
MCP_PROTOCOL_VERSION = "2025-06-18"
TOOL_SEARCH = "exa_web_search"
TOOL_FETCH = "exa_web_fetch"

_session = {}  # {"mcp_url":..., "urn":...}
_rpc_ids = itertools.count(1)

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


async def _ensure_session() -> dict:
    if _session:
        return _session
    mcp_url = os.getenv("DO_AG_MCP_URL", "")
    urn = os.getenv("DO_AG_SESSION_URN", "")
    if mcp_url:
        _session.update(mcp_url=mcp_url, urn=urn)
        return _session
    token = os.getenv("DIGITALOCEAN_TOKEN", "")
    if not token:
        raise RuntimeError("no gateway session: set DO_AG_MCP_URL or DIGITALOCEAN_TOKEN")
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.digitalocean.com/v2/action-gateway/sessions",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json={
                "name": "sidekick-research",
                "actor_id": ACTOR_ID,
                "policy": {"defaultAction": "allow", "rules": [
                    {"tool": TOOL_SEARCH, "action": "allow"},
                    {"tool": TOOL_FETCH, "action": "allow"}]},
                "tools": [TOOL_SEARCH, TOOL_FETCH],
            },
        )
        resp.raise_for_status()
        data = resp.json()
    sess = data.get("session", {})
    mcp_url = data.get("mcpUrl") or sess.get("mcpUrl")
    urn = sess.get("sessionUrn", "")
    if not mcp_url:
        raise RuntimeError(f"session create missing mcpUrl: {str(data)[:200]}")
    _session.update(mcp_url=mcp_url, urn=urn)
    return _session


def _mcp_headers(urn: str) -> dict:
    token = os.getenv("DIGITALOCEAN_TOKEN", "")
    h = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": MCP_PROTOCOL_VERSION,
        "X-Actor-Id": ACTOR_ID,
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    if urn:
        h["X-Session-Id"] = urn
    return h


async def _invoke(tool: str, arguments: dict):
    sess = await _ensure_session()
    payload = {
        "jsonrpc": "2.0",
        "id": next(_rpc_ids),
        "method": "tools/call",
        "params": {
            "name": "action_invoke",
            "arguments": {"tools": [{"tool": tool, "arguments": arguments}]},
        },
    }
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(sess["mcp_url"], headers=_mcp_headers(sess["urn"]),
                                 json=payload)
        resp.raise_for_status()
        data = _parse_mcp_response(resp)
    if "error" in data:
        raise RuntimeError(f"gateway error: {data['error']}")
    return _extract_text(data)


def _parse_mcp_response(resp) -> dict:
    """Streamable HTTP MCP may return plain JSON or an SSE stream."""
    ctype = resp.headers.get("content-type", "")
    if "text/event-stream" in ctype:
        last = None
        for line in resp.text.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                try:
                    last = json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue
        if last is None:
            raise RuntimeError("no JSON-RPC data in SSE stream")
        return last
    return resp.json()


def _extract_text(payload: dict) -> str:
    result = payload.get("result", {})
    texts = [b.get("text", "") for b in result.get("content", [])
             if isinstance(b, dict) and b.get("type") == "text"]
    if texts:
        return "\n".join(texts)
    sc = result.get("structuredContent")
    if sc is not None:
        return json.dumps(sc)
    return json.dumps(result)


def _parse_search(text: str) -> list[dict]:
    try:
        items = json.loads(text)
        if isinstance(items, list):
            return [{"title": i.get("title", ""),
                     "url": i.get("url", ""),
                     "snippet": i.get("snippet", i.get("text", ""))[:300]}
                    for i in items if isinstance(i, dict)]
    except (json.JSONDecodeError, TypeError):
        pass
    return [{"title": "search results", "url": "", "snippet": text[:1500]}]


async def web_search(query: str, n: int = 5) -> list[dict]:
    if os.getenv("DO_AG_MCP_URL") or os.getenv("DIGITALOCEAN_TOKEN"):
        text = await _invoke(TOOL_SEARCH, {"query": query, "max_results": n})
        return _parse_search(text)[:n]
    if DEMO_MODE:
        return _FIXTURES["search"][:n]
    raise RuntimeError("no tool transport configured (DIGITALOCEAN_TOKEN or DEMO_MODE=1)")


async def web_fetch(url: str) -> str:
    if os.getenv("DO_AG_MCP_URL") or os.getenv("DIGITALOCEAN_TOKEN"):
        return await _invoke(TOOL_FETCH, {"url": url})
    if DEMO_MODE:
        return f"Fixture article text for {url}."
    raise RuntimeError("no tool transport configured (DIGITALOCEAN_TOKEN or DEMO_MODE=1)")
