#!/usr/bin/env python3
"""Draw the 26 November 2026 front page: "THE WORLD IN ONE DAY".

A 1024x1024 newspaper front page rendered with Pillow. One hero story
(North Korea's nuclear order), four more panels (US tariffs, Ukraine,
birthright citizenship, the Cairo tanker fire), a culture strip
(Andy Taylor) and an "also today" ticker. Every word is fixed in this
file, so two runs write byte-identical output. No network, no clock,
no randomness.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
SOFT = (94, 88, 76)
RED = (166, 24, 24)
NAVY = (15, 35, 63)
NAVY_SOFT = (214, 224, 238)
GOLD = (212, 164, 42)
PANEL = (255, 253, 247)
LINE = (198, 190, 170)
AMBER = (176, 118, 8)
STEEL = (38, 84, 124)
PLUM = (110, 58, 110)
EMBER = (178, 74, 18)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

MX = 34  # page margin


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns the lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, size, width, max_lines, min_size=13):
    """Largest font size whose wrapped text fits in max_lines lines."""
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, width)


def centred(draw, y, text, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def rule(draw, y, weight=2, fill=INK, x0=MX, x1=W - MX):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


# ---------------------------------------------------------------- icons

def atom_icon(size, color):
    """A gold atom: nucleus plus three tilted orbit rings."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = size // 2
    rx = size // 2 - 10
    ry = size // 6
    for ang in (0, 60, 120):
        ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                   outline=color + (255,), width=5)
        ring = ring.rotate(ang, resample=Image.BICUBIC, center=(cx, cy))
        layer.alpha_composite(ring)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=color + (255,))
    return layer


def percent_icon(size, color):
    """A bold % inside a ring, for the tariffs panel."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([4, 4, size - 4, size - 4], outline=color + (255,), width=5)
    fnt = font(SANS_B, size - 26)
    txt = "%"
    tw = d.textlength(txt, font=fnt)
    th = fnt.size
    d.text(((size - tw) / 2, (size - th) / 2 - 4), txt, font=fnt,
           fill=color + (255,))
    return layer


def jet_icon(size, color):
    """A simple delta jet silhouette, nose to the right."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = size
    pts = [
        (s * 0.94, s * 0.50), (s * 0.62, s * 0.38), (s * 0.30, s * 0.12),
        (s * 0.34, s * 0.44), (s * 0.10, s * 0.50), (s * 0.34, s * 0.56),
        (s * 0.30, s * 0.88), (s * 0.62, s * 0.62),
    ]
    d.polygon(pts, fill=color + (255,))
    return layer


def gavel_icon(size, color):
    """A gavel drawn flat, then tilted, for the courts panel."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([size * 0.18, size * 0.20, size * 0.82, size * 0.38],
                        radius=6, fill=color + (255,))
    d.rectangle([size * 0.46, size * 0.38, size * 0.54, size * 0.86],
                fill=color + (255,))
    d.rectangle([size * 0.30, size * 0.86, size * 0.70, size * 0.92],
                fill=color + (255,))
    return layer.rotate(35, resample=Image.BICUBIC, center=(size / 2, size / 2))


def flame_icon(size, color):
    """A flame teardrop for the tanker-fire panel."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = size
    outer = [
        (s * 0.50, s * 0.04), (s * 0.78, s * 0.34), (s * 0.86, s * 0.62),
        (s * 0.72, s * 0.90), (s * 0.50, s * 0.96), (s * 0.28, s * 0.90),
        (s * 0.14, s * 0.62), (s * 0.24, s * 0.34),
    ]
    d.polygon(outer, fill=color + (255,))
    inner = [
        (s * 0.50, s * 0.40), (s * 0.64, s * 0.60), (s * 0.60, s * 0.82),
        (s * 0.40, s * 0.82), (s * 0.36, s * 0.60),
    ]
    d.polygon(inner, fill=(255, 214, 120, 255))
    return layer


def guitar_icon(size, color):
    """A simple acoustic guitar, tilted, for the obituary strip.

    Drawn flat (body bottom-left, neck to top-right) on its own layer,
    then rotated so it reads as a guitar rather than a note.
    """
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = size
    # body: two overlapping circles make the classic figure-eight
    d.ellipse([s * 0.04, s * 0.52, s * 0.44, s * 0.92], fill=color + (255,))
    d.ellipse([s * 0.16, s * 0.38, s * 0.56, s * 0.78], fill=color + (255,))
    # sound hole
    d.ellipse([s * 0.26, s * 0.58, s * 0.42, s * 0.74],
              fill=(247, 243, 232, 255))
    # neck and headstock, rising to the top-right
    d.polygon([(s * 0.42, s * 0.44), (s * 0.52, s * 0.38),
               (s * 0.86, s * 0.04), (s * 0.94, s * 0.12)],
              fill=color + (255,))
    d.polygon([(s * 0.82, s * 0.02), (s * 0.90, s * -0.02),
               (s * 1.00, s * 0.08), (s * 0.92, s * 0.12)],
              fill=color + (255,))
    return layer.rotate(18, resample=Image.BICUBIC, center=(size / 2, size / 2))


# ---------------------------------------------------------------- layout

def masthead(draw):
    title = font(SERIF_B, 56)
    centred(draw, 22, "THE WORLD IN ONE DAY", title, INK)
    date = font(SANS_B, 24)
    centred(draw, 86, "T H U R S D A Y ,  2 6  N O V E M B E R  2 0 2 6",
            date, RED)
    rule(draw, 120, 3)
    rule(draw, 126, 1)


