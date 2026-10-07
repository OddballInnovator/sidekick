# infra

`app.yaml` is the whole deploy: one App Platform service (FastAPI serves the
API at /api/* and the mobile web UI at /) + one managed Postgres
(`db-s-1vcpu-1gb`). One project, one bill.

## Deploy
```
doctl apps create --spec infra/app.yaml
```
Then fill the secrets (console or `doctl apps update`):
- `DO_INFERENCE_KEY` — Serverless Inference API key
- `DIGITALOCEAN_TOKEN` — DO PAT; the backend mints its Action Gateway session
  with it at first tool call
- `ONESIGNAL_APP_ID` / `ONESIGNAL_API_KEY` — morning push (optional; the
  briefing view works without it)

`DATABASE_URL` is injected automatically from the attached database.
