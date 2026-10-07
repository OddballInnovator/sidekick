"""Chat: streaming responses on Serverless Inference + scheduling intent."""
import json
import os
import re

import httpx

from ..memory.store import save_job, save_message
from . import tools as _tools  # noqa: F401 (kept for explicit tool surface)

INFERENCE_URL = os.getenv("DO_INFERENCE_URL", "https://inference.do-ai.run/v1")
INFERENCE_KEY = os.getenv("DO_INFERENCE_KEY", "")
from .models import resolve_model

SCHEDULE_RE = re.compile(
    r"\bby\s+(\d{1,2}\s?(?:am|pm))\b|\btomorrow morning\b|\bovernight\b|\bby morning\b",
    re.IGNORECASE,
)


def _looks_like_schedule(text: str) -> bool:
    return bool(SCHEDULE_RE.search(text))


def _extract_topic(text: str) -> str:
    # "research X" / "brief me on X" -> X ; fallback: whole message
    m = re.search(r"(?:research|brief me on|look into|find out about)\s+(.+?)(?:\.|$)", text, re.IGNORECASE)
    topic = m.group(1) if m else text
    return topic.strip().rstrip(".")


async def stream_chat(message: str):
    await save_message("user", message)
    if _looks_like_schedule(message):
        topic = _extract_topic(message)
        job = await save_job(topic, status="scheduled")
        reply = (f"Scheduled for 7:00 AM. I will research {topic} overnight "
                 f"and push the briefing to your phone.")
        await save_message("assistant", reply)
        yield f"data: {json.dumps({'text': reply, 'job_id': job['id']})}\n\n"
        yield "data: [DONE]\n\n"
        return

    headers = {"Authorization": f"Bearer {INFERENCE_KEY}"} if INFERENCE_KEY else {}
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream(
            "POST", f"{INFERENCE_URL}/chat/completions",
            headers=headers,
            json={"model": resolve_model(), "messages": [{"role": "user", "content": message}],
                  "stream": True},
        ) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data:"):
                    yield line + "\n\n"
    await save_message("assistant", "[streamed]")
