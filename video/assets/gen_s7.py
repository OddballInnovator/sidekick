#!/usr/bin/env python3
"""Render S7 briefing-view mock frames (PIL), matching the real Sidekick UI."""
import os, re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "s7-frames")
os.makedirs(OUT, exist_ok=True)

W, H = 390, 844
BG = (11, 22, 40); CARD = (19, 34, 56); INK = (242, 245, 249)
DIM = (147, 163, 184); ACCENT = (255, 107, 74); LINE = (30, 47, 71)

def font(size, bold=False):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, size)

def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def header(d):
    d.rectangle([0, 0, W, 64], fill=BG); d.line([0, 64, W, 64], fill=LINE)
    d.text((16, 14), "Sidekick", font=font(17, True), fill=INK)
    d.text((16, 36), "tell it at night \u00b7 wake up to it done", font=font(11), fill=DIM)
    d.ellipse([W - 44, 18, W - 20, 42], outline=DIM, width=2)
    d.text((W - 37, 21), "!", font=font(14, True), fill=DIM)
    # tabs
    d.rectangle([0, 64, W, 104], fill=BG); d.line([0, 104, W, 104], fill=LINE)
    d.text((40, 76), "Chat", font=font(14), fill=DIM)
    d.text((W - 140, 76), "Briefings", font=font(14, True), fill=ACCENT)

# --- briefing body blocks: (kind, text) ---
BLOCKS = [
    ("h1", "AI Infrastructure This Week"),
    ("sub", "Your five-minute briefing \u00b7 October 7, 2026"),
    ("h2", "Power is the new compute"),
    ("p", "Black Hills Corp will spend $1.8 billion (2027\u20132029) on 564 MW of new generation to power a proposed Google data center in Cheyenne, Wyoming. Google covers the full cost so it doesn't hit other ratepayers. Separately, Google signed a 3.59 GW contract with Constellation Energy."),
    ("src", "Reuters, Oct 6"),
    ("h2", "CoreWeave's big swing: Forge"),
    ("p", "At Fully Connected (5,500 attendees), CoreWeave launched Forge \u2014 unifying Weights & Biases, OpenPipe, marimo notebooks, serverless RL, and evals. Also: first production NVIDIA Vera Rubin NVL72 workloads (4.8x inference throughput vs GB200)."),
    ("src", "Futurum Group, Oct 6"),
    ("h2", "$20B for Rubin GPUs in Asia"),
    ("p", "AM Intelligence committed $20 billion and 20,000 Nvidia Vera Rubin GPUs across India and Malaysia. Foxconn posted a 47% revenue jump on AI server demand. The buildout is accelerating."),
    ("src", "AI News Brief \u00b7 TechStartups"),
    ("h2", "Bottom line"),
    ("p", "This week wasn't about models \u2014 it was about electrons and concrete. If you're planning AI capacity, the constraint to watch is grid interconnection, not GPU supply."),
]

def render_blocks(d, y0, y1, blocks):
    y = y0
    min_y = 132  # don't draw over the header
    for kind, text in blocks:
        if y > y1 - 20: break
        if kind == "h1":
            f = font(20, True)
            for ln in wrap(d, text, f, W - 48):
                if y > y1 - 20: break
                if y >= min_y - 20: d.text((24, max(y, min_y)), ln, font=f, fill=INK)
                y += 28
            y += 4
        elif kind == "sub":
            f = font(12)
            if y >= min_y: d.text((24, y), text, font=f, fill=DIM)
            y += 22
        elif kind == "h2":
            f = font(15, True)
            y += 6
            for ln in wrap(d, text, f, W - 48):
                if y > y1 - 20: break
                if y >= min_y: d.text((24, y), ln, font=f, fill=ACCENT)
                y += 22
            y += 2
        elif kind == "p":
            f = font(13)
            for ln in wrap(d, text, f, W - 48):
                if y > y1 - 20: break
                if y >= min_y: d.text((24, y), ln, font=f, fill=INK)
                y += 19
            y += 4
        elif kind == "src":
            f = font(11)
            if y >= min_y: d.text((24, y), "\u2014 " + text, font=f, fill=DIM)
            y += 20
    return y

def frame_briefing_list():
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    header(d)
    y = 124
    d.rounded_rectangle([12, y, W - 12, y + 86], radius=12, fill=CARD)
    d.text((24, y + 12), "AI infrastructure announcements", font=font(15, True), fill=INK)
    d.text((24, y + 36), "October 7, 2026 \u00b7 7:00 AM", font=font(12), fill=DIM)
    d.text((24, y + 58), "tap to read", font=font(12), fill=ACCENT)
    return img

def frame_briefing_open(scroll=0):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    header(d)
    # card
    d.rounded_rectangle([12, 116, W - 12, H - 12], radius=12, fill=CARD)
    # clip to card for scroll effect (simple: offset blocks)
    y0 = 132 - scroll
    render_blocks(d, y0, H - 28, BLOCKS)
    return img

frame_briefing_list().save(f"{OUT}/s7-00-list.png")
# scroll progression
for i, sc in enumerate([0, 120, 240, 360]):
    frame_briefing_open(sc).save(f"{OUT}/s7-01-open-{i:02d}.png")
print("s7 frames written")
