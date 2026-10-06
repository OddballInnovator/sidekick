# Sidekick — video screenplay

## Logline
One developer builds a pocket AI chief of staff that books dinners and watches
flights — entirely on DigitalOcean. No camera, no hands: all screen capture.

## Format
- Target runtime: ~5 minutes. Voiceover recorded after picture lock.
- Capture method: scripted takes (Playwright, golden path from docs/demo-script.md),
  never the messy real build. Bad take = re-run the script.
- Timelapse (6–10x, slight ramp) for: terminal sessions, code, deploys.
- Real time for: first answer streaming, approval gate firing, briefing arriving.

## Act 1 — The problem (0:00–0:45)
Montage, fast cuts: five signup screens, five API-key pages, five billing tabs.
On-screen text: "5 vendors x 4 surfaces = 20 things to manage."
Narration: "This is what it takes to give an AI app a body. Five vendors,
five accounts, five bills — before it does anything useful."
Shot list: screen-record each console's keys/billing page (10–15s each),
cut to the deck's 5x4 matrix.

## Act 2 — The build (0:45–2:30)
Timelapse: repo → App Platform deploy → one API key → inference playground
answering. Beat per phase, each under 20s:
- "One project." (project creation, real time)
- "One key, every model." (model swap in playground, real time)
- "Tools came with the platform." (gateway tool list scroll, timelapse)
Narration keeps the six needs as chapter titles.

## Act 3 — The agent acts (2:30–4:15)
The hero sequence, all real time, phone-frame viewport:
1. "Get me a table for two Friday night, somewhere good near downtown."
   Agent searches (Geoapify + web), returns three options with the pick starred.
2. The approval gate fires: "Book 7:30 at [place]?" [Approve] [Not now].
   Tap Approve. Confirmation arrives.
3. "Watch this flight, grab it under $300." Cut to: briefing arrives
   unprompted — "Booked at $274."
4. "What did I ask you to remember?" — it recites preferences. Memory beat.
Narration: minimal. Let the taps and the confirmations carry it.

## Act 4 — The money shot (4:15–5:00)
Split screen: five vendor dashboards vs one DigitalOcean billing +
observability page. Slow push on the single page.
Closing line: "One stack. The agent just works."
End card: repo + blog links.

## Capture checklist (check off as footage lands)
- [ ] 20-surfaces montage clips
- [ ] Project creation (real time)
- [ ] Model swap in playground (real time)
- [ ] Gateway tool list (timelapse)
- [ ] Restaurant flow hero take (real time, phone frame)
- [ ] Approval tap + confirmation (real time, phone frame)
- [ ] Flight watch → briefing (real time)
- [ ] Memory beat (real time)
- [ ] Billing/observability walkthrough (real time)
- [ ] Voiceover draft per act (generate after picture lock)

## Timelapse recipe (ffmpeg)
`ffmpeg -i in.mp4 -vf "setpts=0.125*PTS" -r 30 -an out.mp4` (8x).
Keep audio out of timelapse clips; narration is laid over in assembly.
