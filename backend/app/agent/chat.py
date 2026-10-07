"""Chat: streaming responses on Serverless Inference + scheduling intent."""
import datetime
import json
import os
import re

import httpx

from ..jobs import scheduler
from ..memory.store import save_job, save_message
from . import tools as _tools  # noqa: F401 (kept for explicit tool surface)
from .research import run_research_job

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


def _next_run_at(text: str) -> datetime.datetime:
    """Next occurrence of the 'by 7am'-style time in the message; default +60s."""
    m = SCHEDULE_RE.search(text)
    now = datetime.datetime.now()
    if m and m.group(1):
        t = m.group(1).lower().replace(" ", "")
        hour = int(re.match(r"\d+", t).group())
        if "pm" in t and hour < 12:
            hour += 12
        if "am" in t and hour == 12:
            hour = 0
        when = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if when <= now:
            when += datetime.timedelta(days=1)
        return when
    return now + datetime.timedelta(seconds=60)
    # "research X" / "brief me on X" -> X ; fallback: whole message
    m = re.search(r"(?:research|brief me on|look into|find out about)\s+(.+?)(?:\.|$)", text, re.IGNORECASE)
    topic = m.group(1) if m else text
    return topic.strip().rstrip(".")


async def stream_chat(message: str):
    await save_message("user", message)
    from .vm import wants_vm, run_vm_task
    if wants_vm(message):
        async for event in run_vm_task(message):
            yield f"data: {json.dumps(event)}\n\n"
        yield "data: [DONE]\n\n"
        return
    if _looks_like_schedule(message):
        topic = _extract_topic(message)
        job = await save_job(topic, status="scheduled")
        when = _next_run_at(message)
        scheduler.add_job(run_research_job, "date", run_date=when,
                          kwargs={"topic": topic, "job_id": job["id"]})
        reply = (f"Scheduled for {when.strftime('%-I:%M %p')}. I will research {topic} overnight "
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
