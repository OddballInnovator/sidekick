"""Sidekick backend: chat, overnight research jobs, briefings."""
import os

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent.chat import stream_chat
from .agent.research import run_research_job
from .jobs import scheduler, schedule_job
from .memory.cache import get_cached_briefing
from .memory.store import get_briefing, init_db, list_briefings, save_subscription

app = FastAPI(title="Sidekick")

# NOTE: the web UI is mounted at / AFTER all /api routes (see bottom of file),
# so /api/* routes take precedence. Single-service deploy, no CORS fuss.


@app.on_event("startup")
async def startup():
    await init_db()
    scheduler.start()


class ChatIn(BaseModel):
    message: str


@app.post("/api/chat")
async def chat(body: ChatIn):
    return StreamingResponse(stream_chat(body.message), media_type="text/event-stream")


class JobIn(BaseModel):
    topic: str
    run_at: str | None = None  # ISO time; None = ASAP (demo seam)


@app.post("/api/jobs/trigger")
async def trigger_job(body: JobIn):
    """The 'morning' seam: run the overnight research job on demand."""
    briefing = await run_research_job(body.topic)
    return {"briefing_id": briefing["id"]}


@app.post("/api/jobs")
async def create_job(body: JobIn):
    job = schedule_job(body.topic, body.run_at)
    return job


@app.get("/api/briefings")
async def briefings():
    return await list_briefings()


@app.get("/api/briefings/{briefing_id}")
async def briefing(briefing_id: int):
    cached = await get_cached_briefing(briefing_id)
    return cached or await get_briefing(briefing_id)


@app.get("/api/health")
async def health():
    return {"ok": True, "demo_mode": os.getenv("DEMO_MODE") == "1"}


# Web UI served at / (registered last so /api routes win).
app.mount("/", StaticFiles(directory="web", html=True), name="web")
