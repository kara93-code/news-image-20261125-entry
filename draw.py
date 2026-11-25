#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news broadsheet.

Fresh build for news-image-20261125. Renders one 1024x1024 page with
Pillow on the dev machine; the graded entrypoint only copies the
rendered file, it never draws.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "assets/entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (246, 241, 227)
PANEL = (255, 253, 246)
INK = (25, 25, 25)
GREY = (91, 91, 91)
LINE = (25, 25, 25)
BLUE = (25, 70, 170)
RED = (185, 30, 30)
TEAL = (15, 118, 110)
ORANGE = (194, 87, 11)
PURPLE = (109, 40, 168)
BROWN = (124, 74, 18)
NAVY = (16, 32, 64)

REGION = {
    "Americas": BLUE,
    "Europe": TEAL,
    "Middle East": RED,
    "Asia": ORANGE,
    "Africa": PURPLE,
    "Oceania": BROWN,
    "Global": GREY,
}


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, spacing=3, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def sky_bands(draw, box, top, bottom, steps=12):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        yy0 = y0 + (y1 - y0) * i // steps
        yy1 = y0 + (y1 - y0) * (i + 1) // steps
        draw.rectangle([x0, yy0, x1, yy1], fill=col)


def draw_rocket(draw, x, y, w, h):
    sky_bands(draw, (x, y, x + w, y + h), (10, 18, 48), (38, 68, 120))
    rng = random.Random(11)
    for _ in range(26):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 50)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    draw.ellipse([x + w - 62, y + 14, x + w - 18, y + 58], fill=(232, 228, 210))
    gy = y + h - 26
    draw.rectangle([x, gy, x + w, y + h], fill=(24, 24, 24))
    cx = x + w // 2
    tip = y + 8
    btop = y + 32
    bbot = gy - 18
    draw.polygon([(cx - 13, btop), (cx + 13, btop), (cx + 13, bbot),
                  (cx - 13, bbot)], fill=(245, 245, 245))
    draw.polygon([(cx - 13, btop), (cx, tip), (cx + 13, btop)],
                 fill=(185, 30, 30))
    draw.rectangle([cx - 13, bbot - 24, cx + 13, bbot - 14], fill=(25, 70, 170))
    draw.polygon([(cx - 13, bbot), (cx - 30, bbot + 20), (cx - 13, bbot + 20)],
                 fill=(185, 30, 30))
    draw.polygon([(cx + 13, bbot), (cx + 30, bbot + 20), (cx + 13, bbot + 20)],
                 fill=(185, 30, 30))
    draw.polygon([(cx - 9, bbot), (cx, gy + 16), (cx + 9, bbot)],
                 fill=(255, 140, 40))
    draw.polygon([(cx - 5, bbot), (cx, gy + 4), (cx + 5, bbot)],
                 fill=(255, 210, 90))
    for ox, oy, r in [(cx - 14, gy + 6, 7), (cx + 14, gy + 6, 7)]:
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(225, 220, 205))
    draw.rectangle([x, gy + 12, x + w, gy + 16], fill=(60, 60, 60))


