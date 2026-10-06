# Sidekick

Sidekick is a pocket AI chief of staff: an OpenClaw-style personal agent that acts in the
real world — restaurants, flights, calendar, inbox — built 100% on
DigitalOcean. Demo vehicle for the integrated AI-app-stack story.

DigitalOcean is the hero of this project. See `docs/PLAN.md` (execution plan),
`docs/SCREENPLAY.md` (video, shot in parallel with the build), and
`docs/demo-script.md` (the golden path).

## Layout
- `backend/` — FastAPI agent loop (inference + tools + approval gate + memory)
- `web/` — mobile web client (App Platform static)
- `infra/` — App Platform spec, notes
- `docs/` — plan, screenplay, demo script

## Quick start
See `backend/README.md`. `DEMO_MODE=1` seeds the demo fixtures.
