"""Postgres: jobs, briefings, messages, preferences."""
import json
import os

import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL", "")
_pool = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
  id SERIAL PRIMARY KEY,
  topic TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'scheduled',
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS briefings (
  id SERIAL PRIMARY KEY,
  job_id INT REFERENCES jobs(id),
  topic TEXT NOT NULL,
  content TEXT NOT NULL,
  sources JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS messages (
  id SERIAL PRIMARY KEY,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS preferences (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS push_subscriptions (
  id SERIAL PRIMARY KEY,
  endpoint TEXT UNIQUE NOT NULL,
  p256dh TEXT NOT NULL,
  auth TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
"""


async def _pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool


async def init_db():
    if not DATABASE_URL:
        return
    pool = await _pool()
    async with pool.acquire() as conn:
        # asyncpg execute() takes one statement at a time — split the schema.
        for stmt in [s.strip() for s in SCHEMA.split(";") if s.strip()]:
            await conn.execute(stmt)


async def save_job(topic: str, status: str = "scheduled") -> dict:
    pool = await _pool()
    row = await pool.fetchrow(
        "INSERT INTO jobs (topic, status) VALUES ($1, $2) RETURNING id, topic, status",
        topic, status)
    return dict(row)


async def update_job(job_id: int, status: str) -> None:
    pool = await _pool()
    await pool.execute("UPDATE jobs SET status=$1 WHERE id=$2", status, job_id)


async def save_briefing(topic: str, content: str, sources: list, job_id: int | None) -> dict:
    pool = await _pool()
    row = await pool.fetchrow(
        "INSERT INTO briefings (job_id, topic, content, sources) VALUES ($1,$2,$3,$4)"
        " RETURNING id, topic, content",
        job_id, topic, content, json.dumps(sources))
    return dict(row)


async def list_briefings() -> list[dict]:
    pool = await _pool()
    rows = await pool.fetch(
        "SELECT id, topic, created_at FROM briefings ORDER BY id DESC LIMIT 20")
    return [dict(r) for r in rows]


async def get_briefing(briefing_id: int) -> dict:
    pool = await _pool()
    row = await pool.fetchrow("SELECT * FROM briefings WHERE id=$1", briefing_id)
    return dict(row) if row else {}


async def save_message(role: str, content: str) -> None:
    pool = await _pool()
    await pool.execute("INSERT INTO messages (role, content) VALUES ($1,$2)", role, content)


async def save_subscription(endpoint: str, p256dh: str, auth: str) -> None:
    pool = await _pool()
    await pool.execute(
        """INSERT INTO push_subscriptions (endpoint, p256dh, auth)
           VALUES ($1,$2,$3)
           ON CONFLICT (endpoint) DO UPDATE SET p256dh=$2, auth=$3""",
        endpoint, p256dh, auth)


async def list_subscriptions() -> list[dict]:
    pool = await _pool()
    rows = await pool.fetch("SELECT endpoint, p256dh, auth FROM push_subscriptions")
    return [dict(r) for r in rows]
