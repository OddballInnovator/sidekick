# Sidekick — execution plan

## Mission
Build a pocket AI chief of staff: an OpenClaw-style personal agent that acts in
the real world (finds restaurants, watches flights, manages calendar and inbox),
built 100% on DigitalOcean. Outputs: working POC, demo video (shot in parallel
with the build, not after), blog post.

## Narrative rules (non-negotiable)
- DigitalOcean is the hero. The builder (Muse) is the crew, never the story.
- Frame everything as single-stack advantages across **building, operating,
  costing**. Never frame around gaps.
- The setup: multi-vendor pain stated concretely — multiple accounts, multiple
  management layers, no single observability layer.
- Shared language everywhere (video, blog, code, docs): the six needs.

## The six needs
1. Meet the user — interface, APIs, streaming, notifications
2. Understand — models, routing, guardrails, evaluation
3. Get work done — agents, tools, permissions, approval
4. Remember — app data, conversations, files, vectors
5. Keep working — webhooks, queues, schedules, background jobs
6. Run reliably — deploy, secure, observe, understand cost

## Architecture (POC)
Our own agent loop (Python/FastAPI) on App Platform, calling:
- **Understand:** Serverless Inference (`inference.do-ai.run/v1`, OpenAI-compatible)
- **Get work done:** Action Gateway MCP endpoint for tools + our own approval gate
  (deterministic, filmable; Harness Runtime is the production path, not the POC path)
- **Remember:** Managed PostgreSQL (+pgvector), Valkey (sessions), Spaces (attachments)
- **Meet the user:** mobile web client (App Platform static), Telegram bot via Functions webhook
- **Keep working:** App Platform jobs (proactive briefings, flight watches)
- **Run reliably:** one DO project, VPC, one bill

Why our own loop instead of a Managed Agents harness: determinism on camera.
Every demo beat must be reproducible. The gateway still supplies the tools, so
the "tools came with the platform" story stays intact.

## Multi-vendor alternative (for the video, montage only — not a real build)
Vercel (meet) + Fireworks (understand) + Daytona (get work done) + Supabase
(remember) + AWS (keep working) = 5 vendors x 4 surfaces (account, access, logs,
bill) = 20 control surfaces vs 4 on DigitalOcean.

## Tool inventory (checked live in DO console, 2026-10-06)
Native in Action Gateway: Web Search, Web Fetch, Code Execution, Geoapify
(maps/geocoding/places), OneSignal (notifications), third-party browser
automation (Anchor Browser, Browserless).
NOT in catalog — register as custom MCP providers or call directly:
Duffel (flights), Gmail, Google Calendar, Telegram Bot API (direct webhook),
restaurant booking (browser automation flow).
Catalog: 551 providers / 18,000+ tools. No per-tool dollar pricing shown.

## Phases (each unlocks a video beat)
- **Phase 0 — Setup.** DO project, repo, App Platform skeleton. Beat: the
  20-surfaces montage + "one project" creation.
- **Phase 1 — Inference + chat.** Chat endpoint on Serverless Inference,
  streaming, model swap. Beat: "same key, every model."
- **Phase 2 — Tools + approval gate.** Tool registry, gateway MCP wiring,
  approval gate on consequential actions, restaurant search demo seam.
  Beat: THE hero shot — agent finds options, approval fires, tap, booked.
- **Phase 3 — Memory.** Postgres schema, pgvector, preferences, conversation
  memory. Beat: "it remembers" across sessions.
- **Phase 4 — Proactive + messaging.** Scheduled jobs (morning briefing, flight
  watch), Telegram webhook. Beat: the briefing arrives unprompted.
- **Phase 5 — Money shot.** Observability + billing walkthrough.
  Beat: one page vs five dashboards.

## Demo seams (build into the app, not around it)
- `DEMO_MODE`: seeds user/preferences, triggers briefing on demand, resets state.
- `docs/demo-script.md`: the exact golden-path prompts and clicks, in order.
- Deterministic fixtures for the hero flows (restaurant options, flight prices).

## Flags
- Inference & Agents balance was $4.69 on 2026-10-06 with auto-reload OFF.
  Web Search/Web Fetch/Code Execution pause at zero. Top up before building/filming.
- Managed Agents is public preview. ADK is deprecated (Oct 1, 2026) — do not use.
- Serverless Inference is prepaid-only; enable auto-reload before any demo.
