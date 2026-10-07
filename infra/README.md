# infra

`app.yaml` is the whole deploy: one App Platform service (FastAPI serves the
API at /api/* and the mobile web UI at /) + managed Postgres + managed Valkey.
Six DO services in one project, one bill: App Platform, Serverless Inference
(+ Inference Router), Action Gateway, Postgres, Valkey.

## Deploy
```
doctl apps create --spec infra/app.yaml
```
Then fill the secrets (console or `doctl apps update`):
- `DO_INFERENCE_KEY` — Serverless Inference API key
- `DO_INFERENCE_ROUTER` — router name (create in console: Inference > Routers,
  cost-efficiency preset, name it `sidekick`); every model call then goes
  through `router:sidekick`, which picks the best model per dollar. Leave as
  REPLACE_ME to use `DO_INFERENCE_MODEL` directly.
- `DIGITALOCEAN_TOKEN` — DO PAT; the backend mints its Action Gateway session
  with it at first tool call
- `VAPID_PRIVATE_KEY` — set at deploy time via API (public key is already in
  app.yaml); enables the morning Web Push. The briefing view works without it.
- Push is Web Push/VAPID direct from the backend — no third-party push vendor.

`DATABASE_URL` is injected automatically from the attached database.
