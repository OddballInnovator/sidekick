#!/usr/bin/env python3
"""Render S5 phone mock frames (PIL) from the real Sidekick design tokens.
Produces a 390x844 phone UI, then assembles a typing+response clip with ffmpeg.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "s5-frames")
os.makedirs(OUT, exist_ok=True)

W, H = 390, 844
BG = (11, 22, 40)
CARD = (19, 34, 56)
INK = (242, 245, 249)
DIM = (147, 163, 184)
ACCENT = (255, 107, 74)
USER_BG = (27, 58, 92)
LINE = (30, 47, 71)

def font(size, bold=False):
    path = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

PROMPT = "By 7am, research the biggest AI infrastructure announcements this week. Five minutes, no fluff."
REPLY = "Scheduled for 7:00 AM. I will research the biggest AI infrastructure announcements this week overnight and push the briefing to your phone."

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def rounded(draw, box, r, fill, outline=None):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline)

def base():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W, 64], fill=BG, outline=LINE)
    d.line([0, 64, W, 64], fill=LINE)
    d.text((16, 14), "Sidekick", font=font(17, True), fill=INK)
    d.text((16, 36), "tell it at night \u00b7 wake up to it done", font=font(11), fill=DIM)
    # bell icon (text glyph, no emoji font)
    d.ellipse([W - 44, 18, W - 20, 42], outline=DIM, width=2)
    d.text((W - 37, 21), "!", font=font(14, True), fill=DIM)
    return img, d

def composer(d, typed=""):
    y = H - 76
    d.rectangle([0, y, W, H], fill=BG)
    d.line([0, y, W, y], fill=LINE)
    # input pill
    rounded(d, [12, y + 12, W - 84, y + 52], 20, CARD, outline=LINE)
    shown = typed if typed else "By 7am, research\u2026"
    col = INK if typed else DIM
    # clip text to pill
    f = font(14)
    while d.textlength(shown, font=f) > W - 120 and len(shown) > 1:
        shown = shown[:-1]
    d.text((26, y + 24), shown, font=f, fill=col)
    # send button
    rounded(d, [W - 72, y + 12, W - 12, y + 52], 20, ACCENT)
    d.text((W - 58, y + 24), "Send", font=font(14, True), fill=(255, 255, 255))
    return y

def msg_bubble(d, y, text, user=False):
    f = font(14)
    lines = wrap(d, text, f, W - 96)
    lh = 20
    h = len(lines) * lh + 20
    x0 = 56 if user else 12
    x1 = W - 12 if user else W - 56
    fill = USER_BG if user else CARD
    rounded(d, [x0, y, x1, y + h], 12, fill)
    ty = y + 10
    for ln in lines:
        d.text((x0 + 12, ty), ln, font=f, fill=INK)
        ty += lh
    return y + h + 10

def job_card(d, y):
    f = font(13)
    lines = wrap(d, "Scheduled \u2014 research runs at 7:00 AM. I\u2019ll push the briefing to your phone.", f, W - 64)
    h = len(lines) * 19 + 20
    rounded(d, [12, y, W - 12, y + h], 12, BG, outline=ACCENT)
    ty = y + 10
    for i, ln in enumerate(lines):
        col = ACCENT if i == 0 else INK
        d.text((24, ty), ln, font=f, fill=col)
        ty += 19
    return y + h + 10

def frame_empty():
    img, d = base()
    f = font(13)
    d.text((W//2 - 90, 300), "No messages yet.", font=f, fill=DIM)
    d.text((W//2 - 130, 324), "Tell it at night. Wake up to it done.", font=f, fill=DIM)
    composer(d)
    return img

def frame_typing(typed):
    img, d = base()
    composer(d, typed)
    return img

def frame_convo():
    img, d = base()
    y = 84
    y = msg_bubble(d, y, PROMPT, user=True)
    y = msg_bubble(d, y, REPLY, user=False)
    job_card(d, y)
    composer(d)
    return img

# --- emit frames ---
frame_empty().save(f"{OUT}/s5-00-empty.png")
# typing progression (24 frames)
n = 24
for i in range(1, n + 1):
    cut = int(len(PROMPT) * i / n)
    frame_typing(PROMPT[:cut]).save(f"{OUT}/s5-01-typing-{i:02d}.png")
frame_convo().save(f"{OUT}/s5-02-sent.png")
print("frames written to", OUT)
