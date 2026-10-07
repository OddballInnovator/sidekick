# Sidekick — execution plan

## Mission
"Tell it at night. Wake up to it done." A pocket agent that takes an overnight
research task, works while you sleep, and delivers a briefing to your phone by
morning — built 100% on DigitalOcean. Outputs: working POC, demo video (shot
in parallel, not after), blog post. Two-day build.

## Narrative rules (non-negotiable)
- DigitalOcean is the hero. The builder is the crew, never the story.
- Frame everything as single-stack advantages across **building, operating,
  costing**. Never frame around gaps. No multi-vendor montage — the demo is
  one flow on one stack, across two surfaces.
- Shared language: the six needs (Meet the user, Understand, Get work done,
  Remember, Keep working, Run reliably).

## The demo flow (two surfaces, no montage)
- **Surface 1 — night, chat:** "By 7am, research [topic] and brief me. Five
  minutes, no fluff." The agent schedules the job and confirms. The scheduled
  job is shown on screen — filmable proof of "keep working."
- **Overnight — the job runs:** web search + fetch through the gateway,
  synthesis on Serverless Inference, briefing saved to Postgres.
- **Surface 2 — morning, phone:** push notification (OneSignal, native in the
  gateway) → open Sidekick → the briefing is waiting, sources linked.

## Architecture (POC, ruthlessly simple)
FastAPI on App Platform (+ static web client, + Managed Postgres):
- `POST /chat` — streaming chat on Serverless Inference; detects scheduling
  intent ("by 7am...") → creates the job, confirms in chat.
- Scheduler — APScheduler in-process (App Platform jobs are the production
  path; in-process is the 2-day path).
- Tools — `web_search`, `web_fetch` via the Action Gateway MCP endpoint;
  `synthesize` via inference. No other tools. No approval gate (research has
  no side effects).
- `POST /jobs/trigger` — the "morning" seam: runs the scheduled job on demand
  for filming. Nobody waits eight hours.
- `GET /briefings`, `GET /briefings/{id}` — the briefing view.
- OneSignal push on job completion.

## Cut list (explicitly out)
Telegram, voice input, approval gate, booking/transaction tools, vector
memory (preferences + conversation log in Postgres is enough), multi-vendor
twin, montage. If it is not chat, schedule, research, briefing, or push,
it does not ship.

## Two-day plan
- **Day 1:** backend (chat streaming + intent → job + research pipeline +
  briefing save), web UI (chat view + briefing view), deploy to App Platform,
  Postgres provisioned. Golden path runs locally by EOD.
- **Day 2:** OneSignal push wiring, golden path on the deployed app, footage
  capture (scripted takes per SCREENPLAY.md), voiceover after picture lock.

## Demo seams
- `POST /jobs/trigger` — "morning" on demand.
- `DEMO_MODE=1` — deterministic topic + canned sources if live search ever
  misbehaves on camera. Prefer live search: fresh results prove it is real.
- `docs/demo-script.md` — the exact prompts and clicks, in order.

## Flags
- Inference & Agents balance was $4.69 on 2026-10-06 with auto-reload OFF.
  Web Search / Web Fetch pause at zero. A console banner during verification
  confirmed: without auto-reload, these tools eventually pause. Top up before
  building/filming.
- Action Gateway programmatic access VERIFIED 2026-10-06: POST
  /v2/action-gateway/sessions (DO PAT) returns sessionUrn + mcpUrl
  (https://actions.do-ai.run/mcp/session/<uuid>); tools invoked over
  Streamable HTTP MCP via action_invoke. Real tool names: exa_web_search
  (query, max_results), exa_web_fetch. Test session "sidekick-research"
  created successfully (e9d2f479-…). Backend implements this in
  app/agent/tools.py; needs DIGITALOCEAN_TOKEN at deploy time.
