"""Valkey: hot state. Briefing cache + current-job pointer.

Postgres is the record; Valkey is the fast lane the phone reads from.
"""
import json
import os

_client = None


def _client_or_none():
    global _client
    url = os.getenv("VALKEY_URL", "")
    if not url:
        return None
    if _client is None:
        import redis.asyncio as redis
        _client = redis.from_url(url, decode_responses=True)
    return _client


async def cache_briefing(briefing: dict) -> None:
    c = _client_or_none()
    if not c:
        return
    await c.set(f"briefing:{briefing['id']}", json.dumps(briefing), ex=3600)
    await c.set("briefing:latest", briefing["id"], ex=3600)


async def get_cached_briefing(briefing_id: int) -> dict | None:
    c = _client_or_none()
    if not c:
        return None
    raw = await c.get(f"briefing:{briefing_id}")
    return json.loads(raw) if raw else None


async def set_current_job(job_id: int, topic: str) -> None:
    c = _client_or_none()
    if not c:
        return
    await c.set("job:current", json.dumps({"job_id": job_id, "topic": topic}), ex=86400)


async def get_current_job() -> dict | None:
    c = _client_or_none()
    if not c:
        return None
    raw = await c.get("job:current")
    return json.loads(raw) if raw else None
