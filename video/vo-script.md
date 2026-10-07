# Sidekick — voiceover script

Narration for the screen-only demo. Generate AFTER picture lock, then tighten
each line to its shot (~2.5 spoken words per second). One narrator track.
Warm, plainspoken, confident — no hype, no jargon.

Rules baked in:
- DigitalOcean gets the credit; the builder is never mentioned.
- Only what the system demonstrably does (verified against
  `backend/app/`: chat → schedule → gateway search/fetch → inference
  synthesis → Postgres save → VAPID web push → briefing view).
- Multi-vendor pain named concretely; single stack argued across building,
  operating, costing. No gaps discussion.
- VO says what is being done and how, THEN the shot shows it.

Total: **338 words ≈ 2 min 15 sec** of narration (target video ~5 min;
the rest is real-time shots and timelapses).

---

## Act 1 — What Sidekick is (S1)

**Shot S1:** phone frame, chat view, real time. The ask is typed; then the
six needs appear one by one.

> This is Sidekick. A pocket agent you brief at night — it researches while
> you sleep, and your morning briefing is waiting when you wake up.

*(25 words ≈ 10 sec — over the phone/chat view as the ask is typed)*

> It is one small app. But nearly every modern AI app needs the same six
> things.

*(16 words ≈ 6 sec — beat, then the six needs start appearing)*

> Meet the user. Understand. Get work done. Remember. Keep working.
> Run reliably.

*(12 words ≈ 5 sec — one need per beat as each appears)*

**Act 1 total: 53 words ≈ 21 sec**

---

## Act 2 — The architecture (S2)

**Shot S2:** static architecture diagram — the six needs as system pieces.

> Those six needs are an architecture. An interface to meet the user.
> Models to understand. Tools with permissions to get work done. Memory to
> remember. Schedules that keep working through the night. And one place
> to watch it all run reliably.

*(41 words ≈ 16 sec — diagram holds; let each clause land on its piece)*

**Act 2 total: 41 words ≈ 16 sec**

---

## Act 3 — Two ways to build it (S3)

**Shot S3a:** static DO single-stack diagram — six services, one frame.

> On DigitalOcean, that architecture is one stack. App Platform runs the
> app. Serverless Inference does the thinking. The Action Gateway hands it
> tools. Postgres remembers. Valkey keeps the hot state. One project, one
> dashboard, one bill.

*(36 words ≈ 14 sec)*

**Shot S3b:** static multi-vendor diagram beside it — five vendor cards,
each repeating account / access / logs / bill. No montage.

> The other way to build it is five vendors. Five accounts, five access
> models, five log dashboards, five bills. Twenty things to manage before
> the app does anything useful.

*(29 words ≈ 12 sec)*

**Bridge to Act 4** (diagrams hold, then cut to timelapse):

> So we built it the first way. Watch.

*(8 words ≈ 3 sec)*

**Act 3 total: 73 words ≈ 29 sec**

---

## Act 4 — Build (S4)

**Shot S4:** timelapse 8x, silent — repo to deployed app: the service, the
database, the cache, all in one project.

> One project. The app, the database, the cache — provisioned together,
> deployed together.

*(12 words ≈ 5 sec — over the opening of the timelapse)*

> No glue code between vendors. No separate accounts to wire up. It just
> builds.

*(14 words ≈ 6 sec — mid-timelapse)*

**Act 4 total: 26 words ≈ 10 sec**

---

## Act 5 — Run it (S5–S8)

### Night — assign (S5)

**Shot S5:** phone frame, real time. The prompt is sent; the agent confirms
the 7am schedule; the job appears in the schedule list; phone goes dark.

> It is 11pm. Time to brief your Sidekick.

*(8 words ≈ 3 sec)*

> By 7am, research the biggest AI infrastructure announcements this week.
> Five minutes, no fluff.

*(14 words ≈ 6 sec — the prompt is typed/sent as this lands)*

> Scheduled for 7am. It will research overnight and push the briefing to
> your phone.

*(14 words ≈ 6 sec — over the agent's confirmation and the job listing)*

> One schedule. One stack. Good night.

*(6 words ≈ 2 sec — phone goes dark)*

**S5 total: 42 words ≈ 17 sec**

### Overnight — the run (S6)

**Shot S6:** timelapse 8x, silent — the job log scrolls: searches issued,
sources fetched, briefing synthesized, saved, push fired.

> While you sleep, it works. Searching the web. Reading the sources.
> Synthesizing the briefing. Saving it. Then pushing it to your phone.

*(22 words ≈ 9 sec)*

**S6 total: 22 words ≈ 9 sec**

### Morning — the payoff (S7)

**Shot S7:** phone frame, real time. The push arrives, the briefing opens,
slow scroll, hold on a sourced claim.

> 7am.

*(1 word — the phone buzzes)*

> Your briefing is ready.

*(4 words ≈ 2 sec — the notification; tap)*

> Five minutes, sources linked.

*(4 words ≈ 2 sec — the briefing opens; slow scroll)*

> Tell it at night. Wake up to it done.

*(9 words ≈ 4 sec — hold on a sourced claim)*

**S7 total: 18 words ≈ 7 sec**

### One stack (S8)

**Shot S8:** real time — the DigitalOcean project view, then observability,
then the billing page. Slow push.

> And here is the part you never see at night. One project ran the whole
> thing — the chat, the schedule, the tools, the memory, the push.

*(26 words ≈ 10 sec — over the project view)*

> One place to watch it. One bill to pay for it. That is what building,
> operating, and costing look like on a single stack.

*(24 words ≈ 10 sec — observability, then the billing page)*

**S8 total: 50 words ≈ 20 sec**

**Act 5 total: 132 words ≈ 53 sec**

---

## Closing — end card (S9)

**Shot S9:** end card.

> Sidekick — tell it at night, wake up to it done. Built on DigitalOcean.

*(13 words ≈ 5 sec)*

---

## Word count summary

| Act | Shots | Words | ≈ Seconds (@2.5 wps) |
|-----|-------|-------|---------------------|
| Act 1 — What Sidekick is | S1 | 53 | 21 |
| Act 2 — The architecture | S2 | 41 | 16 |
| Act 3 — Two ways to build it | S3 | 73 | 29 |
| Act 4 — Build | S4 | 26 | 10 |
| Act 5 — Run it | S5–S8 | 132 | 53 |
| Closing — end card | S9 | 13 | 5 |
| **Total** | | **338** | **≈ 2 min 15 sec** |

Under the ~4-minute narration budget, leaving ~2.5 min of the ~5-min
runtime for real-time shots and timelapses.

## Production notes

- Generate VO only after picture lock; tighten each line to its shot.
- Timelapses (S4, S6) stay silent in the take; VO is laid over in assembly.
- Real-time shots (S5, S7): VO lands on the action it names — the prompt
  line is spoken as the prompt is sent, "7am" as the phone buzzes.
- If the `sidekick` Inference Router is created before filming, Act 3's
  inference line may gain: "through the router, which picks the best model
  for the money." Until then it stays out — the system demonstrably runs
  on the direct model today.
- "Twenty things to manage" = five vendors × (account, access, logs, bill),
  the deck's shared language — not a new claim.
