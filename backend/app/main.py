"""Sidekick backend: chat, overnight research jobs, briefings."""
import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent.chat import stream_chat
from .agent.research import run_research_job
from .jobs import scheduler, schedule_job
from .memory.cache import get_cached_briefing
from .memory.store import _pool as _db_pool
from .memory.store import DATABASE_URL as STORE_DATABASE_URL
from .memory.store import get_briefing, init_db, list_briefings, save_subscription


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    for attempt in range(6):
        try:
            await init_db()
            # prove the tables exist, not just the connection
            pool = await _db_pool()
            await pool.fetchval("SELECT COUNT(*) FROM briefings")
            print("init_db ok, tables verified", flush=True)
            break
        except Exception as e:
            print(f"init_db attempt {attempt + 1} failed: {type(e).__name__}: {e}", flush=True)
            await asyncio.sleep(5)
    scheduler.start()
    yield


app = FastAPI(title="Sidekick", lifespan=lifespan)

# NOTE: the web UI is mounted at / AFTER all /api routes (see bottom of file),
# so /api/* routes take precedence. Single-service deploy, no CORS fuss.


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


@app.get("/api/push/vapid-public-key")
async def vapid_public_key():
    return {"publicKey": os.getenv("VAPID_PUBLIC_KEY", "")}


class PushSub(BaseModel):
    endpoint: str
    keys: dict


@app.post("/api/push/subscribe")
async def push_subscribe(body: PushSub):
    await save_subscription(body.endpoint, body.keys.get("p256dh", ""), body.keys.get("auth", ""))
    return {"ok": True}


@app.get("/api/health")
async def health():
    db_status = "unconfigured"
    pool_status: str = "unconfigured"
    q_status: str = "unconfigured"
    url = os.getenv("DATABASE_URL", "")
    if url:
        try:
            import asyncpg
            conn = await asyncpg.connect(url, timeout=8)
            await conn.execute("SELECT 1")
            await conn.close()
            db_status = "ok"
        except Exception as e:
            db_status = f"error: {type(e).__name__}: {e}"
        try:
            pool = await _db_pool()
            pool_status = f"pool ok (env_len={len(url)}, store_len={len(STORE_DATABASE_URL)}, same={url == STORE_DATABASE_URL})"
        except Exception as e:
            pool_status = f"pool error: {type(e).__name__}: {e}"
        try:
            rows = await list_briefings()
            q_status = f"query ok, {len(rows)} rows"
        except Exception as e:
            q_status = f"query error: {type(e).__name__}: {e}"
    return {"ok": True, "demo_mode": os.getenv("DEMO_MODE") == "1",
            "db": db_status, "pool": pool_status, "query": q_status}


# Web UI served at / (registered last so /api routes win).
app.mount("/", StaticFiles(directory="web", html=True), name="web")
