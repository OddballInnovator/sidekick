#!/usr/bin/env python3
"""S6: overnight job log mock. S9: end card."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
OUT6 = os.path.join(HERE, "s6-frames")
os.makedirs(OUT6, exist_ok=True)

W, H = 1920, 1080
BG = (5, 10, 20); INK = (242, 245, 249); DIM = (147, 163, 184)
ACCENT = (255, 107, 74); GREEN = (80, 200, 120); BLUE = (100, 160, 255)

def font(size, bold=False):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
    return ImageFont.truetype(p, size)

LOG = [
    ("02:00:03", "scheduler", "job fired: overnight-research", DIM),
    ("02:00:04", "gateway", "exa_web_search: 5 results", BLUE),
    ("02:00:11", "gateway", "exa_web_fetch: reuters.com ... ok", BLUE),
    ("02:00:14", "gateway", "exa_web_fetch: futurumgroup.com ... ok", BLUE),
    ("02:00:18", "gateway", "exa_web_fetch: techstartups.com ... ok", BLUE),
    ("02:00:22", "inference", "synthesizing briefing (openai-gpt-5-mini)", BLUE),
    ("02:00:41", "inference", "briefing ready: 6 sections, 5 sources", GREEN),
    ("02:00:42", "postgres", "saved briefing id=1", DIM),
    ("02:00:42", "valkey", "cache warmed", DIM),
    ("02:00:43", "push", "web push queued: 1 subscriber", GREEN),
    ("07:00:00", "push", "delivered: briefing ready", GREEN),
]

def frame(n_lines):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((60, 40), "sidekick \u2014 overnight job log", font=font(28, True), fill=INK)
    d.text((60, 80), "App Platform \u00b7 api \u00b7 runtime logs", font=font(18), fill=DIM)
    y = 140
    f = font(20)
    for ts, svc, msg, col in LOG[:n_lines]:
        if y > H - 60: break
        d.text((60, y), ts, font=f, fill=DIM)
        d.text((200, y), f"[{svc}]", font=f, fill=col)
        d.text((380, y), msg[:70], font=f, fill=INK)
        y += 36
    return img

for i in range(len(LOG) + 1):
    frame(i).save(f"{OUT6}/s6-{i:02d}.png")
print(f"s6: {len(LOG) + 1} frames")

# end card
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.text((W//2 - 130, H//2 - 80), "Sidekick", font=font(64, True), fill=INK)
d.text((W//2 - 210, H//2), "tell it at night \u00b7 wake up to it done", font=font(28), fill=DIM)
d.text((W//2 - 160, H//2 + 60), "built on DigitalOcean", font=font(24), fill=ACCENT)
img.save(os.path.join(HERE, "endcard.png"))
print("endcard written")
