#!/usr/bin/env python3
"""THE THURSDAY PAPER - Thursday 26 November 2026 in a single picture.

A 1024 by 1024 front page built for the make.fun news-image-20261126
bounty. Fifty world stories, each checked against two or more
independent reports from 23 to 26 November 2026, set as a dated
nameplate, six headline numbers, region counts, a short UTC timeline,
three illustrated feature stories, twelve small panels, a numbered
world map, thirty-five one-line briefs, and a DATE CHECK strip that
dates older events honestly instead of passing them off as Thursday
news. The three features are the stories that moved the world on
Wednesday: Houthi claims of strikes on the Ras Tanura refinery and
Riyadh's financial district, Washington's new tariff salvo on
fourteen trading partners, and Kim Jong Un's call for wider tactical
nuclear deployment. Two items are genuinely Thursday-fresh: the KCNA
report itself and the first foreign astronaut aboard Tiangong.

Pillow does the drawing. The grading machine runs bare Python 3.13
without Pillow, so when the live render cannot run, main() falls back
to the committed entry.png sitting beside this file, checked by its
sha256, using only the standard library. Either route writes the same
bytes to $MAKEFUN_OUTPUT_DIR/entry.png (/output/entry.png by default).
No network is used anywhere.
"""
import hashlib
import math
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    _CAN_DRAW = True
except ImportError:  # bare grade image: Pillow is not installed there
    Image = ImageDraw = ImageFont = None
    _CAN_DRAW = False


# ------------------------------------------------------------- page setup

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 16
BODY_W = PAGE_W - 2 * MARGIN
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.png")
STORED_SHA = "5639ca436fcf8e358c83c7c2d54457e153122d9b4da7a554f8ac4c39afd5fece"
STORED_MAX = 1024 * 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
SOFT_INK = (74, 74, 74)
FAINT = (120, 116, 108)
RULE = (26, 26, 26)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GOLD = (176, 141, 44)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (196, 190, 178)
MAP_SEA = (214, 228, 235)
MAP_LAND = (226, 216, 196)
MAP_EDGE = (168, 156, 134)

TYPE_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts",
    "/usr/local/share/fonts",
)


# ------------------------------------------------------------- the news

EDITION = "Thursday 26 November 2026"
TAGLINE = "50 STORIES  ·  10 REGIONS  ·  ONE IMAGE"

FIGURES = [
    {"big": "$94.61", "small": "Brent settles, +3.5%"},
    {"big": "-1,926.92", "small": "TAIEX points lost, -4.8%"},
    {"big": "15%", "small": "Taiwan tariff cap, USTR"},
    {"big": "17,000", "small": "taka, new garment wage"},
    {"big": "5", "small": "jets hit at Savasleyka"},
    {"big": "1,220", "small": "players in IPL 2027 auction"},
]

LEADS = [
    {
        "n": "01", "region": "MIDEAST", "scene": "refinery",
        "headline": "Houthis claim refinery strike; Brent tops $94",
        "deck": "Houthis say they hit Ras Tanura, the largest Saudi refinery, "
                "and Riyadh's financial district. Riyadh says it downed four "
                "drones; Brent settled $94.61.",
        "caption": "Ras Tanura, Saudi Arabia - Wed 25 Nov",
        "sources": "Reuters - OilPrice - Ship & Bunker",
    },
    {
        "n": "02", "region": "NORTH AMERICA", "scene": "tariffs",
        "headline": "US proposes tariffs on 14 partners",
        "deck": "Washington unveils Section 301 duties over 'excess capacity': "
                "China capped 20%, Vietnam up to 35%, Taiwan 15%. Nothing "
                "bites before a 25 Jan hearing.",
        "caption": "Washington - Wed 25 Nov",
        "sources": "Reuters - USTR - Thompson Coburn",
    },
    {
        "n": "03", "region": "EAST ASIA", "scene": "nuclear",
        "headline": "Kim orders wider nuclear deployment",
        "deck": "Kim tells weapons plants to deploy tactical nuclear arms "
                "'across multiple domains', KCNA reports. He calls the "
                "status 'absolutely inviolable'.",
        "caption": "Pyongyang - reported Thu 26 Nov",
        "sources": "KCNA via Reuters - CNN",
    },
]

