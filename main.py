#!/usr/bin/env python3
"""news-image-20261124 round 2: Tuesday 24 November 2026 in one picture.

Stdlib-only Python 3.13. Renders one 1024x1024 PNG (zlib+struct, no Pillow,
no third-party imports, no fonts on disk -- hand-authored 5x7 bitmap font).
Deterministic: two runs produce identical bytes.

FIX vs round 1: round 1 exited 1 in the grader because MAKEFUN_OUTPUT_DIR
did not exist yet and the file was opened without creating it. This program
calls os.makedirs(MAKEFUN_OUTPUT_DIR, exist_ok=True) before writing.
"""
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (246, 241, 227)
INK = (20, 20, 31)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
RED = (179, 35, 27)
BLUE = (29, 78, 137)
GREEN = (30, 122, 52)
GOLD = (196, 138, 20)
ORANGE = (214, 96, 20)
TEAL = (14, 122, 110)
GREY = (110, 110, 108)
LIGHT = (255, 255, 255)
SEA = (36, 96, 140)
SKY = (214, 226, 238)
PITCH = (46, 139, 67)

# 5x7 bitmap font, authored by hand. Each glyph: 7 rows of 5 bits.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "~": ("00000", "00000", "01101", "10110", "00000", "00000", "00000"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
}


def normalise(s):
    """Uppercase everything and map unsupported glyphs to font glyphs."""
    s = s.upper()
    repl = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
            "\u2014": "-", "\u2013": "-", "\u00d7": "X", "\u00b7": ".",
            "\u2192": ">", "\u2191": "^", "\u2193": "V", "\u20ac": "E",
            "\u00a3": "L", "\u2010": "-", "\u2212": "-"}
    for k, v in repl.items():
        s = s.replace(k, v)
    return "".join(ch if ch in FONT else " " for ch in s)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def polyline(self, pts, c, t=2):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            self.line(x0, y0, x1, y1, c, t)

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d2 <= r * r:
                        self.set(xx, yy, c)
                else:
                    if r * r - 2 * r <= d2 <= r * r:
                        self.set(xx, yy, c)

    def triangle(self, pts, c):
        (x0, y0), (x1, y1), (x2, y2) = pts
        ymin = min(y0, y1, y2)
        ymax = max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                       ((x1, y1), (x2, y2)),
                                       ((x2, y2), (x0, y0))):
                if ay == by:
                    continue
                if min(ay, by) <= yy <= max(ay, by):
                    xs.append(ax + (bx - ax) * (yy - ay) / (by - ay))
            if len(xs) >= 2:
                for xx in range(int(min(xs)), int(max(xs)) + 1):
                    self.set(xx, yy, c)


def text_w(s, scale):
    return len(normalise(s)) * 6 * scale - scale


def draw_char(cv, x, y, ch, scale, c):
    g = FONT.get(ch, FONT[" "])
    for r, row in enumerate(g):
        for col, bit in enumerate(row):
            if bit == "1":
                cv.fill_rect(x + col * scale, y + r * scale, scale, scale, c)


def draw_text(cv, x, y, s, scale, c, bold=False):
    s = normalise(s)
    cx = x
    for ch in s:
        draw_char(cv, cx, y, ch, scale, c)
        if bold:
            draw_char(cv, cx + 1, y, ch, scale, c)
        cx += 6 * scale
    return cx


