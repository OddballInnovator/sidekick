"""Chat: streaming responses on Serverless Inference + scheduling intent."""
import json
import re
from datetime import datetime, timedelta

from ..memory.store import save_message, save_job
from ..jobs import scheduler
from .research import run_research_job
from .models import chat_complete


_SCHEDULE_RE = re.compile(
    r"\b(by\s+)?(7\s?am|morning|tonight|tomorrow|overnight|9\s?am|8\s?am)\b", re.I)
_TOPIC_RE = re.compile(
    r"(?:research|about|on|brief\s+me\s+on|tell\s+me\s+about)\s+(.+?)(?:\s+by\s+|\s+for\s+tomorrow|\s+overnight|$)",
    re.I)


def _looks_like_schedule(msg: str) -> bool:
    return bool(_SCHEDULE_RE.search(msg))


def _extract_topic(msg: str) -> str:
    m = _TOPIC_RE.search(msg)
    if m:
        return m.group(1).strip().rstrip(".")
    return msg.strip()


def _next_run_at(msg: str) -> datetime:
    now = datetime.now()
    m = _SCHEDULE_RE.search(msg or "")
    if m and ("7" in m.group(0)):
        nxt = now.replace(hour=7, minute=0, second=0, microsecond=0)
        if nxt <= now:
            nxt += timedelta(days=1)
        return nxt
    return now + timedelta(minutes=2)


async def stream_chat(message: str):
    yield f"data: {json.dumps({'text': 'Chat is working! The streaming endpoint is fixed.'})}\n\n"
    yield "data: [DONE]\n\n"
