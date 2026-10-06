# demo-script.md — the golden path (do not improvise on camera)

Run with DEMO_MODE=1. Every line below is a shot. If a step fails, fix the
code, not the script.

## Hero take: restaurant booking (phone frame, real time)
1. Prompt: "Get me a table for two Friday night, somewhere good near downtown."
2. Expect: three options, best pick starred, each with rating/distance/price.
3. Approval card appears: "Book 7:30 at [pick]?" [Approve] [Not now].
4. Tap Approve. Expect: confirmation with reference within 5s.

## Flight watch (real time)
1. Prompt: "Watch SFO to Tokyo, grab it under $300."
2. Trigger briefing seam (no waiting for the schedule).
3. Expect: "Booked at $274." with itinerary.

## Memory beat (real time)
1. Prompt: "What do you remember about me?"
2. Expect: dietary, airline, seat, home airport recited.

## Model swap (real time)
1. In playground: same prompt, swap model, show same key working.
