# demo-script.md — the golden path (do not improvise on camera)

Every step is a shot. VO says what we are doing and how, then the screen does
and shows it. If a step fails, fix the code, not the script.

Filmed topic: the biggest AI infrastructure announcements this week.
(Topic is the user's pick; this is the locked take. Live search preferred —
fresh results prove it is real. DEMO_MODE=1 only if search misbehaves.)

## Night — assign (phone frame, real time)
VO: "It is 11pm. By 7am, research the biggest AI infrastructure announcements
this week — five minutes, no fluff."
1. Prompt: "By 7am, research the biggest AI infrastructure announcements this
   week. Five minutes, no fluff."
2. Expect: "Scheduled for 7:00 AM. I will research overnight and push the
   briefing to your phone."
VO: "One schedule. One stack. Good night."
3. Expect: the job visible in the schedule list. Phone goes dark.

## Overnight — the run (timelapse)
VO: "While you sleep, it works."
1. Trigger: POST /jobs/trigger (the "morning" seam).
2. Expect: searches issued → sources fetched → briefing synthesized → saved;
   push notification fires.

## Morning — the payoff (phone frame, real time)
VO: "7am."
1. Expect: push notification "Your briefing is ready." Tap it.
2. Expect: briefing view — the research, five minutes, sources linked.
VO: "Wake up to it done."
3. Slow scroll through the briefing. Hold on one sourced claim.

## One stack (real time)
VO: "Chat, schedule, tools, memory, push, one bill. One project on
DigitalOcean ran the whole night."
1. Show the DO project (app + database + jobs), then the billing page.
