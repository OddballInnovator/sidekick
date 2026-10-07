#!/usr/bin/env python3
"""S4: build timelapse — terminal montage from real git history."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "s4-frames")
os.makedirs(OUT, exist_ok=True)
REPO = os.path.join(HERE, "..")

W, H = 1920, 1080
BG = (5, 10, 20); INK = (242, 245, 249); DIM = (147, 163, 184)
ACCENT = (255, 107, 74); GREEN = (80, 200, 120)

def font(size, bold=False):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
    return ImageFont.truetype(p, size)

# real commits, newest last
log = subprocess.run(["git", "-C", REPO, "log", "--reverse", "--format=%s", "-12"],
                     capture_output=True, text=True).stdout.strip().split("\n")
files = subprocess.run(["git", "-C", REPO, "ls-files", "backend", "web", "infra"],
                       capture_output=True, text=True).stdout.strip().split("\n")

def frame(lines_shown, files_shown):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((60, 40), "sidekick \u2014 build log", font=font(28, True), fill=INK)
    y = 110
    f = font(20)
    for i, msg in enumerate(log[:lines_shown]):
        if y > H - 120: break
        d.text((60, y), "$ git commit", font=f, fill=DIM)
        y += 30
        # wrap commit msg
        words, line, cur = msg.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) < W - 160: cur = t
            else: line.append(cur); cur = w
        if cur: line.append(cur)
        for ln in line[:2]:
            d.text((80, y), ln[:80], font=f, fill=GREEN); y += 28
        y += 12
    # file tree footer
    d.text((60, H - 80), f"{files_shown} files \u00b7 backend + web + infra \u00b7 deploying to App Platform",
           font=font(18), fill=ACCENT)
    return img

n = len(log)
for i in range(n + 1):
    frame(i, int(len(files) * i / max(n, 1))).save(f"{OUT}/s4-{i:02d}.png")
print(f"s4 frames: {n + 1}")
