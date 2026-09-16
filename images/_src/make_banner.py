#!/usr/bin/env python3
"""Composite the GOODSINFINITE banner: AI background + pixel-perfect text overlay."""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = r"E:\workbuddy\2026-08-18-12-10-21\goodsinfinite\images\_src\Abstract_minimalist_ultra_wide_2026-09-14T04-25-48.png"
OUT = r"E:\workbuddy\2026-08-18-12-10-21\goodsinfinite\images"
FONT_B = r"C:\Windows\Fonts\arialbd.ttf"   # bold
FONT_R = r"C:\Windows\Fonts\arial.ttf"     # regular

W, H = 3200, 1000  # 2x retina

# ---- load + cover-crop background ----
bg = Image.open(SRC).convert("RGB")
sw, sh = bg.size
scale = max(W / sw, H / sh)
bg = bg.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width + W) // 2, (bg.height + H) // 2))

# ---- left-strong dark gradient overlay (legibility, like hero::after) ----
overlay = Image.new("RGBA", (W, H), (7, 22, 44, 0))
alpha = Image.new("L", (W, 1))
row = [int(240 * (1 - x / W) + 70 * (x / W)) for x in range(W)]
alpha.putdata(row)
overlay.putalpha(alpha.resize((W, H)))
canvas = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

d = ImageDraw.Draw(canvas, "RGBA")

# ---- fonts (sized for 2x canvas) ----
def fit_font(text, base, max_w, font_path, step=4):
    f = ImageFont.truetype(font_path, base)
    while d.textlength(text, font=f) > max_w and base > step:
        base -= step
        f = ImageFont.truetype(font_path, base)
    return f, base

PAD = 170
USABLE = W - 2 * PAD

# Line 1 (headline)
L1 = "ENTER CHINA WITHOUT UNNECESSARY COMPLEXITY"
f1, s1 = fit_font(L1, 116, USABLE, FONT_B)
# Line 2 (subline)
L2 = "China Market Entry · 1210 Bonded Import · Customs · E-commerce · Fulfillment"
f2, s2 = fit_font(L2, 50, USABLE, FONT_R)

WHITE = (255, 255, 255, 255)
LIGHT = (210, 226, 255, 255)   # soft light blue
MUTE  = (176, 192, 220, 255)   # muted for credit

# vertical group, centered slightly above middle
y1 = int(H * 0.40) - s1
y2 = y1 + s1 + 26
# accent bar to the left of the headline
bar_w, bar_h = 12, int(s1 * 0.92)
bar_x, bar_y = PAD, y1 + 6
d.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(27, 138, 90, 255))  # brand green
tx = PAD + bar_w + 34

d.text((tx, y1), L1, font=f1, fill=WHITE)
d.text((tx, y2), L2, font=f2, fill=LIGHT)

# bottom-right credit (also covers the source watermark)
CREDIT = "Bing Wei  |  GOODSINFINITE"
fc = ImageFont.truetype(FONT_R, 30)
cw = d.textlength(CREDIT, font=fc)
d.text((W - PAD - cw, H - PAD - 38), CREDIT, font=fc, fill=MUTE)

# ---- save hi-res + web version ----
hi = os.path.join(OUT, "banner-enter-china@2x.png")
web = os.path.join(OUT, "banner-enter-china.png")
canvas.save(hi, "PNG")
canvas.resize((1600, 500), Image.LANCZOS).save(web, "PNG")
print("saved:", hi, web)
print("headline size:", s1, "subline size:", s2)