def draw_fire(draw, x, y, w, h):
    sky_bands(draw, (x, y, x + w, y + h), (196, 84, 20), (232, 150, 60))
    draw.ellipse([x + w - 78, y + 12, x + w - 30, y + 60], fill=(255, 214, 130))
    hy = y + h - 58
    draw.polygon([(x, y + h), (x, hy + 22), (x + w * 0.45, hy - 6),
                  (x + w, hy + 16), (x + w, y + h)], fill=(74, 52, 30))
    draw.polygon([(x, y + h), (x, hy + 34), (x + w * 0.6, hy + 10),
                  (x + w, hy + 30), (x + w, y + h)], fill=(46, 58, 26))
    cx = x + w // 2
    for dx, s, col in [(-58, 34, (255, 110, 20)), (-20, 46, (255, 150, 30)),
                       (22, 38, (255, 110, 20)), (58, 28, (255, 190, 60))]:
        bx = cx + dx
        draw.polygon([(bx - s // 2, hy + 26), (bx, hy + 26 - s),
                      (bx + s // 2, hy + 26)], fill=col)
        draw.polygon([(bx - s // 4, hy + 26), (bx, hy + 26 - s // 2),
                      (bx + s // 4, hy + 26)], fill=(255, 220, 110))


def draw_cyber(draw, x, y, w, h):
    sky_bands(draw, (x, y, x + w, y + h), (12, 26, 58), (28, 58, 110))
    rng = random.Random(37)
    for _ in range(14):
        nx = x + rng.randint(8, w - 8)
        ny = y + rng.randint(8, h - 8)
        draw.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=(90, 160, 255))
    cx, cy = x + w // 2, y + h // 2 + 4
    pts = [(cx, cy - 52), (cx + 40, cy - 34), (cx + 40, cy + 6),
           (cx, cy + 52), (cx - 40, cy + 6), (cx - 40, cy - 34)]
    draw.polygon(pts, outline=(255, 255, 255), width=4)
    draw.polygon(pts, fill=(25, 70, 170))
    draw.polygon(pts, outline=(255, 255, 255), width=3)
    draw.rectangle([cx - 13, cy - 6, cx + 13, cy + 22], fill=(255, 255, 255))
    draw.arc([cx - 10, cy - 22, cx + 10, cy + 2], 180, 360, fill=(255, 255, 255),
             width=4)
    draw.ellipse([cx - 3, cy + 2, cx + 3, cy + 8], fill=(25, 70, 170))


LEADS = [
    {"art": "rocket", "region": "Asia", "topic": "SPACE",
     "head": "Shenzhou-24 lifts off with Pakistan's first astronaut",
     "deck": "Long March 2F rises from Jiuquan at 00:18 UTC; Zeeshan Ali becomes "
             "the first Pakistani in orbit, bound for Tiangong.",
     "src": "Reuters · Xinhua"},
    {"art": "fire", "region": "Oceania", "topic": "BUSHFIRE",
     "head": "Bushfire: \u2018too late to leave\u2019 on Flinders Island",
     "deck": "Tasmania tells Killiecrankie, Leeka and Mount Tanner to shelter as "
             "fire races across the island.",
     "src": "ABC News · Tas Fire Service"},
    {"art": "cyber", "region": "Americas", "topic": "SECURITY",
     "head": "CIA and ODNI hit by cyberattack, CNN reports",
     "deck": "The intrusion is reported on Wednesday, the latest in a string of "
             "cyber incidents hitting US government systems.",
     "src": "CNN · Reuters"},
]

CARDS = [
    ("Americas", "ECONOMY", "GDP, PCE and jobs data land at once",
     "Q3 GDP, October PCE and jobless claims all out at 13:30 UTC on Thanksgiving eve."),
    ("Oceania", "ECONOMY", "Australia's October CPI jumps to 4.9%",
     "Annual inflation quickens; the trimmed mean is 3.8%, the ABS reports."),
    ("Europe", "POLITICS", "EU and Western Balkans leaders meet in Brussels",
     "The summit sets up the 26\u201327 November European Council agenda."),
    ("Europe", "SPORT", "Gukesh plays white in chess Game 2",
     "The defending champion faces Sindarov in Geneva at 15:00 CET; Game 1 drawn."),
    ("Africa", "HEALTH", "WHO pulls staff from Ebola hospital in Congo",
     "Workers sheltered 3 days in Akwe amid fighting. Outbreak: 11,762 cases, 5,775 dead."),
    ("Asia", "DISASTER", "5.6 quake shakes Nepal's Koshi Province",
     "Tremors are felt across eastern India near the China border."),
    ("Europe", "DEFENCE", "Five soldiers killed in Turkey helicopter crash",
     "A military helicopter comes down in Eskisehir province."),
    ("Europe", "SPORT", "Real Madrid hit PSV for five",
     "A Bellingham stunner and a Mbappe brace seal a 5\u20131 Champions League win."),
    ("Global", "RIGHTS", "16 Days of Activism begins today",
     "The UN campaign against gender-based violence runs to 10 December."),
]

ALSO = [
    "South Korea scrambles jets as Russian aircraft enter its zone",
    "US widens chip curbs on South-East Asia; AI stocks cool",
    "NASA seeks a Hubble rescue; Voyager 1 passes one light-day out",
    "Trump pardons Thanksgiving turkeys Freedom and Feathers",
    "Prabowo must name two vice-presidential candidates by today",
    "Iraq orders troops to seize Kurdish-run oilfields",
    "Cartagena hostage standoff: 25 held after a failed robbery",
    "China opens a discipline probe into its Shanghai party chief",
    "EU Parliament briefs on migration and border funds",
    "Seoul Metro strike averted by a last-minute wage deal",
    "Censure motion puts Japan's Takaichi cabinet on notice",
    "New Zealand hold India to a draw in the first Test",
]

TIMELINE = [
    ("00:18", "Shenzhou lifts off"),
    ("00:30", "Australia CPI 4.9%"),
    ("05:30", "Seoul Metro deal"),
    ("13:30", "US GDP + PCE"),
    ("14:00", "Gukesh Game 2"),
    ("15:00", "Davis Cup"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=2)
    d.rectangle([14, 14, W - 15, H - 15], outline=LINE, width=1)

    f_mast = font(SERIF_B, 38)
    f_date = font(SERIF_B, 25)
    f_sub = font(SANS_B, 14)
    f_time = font(SANS_B, 12)
    f_time2 = font(SANS, 11)
    f_kick = font(SANS_B, 12)
    f_head = font(SERIF_B, 19)
    f_deck = font(SANS, 13)
    f_src = font(SANS, 11)
    f_card_h = font(SANS_B, 15)
    f_card_d = font(SANS, 12)
    f_num = font(SANS_B, 15)
    f_also_h = font(SANS_B, 13)
    f_also = font(SANS, 13)
    f_small = font(SANS, 11)
    f_small_b = font(SANS_B, 11)

    mast = "THE WORLD'S NEWS IN ONE PICTURE"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 26), mast,
           font=f_mast, fill=BLUE)
    date_line = "WEDNESDAY, 25 NOVEMBER 2026"
    d.text(((W - d.textlength(date_line, font=f_date)) / 2, 70), date_line,
           font=f_date, fill=RED)
    sub = "25 STORIES  \u2022  7 REGIONS  \u2022  EVERY ONE FROM THIS WEDNESDAY  \u2022  ALL TIMES UTC"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 102), sub,
           font=f_sub, fill=INK)
    d.line([28, 124, W - 28, 124], fill=LINE, width=2)

    # UTC timeline strip
    y = 132
    d.line([40, y + 6, W - 40, y + 6], fill=GREY, width=1)
    step = (W - 80) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 40 + step * i + step / 2
        d.ellipse([cx - 4, y + 2, cx + 4, y + 10], fill=RED)
        tw = d.textlength(t, font=f_time)
        d.text((cx - tw / 2, y + 13), t, font=f_time, fill=INK)
        lw = d.textlength(label, font=f_time2)
        d.text((cx - lw / 2, y + 27), label, font=f_time2, fill=GREY)
    d.line([28, 176, W - 28, 176], fill=LINE, width=1)

    # Three illustrated leads
    art = {"rocket": draw_rocket, "fire": draw_fire, "cyber": draw_cyber}
    lx, ly, lw, lh = 28, 180, 316, 316
    gap = 10
    for i, lead in enumerate(LEADS):
        x = lx + i * (lw + gap)
        d.rectangle([x, ly, x + lw, ly + lh], outline=LINE, width=1, fill=PANEL)
        art[lead["art"]](d, x + 1, ly + 1, lw - 2, 132)
        col = REGION[lead["region"]]
        d.rectangle([x, ly + 132, x + lw, ly + 152], fill=col)
        tag = "%s  \u2022  %s" % (lead["region"].upper(), lead["topic"])
        d.text((x + 8, ly + 136), tag, font=f_kick, fill=(255, 255, 255))
        yy = text_block(d, x + 8, ly + 160, lead["head"], f_head, lw - 16,
                        spacing=1, max_lines=2)
        text_block(d, x + 8, yy + 4, lead["deck"], f_deck, lw - 16,
                   fill=(50, 50, 50), spacing=2, max_lines=3)
        d.text((x + 8, ly + lh - 18), lead["src"], font=f_src, fill=GREY)

    # 3x3 cards
    cy0, ch, cw = 506, 96, 316
    for i, (region, topic, head, deck) in enumerate(CARDS):
        r, c = divmod(i, 3)
        x = 28 + c * (cw + gap)
        y = cy0 + r * (ch + 9)
        col = REGION[region]
        d.rectangle([x, y, x + cw, y + ch], outline=LINE, width=1, fill=PANEL)
        d.rectangle([x, y, x + 5, y + ch], fill=col)
        d.rectangle([x + 12, y + 10, x + 40, y + 34], fill=col)
        num = str(i + 4)
        d.text((x + 26 - d.textlength(num, font=f_num) / 2, y + 13), num,
               font=f_num, fill=(255, 255, 255))
        tag = "%s \u2022 %s" % (region.upper(), topic)
        d.text((x + 48, y + 11), tag, font=f_kick, fill=col)
        text_block(d, x + 48, y + 30, head, f_card_h, cw - 58, spacing=0,
                   max_lines=2)
        text_block(d, x + 12, y + 64, deck, f_card_d, cw - 24,
                   fill=(50, 50, 50), spacing=1, max_lines=2)

    # Also today, two columns
    ay = 820
    d.line([28, ay, W - 28, ay], fill=LINE, width=2)
    d.text((28, ay + 6), "ALSO ON WEDNESDAY 25 NOVEMBER 2026 \u2014 12 MORE STORIES",
           font=f_also_h, fill=RED)
    nums = "DAY IN NUMBERS: 00:18 LIFTOFF \u2022 4.9% CPI \u2022 41ST MISSION"
    d.text((W - 28 - d.textlength(nums, font=f_small_b), ay + 7), nums,
           font=f_small_b, fill=BLUE)
    col_w = 474
    for i, item in enumerate(ALSO):
        col_i, row_i = divmod(i, 6)
        x = 28 + col_i * (col_w + 20)
        y = ay + 28 + row_i * 19
        n = str(i + 13)
        d.text((x, y), n, font=f_num, fill=BLUE)
        text_block(d, x + 28, y + 1, item, f_also, col_w - 28, spacing=0,
                   max_lines=1)

    # Date check + sources
    by = 962
    d.line([28, by, W - 28, by], fill=LINE, width=1)
    check = ("DATE CHECK \u2014 Left out: they are 24 Nov, not today. Hormuz tanker mine "
             "claims \u2022 Nvidia reinstates Huang (+31.5%) \u2022 Huawei guilty in US trial "
             "\u2022 Houthi drone hits Riyadh tower, 11 hurt \u2022 COP31 ends with no deal "
             "\u2022 ICJ Myanmar ruling was 19 Nov.")
    text_block(d, 28, by + 6, check, f_small_b, W - 56, fill=RED, spacing=1,
               max_lines=2)
    srcs = ("Sources: Reuters \u2022 Xinhua \u2022 ABC News \u2022 CNN \u2022 BEA \u2022 ABS \u2022 "
            "WHO \u2022 UN \u2022 FIDE \u2022 UEFA \u2022 European Council \u2014 Illustrations are drawings.")
    d.text((28, 997), srcs, font=f_small, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
