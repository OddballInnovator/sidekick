# video/ — the demo, captured in parallel with the build

The video is not a phase at the end. Every build milestone produces its shot
before we move on. Scripted takes only (Playwright, golden path from
`docs/demo-script.md`). Bad take = re-run the script, never the messy real build.

## How a shot gets made
1. The feature works via the golden path.
2. Record the scripted take (see shot list for framing: timelapse vs real time).
3. Log it below with the take filename. Check it off.
4. Move to the next milestone.

## Shot log (mirrors the screenplay's five acts)
| ID | Shot | Framing | Status | Take |
|----|------|---------|--------|------|
| S1 | Phone + six needs appearing (Act 1) | real time | pending | |
| S2 | Architecture diagram (Act 2) | static asset | pending | |
| S3 | DO stack diagram + multi-vendor diagram (Act 3) | static assets | pending | |
| S4 | Build timelapse, repo to deployed app (Act 4) | timelapse 8x | pending | |
| S5 | Night assign + schedule confirm (Act 5) | real time, phone frame | pending | |
| S6 | Overnight job log (Act 5) | timelapse 8x | pending | |
| S7 | Push + briefing scroll, hold on sourced claim (Act 5) | real time, phone frame | pending | |
| S8 | Project + observability + billing (Act 5) | real time | pending | |
| S9 | Voiceover laid under picture lock | post | pending | |

## Files
- `takes/` — raw captures, named `<ID>-take<N>.mp4` (not committed; too big —
  keep local or in Spaces).
- `assets/` — the three static diagrams (architecture, DO stack, multi-vendor).
- `timelapse.sh` — the 8x recipe.
- Narration draft lives in `docs/SCREENPLAY.md`; VO is generated after picture lock.