def hero(draw, img):
    x0, y0, x1, y1 = MX, 138, W - MX, 424
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=NAVY)
    draw.rounded_rectangle([x0, y0, x1, y0 + 8], radius=6, fill=NAVY)
    tx = x0 + 26
    kicker = font(SANS_B, 17)
    draw.text((tx, y0 + 20), "ASIA  ·  SECURITY  ·  LEAD STORY",
              font=kicker, fill=GOLD)
    head, lines = fit_lines(draw, "KIM ORDERS WIDER NUCLEAR DEPLOYMENT",
                            SERIF_B, 46, 600, 2, min_size=30)
    yy = y0 + 52
    for line in lines:
        draw.text((tx, yy), line, font=head, fill=(255, 255, 255))
        yy += head.size + 6
    body, blines = fit_lines(
        draw,
        "North Korea's Kim Jong Un tells weapons chiefs to spread "
        "tactical nuclear arms across more domains, and declares its "
        "nuclear-weapons status \u201cabsolutely inviolable\u201d.",
        SANS, 20, 600, 3, min_size=16)
    yy += 8
    for line in blines:
        draw.text((tx, yy), line, font=body, fill=NAVY_SOFT)
        yy += body.size + 7
    img.paste(atom_icon(230, GOLD), (x1 - 262, y0 + 30),
              atom_icon(230, GOLD))
    src = font(SANS, 14)
    draw.text((tx, y1 - 30), "KCNA, via Reuters  ·  reported Thursday",
              font=src, fill=(160, 175, 200))


def story_panel(draw, img, x, y, w, h, accent, kicker, headline, body,
                icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL,
                           outline=LINE, width=1)
    draw.rectangle([x + 14, y + 14, x + 64, y + 18], fill=accent)
    kf = font(SANS_B, 15)
    draw.text((x + 14, y + 26), kicker, font=kf, fill=accent)
    text_w = w - 28 - 74
    head, lines = fit_lines(draw, headline, SERIF_B, 26, text_w, 2,
                            min_size=20)
    yy = y + 50
    for line in lines:
        draw.text((x + 14, yy), line, font=head, fill=INK)
        yy += head.size + 4
    bf, blines = fit_lines(draw, body, SANS, 17, text_w, 3, min_size=14)
    yy += 6
    for line in blines:
        draw.text((x + 14, yy), line, font=bf, fill=SOFT)
        yy += bf.size + 5
    img.paste(icon, (x + w - 78, y + 46), icon)


def culture_strip(draw, img):
    x0, y0, x1, y1 = MX, 828, W - MX, 908
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(232, 222, 200),
                           outline=LINE, width=1)
    img.paste(guitar_icon(64, (74, 52, 32)), (x0 + 14, y0 + 8),
              guitar_icon(64, (74, 52, 32)))
    kf = font(SANS_B, 15)
    draw.text((x0 + 94, y0 + 10), "CULTURE  ·  OBITUARY", font=kf, fill=RED)
    hf = font(SERIF_B, 26)
    draw.text((x0 + 94, y0 + 32),
              "Duran Duran guitarist Andy Taylor dies at 65",
              font=hf, fill=INK)
    bf = font(SANS, 16)
    draw.text((x0 + 94, y0 + 60),
              "The new-wave band's guitarist and songwriter, reported Thursday.",
              font=bf, fill=SOFT)


def ticker(draw):
    x0, y0, x1, y1 = MX, 924, W - MX, 962
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=INK)
    text = ("ALSO TODAY:  Norway court voids oil licences  \u2022  Kenya's "
            "last Ebola patient goes home  \u2022  Chess: Gukesh\u2013Sindarov "
            "Game 2 drawn  \u2022  Thanksgiving in the US")
    fnt, _ = fit_lines(draw, text, SANS_B, 15, x1 - x0 - 24, 1, min_size=12)
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y0 + (y1 - y0 - fnt.size) / 2 - 1), text,
              font=fnt, fill=(240, 236, 224))


def footer(draw):
    fnt = font(SANS, 13)
    centred(draw, 974,
            "Sources: Reuters  ·  CNN  ·  The Hindu  ·  BBC  —  full list in SOURCES.md",
            fnt, SOFT)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    hero(draw, img)
    gw, gh, gap = 470, 176, 16
    gx = MX
    gy = 440
    story_panel(draw, img, gx, gy, gw, gh, AMBER, "TRADE  ·  WASHINGTON",
                "TRUMP UNVEILS NEW TARIFFS ON 14 PARTNERS",
                "China faces up to 40% and the EU 15% in a salvo aimed at "
                "factory overcapacity; duties start after a January hearing.",
                percent_icon(64, AMBER))
    story_panel(draw, img, gx + gw + gap, gy, gw, gh, STEEL,
                "WAR IN UKRAINE  ·  KYIV",
                "UKRAINE SAYS IT HIT A RUSSIAN AIR BASE",
                "Kyiv says the strike damaged five planes \u2014 the latest "
                "long-range blow in the war.",
                jet_icon(64, STEEL))
    story_panel(draw, img, gx, gy + gh + gap, gw, gh, PLUM,
                "U.S. COURTS  ·  WASHINGTON",
                "SECOND JUDGE BLOCKS BIRTHRIGHT ORDER",
                "Trump's newest order curtailing birthright citizenship is "
                "halted by a second federal judge.",
                gavel_icon(64, PLUM))
    story_panel(draw, img, gx + gw + gap, gy + gh + gap, gw, gh, EMBER,
                "EGYPT  ·  DISASTER",
                "TANKER CRASH FIRE KILLS AT LEAST 30 NEAR CAIRO",
                "A fuel tanker crash ignites a huge fire on the highway "
                "ringing the Egyptian capital.",
                flame_icon(64, EMBER))
    culture_strip(draw, img)
    ticker(draw)
    footer(draw)
    img.save(OUT, format="PNG")
    print("wrote " + OUT)


if __name__ == "__main__":
    build()
