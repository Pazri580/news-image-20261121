#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page.

A single 1024x1024 RGB newspaper front page, "THE WORLD IN ONE PAGE",
with five stories first reported on Saturday 21 November 2026 and a
ticker of shorter items from the same day. Everything is drawn with
Pillow shapes and DejaVu fonts; no photos, logos or outside assets.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (248, 244, 233)
INK = (25, 25, 25)
PANEL = (255, 255, 255)
GREY = (90, 90, 90)
RULE = (25, 25, 25)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines; return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.35)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, max_w, text, start_size, max_lines=2):
    """Draw a headline, shrinking the font until it fits max_lines."""
    size = start_size
    while size > 18:
        f = font("DejaVuSans-Bold.ttf", size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return draw_lines(draw, x, y, lines, f, leading=int(size * 1.12))
        size -= 2
    f = font("DejaVuSans-Bold.ttf", size)
    lines = wrap(draw, text, f, max_w)[:max_lines]
    return draw_lines(draw, x, y, lines, f, leading=int(size * 1.12))


def fit_body(draw, x, y, max_w, max_h, text, start_size=20):
    """Draw body text inside a box, shrinking the font until it fits."""
    size = start_size
    while size > 14:
        f = font("DejaVuSans.ttf", size)
        lines = wrap(draw, text, f, max_w)
        leading = int(size * 1.32)
        if len(lines) * leading <= max_h:
            return draw_lines(draw, x, y, lines, f, leading=leading)
        size -= 1
    f = font("DejaVuSans.ttf", size)
    lines = wrap(draw, text, f, max_w)
    leading = int(size * 1.32)
    lines = lines[: max(1, max_h // leading)]
    return draw_lines(draw, x, y, lines, f, leading=leading)


def panel(draw, x, y, w, h, accent, kicker):
    """White panel with a coloured top bar and a small kicker label."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=(60, 60, 60), width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)
    draw.text((x + 16, y + 18), kicker, font=SANS_B(16), fill=accent)
    return y + 44


def mountains(draw, x, y, w, h, base, peak_col, snow_col):
    """A simple mountain range silhouette inside the given box."""
    pts = [(x, y + h), (x + w * 0.18, y + h * 0.25), (x + w * 0.34, y + h * 0.62),
           (x + w * 0.52, y + h * 0.08), (x + w * 0.72, y + h * 0.55),
           (x + w * 0.88, y + h * 0.30), (x + w, y + h)]
    draw.polygon(pts, fill=peak_col)
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=base)
    draw.polygon([(x + w * 0.52, y + h * 0.08), (x + w * 0.46, y + h * 0.30),
                  (x + w * 0.58, y + h * 0.30)], fill=snow_col)
    draw.polygon([(x + w * 0.18, y + h * 0.25), (x + w * 0.13, y + h * 0.42),
                  (x + w * 0.23, y + h * 0.42)], fill=snow_col)


def seismograph(draw, x, y, w, h, col):
    """A jagged seismograph trace."""
    pts = []
    n = 26
    for i in range(n + 1):
        px = x + i * w / n
        if i in (0, 1, 2, n - 2, n - 1, n):
            py = y + h / 2
        else:
            amp = h * (0.42 if i % 5 == 0 else 0.18)
            py = y + h / 2 + (amp if i % 2 else -amp)
        pts.append((px, py))
    draw.line(pts, fill=col, width=4, joint="curve")


def globe(draw, cx, cy, r, col):
    """A simple globe: circle with meridians and parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=col, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=col, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=col, width=3)
    draw.arc([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], 0, 360, fill=col, width=2)


def scales(draw, cx, cy, col):
    """Simple scales of justice, kept inside a ~96px wide box."""
    draw.line([cx, cy - 40, cx, cy + 40], fill=col, width=5)
    draw.line([cx - 38, cy - 26, cx + 38, cy - 26], fill=col, width=5)
    draw.polygon([(cx, cy - 46), (cx - 10, cy - 30), (cx + 10, cy - 30)], fill=col)
    for sx in (cx - 38, cx + 38):
        draw.line([sx, cy - 26, sx, cy + 4], fill=col, width=3)
        draw.arc([sx - 18, cy - 4, sx + 18, cy + 28], 0, 180, fill=col, width=4)
        draw.line([sx - 18, cy + 12, sx + 18, cy + 12], fill=col, width=4)
    draw.rectangle([cx - 28, cy + 40, cx + 28, cy + 47], fill=col)


def droplet(draw, x, y, w, h, col):
    """A water droplet that fits exactly inside the given box."""
    draw.ellipse([x, y + h * 0.35, x + w, y + h], fill=col)
    draw.polygon([(x + w / 2, y), (x, y + h * 0.45), (x + w, y + h * 0.45)], fill=col)
    draw.ellipse([x + w * 0.28, y + h * 0.55, x + w * 0.48, y + h * 0.85],
                 fill=(255, 255, 255))


def house_heart(draw, x, y, w, h, col):
    """A house outline with a heart, fitted inside the given box."""
    draw.polygon([(x, y + h * 0.32), (x + w / 2, y), (x + w, y + h * 0.32)], fill=col)
    draw.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.88, y + h],
                   fill=(255, 255, 255))
    draw.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.88, y + h],
                   outline=col, width=5)
    hx, hy, s = x + w / 2, y + h * 0.66, 11
    draw.ellipse([hx - s, hy - s * 0.6, hx, hy + s * 0.4], fill=(178, 52, 46))
    draw.ellipse([hx, hy - s * 0.6, hx + s, hy + s * 0.4], fill=(178, 52, 46))
    draw.polygon([(hx - s, hy), (hx + s, hy), (hx, hy + s * 1.2)], fill=(178, 52, 46))


