# Sidekick — video screenplay

## Logline
Tell it at night. Wake up to it done. A pocket agent that researches overnight
and briefs you by morning — on one stack. No camera, no hands: all screen
capture. No montage.

## Format
- Target runtime: ~3–4 minutes. Voiceover generated after picture lock.
- Narration rule: VO first (say what we are doing and how), then the shot
  (do and show). Never explain over a shot of something else.
- Capture: scripted takes (Playwright, golden path from docs/demo-script.md).
  Bad take = re-run. Timelapse (6–10x) for the overnight run; real time for
  the schedule confirmation, the push arriving, and the briefing.

## Act 1 — The test (0:00–0:40)
VO: "The real test of a personal agent is not chatting. It is what it does
while you are not looking."
SHOW: phone on a nightstand, clock at 11pm. Open Sidekick, chat view.
VO: "It is 11pm. By 7am, research [topic] — five minutes, no fluff."
SHOW: the prompt is sent. The agent replies: "Scheduled for 7:00 AM. I will
research overnight and push the briefing to your phone."
VO: "One schedule. One stack. Good night."
SHOW: the scheduled job, listed on screen. Phone goes dark.

## Act 2 — Overnight (0:40–1:40)
VO: "While you sleep, it works."
SHOW: timelapse — the job runs: searches issued, sources fetched, briefing
synthesized, saved. Keep it abstract: a job log scrolling, not code.
VO: "Search, read, synthesize — tools from the platform, models on tap,
everything saved to its memory."
SHOW: the briefing lands in the database; push notification fires.

## Act 3 — Morning (1:40–3:00)
VO: "7am."
SHOW: real time — the phone buzzes. Push notification: "Your briefing is
ready." Tap it. Sidekick opens to the briefing: the research, five minutes,
sources linked.
VO: "Wake up to it done."
SHOW: slow scroll through the briefing. Hold on a sourced claim.

## Act 4 — One stack (3:00–3:40)
VO: "Chat, schedule, tools, memory, push, one bill. One project on
DigitalOcean ran the whole night."
SHOW: the DO project — app, database, jobs — then the billing page. Slow
push. End card: repo + blog.

## Full narration draft
The VO lines above are the draft. After picture lock: tighten to picture,
generate voiceover, lay under.

## Capture checklist
- [ ] Night chat: prompt sent, schedule confirmed (real time, phone frame)
- [ ] Scheduled job listed on screen (real time)
- [ ] Overnight run timelapse (job log scrolling)
- [ ] Push notification arriving (real time, phone frame)
- [ ] Briefing view scroll (real time, phone frame)
- [ ] DO project + billing page (real time)
- [ ] Voiceover generated and laid under (after picture lock)

## Timelapse recipe (ffmpeg)
`ffmpeg -i in.mp4 -vf "setpts=0.125*PTS" -r 30 -an out.mp4` (8x).
No audio under timelapse; narration is laid over in assembly.
