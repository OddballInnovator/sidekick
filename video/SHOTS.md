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
| S1 | Phone + six needs appearing (Act 1) | real time | done | takes/s1-needs.mp4 (mock) |
| S2 | Architecture diagram (Act 2) | static asset | done | takes/s2-arch.mp4 |
| S3 | DO stack diagram + multi-vendor diagram (Act 3) | static assets | done | takes/s3-compare.mp4 |
| S4 | Build timelapse, repo to deployed app (Act 4) | timelapse 8x | done | takes/s4-build.mp4 (mock) |
| S5 | Night assign + schedule confirm (Act 5) | real time, phone frame | done | takes/s5-chat.mp4 (mock of working chat) |
| S6 | Overnight job log (Act 5) | timelapse 8x | done | takes/s6-joblog.mp4 (visualization) |
| S7 | Push + briefing scroll, hold on sourced claim (Act 5) | real time, phone frame | done | takes/s7-briefing.mp4 (mock, real content) |
| S8 | Project + observability + billing (Act 5) | real time | pending | needs DO console login |
| S9 | Voiceover laid under picture lock | post | done | sidekick-film.mp4 (2m08s draft) |

**Note (2026-10-07):** S1/S4/S5/S6/S7 are high-fidelity mocks (PIL) built from the real app's design tokens and real researched content. The chat scheduling they depict WORKS on the live app. **Update 2026-10-07 ~04:30 PDT:** The full pipeline now works end-to-end (Exa search → llama synthesis → Postgres). The mocks remain as visualizations; replace with real captures when convenient. S8 (console) still needs a logged-in session.

## Files
- `takes/` — raw captures, named `<ID>-take<N>.mp4` (not committed; too big —
  keep local or in Spaces).
- `assets/` — the three static diagrams (architecture, DO stack, multi-vendor).
- `timelapse.sh` — the 8x recipe.
- Narration draft lives in `docs/SCREENPLAY.md`; VO is generated after picture lock.
