# video/ — the demo, captured in parallel with the build

The video is not a phase at the end. Every build milestone produces its shot
before we move on. Scripted takes only (Playwright, golden path from
`docs/demo-script.md`). Bad take = re-run the script, never the messy real build.

## How a shot gets made
1. The feature works via the golden path.
2. Record the scripted take (see SHOTS.md for framing: timelapse vs real time).
3. Log it below with the take filename. Check it off.
4. Move to the next milestone.

## Shot log
| ID | Shot | Framing | Status | Take |
|----|------|---------|--------|------|
| S1 | Night chat: prompt sent, schedule confirmed | real time, phone frame | pending | |
| S2 | Scheduled job listed on screen | real time | pending | |
| S3 | Overnight run (job log scrolling) | timelapse 8x | pending | |
| S4 | Push notification arriving, tap it | real time, phone frame | pending | |
| S5 | Briefing view scroll, hold on a sourced claim | real time, phone frame | pending | |
| S6 | DO project (app + db + jobs) then billing page | real time | pending | |
| S7 | Voiceover laid under picture lock | post | pending | |

## Files
- `takes/` — raw captures, named `<ID>-take<N>.mp4` (not committed; too big —
  keep local or in Spaces).
- `timelapse.sh` — the 8x recipe.
- Narration draft lives in `docs/SCREENPLAY.md`; VO is generated after picture lock.