def draw_text_centered(cv, cx, y, s, scale, c, bold=False):
    draw_text(cv, cx - text_w(s, scale) // 2, y, s, scale, c, bold=bold)


def wrap_lines(s, scale, max_w):
    s = normalise(s)
    lines = []
    cur = ""
    for w in s.split(" "):
        t = (cur + " " + w).strip()
        if text_w(t, scale) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(cv, x, y, s, scale, c, max_w, line_h=None, bold=False):
    if line_h is None:
        line_h = 7 * scale + 2
    lines = wrap_lines(s, scale, max_w)
    for ln in lines:
        draw_text(cv, x, y, ln, scale, c, bold=bold)
        y += line_h
    return y


def png_bytes(w, h, rgb):
    raw = bytearray()
    for yy in range(h):
        raw.append(0)
        raw += rgb[yy * w * 3:(yy + 1) * w * 3]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- scenes
def scene_markets(cv, x, y, w, h):
    """Falling-line chart: Monday's green spike, Tuesday's red slide."""
    cv.fill_rect(x, y, w, h, LIGHT)
    cv.rect(x, y, w, h, INK, 1)
    base = y + h - 14
    cv.line(x + 8, base, x + w - 8, base, GREY, 1)
    cv.line(x + 8, y + 8, x + 8, base, GREY, 1)
    pts_green = [(x + 12, base - 6), (x + 70, base - 10),
                 (x + 130, base - 58), (x + 190, base - 66)]
    cv.polyline(pts_green, GREEN, 3)
    pts_red = [(x + 190, base - 66), (x + 260, base - 40),
               (x + 330, base - 30), (x + 400, base - 18),
               (x + w - 14, base - 12)]
    cv.polyline(pts_red, RED, 3)
    # arrowhead on the red fall
    cv.triangle([(x + w - 14, base - 12), (x + w - 26, base - 20),
                 (x + w - 26, base - 6)], RED)
    draw_text(cv, x + 14, y + 6, "MON +31.5%", 1, GREEN, bold=True)
    draw_text(cv, x + w - 120, y + 8, "TUE -2.0%", 1, RED, bold=True)


def scene_hormuz(cv, x, y, w, h):
    """Tanker ablaze on a blue sea, flames and smoke."""
    cv.fill_rect(x, y, w, h, SKY)
    cv.rect(x, y, w, h, INK, 1)
    sea_y = y + int(h * 0.62)
    cv.fill_rect(x, sea_y, w, h - (sea_y - y), SEA)
    # waves
    for wx in range(x + 6, x + w - 6, 26):
        cv.line(wx, sea_y + 12, wx + 12, sea_y + 12, LIGHT, 2)
    # tanker hull
    hx, hy, hw, hh = x + 60, sea_y - 26, w - 120, 30
    cv.fill_rect(hx, hy, hw, hh, (30, 30, 34))
    cv.fill_rect(hx, hy - 14, 70, 14, (60, 60, 66))       # deck house
    cv.fill_rect(hx + 76, hy - 22, 16, 22, RED)           # funnel
    cv.fill_rect(hx + hw - 24, hy - 8, 18, 8, GOLD)       # stern light
    # flames (kept inside the scene box)
    for fx, fh in ((hx + 90, 20), (hx + 150, 22), (hx + 210, 20),
                   (hx + 270, 18), (hx + 330, 20)):
        cv.triangle([(fx - 16, hy - 2), (fx, hy - fh), (fx + 16, hy - 2)],
                    ORANGE)
        cv.triangle([(fx - 8, hy - 2), (fx, hy - fh + 10), (fx + 8, hy - 2)],
                    GOLD)


def scene_huawei(cv, x, y, w, h):
    """Courthouse columns and the scales of justice."""
    cv.fill_rect(x, y, w, h, LIGHT)
    cv.rect(x, y, w, h, INK, 1)
    base = y + h - 8
    # courthouse on the left (all coordinates relative to scene height)
    bx = x + 16
    cv.fill_rect(bx, base, 120, 6, INK)
    cv.fill_rect(bx + 8, base - 8, 104, 8, INK)
    for cx in (bx + 14, bx + 52, bx + 90):
        cv.fill_rect(cx, base - 34, 10, 26, INK)
    cv.triangle([(bx - 4, base - 34), (bx + 60, base - 52),
                 (bx + 124, base - 34)], NAVY2)
    cv.circle(bx + 60, base - 42, 5, GOLD)
    # scales on the right
    sx = x + w - 130
    cv.line(sx + 40, y + 8, sx + 40, base, INK, 3)
    cv.line(sx + 4, y + 14, sx + 76, y + 14, INK, 3)
    cv.line(sx + 4, y + 14, sx + 4, base - 16, INK, 2)
    cv.line(sx + 76, y + 14, sx + 76, base - 16, INK, 2)
    cv.triangle([(sx - 8, base - 16), (sx + 16, base - 16),
                 (sx + 4, base - 4)], GOLD)
    cv.triangle([(sx + 64, base - 16), (sx + 88, base - 16),
                 (sx + 76, base - 4)], GOLD)
    cv.fill_rect(sx + 24, base, 32, 5, INK)
    draw_text(cv, x + 150, y + h - 18, "10 OF 12 COUNTS", 1, RED, bold=True)


def scene_ucl(cv, x, y, w, h):
    """A football pitch, ball, and the two confirmed full-time scores."""
    cv.fill_rect(x, y, w, h, PITCH)
    cv.rect(x, y, w, h, INK, 1)
    cv.rect(x + 10, y + 8, w - 20, h - 16, LIGHT, 1)
    cv.line(x + w // 2, y + 8, x + w // 2, y + h - 8, LIGHT, 1)
    cv.circle(x + w // 2, y + h // 2, 16, LIGHT, fill=False)
    cv.circle(x + 70, y + h // 2, 11, LIGHT)
    cv.circle(x + 70, y + h // 2, 4, INK)
    cv.circle(x + w - 70, y + h // 2, 11, LIGHT)
    cv.circle(x + w - 70, y + h // 2, 4, INK)
    draw_text(cv, x + 14, y + h - 20, "GAL 1-0 AVL", 1, LIGHT, bold=True)
    draw_text(cv, x + w - 118, y + h - 20, "BOD 1-0 LASK", 1, LIGHT, bold=True)


PRESS = "22:00 UTC"  # hardcoded: the program must stay deterministic

LEADS = [
    dict(title="MARKETS: MONDAY'S RALLY FADES", color=BLUE,
         scene=scene_markets, lines=[
             "TUE CLOSE: NASDAQ -2.0% TO 23,604",
             "S&P -1.0% TO 7,168 - DOW +0.2% 49,678",
             "NVIDIA -8.3% TO $151.37 AFTER MON +31.5%",
             "ASIA: NIKKEI +3.9% 58,654 - KOSPI +7.5%",
         ]),
    dict(title="HORMUZ: 4TH TANKER BURNS", color=RED,
         scene=scene_hormuz, lines=[
             "4TH TANKER HITS A MINE AND BURNS",
             "IN THE STRAIT OF HORMUZ - IRAN SAYS TUE",
             "3 TANKERS ABLAZE EARLIER THE SAME DAY",
         ]),
    dict(title="HUAWEI CONVICTED IN US", color=NAVY2,
         scene=scene_huawei, lines=[
             "US JURY: GUILTY ON 10 OF 12 COUNTS",
             "DECEIVING BANKS OVER IRAN BUSINESS",
             "AND STEALING US TRADE SECRETS",
         ]),
    dict(title="CHAMPIONS LEAGUE - MATCHDAY 5", color=(24, 96, 44),
         scene=scene_ucl, lines=[
             "ARSENAL 1-1 DORTMUND (FT)",
             "MAN CITY 2-2 NAPOLI (FT)",
             "REAL MADRID 5-1 PSV (FT)",
         ]),
]

REGIONS = [
    ("NORTH AMERICA", BLUE, [
        "TRUMP TARIFF PROBE DUE: 16 PARTNERS",
        "CONFIDENCE 103.3 - BEST SINCE JAN 2025",
        "TRUMP SPEEDS EXECUTIONS",
        "STATES SUE MUSK OVER GROK",
        "US DRONE HELPED CATCH EL CHAPO ISIDRO",
    ]),
    ("EUROPE", (106, 63, 160), [
        "SERBIA SCHOOL SHOOTING: 2 HURT, TEEN HELD",
        "SWEDEN TO VOTE 30 NOV ON KRISTERSSON",
        "NATO VOWS TO DEFEND SPACE",
        "490,000 RUSSIAN WAR DEAD, 1,000 SUICIDES",
        "PELICOT SHOCKED BY PHOTOS",
    ]),
    ("MIDDLE EAST", RED, [
        "GAZA: 6 KILLED; 1,675 DEAD SINCE OCT 10",
        "RIYADH FINANCE TOWER HIT IN 'TERRORIST ATTACK'",
        "IRAQ PM TAKES KURDISTAN CROSSINGS",
        "OXFAM: GAZA A 'TOXIC LAND'",
    ]),
    ("ASIA", ORANGE, [
        "CHINA PROBES POLITBURO MEMBER CHEN JINING",
        "CHINA EXTENDS GALLIUM EXPORT PAUSE TO 27 JAN",
        "CHINA DEATH SENTENCE FOR SPYING OFFICIAL MA",
        "N KOREA THREATENS TO CLOSE SWISS OFFICE",
    ]),
    ("SOUTH ASIA", GREEN, [
        "NEPAL 5.3 QUAKE, FELT IN 5 NATIONS, NO DEAD",
        "HASINA SEEKS RETURN; DHAKA: AS PRISONER",
        "BANGLADESH MASS TYPHOID VACCINATION BEGINS",
        "INDIA ARMY SEARCHES AFTER HIMALAYAN FLOOD",
    ]),
    ("AFRICA", (138, 109, 27), [
        "~175 MIGRANTS MISSING AFTER BOAT LOST OFF SENEGAL",
        "SUDAN RSF SPLINTER DEFECTS TO ARMY IN KHARTOUM",
        "TRIPOLI DEMANDS ANSWERS FROM KYIV",
    ]),
    ("LATIN AMERICA", TEAL, [
        "BRAZIL GDP FORECAST CUT TO 1.9%",
        "BUKELE NAMES 3 SOLDIERS KILLED IN HAITI BLAST",
        "HIPPO COVE REOPENS AFTER HURRICANE FIONA",
    ]),
    ("OCEANIA", (74, 107, 138), [
        "AUSTRALIA FM WONG WARNS US-CHINA RIVALRY",
        "STRAINING CONFLICT SAFEGUARDS",
    ]),
    ("WORLD", (51, 51, 51), [
        "UK SANCTIONS HOUTHIS + 4",
        "S&P SEEN AT 8,150 BY END-2027",
        "THAI COURT UPHOLDS MP VERDICT",
        "INDONESIA CANDY FACTORY BODIES",
        "POPE DIARY VISIONS",
    ]),
]


def lead_panel(cv, x, y, w, h, lead):
    cv.fill_rect(x, y, w, h, LIGHT)
    cv.rect(x, y, w, h, INK, 1)
    cv.fill_rect(x, y, w, 26, lead["color"])
    draw_text(cv, x + 8, y + 6, lead["title"], 2, LIGHT, bold=True)
    scene_h = 84 if h > 180 else 64
    lead["scene"](cv, x + 8, y + 34, w - 16, scene_h)
    ty = y + 34 + scene_h + 8
    for ln in lead["lines"]:
        draw_text(cv, x + 8, ty, ln, 2, INK)
        ty += 16


def region_box(cv, x, y, w, h, name, color, stories):
    cv.fill_rect(x, y, w, h, LIGHT)
    cv.rect(x, y, w, h, INK, 1)
    cv.fill_rect(x, y, w, 24, color)
    draw_text(cv, x + 8, y + 5, name, 2, LIGHT, bold=True)
    sy = y + 28
    for s in stories:
        lines = wrap_lines(s, 2, w - 28)
        cv.fill_rect(x + 8, sy + 4, 6, 6, color)
        for ln in lines:
            draw_text(cv, x + 20, sy, ln, 2, INK)
            sy += 15
        sy += 2


def render():
    cv = Canvas(W, H, PAPER)
    # header
    cv.fill_rect(0, 0, W, 88, NAVY)
    draw_text_centered(cv, W // 2, 12, "TUESDAY 24 NOVEMBER 2026", 4,
                       LIGHT, bold=True)
    draw_text_centered(cv, W // 2, 52,
                       "THE WORLD IN ONE PICTURE - 38 STORIES - 9 REGIONS",
                       2, GOLD, bold=True)
    # lead rows
    lead_panel(cv, 8, 94, 500, 198, LEADS[0])
    lead_panel(cv, 516, 94, 500, 198, LEADS[1])
    lead_panel(cv, 8, 300, 500, 162, LEADS[2])
    lead_panel(cv, 516, 300, 500, 162, LEADS[3])
    # region grid: 3 x 3
    for i, (name, color, stories) in enumerate(REGIONS):
        x = 8 + (i % 3) * 338
        y = 470 + (i // 3) * 160
        region_box(cv, x, y, 332, 158, name, color, stories)
    # footer: DATE CHECK
    fy = 956
    draw_text(cv, 8, fy, "DATE CHECK - NOT TODAY, LEFT OUT:", 2, RED, bold=True)
    draw_text(cv, 8, fy + 16,
              "NVDA +31.5% (MON) - IOWA BLAST PAUSE (MON) - IRAN 'ALL TOOLS' (MON)",
              2, INK)
    draw_text(cv, 8, fy + 32,
              "COP31 BACKLASH (MON) - UKRAINE SHIP OFF LIBYA (MON) - ICJ MYANMAR (19 NOV)",
              2, INK)
    draw_text(cv, 8, fy + 48,
              "CHAPO CAPTURE (WEEKEND) - PRESS " + PRESS +
              " - AP REUTERS AFP XINHUA ANADOLU", 2, INK)
    return cv


def main():
    data = png_bytes(W, H, render().px)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if outdir:
        # Round 1 fix: the grader's output dir may not exist yet.
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "entry.png")
        with open(path, "wb") as f:
            f.write(data)
        print("wrote %s (%d bytes)" % (path, len(data)))
    else:
        with open("entry.png", "wb") as f:
            f.write(data)
        print("wrote entry.png (%d bytes)" % len(data))


if __name__ == "__main__":
    main()
