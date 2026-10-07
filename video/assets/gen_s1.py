#!/usr/bin/env python3
"""S1: six universal needs appearing one by one on a phone mock."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "s1-frames")
os.makedirs(OUT, exist_ok=True)

W, H = 390, 844
BG = (11, 22, 40); CARD = (19, 34, 56); INK = (242, 245, 249)
DIM = (147, 163, 184); ACCENT = (255, 107, 74); LINE = (30, 47, 71)

NEEDS = [
    ("1", "Meet the user", "wherever they are"),
    ("2", "Understand", "what they're asking"),
    ("3", "Get work done", "with real tools"),
    ("4", "Remember", "across sessions"),
    ("5", "Keep working", "while they sleep"),
    ("6", "Run reliably", "one stack, one bill"),
]

def font(size, bold=False):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, size)

def frame(n_visible):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((W//2 - 105, 60), "Every assistant needs six things", font=font(15, True), fill=INK)
    y = 120
    for i, (num, title, sub) in enumerate(NEEDS):
        if i >= n_visible: break
        d.rounded_rectangle([16, y, W - 16, y + 84], radius=12, fill=CARD)
        d.ellipse([32, y + 22, 68, y + 58], fill=ACCENT)
        d.text((41, y + 28), num, font=font(16, True), fill=(255, 255, 255))
        d.text((80, y + 20), title, font=font(15, True), fill=INK)
        d.text((80, y + 44), sub, font=font(12), fill=DIM)
        y += 96
    # footer
    d.text((W//2 - 95, H - 60), "Sidekick meets all six.", font=font(13), fill=DIM)
    return img

frame(0).save(f"{OUT}/s1-00-title.png")
for i in range(1, 7):
    frame(i).save(f"{OUT}/s1-0{i}-needs.png")
print("s1 frames written")
