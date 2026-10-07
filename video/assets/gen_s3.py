#!/usr/bin/env python3
"""Generate s3-do-vs-multivendor.png — one stack vs multi-vendor (1920x1080)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BG = (11, 18, 32)
PANEL = (17, 26, 43)
PANEL_LINE = (38, 54, 82)
DO_BLUE = (0, 128, 255)
TXT = (255, 255, 255)
SUB = (154, 167, 189)
MUT = (107, 122, 147)
GREEN = (52, 199, 123)
RED = (229, 72, 77)
RED_DIM = (120, 60, 66)
CHIP = (24, 38, 62)
VTAG = (46, 34, 40)

FD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FDB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(size, bold=False):
    return ImageFont.truetype(FDB if bold else FD, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def rrect(xy, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def ctext(cx, y, s, font, fill=TXT):
    bb = d.textbbox((0, 0), s, font=font)
    d.text((cx - (bb[2] - bb[0]) / 2, y), s, font=font, fill=fill)

def ltext(x, y, s, font, fill=TXT):
    d.text((x, y), s, font=font, fill=fill)

def dashed_vline(x, y1, y2, fill=(90, 96, 112), width=2, dash=10, gap=8):
    y = y1
    while y < y2:
        d.line([x, y, x, min(y + dash, y2)], fill=fill, width=width)
        y += dash + gap

# ---------- title ----------
ltext(80, 44, "Two ways to build it", f(44, bold=True))
ltext(80, 104, "Same architecture. Different stack.", f(22), SUB)
# divider
d.line([960, 150, 960, 990], fill=(38, 54, 82), width=2)

# ================= LEFT: one stack =================
ltext(110, 160, "One stack", f(30, bold=True), DO_BLUE)
rrect([110, 215, 900, 640], 20, fill=(13, 21, 38), outline=DO_BLUE, width=2)
ltext(140, 232, "DigitalOcean", f(20, bold=True), DO_BLUE)

chips = ["App Platform", "Serverless Inference + Router", "Action Gateway",
         "Managed Postgres", "Managed Valkey", "Web Push"]
# 2 rows x 3 cols inside 110..900
cw, chh = 230, 120
xs = [150, 395, 640]
ys = [300, 450]
for i, c in enumerate(chips):
    x, y = xs[i % 3], ys[i // 3]
    rrect([x, y, x + cw, y + chh], 14, fill=CHIP, outline=(52, 72, 104), width=1)
    # wrap text
    if " + " in c:
        a, b = c.split(" + ")
        ctext(x + cw / 2, y + 28, a, f(19, bold=True))
        ctext(x + cw / 2, y + 56, "+ " + b, f(19, bold=True))
    else:
        ctext(x + cw / 2, y + 44, c, f(19, bold=True))

checks = ["one account", "one control plane \u00b7 one observability layer", "one bill"]
yy = 700
for c in checks:
    ltext(140, yy, "\u2713", f(24, bold=True), GREEN)
    ltext(180, yy, c, f(23), TXT)
    yy += 62
ltext(140, yy + 8, "Calm. Everything in one place.", f(20), MUT)

# ================= RIGHT: multi-vendor =================
ltext(1020, 160, "The multi-vendor alternative", f(30, bold=True), RED)
vendors = ["Vendor A \u2014 hosting", "Vendor B \u2014 LLM API", "Vendor C \u2014 search API",
           "Vendor D \u2014 database", "Vendor E \u2014 push service"]
vy = 215
vh = 108
gap = 26
for i, v in enumerate(vendors):
    rrect([1070, vy, 1810, vy + vh], 14, fill=(26, 22, 26), outline=(72, 60, 64), width=1)
    ltext(1100, vy + 16, v, f(21, bold=True))
    ltext(1100, vy + 52, "account  \u00b7  dashboard  \u00b7  logs  \u00b7  bill", f(17), MUT)
    # small "silo" marker on the right
    ltext(1690, vy + 52, "silo", f(17), RED_DIM)
    vy += vh + gap

# dashed broken connectors between vendor boxes to stress fragmentation
yy = 215 + vh
for _ in range(4):
    dashed_vline(1440, yy + 4, yy + gap - 4, fill=(110, 70, 74))
    ctext(1440, yy + 2, "\u00d7", f(20, bold=True), RED)
    yy += vh + gap

crosses = ["five accounts \u00b7 five access models", "five dashboards \u00b7 five log silos",
           "five bills \u00b7 no shared observability"]
yy = 215 + 5 * (vh + gap) + 6
for c in crosses:
    ltext(1100, yy, "\u00d7", f(24, bold=True), RED)
    ltext(1140, yy, c, f(23), TXT)
    yy += 56

img.save("/home/hatch/workspace/sidekick/video/assets/s3-do-vs-multivendor.png")
print("saved s3-do-vs-multivendor.png", img.size)