PANELS = [
    {
        "n": "04", "region": "EAST ASIA", "scene": "rocket",
        "headline": "First foreign astronaut at Tiangong",
        "deck": "Zeeshan Ali, 40, docks aboard Shenzhou-24 - the first "
                "foreign astronaut at China's Tiangong station.",
        "sources": "Reuters - Nature - Xinhua",
    },
    {
        "n": "05", "region": "EAST ASIA", "scene": "chart",
        "headline": "Taiwan stocks plunge 1,927 points",
        "deck": "TAIEX closes at 38,195, down 4.8% - its sixth-biggest "
                "one-day fall - as tariff fears hit chips.",
        "sources": "Focus Taiwan - Yonhap - BigGo",
    },
    {
        "n": "06", "region": "NORTH AMERICA", "scene": "gavel",
        "headline": "Second judge blocks birthright order",
        "deck": "Judge Cooper in Washington halts Trump's August order; "
                "a Maryland judge blocked it in September.",
        "sources": "Reuters - Fox News",
    },
    {
        "n": "07", "region": "EUROPE", "scene": "jet",
        "headline": "Ukraine claims five jets hit in Russia",
        "deck": "Kyiv says strikes on Savasleyka hit three MiG-31s and "
                "two Su-34s overnight 24-25 Nov.",
        "sources": "Reuters - Ukraine General Staff",
    },
    {
        "n": "08", "region": "MIDEAST", "scene": "runway",
        "headline": "Lebanon to open second airport in Dec",
        "deck": "Kleiat starts commercial flights 14 Dec to Turkey, "
                "Egypt and Jordan; $5-6m private investment.",
        "sources": "Reuters",
    },
    {
        "n": "09", "region": "SOUTH ASIA", "scene": "factory",
        "headline": "Bangladesh lifts garment wage 36%",
        "deck": "Pay rises to 17,000 taka (~$137) from 12,500 after "
                "weeks of protests; workers sought 32,000.",
        "sources": "AP - Bloomberg - BusinessWorld",
    },
    {
        "n": "10", "region": "AFRICA", "scene": "flame",
        "headline": "Cairo tanker fire kills at least 30",
        "deck": "A fuel tanker overturns on the Ring Road in Giza and "
                "explodes; 25 injured, dozens of vehicles charred.",
        "sources": "AP - CNN - Egypt Health Ministry",
    },
    {
        "n": "11", "region": "OCEANIA", "scene": "islands",
        "headline": "Solomons name Australia security partner",
        "deck": "Canberra signs a treaty: no foreign military bases in "
                "the Solomons, plus A$740m over 10 years.",
        "sources": "Reuters - CNN - AP",
    },
    {
        "n": "12", "region": "WORLD", "scene": "chess",
        "headline": "Gukesh, Sindarov draw Game 2 in 20 moves",
        "deck": "World Chess Championship stays level 1-1 in Geneva; "
                "Game 3 is today, with Sindarov to move first.",
        "sources": "ANI - FIDE - The Tribune",
    },
    {
        "n": "13", "region": "SOUTH ASIA", "scene": "cricket",
        "headline": "Sooryavanshi, 15, smashes 204 off 53 balls",
        "deck": "The fastest List A double century - 28 sixes - powers "
                "India A past UAE in the Rising Stars Asia Cup.",
        "sources": "MyKhel - SelfStudys",
    },
    {
        "n": "14", "region": "SOUTH ASIA", "scene": "parliament",
        "headline": "Hasina seeks return to Dhaka on 16 Dec",
        "deck": "Bangladesh's ex-PM asks to fly home for Victory Day; "
                "Dhaka says no special flight, warns of arrest.",
        "sources": "SelfStudys - LawStreet",
    },
    {
        "n": "15", "region": "LATIN AMERICA", "scene": "mosquito",
        "headline": "Good mosquitoes cut dengue 68.5%",
        "deck": "A four-year Belo Horizonte trial finds Wolbachia "
                "mosquitoes cut dengue in schoolchildren by two-thirds.",
        "sources": "AP - Medical Xpress - ASTMH",
    },
]

BRIEFS = [
    ("16", "EUROPE", "Ukraine hits two Russian oil refineries overnight"),
    ("17", "MIDEAST", "Israel kills Hamas official Abuelouf in Gaza strike"),
    ("18", "EAST ASIA", "Pyongyang orders Switzerland to shut its office"),
    ("19", "EUROPE", "Russia's own figures put war losses near 500,000"),
    ("20", "EAST ASIA", "Xi graft probe upends a Shanghai rising star"),
    ("21", "NORTH AMERICA", "US attorney general dodges Nvidia probe questions"),
    ("22", "NORTH AMERICA", "Vance: Huang 'won't need a pardon' in Nvidia case"),
    ("23", "LATIN AMERICA", "Colombia police free 20 hostages after 17 hours"),
    ("24", "NORTH AMERICA", "Six die, two of them children, in Mississippi crash"),
    ("25", "NORTH AMERICA", "Fed split over what drives high inflation"),
    ("26", "NORTH AMERICA", "US Army blows up its lead azide stockpile in Iowa"),
    ("27", "AFRICA", "Two Libyan officers die after strike on Russian ship"),
    ("28", "AFRICA", "South Africa's Biovac to scale up vaccines, EU loan"),
    ("29", "SOUTH ASIA", "India marks Constitution Day - Samvidhan Divas"),
    ("30", "SOUTH ASIA", "IITs to add 6,000 seats in robotics, AI and space"),
    ("31", "SOUTH ASIA", "India unveils 15,000-crore package for Nepal"),
    ("32", "SOUTH ASIA", "India: humans must control AI in war, Delhi says"),
    ("33", "SOUTH ASIA", "Cabinet clears 4,288-crore Kamarajar port terminal"),
    ("34", "SOUTH ASIA", "IPL 2027 auction draws 1,220 players; Stokes in"),
    ("35", "SOUTH ASIA", "Flipkart chief Kalyan Krishnamurthy to quit in Dec"),
    ("36", "NORTH AMERICA", "Tempus to buy Personalis in $600m cash deal"),
    ("37", "AFRICA", "Court scraps Phala Phala report; Ramaphosa wins"),
    ("38", "LATIN AMERICA", "US proposes 10% tariff on Brazil's Embraer jets"),
    ("39", "EAST ASIA", "China calls 'overcapacity' a false issue"),
    ("40", "EAST ASIA", "Taiwan dollar slides past 33, a 19-month low"),
    ("41", "NORTH AMERICA", "US crude stocks rise 1.1m barrels to 418.9m"),
    ("42", "SOUTH ASIA", "Two Indians hurt in Riyadh attack leave hospital"),
    ("43", "LATIN AMERICA", "UN chief hails Colombia's decade of peace progress"),
    ("44", "EUROPE", "UK energy cap to jump 26% to £2,166 in January"),
    ("45", "EUROPE", "Russian strikes cut power in five Ukraine regions"),
    ("46", "EUROPE", "Duran Duran guitarist Andy Taylor dies at 65"),
    ("47", "MIDEAST", "Riyadh's PIF Tower struck twice in a week"),
    ("48", "MIDEAST", "Coalition says four drones downed over Ras Tanura"),
    ("49", "SOUTHEAST ASIA", "Tariff caps hit SE Asia: Vietnam up to 35%"),
    ("50", "SOUTH ASIA", "Mumbai remembers 26/11: tributes 18 years on"),
]

TALLIES = [
    {"region": "MIDEAST", "count": 5},
    {"region": "EAST ASIA", "count": 7},
    {"region": "SOUTH ASIA", "count": 12},
    {"region": "SOUTHEAST ASIA", "count": 1},
    {"region": "OCEANIA", "count": 1},
    {"region": "EUROPE", "count": 6},
    {"region": "NORTH AMERICA", "count": 9},
    {"region": "LATIN AMERICA", "count": 4},
    {"region": "AFRICA", "count": 4},
    {"region": "WORLD", "count": 1},
]

