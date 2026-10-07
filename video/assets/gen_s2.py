#!/usr/bin/env python3
"""Generate s2-architecture.png — Sidekick system architecture (1920x1080)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BG = (11, 18, 32)          # deep navy
PANEL = (17, 26, 43)       # slightly lighter navy
PANEL_LINE = (38, 54, 82)
DO_BLUE = (0, 128, 255)
DO_BLUE_DIM = (0, 128, 255)
TXT = (255, 255, 255)
SUB = (154, 167, 189)
MUT = (107, 122, 147)
AMBER = (255, 176, 32)
GREEN = (52, 199, 123)
TAG_BG = (16, 42, 78)
TAG_TX = (120, 190, 255)
BUBBLE = (24, 36, 58)

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

def tag(x, y, s):
    """Need pill tag at (x, y). Returns width."""
    font = f(17, bold=True)
    bb = d.textbbox((0, 0), s, font=font)
    w = bb[2] - bb[0] + 28
    rrect([x, y, x + w, y + 34], 17, fill=TAG_BG)
    d.text((x + 14, y + 5), s, font=font, fill=TAG_TX)
    return w

def arrow(x1, y1, x2, y2, color=(90, 106, 138), w=3, label=None):
    d.line([x1, y1, x2, y2], fill=color, width=w)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    s = 12
    pts = [(x2, y2),
           (x2 - s * math.cos(ang - 0.42), y2 - s * math.sin(ang - 0.42)),
           (x2 - s * math.cos(ang + 0.42), y2 - s * math.sin(ang + 0.42))]
    d.polygon(pts, fill=color)
    if label:
        ctext((x1 + x2) / 2, (y1 + y2) / 2 - 34, label, f(17), MUT)

# ---------- title ----------
ltext(80, 44, "Sidekick \u2014 the architecture", f(44, bold=True))
ltext(80, 104, "Six needs. One system. Night to morning.", f(22), SUB)

# ---------- DigitalOcean boundary ----------
rrect([60, 165, 1860, 995], 24, fill=(13, 21, 38), outline=DO_BLUE, width=2)
ltext(92, 182, "DigitalOcean", f(21, bold=True), DO_BLUE)

# ---------- Row 1: night -> platform -> morning ----------
RY1, RY2 = 265, 520  # row 1 box top/bottom
# night phone
rrect([110, RY1, 570, RY2], 18, fill=PANEL, outline=PANEL_LINE, width=1)
ltext(140, RY1 + 18, "11 PM", f(20, bold=True), AMBER)
ltext(140, RY1 + 50, "Mobile web client", f(24, bold=True))
# chat bubble
rrect([140, RY1 + 96, 540, RY1 + 196], 12, fill=BUBBLE)
ltext(158, RY1 + 108, "\u201cBy 7am, research the biggest AI", f(18))
ltext(158, RY1 + 134, "infrastructure announcements this", f(18))
ltext(158, RY1 + 160, "week. Five minutes, no fluff.\u201d", f(18))
tag(140, RY2 - 52, "1 \u00b7 Meet the user")

arrow(570, (RY1 + RY2) / 2, 690, (RY1 + RY2) / 2)

# app platform
rrect([690, RY1, 1230, RY2], 18, fill=PANEL, outline=PANEL_LINE, width=1)
ltext(720, RY1 + 18, "App Platform", f(24, bold=True))
ltext(720, RY1 + 58, "FastAPI API + web client", f(19), SUB)
ltext(720, RY1 + 92, "Scheduler runs the night job", f(19), SUB)
ltext(720, RY1 + 126, "Serves the morning briefing", f(19), SUB)
tag(720, RY2 - 52, "5 \u00b7 Keep working")

arrow(1230, (RY1 + RY2) / 2, 1350, (RY1 + RY2) / 2, label="Web Push \u00b7 VAPID")

# morning phone
rrect([1350, RY1, 1810, RY2], 18, fill=PANEL, outline=PANEL_LINE, width=1)
ltext(1380, RY1 + 18, "7 AM", f(20, bold=True), AMBER)
ltext(1380, RY1 + 50, "Morning briefing", f(24, bold=True))
rrect([1380, RY1 + 96, 1780, RY1 + 150], 12, fill=BUBBLE)
ltext(1398, RY1 + 108, "Sidekick \u2014 your briefing is ready", f(18))
ltext(1380, RY1 + 162, "Briefing with sources", f(19), SUB)
tag(1380, RY2 - 52, "1 \u00b7 Meet the user")

# ---------- Row 2: capabilities + state ----------
CY1, CY2 = 610, 850
# bus line from App Platform down
d.line([300, 565, 1620, 565], fill=(90, 106, 138), width=3)
d.line([960, 520, 960, 565], fill=(90, 106, 138), width=3)
for cx in (300, 740, 1180, 1620):
    d.line([cx, 565, cx, CY1], fill=(90, 106, 138), width=3)

boxes = [
    (110, 490, "Inference Router", ["\u2192 Serverless Inference", "synthesis \u00b7 best model per dollar"], "2 \u00b7 Understand"),
    (550, 930, "Action Gateway", ["Exa \u00b7 web_search \u00b7 web_fetch", "tools with permissions"], "3 \u00b7 Get work done"),
    (990, 1370, "Managed Postgres", ["jobs \u00b7 messages \u00b7 subscriptions", "briefings"], "4 \u00b7 Remember"),
    (1430, 1810, "Managed Valkey", ["briefing cache \u00b7 hot state", "fast reads"], "4 \u00b7 Remember"),
]
for x1, x2, title, lines, need in boxes:
    rrect([x1, CY1, x2, CY2], 18, fill=PANEL, outline=PANEL_LINE, width=1)
    ltext(x1 + 30, CY1 + 22, title, f(23, bold=True))
    yy = CY1 + 62
    for ln in lines:
        ltext(x1 + 30, yy, ln, f(18), SUB)
        yy += 32
    tag(x1 + 30, CY2 - 52, need)

# ---------- footer: run reliably ----------
ctext(960, 906, "6 \u00b7 Run reliably \u2014 one project \u00b7 one dashboard \u00b7 one bill", f(21, bold=True), SUB)

img.save("/home/hatch/workspace/sidekick/video/assets/s2-architecture.png")
print("saved s2-architecture.png", img.size)
