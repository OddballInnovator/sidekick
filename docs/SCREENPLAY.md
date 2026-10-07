# Sidekick — video screenplay

## Logline
Tell it at night. Wake up to it done. A pocket agent that researches overnight
and briefs you by morning — built on one stack. No camera, no hands: all
screen capture. No montage.

## Spine (shared with the stakeholder deck)
1. What we are building — and why most modern AI apps need the same six things.
2. The architecture those six needs demand.
3. Two ways to build it: the DigitalOcean single stack vs. the multi-vendor
   alternative (static diagram, not a montage).
4. Build a little (timelapse).
5. Run it — then observability, cost, and the one-stack benefits.

## Format
- Target runtime: ~5 minutes. Voiceover generated after picture lock.
- Narration rule: VO first (say what we are doing and how), then the shot
  (do and show). Never explain over a shot of something else.
- Capture: scripted takes (Playwright, golden path from docs/demo-script.md).
  Bad take = re-run. Timelapse (6–10x) for the build and the overnight run;
  real time for the schedule confirmation, the push arriving, the briefing.

## Act 1 — What we are building (0:00–0:45)
VO: "Sidekick. A pocket agent you brief at night — it researches while you
sleep, and your morning briefing is waiting when you wake up."
SHOW: the phone, chat view. The ask is typed.
VO: "It is one app. But look closer — nearly every modern AI app needs the
same six things."
SHOW: the six needs appear, one by one: meet the user, understand, get work
done, remember, keep working, run reliably.

## Act 2 — The architecture (0:45–1:30)
VO: "Those six needs are an architecture. An interface. Models. Tools with
permissions. Memory. Schedules that survive the night. And one place to watch
it all and pay for it."
SHOW: the six needs as an architecture diagram — clean, static.

## Act 3 — Two ways to build it (1:30–2:30)
VO: "On DigitalOcean, that architecture is one stack. App Platform runs it.
Serverless Inference — through the router, best model per dollar — thinks.
The Action Gateway hands it tools. Postgres remembers. Valkey keeps the hot
state. One project, one bill."
SHOW: the DO stack diagram — six services, one frame.
VO: "The alternative is five vendors. Five accounts, five access models, five
log dashboards, five bills — twenty things to manage before the app does
anything useful."
SHOW: the multi-vendor diagram beside it — five vendor cards, each repeating
account / access / logs / bill. Static. No montage.

## Act 4 — Build a little (2:30–3:30)
VO: "So we built it on the single stack. Watch."
SHOW: timelapse — repo to deployed app: the service, the database, the cache,
all in one project.

## Act 5 — Run it (3:30–5:00)
VO: "It is 11pm. By 7am, research the biggest AI infrastructure announcements
this week — five minutes, no fluff."
SHOW: real time, phone frame — the prompt is sent; the agent confirms the
7am schedule; the job is listed.
VO: "While you sleep, it works — searching, reading, synthesizing, saving."
SHOW: timelapse — the job log scrolls.
VO: "7am."
SHOW: real time — the phone buzzes, the briefing opens, a slow scroll, hold
on a sourced claim. "Wake up to it done."
VO: "And when it runs: one dashboard, one bill. Chat, schedule, tools,
memory, push — one project on DigitalOcean ran the whole night."
SHOW: the DO project, observability, the billing page. Slow push. End card.

## Full narration draft
The VO lines above are the draft. After picture lock: tighten to picture
(~2.5 words per second of shot), generate voiceover, lay under.

## Capture checklist
- [ ] Act 1: phone + six needs appearing (real time)
- [ ] Act 2: architecture diagram (static asset)
- [ ] Act 3: DO stack diagram + multi-vendor diagram (static assets)
- [ ] Act 4: build timelapse (repo to deployed app)
- [ ] Act 5a: night assign + schedule confirm (real time, phone frame)
- [ ] Act 5b: overnight job log (timelapse)
- [ ] Act 5c: push + briefing scroll (real time, phone frame)
- [ ] Act 5d: project + observability + billing (real time)
- [ ] Voiceover generated and laid under (after picture lock)

## Static assets needed (no filming)
- Architecture diagram (six needs)
- DO single-stack diagram (six services, one project)
- Multi-vendor diagram (five vendors x account/access/logs/bill)

## Timelapse recipe
`./video/timelapse.sh in.mp4 out.mp4` (8x). No audio under timelapse;
narration is laid over in assembly.