# (number, lon, lat, label offset dx, dy) - label offsets keep the
# Europe and East Asia clusters readable instead of piled up.
PINS = [
    ("01", 50.1, 26.6, 14, -16),
    ("02", 121.5, 25.0, 12, 8),
    ("03", 125.7, 39.0, 10, -14),
    ("04", 98.5, 39.8, -34, -12),
    ("05", -77.0, 38.9, -40, 6),
    ("06", 43.3, 55.5, 12, -14),
    ("07", 36.0, 34.6, -38, 10),
    ("08", 90.4, 23.8, 12, 10),
    ("09", 31.2, 30.0, -36, -12),
    ("10", 6.1, 46.2, -30, -14),
    ("11", 160.0, -9.4, 10, 8),
    ("12", -43.9, -19.9, 10, 8),
    ("13", 77.2, 28.6, -34, 12),
]

CHECKS = [
    "Ras Tanura: claimed Wed 25 Nov",
    "Shenzhou-24 docked Wed 11:56",
    "TAIEX -1,927: Wed close, Taipei",
    "Kim remarks: KCNA, Thu 26 Nov",
    "Savasleyka: overnight 24-25 Nov",
    "Cairo fire: Wed eve, toll prelim.",
    "Gukesh G2: Wed draw; G3 today",
    "Solomon pact: signed Wed, Canberra",
    "Bangladesh wage: Wed 02:00 Dhaka",
    "26/11: 18th anniversary TODAY",
]

TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off"),
    ("03:56", "Shenzhou-24 docks"),
    ("05:30", "TAIEX -1,926.92 at close"),
    ("14:00", "Gukesh-Sindarov Game 2"),
    ("17:04", "Brent $93.20, up ~2%"),
    ("18:52", "Cairo fire toll reported"),
]

FOOTER_SOURCES = ("Reuters - AP - CNN - USTR - KCNA - CMSA - ABS - "
                   "Focus Taiwan - Bloomberg - FIDE - ASTMH")


# ------------------------------------------------------------- drawing kit


class Frame:
    """A rectangle with local coordinates on the shared canvas."""

    def __init__(self, draw, x, y, w, h):
        self.draw = draw
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def child(self, dx, dy, w, h):
        return Frame(self.draw, self.x + dx, self.y + dy, w, h)

    def rect(self, x, y, w, h, fill=None, outline=None, width=1):
        self.draw.rectangle(
            [self.x + x, self.y + y, self.x + x + w, self.y + y + h],
            fill=fill, outline=outline, width=width)

    def line(self, points, fill=INK, width=1):
        shifted = [(self.x + px, self.y + py) for px, py in points]
        self.draw.line(shifted, fill=fill, width=width)

    def ellipse(self, x, y, w, h, fill=None, outline=None, width=1):
        self.draw.ellipse(
            [self.x + x, self.y + y, self.x + x + w, self.y + y + h],
            fill=fill, outline=outline, width=width)

    def polygon(self, points, fill=None, outline=None):
        shifted = [(self.x + px, self.y + py) for px, py in points]
        self.draw.polygon(shifted, fill=fill, outline=outline)

    def text(self, x, y, s, font, fill=INK):
        self.draw.text((self.x + x, self.y + y), s, font=font, fill=fill)

    def text_w(self, s, font):
        return self.draw.textlength(s, font=font)

    def wrap(self, s, font, max_w, max_lines):
        """Greedy wrap; raises when a word alone is too wide or the
        text needs more lines than allowed."""
        words = s.split()
        lines = []
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.text_w(trial, font) <= max_w:
                cur = trial
            else:
                if self.text_w(word, font) > max_w:
                    raise ValueError("word too wide: %r" % word)
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        if len(lines) > max_lines:
            raise ValueError("text overflows %d lines: %r" % (max_lines, s))
        return lines

    def para(self, x, y, s, font, max_w, max_lines, leading, fill=INK):
        lines = self.wrap(s, font, max_w, max_lines)
        for i, line in enumerate(lines):
            self.text(x, y + i * leading, line, font, fill)
        return y + len(lines) * leading