def small_panel(draw, x, y, w, h, accent, kicker, icon, head, body):
    """A two-column story panel: icon left, headline right, body below."""
    ty = panel(draw, x, y, w, h, accent, kicker)
    icon(x + 14, ty + 6, 96, 88)
    headline(draw, x + 124, ty + 4, w - 140, head, 30, max_lines=2)
    fit_body(draw, x + 16, ty + 102, w - 32, y + h - 10 - (ty + 102), body)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer double border
    d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=2)
    d.rectangle([12, 12, W - 13, H - 13], outline=RULE, width=1)

    # ---------- masthead ----------
    title = "THE WORLD IN ONE PAGE"
    tf = SERIF_B(56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    d.line([28, 96, W - 28, 96], fill=RULE, width=3)
    d.line([28, 101, W - 28, 101], fill=RULE, width=1)
    date = "Saturday 21 November 2026"
    df = SANS_B(25)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 110), date, font=df, fill=INK)
    lf = SANS_B(17)
    d.text((28, 116), "WORLD NEWS", font=lf, fill=GREY)
    right = "ONE DAY, ONE PAGE"
    rw = d.textlength(right, font=lf)
    d.text((W - 28 - rw, 116), right, font=lf, fill=GREY)

    # ---------- lead: Peru earthquake ----------
    x0, y0, w0, h0 = 20, 152, 984, 248
    accent = (179, 69, 46)
    ty = panel(d, x0, y0, w0, h0, accent, "LEAD  •  SOUTH AMERICA")
    ix, iy, iw, ih = x0 + 14, ty + 4, 300, h0 - 62
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=(232, 226, 214),
                outline=(150, 150, 150), width=1)
    mountains(d, ix + 10, iy + 12, iw - 20, ih - 46, (120, 110, 100),
              (96, 104, 122), (250, 250, 250))
    seismograph(d, ix + 12, iy + ih - 34, iw - 24, 26, (179, 69, 46))
    tx = x0 + 336
    y = headline(d, tx, ty, w0 - 336 - 18, "M6.9 QUAKE SHAKES PERU'S ANDES", 40)
    body = ("A magnitude 6.9 earthquake struck central Peru in the early "
            "hours of Saturday, its tremors felt in Lima. No damage or "
            "casualties were reported.")
    fit_body(d, tx, y + 8, w0 - 336 - 18, y0 + h0 - 10 - (y + 8), body,
             start_size=21)

    # ---------- row 2 ----------
    y1, h1 = 414, 232
    x1, w1 = 20, 484
    x2, w2 = 520, 484
    small_panel(d, x1, y1, w1, h1, (46, 125, 79), "CLIMATE  •  ANTALYA",
                lambda x, y, w, h: globe(d, x + w / 2, y + h / 2, 42, (46, 125, 79)),
                "COP31 RUNS INTO OVERTIME",
                "Talks miss their Friday deadline. A third draft is due on "
                "Saturday as France and Panama threaten to block any deal "
                "that drops fossil fuels.")
    small_panel(d, x2, y1, w2, h1, (31, 78, 121), "JUSTICE  •  UNITED STATES",
                lambda x, y, w, h: scales(d, x + w / 2, y + h / 2, (31, 78, 121)),
                "FINED $811M — THE SCAMS DIDN'T STOP",
                "A BBC investigation finds the immigration bail business "
                "fined $811m for conning detained migrants kept operating "
                "under a new name.")

    # ---------- row 3 ----------
    y2, h2 = 660, 228
    small_panel(d, x1, y2, w1, h2, (27, 108, 168), "WATER  •  SOUTH AFRICA",
                lambda x, y, w, h: droplet(d, x + 16, y + 4, 64, 82, (27, 108, 168)),
                "JOBURG TURNS OFF THE TAPS",
                "Level 2 water restrictions begin today in Johannesburg, "
                "aiming to cut use by 200 million litres a day. Garden "
                "watering and hosing are banned.")
    small_panel(d, x2, y2, w2, h2, (122, 74, 143), "HEALTH  •  AUSTRALIA",
                lambda x, y, w, h: house_heart(d, x + 8, y + 4, 84, 84, (122, 74, 143)),
                "HOME BIRTHS AT RISK",
                "Australian midwives warn private home-birth services could "
                "collapse when an insurance exemption expires on 31 December.")

    # ---------- ticker ----------
    ty0, th = 902, 108
    d.rectangle([20, ty0, 1004, ty0 + th], fill=(25, 25, 25))
    d.text((36, ty0 + 12), "ALSO TODAY", font=SANS_B(18), fill=(232, 196, 90))
    items = [
        "Melania Trump calls for \u201cpeace\u201d at an Amazon premiere",
        "Actor E.J. Carroll dies at 66",
        "Northern Ireland doctors plan a further strike",
        "Victorian Greens seek an injunction over vote cards",
    ]
    tick = "   \u2022   ".join(items)
    lines = wrap(d, tick, SANS(19), 1004 - 36 - 36)
    draw_lines(d, 36, ty0 + 42, lines, SANS(19), fill=(245, 245, 245), leading=27)

    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
