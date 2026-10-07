"""The overnight pipeline: search -> fetch -> synthesize -> save -> notify."""
import os

import httpx

from ..memory.cache import cache_briefing
from ..memory.store import save_briefing, update_job
from .notify import push_briefing_ready
from .tools import web_fetch, web_search

INFERENCE_URL = os.getenv("DO_INFERENCE_URL", "https://inference.do-ai.run/v1")
INFERENCE_KEY = os.getenv("DO_INFERENCE_KEY", "")
from .models import resolve_model


async def run_research_job(topic: str, job_id: int | None = None) -> dict:
    if job_id:
        await update_job(job_id, "running")
    results = await web_search(f"{topic}", n=5)
    sources = []
    for r in results[:4]:
        try:
            text = await web_fetch(r["url"])
        except Exception:
            text = r.get("snippet", "")
        sources.append({"title": r["title"], "url": r["url"], "text": text[:4000]})
    briefing_md = await _synthesize(topic, sources)
    briefing = await save_briefing(topic, briefing_md, sources, job_id)
    await cache_briefing(briefing)
    if job_id:
        await update_job(job_id, "done")
    await push_briefing_ready(topic, briefing["id"])
    return briefing


async def _synthesize(topic: str, sources: list[dict]) -> str:
    context = "\n\n".join(
        f"## {s['title']} ({s['url']})\n{s['text']}" for s in sources
    )
    prompt = (f"Write a five-minute morning briefing on: {topic}. "
              f"Be crisp, no fluff. Link claims to sources. Markdown.\n\n{context}")
    headers = {"Authorization": f"Bearer {INFERENCE_KEY}"} if INFERENCE_KEY else {}
    async with httpx.AsyncClient(timeout=180) as client:
        resp = await client.post(
            f"{INFERENCE_URL}/chat/completions", headers=headers,
            json={"model": resolve_model(),
                  "messages": [{"role": "user", "content": prompt}]},
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