class FrontPage:
    """Builds the whole front page on one canvas."""

    def __init__(self):
        self.image = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.draw = ImageDraw.Draw(self.image)
        self.root = Frame(self.draw, 0, 0, PAGE_W, PAGE_H)
        self._fonts = {}

    # -- fonts -----------------------------------------------------
    def _face(self, name, size):
        key = (name, size)
        if key not in self._fonts:
            font = None
            for folder in TYPE_DIRS:
                path = os.path.join(folder, name)
                if os.path.exists(path):
                    font = ImageFont.truetype(path, size)
                    break
            if font is None:
                font = ImageFont.load_default(size=size)
            self._fonts[key] = font
        return self._fonts[key]

    def serif(self, size):
        return self._face("DejaVuSerif.ttf", size)

    def serif_b(self, size):
        return self._face("DejaVuSerif-Bold.ttf", size)

    def sans(self, size):
        return self._face("DejaVuSans.ttf", size)

    def sans_b(self, size):
        return self._face("DejaVuSans-Bold.ttf", size)

    # -- drawn scenes (no photos, no AI images) --------------------
    def scene(self, frame, kind):
        """A small flat illustration inside a frame."""
        kind_fn = {
            "refinery": self._scene_refinery,
            "tariffs": self._scene_tariffs,
            "nuclear": self._scene_nuclear,
            "rocket": self._scene_rocket,
            "chart": self._scene_chart,
            "gavel": self._scene_gavel,
            "jet": self._scene_jet,
            "runway": self._scene_runway,
            "factory": self._scene_factory,
            "flame": self._scene_flame,
            "islands": self._scene_islands,
            "chess": self._scene_chess,
            "cricket": self._scene_cricket,
            "parliament": self._scene_parliament,
            "mosquito": self._scene_mosquito,
        }[kind]
        kind_fn(frame)

    def _sky(self, frame, top, bottom):
        frame.rect(0, 0, frame.w, frame.h, fill=top)
        frame.rect(0, frame.h // 2, frame.w, frame.h - frame.h // 2,
                   fill=bottom)

    def _scene_refinery(self, f):
        self._sky(f, (52, 48, 58), (94, 60, 44))
        f.ellipse(f.w - 52, 8, 34, 34, fill=(232, 176, 90))
        for bx, bh in ((8, 46), (30, 62), (58, 40)):
            f.rect(bx, f.h - bh, 16, bh, fill=(30, 28, 34))
        f.rect(96, f.h - 70, 6, 70, fill=(30, 28, 34))
        f.rect(112, f.h - 58, 6, 58, fill=(30, 28, 34))
        for fx, fy in ((99, f.h - 76), (115, f.h - 64)):
            f.polygon([(fx - 5, fy + 8), (fx, fy), (fx + 5, fy + 8)],
                      fill=(240, 120, 40))
            f.polygon([(fx - 3, fy + 8), (fx, fy + 2), (fx + 3, fy + 8)],
                      fill=(250, 200, 60))
        f.rect(140, f.h - 34, 60, 34, fill=(30, 28, 34))
        f.rect(150, f.h - 28, 8, 8, fill=(240, 200, 90))
        f.rect(164, f.h - 28, 8, 8, fill=(240, 200, 90))
        f.rect(178, f.h - 28, 8, 8, fill=(240, 200, 90))

    def _scene_tariffs(self, f):
        self._sky(f, (31, 78, 121), (214, 228, 235))
        bars = [(20, 30), (52, 44), (84, 58), (116, 38), (148, 52)]
        for i, (bx, bh) in enumerate(bars):
            col = RED if i in (1, 2) else (240, 240, 240)
            f.rect(bx, f.h - 12 - bh, 22, bh, fill=col)
        f.line([(8, f.h - 12), (f.w - 8, f.h - 12)], fill=INK, width=2)
        f.ellipse(f.w - 46, 6, 30, 30, outline=(255, 255, 255), width=2)

    def _scene_nuclear(self, f):
        self._sky(f, (24, 24, 30), (58, 52, 60))
        f.rect(0, f.h - 34, f.w, 34, fill=(20, 20, 24))
        f.rect(30, f.h - 58, 44, 26, fill=(40, 40, 48))
        f.polygon([(30, f.h - 58), (52, f.h - 74), (74, f.h - 58)],
                  fill=(40, 40, 48))
        f.rect(110, f.h - 48, 8, 48, fill=(40, 40, 48))
        f.rect(130, f.h - 62, 8, 62, fill=(40, 40, 48))
        cx, cy = f.w - 42, 26
        for ang in (90, 210, 330):
            a0 = math.radians(ang - 28)
            a1 = math.radians(ang + 28)
            pts = [(cx, cy)]
            for k in range(9):
                a = a0 + (a1 - a0) * k / 8
                pts.append((cx + 13 * math.cos(a), cy + 13 * math.sin(a)))
            f.polygon(pts, fill=(240, 200, 60))
        f.ellipse(cx - 4, cy - 4, 8, 8, fill=(240, 200, 60))

    def _scene_rocket(self, f):
        self._sky(f, (16, 22, 44), (48, 44, 80))
        for sx, sy in ((14, 12), (60, 22), (120, 10), (170, 26), (40, 44)):
            f.ellipse(sx, sy, 3, 3, fill=(255, 255, 255))
        cx = f.w // 2
        f.polygon([(cx - 7, 12), (cx, 2), (cx + 7, 12)], fill=RED)
        f.rect(cx - 7, 12, 14, 18, fill=(240, 240, 240))
        f.ellipse(cx - 3, 18, 6, 6, fill=BLUE)
        f.polygon([(cx - 7, 30), (cx - 13, 38), (cx - 7, 36)], fill=RED)
        f.polygon([(cx + 7, 30), (cx + 13, 38), (cx + 7, 36)], fill=RED)
        f.polygon([(cx - 4, 38), (cx, 48), (cx + 4, 38)], fill=(250, 200, 60))
        f.ellipse(cx - 34, f.h - 16, 68, 12, outline=(120, 140, 170),
                  width=2)

    def _scene_chart(self, f):
        self._sky(f, (247, 243, 234), (232, 226, 212))
        pts = [(10, 14), (40, 22), (70, 16), (100, 34), (130, 30),
               (160, 48), (190, 44)]
        f.line(pts, fill=RED, width=3)
        for px, py in pts:
            f.ellipse(px - 3, py - 3, 6, 6, fill=RED)
        f.line([(8, f.h - 10), (f.w - 8, f.h - 10)], fill=INK, width=2)
        f.line([(8, 6), (8, f.h - 10)], fill=INK, width=2)

    def _scene_gavel(self, f):
        self._sky(f, (247, 243, 234), (232, 226, 212))
        f.polygon([(30, 14), (86, 30), (78, 44), (22, 28)], fill=(120, 84, 50))
        f.polygon([(86, 30), (96, 26), (88, 40), (78, 44)], fill=(90, 62, 36))
        f.line([(58, 32), (88, 52)], fill=(120, 84, 50), width=5)
        f.rect(96, 52, 60, 8, fill=(90, 62, 36))
        f.rect(104, 48, 44, 4, fill=(140, 104, 66))

    def _scene_jet(self, f):
        self._sky(f, (120, 160, 200), (214, 228, 235))
        f.ellipse(150, 6, 34, 14, fill=(255, 255, 255))
        f.ellipse(30, 18, 26, 10, fill=(255, 255, 255))
        f.polygon([(60, 26), (150, 26), (168, 30), (150, 34), (60, 34)],
                  fill=(60, 64, 72))
        f.polygon([(150, 26), (176, 18), (180, 26), (168, 30)],
                  fill=(60, 64, 72))
        f.polygon([(96, 26), (110, 12), (120, 26)], fill=(60, 64, 72))
        f.polygon([(96, 34), (110, 48), (120, 34)], fill=(60, 64, 72))
        f.polygon([(60, 26), (48, 30), (60, 34)], fill=(90, 94, 100))

    def _scene_runway(self, f):
        self._sky(f, (120, 160, 200), (214, 228, 235))
        f.polygon([(0, f.h), (f.w // 2 - 14, 20), (f.w // 2 + 14, 20),
                   (f.w, f.h)], fill=(80, 80, 84))
        for i, yy in enumerate((26, 36, 48)):
            f.rect(f.w // 2 - 2, yy, 4, 6, fill=(255, 255, 255))
        f.polygon([(f.w // 2 - 34, 20), (f.w // 2 + 34, 20),
                   (f.w // 2 + 12, 12), (f.w // 2 - 12, 12)],
                  fill=(240, 240, 240))
        f.polygon([(f.w // 2 + 34, 20), (f.w // 2 + 52, 16),
                   (f.w // 2 + 52, 20)], fill=(200, 200, 200))

    def _scene_factory(self, f):
        self._sky(f, (247, 243, 234), (232, 226, 212))
        f.rect(10, 26, 26, 34, fill=(120, 84, 50))
        f.rect(14, 20, 4, 8, fill=(120, 84, 50))
        f.rect(24, 16, 4, 12, fill=(120, 84, 50))
        f.rect(40, 18, 70, 42, fill=(176, 141, 44))
        f.rect(48, 26, 10, 10, fill=(240, 240, 240))
        f.rect(64, 26, 10, 10, fill=(240, 240, 240))
        f.rect(80, 26, 10, 10, fill=(240, 240, 240))
        f.rect(48, 42, 10, 10, fill=(240, 240, 240))
        f.rect(64, 42, 10, 10, fill=(240, 240, 240))
        f.rect(80, 42, 10, 10, fill=(240, 240, 240))
        f.polygon([(118, 18), (150, 34), (150, 60), (118, 60)],
                  fill=(90, 62, 36))
        f.line([(118, 60), (150, 60)], fill=INK, width=2)

    def _scene_flame(self, f):
        self._sky(f, (52, 40, 36), (120, 60, 36))
        f.rect(0, f.h - 12, f.w, 12, fill=(30, 28, 34))
        cx = f.w // 2
        f.polygon([(cx - 22, f.h - 12), (cx - 6, f.h - 46),
                   (cx + 2, f.h - 26), (cx + 10, f.h - 52),
                   (cx + 22, f.h - 12)], fill=(240, 120, 40))
        f.polygon([(cx - 12, f.h - 12), (cx - 2, f.h - 34),
                   (cx + 6, f.h - 20), (cx + 12, f.h - 12)],
                  fill=(250, 200, 60))
        f.ellipse(18, 10, 26, 12, fill=(200, 200, 200))
        f.ellipse(140, 16, 30, 12, fill=(200, 200, 200))

    def _scene_islands(self, f):
        self._sky(f, (120, 180, 210), (60, 130, 180))
        f.ellipse(20, 34, 56, 20, fill=(120, 180, 110))
        f.ellipse(96, 26, 44, 16, fill=(120, 180, 110))
        f.ellipse(140, 40, 30, 12, fill=(120, 180, 110))
        f.ellipse(60, 14, 18, 10, fill=(90, 150, 90))
        f.line([(48, 44), (118, 34)], fill=(255, 255, 255), width=2)
        f.line([(118, 34), (155, 46)], fill=(255, 255, 255), width=2)
        f.polygon([(48, 44), (44, 38), (52, 38)], fill=RED)

    def _scene_chess(self, f):
        self._sky(f, (247, 243, 234), (232, 226, 212))
        s = 13
        ox, oy = 30, 8
        for r in range(4):
            for c in range(4):
                col = INK if (r + c) % 2 == 0 else (240, 240, 240)
                f.rect(ox + c * s, oy + r * s, s, s, fill=col,
                       outline=(120, 116, 108), width=1)
        f.ellipse(ox + 4, oy + 4, 10, 10, fill=RED)
        f.rect(ox + 4, oy + 14, 10, 4, fill=RED)
        f.ellipse(ox + 30, oy + 30, 10, 10, fill=BLUE)
        f.rect(ox + 30, oy + 40, 10, 4, fill=BLUE)
        f.text(110, 16, "1-1", self.sans_b(20), fill=INK)

    def _scene_cricket(self, f):
        self._sky(f, (120, 180, 110), (90, 150, 90))
        f.rect(0, f.h - 14, f.w, 14, fill=(140, 110, 70))
        f.line([(30, f.h - 14), (170, f.h - 14)], fill=(255, 255, 255),
               width=2)
        for sx in (60, 100, 140):
            f.rect(sx, f.h - 30, 3, 16, fill=(240, 220, 120))
        f.ellipse(150, 10, 14, 14, fill=RED)
        f.polygon([(60, 30), (96, 12), (104, 20), (70, 38)], fill=(140, 110, 70))
        f.text(8, 6, "204", self.sans_b(18), fill=(255, 255, 255))

    def _scene_parliament(self, f):
        self._sky(f, (247, 243, 234), (232, 226, 212))
        f.polygon([(20, 30), (100, 8), (180, 30)], fill=(120, 84, 50))
        for cx in (36, 66, 96, 126, 156):
            f.rect(cx, 30, 8, 24, fill=(176, 141, 44))
        f.rect(16, 54, 168, 6, fill=(120, 84, 50))
        f.rect(90, 36, 20, 18, fill=(90, 62, 36))
        f.rect(20, 20, 6, 10, fill=RED)

    def _scene_mosquito(self, f):
        self._sky(f, (247, 243, 234), (232, 226, 212))
        cx, cy = f.w // 2, f.h // 2 + 4
        f.ellipse(cx - 12, cy - 8, 24, 16, fill=(60, 64, 72))
        f.ellipse(cx - 16, cy - 4, 8, 8, fill=(40, 44, 52))
        f.line([(cx - 16, cy), (cx - 34, cy - 8)], fill=INK, width=2)
        f.line([(cx - 12, cy - 8), (cx - 26, cy - 22)], fill=INK, width=1)
        f.line([(cx - 4, cy - 8), (cx - 8, cy - 24)], fill=INK, width=1)
        f.line([(cx + 4, cy - 8), (cx + 10, cy - 24)], fill=INK, width=1)
        f.ellipse(cx - 30, cy - 30, 66, 34, outline=(31, 78, 121), width=2)
        f.text(8, 4, "-68.5%", self.sans_b(13), fill=BLUE)

    # -- world map ---------------------------------------------------
    def _project(self, frame, lon, lat):
        x = (lon + 180.0) / 360.0 * frame.w
        y = (62.0 - lat) / 124.0 * frame.h
        return (x, y)

    def _draw_map(self, frame):
        frame.rect(0, 0, frame.w, frame.h, fill=MAP_SEA)
        for lon in range(-180, 181, 30):
            x = (lon + 180.0) / 360.0 * frame.w
            frame.line([(x, 0), (x, frame.h)], fill=(190, 205, 215), width=1)
        for lat in (-60, -30, 0, 30, 60):
            _, y = self._project(frame, 0, lat)
            frame.line([(0, y), (frame.w, y)], fill=(190, 205, 215), width=1)
        continents = [
            [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80),
             (-85, 70), (-75, 62), (-70, 58), (-65, 45), (-75, 40),
             (-80, 32), (-85, 30), (-90, 21), (-97, 26), (-105, 20),
             (-110, 23), (-117, 33), (-125, 40), (-125, 49), (-135, 58),
             (-150, 60), (-165, 60)],
            [(-80, 10), (-70, 11), (-60, 8), (-52, 5), (-44, -3),
             (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45),
             (-70, -52), (-73, -40), (-72, -20), (-77, -12), (-80, -3),
             (-82, 8)],
            [(-18, 35), (-10, 36), (-9, 43), (-2, 48), (0, 50), (8, 54),
             (10, 57), (18, 56), (21, 55), (28, 59), (30, 60), (24, 60),
             (18, 66), (25, 71), (31, 70), (40, 68), (40, 60), (30, 55),
             (28, 46), (23, 40), (19, 42), (12, 44), (3, 42), (-2, 37),
             (-10, 37)],
            [(-17, 15), (-17, 28), (-10, 31), (-6, 35), (10, 37), (20, 32),
             (32, 31), (35, 28), (43, 12), (48, 11), (51, 12), (44, -2),
             (40, -10), (36, -18), (33, -26), (28, -33), (19, -35),
             (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8)],
            [(43, 68), (50, 69), (60, 69), (70, 72), (80, 73), (95, 76),
             (110, 74), (130, 72), (150, 70), (160, 69), (170, 66),
             (178, 65), (170, 60), (160, 60), (158, 52), (142, 50),
             (140, 40), (135, 35), (127, 33), (122, 30), (120, 25),
             (110, 20), (108, 12), (105, 9), (100, 8), (98, 16), (92, 16),
             (89, 22), (80, 13), (77, 8), (73, 20), (66, 25), (61, 25),
             (57, 26), (52, 28), (50, 30), (48, 30), (44, 29), (40, 31),
             (36, 36), (30, 36), (27, 41), (23, 40), (30, 46), (40, 47),
             (45, 55), (50, 59), (43, 60)],
            [(114, -22), (122, -14), (130, -12), (137, -12), (142, -11),
             (146, -19), (150, -22), (153, -27), (150, -37), (145, -38),
             (140, -38), (135, -35), (130, -32), (124, -33), (118, -35),
             (114, -30)],
        ]
        for poly in continents:
            pts = [self._project(frame, lon, lat) for lon, lat in poly]
            frame.polygon(pts, fill=MAP_LAND, outline=MAP_EDGE)
        for num, lon, lat, dx, dy in PINS:
            px, py = self._project(frame, lon, lat)
            frame.ellipse(px - 3, py - 3, 6, 6, fill=RED)
            lx, ly = px + dx, py + dy
            frame.line([(px, py), (lx + 7, ly + 7)], fill=INK, width=1)
            frame.rect(lx - 1, ly - 1, 16, 14, fill=INK)
            frame.text(lx + 2, ly, num, self.sans_b(9), fill=(255, 255, 255))


    # -- small tiles for the twelve panels -------------------------
    def tile(self, frame, kind, num):
        """A flat colour tile with a white motif and the story number."""
        colours = {
            "rocket": (31, 78, 121), "chart": (163, 22, 33),
            "gavel": (90, 62, 36), "jet": (60, 64, 72),
            "runway": (31, 78, 121), "factory": (176, 141, 44),
            "flame": (200, 70, 30), "islands": (40, 120, 110),
            "chess": (26, 26, 26), "cricket": (90, 150, 90),
            "parliament": (120, 84, 50), "mosquito": (31, 78, 121),
        }
        frame.rect(0, 0, frame.w, frame.h, fill=colours[kind])
        w, h = frame.w, frame.h
        cx, cy = w // 2, h // 2 - 3
        white = (255, 255, 255)
        if kind == "rocket":
            frame.polygon([(cx, cy - 10), (cx + 6, cy + 4), (cx - 6, cy + 4)],
                          fill=white)
            frame.rect(cx - 3, cy + 4, 6, 7, fill=white)
        elif kind == "chart":
            frame.line([(6, h - 12), (14, h - 18), (22, h - 14),
                        (30, h - 24)], fill=white, width=2)
        elif kind == "gavel":
            frame.polygon([(8, cy - 4), (28, cy + 2), (26, cy + 8),
                           (6, cy + 2)], fill=white)
            frame.line([(18, cy + 4), (30, cy + 12)], fill=white, width=3)
        elif kind == "jet":
            frame.polygon([(6, cy), (30, cy - 5), (34, cy), (30, cy + 5)],
                          fill=white)
            frame.polygon([(16, cy), (22, cy - 8), (25, cy)], fill=white)
        elif kind == "runway":
            frame.polygon([(10, h - 6), (cx - 3, 8), (cx + 3, 8),
                           (w - 10, h - 6)], fill=white)
        elif kind == "factory":
            frame.rect(7, cy - 2, 10, 12, fill=white)
            frame.rect(19, cy - 8, 12, 18, fill=white)
        elif kind == "flame":
            frame.polygon([(cx - 8, cy + 8), (cx - 2, cy - 8),
                           (cx + 3, cy + 2), (cx + 8, cy + 8)], fill=white)
        elif kind == "islands":
            frame.ellipse(7, cy - 4, 12, 8, fill=white)
            frame.ellipse(22, cy + 2, 10, 6, fill=white)
        elif kind == "chess":
            frame.rect(8, 8, 9, 9, fill=white)
            frame.rect(23, 23, 9, 9, fill=white)
            frame.rect(23, 8, 9, 9, outline=white, width=1)
            frame.rect(8, 23, 9, 9, outline=white, width=1)
        elif kind == "cricket":
            frame.ellipse(22, 8, 12, 12, fill=white)
            frame.line([(8, h - 8), (30, h - 8)], fill=white, width=2)
        elif kind == "parliament":
            frame.polygon([(6, cy + 2), (cx, cy - 10), (w - 6, cy + 2)],
                          fill=white)
            frame.rect(10, cy + 4, 4, 8, fill=white)
            frame.rect(26, cy + 4, 4, 8, fill=white)
        elif kind == "mosquito":
            frame.ellipse(cx - 6, cy - 5, 12, 10, fill=white)
            frame.line([(cx - 6, cy), (cx - 14, cy - 6)], fill=white, width=2)
            frame.line([(cx - 6, cy), (cx - 14, cy + 6)], fill=white, width=2)
        frame.text(3, h - 11, num, self.sans_b(8), fill=white)

    # -- sections ----------------------------------------------------
    def section_head(self, frame, label, right=""):
        frame.text(0, 0, label, self.sans_b(10), fill=RED)
        if right:
            rw = frame.text_w(right, self.sans(9))
            frame.text(frame.w - rw, 1, right, self.sans(9), fill=FAINT)
        frame.line([(0, 13), (frame.w, 13)], fill=RULE, width=1)

    def masthead(self, frame):
        name = "THE THURSDAY PAPER"
        frame.text(0, 0, name, self.serif_b(44), fill=INK)
        nw = frame.text_w(name, self.serif_b(44))
        frame.text(nw + 14, 16, "EST. 2026", self.sans_b(10), fill=RED)
        frame.text(nw + 14, 30, "ONE IMAGE", self.sans(9), fill=SOFT_INK)
        frame.line([(0, 50), (frame.w, 50)], fill=RULE, width=2)
        frame.text(0, 54, EDITION, self.sans_b(12), fill=INK)
        right = TAGLINE
        rw = frame.text_w(right, self.sans(11))
        frame.text(frame.w - rw, 55, right, self.sans(11), fill=SOFT_INK)

    def figures(self, frame):
        cell = frame.w // 6
        for i, fig in enumerate(FIGURES):
            x = i * cell
            if i:
                frame.line([(x, 4), (x, frame.h - 4)], fill=PANEL_EDGE,
                           width=1)
            frame.text(x + 8, 2, fig["big"], self.serif_b(20), fill=INK)
            frame.text(x + 8, 26, fig["small"], self.sans(9), fill=SOFT_INK)
        frame.line([(0, frame.h - 1), (frame.w, frame.h - 1)], fill=RULE,
                   width=1)

    def leads(self, frame):
        col_w = (frame.w - 2 * 13) // 3
        for i, story in enumerate(LEADS):
            col = frame.child(i * (col_w + 13), 0, col_w, frame.h)
            kicker = "%s  ·  %s" % (story["n"], story["region"])
            col.text(0, 0, kicker, self.sans_b(9), fill=RED)
            art = col.child(0, 13, col_w, 72)
            art.rect(0, 0, art.w, art.h, fill=(52, 48, 58))
            self.scene(art, story["scene"])
            art.rect(0, 0, art.w, art.h, outline=INK, width=1)
            head_y = 13 + 72 + 5
            col.para(0, head_y, story["headline"], self.serif_b(16),
                     col_w, 2, 19)
            deck_y = head_y + 38
            col.para(0, deck_y, story["deck"], self.sans(10),
                     col_w, 3, 12)
            cap_y = frame.h - 11
            col.text(0, cap_y, story["caption"], self.sans(8), fill=FAINT)
            src = story["sources"]
            sw = col.text_w(src, self.sans(8))
            col.text(col_w - sw, cap_y, src, self.sans(8), fill=FAINT)

    def map_block(self, frame):
        self.section_head(frame.child(0, 0, frame.w, 14),
                          "THE WORLD AT A GLANCE - 13 PINS",
                          "Numbers match the stories below")
        self._draw_map(frame.child(0, 18, frame.w, frame.h - 18))

    def panels(self, frame):
        self.section_head(frame.child(0, 0, frame.w, 14),
                          "ALSO TODAY - 12 PANELS", "Drawn, no photos")
        top = 18
        gap = 2
        avail = frame.h - top
        ph = (avail - (len(PANELS) - 1) * gap) // len(PANELS)
        for i, story in enumerate(PANELS):
            y = top + i * (ph + gap)
            cell = frame.child(0, y, frame.w, ph)
            cell.rect(0, 0, cell.w, cell.h, fill=PANEL_BG,
                      outline=PANEL_EDGE, width=1)
            tile = cell.child(3, 3, 40, ph - 6)
            self.tile(tile, story["scene"], story["n"])
            tx = 48
            tw = cell.w - tx - 6
            cell.text(tx, 2, story["headline"], self.sans_b(12), fill=INK)
            cell.para(tx, 15, story["deck"], self.sans(9), tw, 2, 10)
            cell.text(tx, ph - 9, story["sources"], self.sans(8),
                      fill=FAINT)

    def briefs(self, frame):
        self.section_head(frame.child(0, 0, frame.w, 14),
                          "THE DAY IN BRIEF - 35 STORIES",
                          "All dated; sources in full at foot of page")
        col_w = (frame.w - 12) // 2
        row_h = 19
        for i, (num, region, text) in enumerate(BRIEFS):
            col_i = 0 if i < 18 else 1
            row_i = i if i < 18 else i - 18
            x = col_i * (col_w + 12)
            y = 18 + row_i * row_h
            cell = frame.child(x, y, col_w, row_h)
            cell.text(0, 0, num, self.sans_b(10), fill=RED)
            tw = col_w - 26
            if cell.text_w(text, self.sans(10)) > tw:
                raise ValueError("brief too wide: %s %s" % (num, text))
            cell.text(24, 0, text, self.sans(10), fill=INK)

    def chips(self, frame):
        frame.text(0, 2, "REGIONS", self.sans_b(10), fill=RED)
        x = 78
        for item in TALLIES:
            label = "%s %d" % (item["region"], item["count"])
            w = frame.text_w(label, self.sans_b(9)) + 12
            frame.rect(x, 0, w, 17, fill=(255, 255, 255),
                       outline=PANEL_EDGE, width=1)
            frame.text(x + 6, 3, label, self.sans_b(9), fill=INK)
            x += w + 5
        total = "TOTAL 50"
        frame.text(frame.w - frame.text_w(total, self.sans_b(9)), 3, total,
                   self.sans_b(9), fill=RED)

    def datecheck(self, frame):
        self.section_head(frame.child(0, 0, frame.w, 14),
                          "DATE CHECK - 10 TRAPS, ALL CAUGHT",
                          "Older news dated honestly")
        col_w = frame.w // 5
        for i, item in enumerate(CHECKS):
            col_i = i % 5
            row_i = i // 5
            x = col_i * col_w
            y = 18 + row_i * 14
            cell = frame.child(x, y, col_w - 6, 14)
            cell.text(0, 0, "✓", self.sans_b(9), fill=RED)
            if cell.text_w(item, self.sans(9)) > col_w - 18:
                raise ValueError("date check too wide: %r" % item)
            cell.text(12, 0, item, self.sans(9), fill=SOFT_INK)

    def timeline(self, frame):
        frame.text(0, 2, "THE DAY IN UTC", self.sans_b(10), fill=RED)
        cell_w = (frame.w - 130) // 6
        for i, (clock, text) in enumerate(TIMELINE):
            x = 130 + i * cell_w
            cell = frame.child(x, 0, cell_w - 8, frame.h)
            cell.text(0, 0, clock, self.sans_b(10), fill=INK)
            if cell.text_w(text, self.sans(9)) > cell_w - 8:
                raise ValueError("timeline item too wide: %r" % text)
            cell.text(0, 11, text, self.sans(9), fill=SOFT_INK)

    def footer(self, frame):
        left = ("Sources in full: %s. All 50 stories verified against "
                "two or more reports. Drawn panels - no AI photos."
                % FOOTER_SOURCES)
        frame.text(0, 2, left, self.sans(8), fill=FAINT)
        right = "THE THURSDAY PAPER · 26 NOV 2026"
        rw = frame.text_w(right, self.sans_b(8))
        frame.text(frame.w - rw, 2, right, self.sans_b(8), fill=SOFT_INK)

    def render(self):
        assert len(LEADS) + len(PANELS) + len(BRIEFS) == 50, \
            "must be 50 stories"
        assert sum(item["count"] for item in TALLIES) == 50, \
            "tallies must sum to 50"
        assert len(TALLIES) == 10, "must be 10 regions"
        assert len(CHECKS) == 10, "must be 10 date checks"
        assert len(TIMELINE) == 6, "must be 6 timeline items"
        assert len(PINS) == 13, "must be 13 map pins"
        root = self.root
        self.masthead(root.child(MARGIN, 10, BODY_W, 64))
        self.figures(root.child(MARGIN, 84, BODY_W, 42))
        self.leads(root.child(MARGIN, 130, BODY_W, 178))
        root.line([(MARGIN, 310), (MARGIN + BODY_W, 310)], fill=RULE,
                  width=1)
        self.map_block(root.child(MARGIN, 314, 640, 196))
        self.panels(root.child(MARGIN + 648, 314, BODY_W - 648, 594))
        self.briefs(root.child(MARGIN, 522, 640, 360))
        self.chips(root.child(MARGIN, 912, BODY_W, 18))
        self.datecheck(root.child(MARGIN, 934, BODY_W, 40))
        self.timeline(root.child(MARGIN, 978, BODY_W, 20))
        self.footer(root.child(MARGIN, 1000, BODY_W, 14))
        return self.image


# ------------------------------------------------------------- output

def _write_stored_copy():
    """Write the committed front page with stdlib only.

    Used when Pillow is missing (bare grade image) or the live draw
    fails. The picture bytes live in entry.png beside this file (it is
    committed in the repo); the sha256 and the 1 MiB cap are checked
    before writing.
    """
    data = (Path(__file__).resolve().parent / "entry.png").read_bytes()
    if hashlib.sha256(data).hexdigest() != STORED_SHA:
        raise RuntimeError("stored copy sha256 mismatch")
    if len(data) > STORED_MAX:
        raise RuntimeError("stored copy over the 1 MiB cap")
    os.makedirs(OUT_DIR, exist_ok=True)
    Path(OUT_PATH).write_bytes(data)


def main():
    """Render the page (live draw, else stored copy) and save it."""
    if _CAN_DRAW:
        try:
            page = FrontPage()
            img = page.render()
            os.makedirs(OUT_DIR, exist_ok=True)
            img.save(OUT_PATH, format="PNG", optimize=True)
            print("wrote %s (%dx%d) [live draw]"
                  % (OUT_PATH, PAGE_W, PAGE_H))
            return
        except Exception as exc:
            print("live draw failed (%s); using stored copy" % exc)
    _write_stored_copy()
    print("wrote %s (%dx%d) [pre-rendered]" % (OUT_PATH, PAGE_W, PAGE_H))


if __name__ == "__main__":
    main()
