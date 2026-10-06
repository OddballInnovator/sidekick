# backend — agent loop (FastAPI)

## Phases
- Phase 1: `/chat` — Serverless Inference, streaming, model swap (`agent/chat.py`)
- Phase 2: tool registry + Action Gateway MCP (`tools/`), approval gate (`agent/approval.py`)
- Phase 3: memory — Postgres + pgvector (`memory/store.py`)
- Phase 4: jobs — briefing, flight watch (`jobs/`); Telegram webhook (`webhooks/`)

## Env
See `.env.example`. `DEMO_MODE=1` enables fixtures in `agent/fixtures.py`.
