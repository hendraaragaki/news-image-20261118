#!/usr/bin/env python3
"""news-image-20261118 — "Sum up 18 November's world news in one image".

Draws a 1024x1024 newspaper front page for Wednesday 18 November 2026
and writes it to $MAKEFUN_OUTPUT_DIR/entry.png.

Pure Python standard library only: a hand-rolled RGB canvas, a hand-rolled
PNG encoder (zlib + CRC32), and bitmap fonts embedded as base64 blobs
(rendered once from DejaVu at build time, decoded here). No network, no
clock, no randomness — two runs write byte-identical files.
"""
import base64
import math
import os
import struct
import zlib

FONT_SANS = "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"
FONT_SANSB = "Rk5UMQATAAUAZgAgBwAAAAAAIQkCBAUPcHBwcHBwcHBwcABwcHBwACIKAQQIBWdnZ2dnACMRAQQPDwM4BzAGMAYwf/x//AxgDGAM4P/4//gYwBnAOYAxgAAkDgEEDBIGAAYAH4B/4HZgdgB2AH+AP+Af4AfgBvBG4H/gP4AGAAYABgAAJRQABBQPPgYAfwYAcwwAYxwAYxgAczAAfzAAPmfAAO/gAM7gAYxgAYxgAw7gBg/gBgfAACYRAQQQDweAH+AcIDwAHAAeAD8Of45z3vP88fzw+Hj4P/wfngAnBgEEBAVgYGBgYAAoCQEEBxIcHDg4OHBwcHBwcHBweDg4HBwAKQkBBAcScHA4ODwcHBwcHBwcHDw4OHBwACoKAAQKCQwADABMwH+AHgB/gEzADAAMAAArEQIHDQwHAAcABwAHAAcA//j/+AcABwAHAAcABwAALAgBDwUHeHh4cHDgwAAtCAEMBwP8/PwALggCDwQE8PDw8AAvBwAECBAGBg4MDBwYGDgwMHBgYODAADAOAAQNDw+AH+A88DhweHh4eHh4eHh4eHh4eHg4cDzwH+APgAAxDgIECw8+AP4AzgAOAA4ADgAOAA4ADgAOAA4ADgAOAP/g/+AAMg4BBAwPPwB/wGPgAeAB4AHgAeADwAeADwAeADwAeAB/4H/gADMOAQQMDz+Af8BD4AHgAeADwB+AH8AD4AHgAOAB4MPg/8A/AAA0DgAEDQ8D4APgB+AP4A/gHeA54DngceBx4H/4f/gB4AHgAeAANQ4BBAwPf8B/wHAAcABwAH+Af8BD4AHgAOAA4AHgQ+B/wD8AADYOAQQMDw/AH+A8IHgAcAD3gP/g+eDw8PDwcPBw8HngP8APgAA3DgEEDA//4P/gAeAB4APAA8AHgAeAB4APAA8AHgAeABwAPAAAOA4BBAwPH4B/4HngcOBw4HngP8A/wHng8ODw8PDweeB/4B+AADkOAQQMDx8AP8BxwPHg8ODw8PHwcfB/8B7gAOAB4EPAf4A/AAA6CAIIBAvw8PDwAAAA8PDw8AA7CAEIBQ54eHh4AAAAeHh4eHBg4AA8EQIHDQsAGAD4A/AfgPwA8AD8AB+AA/AA+AAYAD0RAgoNBv/4//gAAAAA//j/+AA+EQIHDQvAAPAAfgAPwAHwAHgB8A/AfgDwAMAAAD8MAQQKDz4A/4DHgAOAB4AHgA8AHgAcADwAAAA8ADwAPAA8AABAFAEEEhID8AAP/AAeDgA4AwBx2YBj+YBnOIDGGMDGGMDGGIDGGYBnO4Bj/wBx3AA4BAAcHAAP/AAD8AAAQQ8ABBAPB8AH4AfgD+AP8A7wHnAeeDx4PDg//H/8eBxwHvAeAEIPAQQND3/Af+B48HjwePB48H/gf+B48Hh4eHh4eHjwf/B/wABDDwEEDQ8H4B/wPBB4AHAA8ADwAPAA8ADwAHAAeAA8EB/wB+AARBEBBA8Pf8B/8Hj4eHx4PHg8eBx4HngceDx4PHh8ePh/8H/AAEUOAQQMD3/gf+B4AHgAeAB4AH/gf+B4AHgAeAB4AHgAf+B/4ABGDgEECw9/4H/geAB4AHgAeAB/4H/geAB4AHgAeAB4AHgAeAAARxABBA4PB/Af+DwIeABwAPAA8ADw/PD88DxwPHg8PDwf/AfwAEgRAQQOD3g8eDx4PHg8eDx4PH/8f/x4PHg8eDx4PHg8eDx4PABJBwEEBQ94eHh4eHh4eHh4eHh4eHgASgf+BAgTDw8PDw8PDw8PDw8PDw8PDh58eABLEAEEEA94PHh4ePB54HvAf4B/AH8Af4B/wHvgefB4+Hh8eD4ATA0BBAwPeAB4AHgAeAB4AHgAeAB4AHgAeAB4AHgAeAB/4H/gAE0UAQQSD3wPgHwPgH4fgH4fgH4/gHc/gHc3gHP3gHP3gHHngHHngHDHgHAHgHAHgHAHgABOEQEEDg94PHw8fDx+PH48fzx3PHO8c7xx/HH8cPxw/HB8cHwATxEBBA8PD+Af8Dx4eDzwHvAe8B7wHvAe8B7wHng8PHgf8A/gAFAPAQQND3/Af/B48Hh4eHh4eHh4ePB/8H/AeAB4AHgAeAB4AABREQEEDxIP4B/wPHh4PPAe8B7wHvAe8B7wHvAeeDw8eB/wD+AA8AB4ADgAUg8BBA4Pf8B/4HjwePB48HjweOB/wH/AeeB48HjweHh4eHg8AFMOAQQMDx/gP+B4YHAg8AB4AH+AP+Af8AHwAPAA8GDwf+A/gABUDgAEDg///P/8B4AHgAeAB4AHgAeAB4AHgAeAB4AHgAeAB4AAVRABBA4PeDh4OHg4eDh4OHg4eDh4OHg4eDh4OHh4PHg/8A/AAFYPAAQQD/AecB54HHg8ODw8ODx4HHgecA7wD/AP4AfgB+AHwABXFgAEFg9weDh4eDh4eHh4/Hg4/HA4/HA8zPA9zvAdzuAdzuAfh+Afh+Afh+APh8APg8AAWA8ABA8PeBw4PDx4HngP8A/gB+AHwAfgD+Ae8B54PHh4PHgeAFkO/wQQD3gePB48PB54D3gP8AfwA+ADwAPAA8ADwAPAA8ADwABaDgAEDg9/+H/4APgA+AHwA+AHwAfAD4AfAD4APgB8AH/8f/wAWwkBBAcSfn5wcHBwcHBwcHBwcHBwcH5+AFwHAAQIEMDgYGBwMDA4GBgcDAwOBgYAXQkBBAcS/PwcHBwcHBwcHBwcHBwcHPz8AF4RAgQNBQcAD4AdwDjgYDAAXwoAFgoC/8D/wABgCgEDBgTgcDAYAGEOAAgMCz+AP+AA8ADwH/A/8HjwcPB58H/wHvAAYg4BBA0PcABwAHAAcABzwH/gePB48HBwcHBwcHjwePB/4HPAAGMMAAgLCw+AH+A8AHgAeAB4AHgAeAA8AB/gD4AAZA4ABA0PAHgAeAB4AHgOeD/4PPh4eHh4eHh4eHh4PPg/+A54AGUOAAgNCw/AP+A48Hhwf/h/+HgAeAA8ED/wD8AAZgkABAkPD4AfgDwAPAD/gP+APAA8ADwAPAA8ADwAPAA8ADwAAGcOAAgNDw54P/g8+Hh4eHh4eHh4eHg8+D/4DngAcCDwP+APgABoDgEEDA9wAHAAcABwAHPAf+B44HjwcPBw8HDwcPBw8HDwcPAAaQcBBAUPcHBwAHBwcHBwcHBwcHBwAGoH/wQHExwcHAAcHBwcHBwcHBwcHBw8+PAAaw0BBA0PcABwAHAAcABw8HHgc8B3gH8AfgB/AHeAc8Bx4HDwAGwHAQQFD3BwcHBwcHBwcHBwcHBwcABtFQEIEwtzj4B/38B588Bw8cBw4cBw4cBw4cBw4cBw4cBw4cBw4cAAbg4BCAwLc8B/4HjgePBw8HDwcPBw8HDwcPBw8ABvDgAIDQsPwD/gPPB4eHh4eHh4eHh4PPA/4A/AAHAOAQgND3PAf+B48HjwcHBwcHBwePB48H/gc8BwAHAAcABwAABxDgAIDQ8OeD/4PPh4eHh4eHh4eHh4PPg/+A54AHgAeAB4AHgAcgoBCAkLc4B/gHgAeABwAHAAcABwAHAAcABwAABzDAEICgs/AH+A4IDgAP4Af4AfwAPAw8D/gD8AAHQKAAUKDjwAPAA8AP+A/4A8ADwAPAA8ADwAPAA8AD+AH4AAdQ4BCAwLcPBw8HDwcPBw8HDwcPBw8Hnwf/A88AB2DQAIDQvweHBwePA44DjgPeAdwB/AD4APgA+AAHcSAAgSC3DjwHHjgHnjgDnzgDn3gDu3AD8/AB8/AB8/AB8eAB8eAAB4DQAIDQt48DjgPeAfwA+AD4APgB/APeB44HBwAHkNAAgND/BwcHB48DjgPOAd4B3AH8APgA+AB4AHAAcAPgA8AAB6DAAICwt/4H/gA+AHwA+ADwAeADwAeAB/4H/gAHsOAgQKEgfAD8AOAA4ADgAOAB4AHgD8APwAHgAeAA4ADgAOAA4AD8AHwAB8BwIEAxRgYGBgYGBgYGBgYGBgYGBgYGBgYAB9DgIEChL4APwAHgAeAB4AHgAeAA4AD8APwA4AHgAeAB4AHgAeAPwA+AAAfhECCg0FAAB+GP/4w+AAACWyDwAGEBAAAAEAAYADgAPAB8AH4A/gD/Af8B/4P/g//H/8f/4AACW8DwAGEBD//n/+f/w//D/4H/gf8A/wD+AH4AfAA8ADgAGAAQAAAAC3CAIKBATw8PDwIBQUAQwSA///wP//wP//wCATCgEMCAP///8gIg0CCAgHHD5/f38+HCYFEgEEEBAAAAAAAYABgAGAA8B//j/8D/AH4AfgD/AOcAgQAAAAAA=="
FONT_SERIFB = "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"

W, H = 1024, 1024
PAPER = (253, 251, 245)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (20, 38, 63)
ORANGE = (245, 158, 11)
YELLOW = (253, 224, 71)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
TEAL = (13, 148, 136)
BLUE = (37, 99, 235)
PURPLE = (126, 34, 206)
GREEN = (21, 128, 61)
AMBER = (180, 83, 9)


# ---------------------------------------------------------------- fonts
def _load_font(blob):
    raw = base64.b64decode(blob)
    assert raw[:4] == b"FNT1"
    ascent, descent, count = struct.unpack(">HHH", raw[4:10])
    glyphs = {}
    i = 10
    for _ in range(count):
        cp, adv, dx, dy, w, h = struct.unpack(">HbbbbB", raw[i:i + 7])
        i += 7
        stride = (w + 7) // 8
        bits = raw[i:i + stride * h]
        i += stride * h
        glyphs[cp] = (adv, dx, dy, w, h, bits)
    return {"ascent": ascent, "descent": descent, "glyphs": glyphs}


class Font:
    def __init__(self, blob):
        d = _load_font(blob)
        self.ascent = d["ascent"]
        self.descent = d["descent"]
        self.glyphs = d["glyphs"]
        self._cache = {}

    def _scaled(self, cp, scale):
        key = (cp, scale)
        g = self._cache.get(key)
        if g is None:
            adv, dx, dy, w, h, bits = self.glyphs.get(
                cp, self.glyphs[ord("?")])
            if w == 0 or h == 0:
                g = (int(round(adv * scale)), 0, 0, 0, 0, [])
                self._cache[key] = g
                return g
            sw = max(1, int(round(w * scale)))
            sh = max(1, int(round(h * scale)))
            rows = []
            stride = (w + 7) // 8
            for j in range(sh):
                sy = min(h - 1, int(j / scale))
                src = bits[sy * stride:(sy + 1) * stride]
                row = bytearray(sw)
                for i in range(sw):
                    sx = min(w - 1, int(i / scale))
                    if src[sx // 8] & (0x80 >> (sx % 8)):
                        row[i] = 1
                rows.append(bytes(row))
            g = (int(round(adv * scale)), int(round(dx * scale)),
                 int(round(dy * scale)), sw, sh, rows)
            self._cache[key] = g
        return g

    def text_width(self, s, scale):
        return sum(self._scaled(ord(ch), scale)[0] for ch in s)

    def draw(self, cv, x, y, s, scale, color):
        """Draw text; y is the top of the em box. Returns end x."""
        cx = x
        for ch in s:
            adv, dx, dy, w, h, rows = self._scaled(ord(ch), scale)
            if w and h:
                gx = cx + dx
                gy = y + dy
                for j, row in enumerate(rows):
                    yy = gy + j
                    if 0 <= yy < cv.h:
                        i = 0
                        while i < w:
                            if row[i]:
                                j0 = i
                                while i < w and row[i]:
                                    i += 1
                                cv.fill(gx + j0, yy, i - j0, 1, color)
                            else:
                                i += 1
            cx += adv
        return cx


SANS = Font(FONT_SANS)
SANSB = Font(FONT_SANSB)
SERIFB = Font(FONT_SERIFB)


def wrap(font, text, scale, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if font.text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill(0, 0, w, h, bg)

    def fill(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            o = (yy * self.w + x0) * 3
            self.px[o:o + len(row)] = row

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for y in range(-r, r + 1):
            half = int(math.sqrt(max(0, r * r - y * y)))
            self.fill(cx - half, cy + y, 2 * half + 1, 1, c)

    def ring(self, cx, cy, r, t, c):
        for y in range(-r, r + 1):
            half = int(math.sqrt(max(0, r * r - y * y)))
            self.fill(cx - half, cy + y, t, 1, c)
            self.fill(cx + half - t + 1, cy + y, t, 1, c)


def fill_poly(cv, pts, c):
    ys = [p[1] for p in pts]
    y0 = max(0, int(math.floor(min(ys))))
    y1 = min(cv.h - 1, int(math.ceil(max(ys))))
    n = len(pts)
    for y in range(y0, y1 + 1):
        xs = []
        for i in range(n):
            x1, y1v = pts[i]
            x2, y2v = pts[(i + 1) % n]
            if (y1v <= y < y2v) or (y2v <= y < y1v):
                t = (y - y1v) / (y2v - y1v)
                xs.append(x1 + t * (x2 - x1))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            xa = max(0, int(math.floor(xs[k])))
            xb = min(cv.w - 1, int(math.ceil(xs[k + 1])))
            if xb >= xa:
                cv.fill(xa, y, xb - xa + 1, 1, c)


def starburst(cv, cx, cy, r1, r2, n, c):
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    fill_poly(cv, pts, c)


def missile(cv, x0, y0, x1, y1, w, body):
    """A missile flying from (x0, y0) tail to (x1, y1) nose, with flame."""
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    px, py = -uy, ux
    hw = w / 2.0
    # flame behind the tail
    fx, fy = x0 - ux * 34, y0 - uy * 34
    fill_poly(cv, [(x0 + px * 7, y0 + py * 7),
                   (x0 - px * 7, y0 - py * 7),
                   (fx, fy)], ORANGE)
    fill_poly(cv, [(x0 + px * 4, y0 + py * 4),
                   (x0 - px * 4, y0 - py * 4),
                   (x0 - ux * 20, y0 - uy * 20)], YELLOW)
    # body
    fill_poly(cv, [(x0 + px * hw, y0 + py * hw),
                   (x0 - px * hw, y0 - py * hw),
                   (x1 - px * hw, y1 - py * hw),
                   (x1 + px * hw, y1 + py * hw)], body)
    # nose cone
    nx, ny = x1 + ux * 22, y1 + uy * 22
    fill_poly(cv, [(x1 + px * hw, y1 + py * hw),
                   (x1 - px * hw, y1 - py * hw),
                   (nx, ny)], body)
    # tail fins
    bx, by = x0 + ux * 14, y0 + uy * 14
    fill_poly(cv, [(bx + px * hw, by + py * hw),
                   (bx - px * hw, by - py * hw),
                   (bx - px * (hw + 16), by - py * (hw + 16))], body)
    fill_poly(cv, [(bx + px * hw, by + py * hw),
                   (bx - px * hw, by - py * hw),
                   (bx + px * (hw + 16), by + py * (hw + 16))], body)


# ---------------------------------------------------------------- icons
def icon_globe(cv, x, y):
    cx, cy = x + 32, y + 32
    cv.ring(cx, cy, 20, 3, WHITE)
    cv.fill(cx - 2, cy - 20, 3, 41, WHITE)
    cv.fill(cx - 20, cy - 2, 41, 3, WHITE)


def icon_quad(cv, x, y):
    cx, cy = x + 32, y + 32
    pts = [(cx - 13, cy - 13), (cx + 13, cy - 13),
           (cx + 13, cy + 13), (cx - 13, cy + 13)]
    for i in range(4):
        a = pts[i]
        b = pts[(i + 1) % 4]
        cv.line(a[0], a[1], b[0], b[1], WHITE, 3)
    for px, py in pts:
        cv.disc(px, py, 7, WHITE)


def icon_parliament(cv, x, y):
    cx, cy = x + 32, y + 32
    fill_poly(cv, [(cx - 22, cy - 2), (cx + 22, cy - 2), (cx, cy - 20)],
              WHITE)
    for ox in (-18, -2, 13):
        cv.fill(cx + ox, cy + 2, 5, 18, WHITE)
    cv.fill(cx - 24, cy + 22, 48, 4, WHITE)


def icon_ballot(cv, x, y):
    cx, cy = x + 32, y + 32
    cv.fill(cx - 20, cy - 14, 40, 3, WHITE)
    cv.fill(cx - 20, cy + 11, 40, 3, WHITE)
    cv.fill(cx - 20, cy - 14, 3, 28, WHITE)
    cv.fill(cx + 17, cy - 14, 3, 28, WHITE)
    cv.fill(cx - 10, cy - 6, 20, 3, WHITE)
    cv.line(cx - 12, cy + 2, cx - 4, cy + 10, WHITE, 3)
    cv.line(cx - 4, cy + 10, cx + 14, cy - 10, WHITE, 3)


def icon_virus(cv, x, y):
    cx, cy = x + 32, y + 32
    for i in range(8):
        a = math.pi * i / 4
        cv.line(cx + int(13 * math.cos(a)), cy + int(13 * math.sin(a)),
                cx + int(21 * math.cos(a)), cy + int(21 * math.sin(a)),
                WHITE, 3)
    cv.ring(cx, cy, 13, 3, WHITE)
    cv.disc(cx, cy, 4, WHITE)


def icon_cross(cv, x, y):
    cx, cy = x + 32, y + 32
    cv.disc(cx, cy, 18, WHITE)
    cv.fill(cx - 4, cy - 12, 8, 24, RED)
    cv.fill(cx - 12, cy - 4, 24, 8, RED)


# ---------------------------------------------------------------- stories
# (kicker, kicker color, headline, body, icon)
STORIES = [
    ("ASIA — APEC SUMMIT", TEAL, "APEC OPENS IN SHENZHEN",
     "Xi meets Putin in Shenzhen; a Trump–Xi–Putin trilateral is set for "
     "Thursday. Xi pledges to fight protectionism.", icon_globe),
    ("ASIA — THE QUAD", BLUE, "QUAD MEETS IN MANILA",
     "First Quad meeting in over two years. Trump announces a Philippines "
     "trade deal after meeting Marcos Jr.", icon_quad),
    ("MIDDLE EAST — ISRAEL", PURPLE, "KAHANA ELECTED SPEAKER",
     "Knesset elects Matan Kahana, a win for PM-elect Eisenkot. Trump's "
     "Board of Peace says Israel and Hamas failed commitments.",
     icon_parliament),
    ("AMERICAS — U.S. SENATE", GREEN, "PELTOLA FLIPS ALASKA",
     "Democrat Mary Peltola beats Dan Sullivan. Democrats take a 56–44 "
     "Senate majority.", icon_ballot),
    ("HEALTH — UNITED STATES", AMBER, "MEASLES-FREE STATUS LOST",
     "First loss in 26 years: 5,412 cases in 2026 and 10 deaths, health "
     "officials confirm.", icon_virus),
    ("HEALTH — AFRICA", RED, "EBOLA SURGE IN DR CONGO",
     "More than 11,000 cases in the second-largest outbreak on record.",
     icon_cross),
]

TICKER = [
    "MARKETS — S&P 500 7,340.53 ▼1.03%   ·   Nasdaq 24,328.38 ▼0.74%   ·   "
    "Nikkei 225 59,024.28 ▲0.28%",
    "Hang Seng 23,297.16 ▼0.90%   ·   Brent crude $91.55 ▼1.71%   ·   "
    "Gold $3,775   ·   VIX 25.46 ▲11.13%",
]


def draw_cell(cv, x, y, w, kicker, kcolor, headline, body, icon):
    cv.fill(x, y + 2, 64, 64, kcolor)
    icon(cv, x, y + 2)
    tx = x + 76
    tw = w - 76
    SANSB.draw(cv, tx, y + 2, kicker, 0.8, kcolor)
    hlines = wrap(SANSB, headline, 1.15, tw)
    hy = y + 24
    for ln in hlines:
        SANSB.draw(cv, tx, hy, ln, 1.15, INK)
        hy += 29
    by = hy + 6
    for ln in wrap(SANS, body, 0.85, tw):
        SANS.draw(cv, tx, by, ln, 0.85, INK)
        by += 21


def draw_page():
    cv = Canvas(W, H, PAPER)
    # masthead
    title = "THE WORLD"
    tw = SERIFB.text_width(title, 4.0)
    SERIFB.draw(cv, (W - tw) // 2, 16, title, 4.0, INK)
    cv.fill(36, 138, W - 72, 3, INK)
    cv.fill(36, 144, W - 72, 1, INK)
    # dateline
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = SANSB.text_width(date, 1.3)
    SANSB.draw(cv, (W - dw) // 2, 154, date, 1.3, INK)
    SANS.draw(cv, 36, 158, "VOL. I — NO. 322", 0.8, GREY)
    right = "ONE DAY • ONE PAGE"
    SANS.draw(cv, W - 36 - SANS.text_width(right, 0.8), 158, right, 0.8,
              GREY)
    cv.fill(36, 188, W - 72, 1, INK)

    # lead story
    SANSB.draw(cv, 36, 204, "GULF CRISIS  •  LEAD STORY", 0.9, RED)
    y = 230
    for ln in ("U.S. STRIKES IRAN MISSILE", "SITE; TEHRAN HITS BACK"):
        SANSB.draw(cv, 36, y, ln, 2.0, INK)
        y += 46
    body = ("U.S. warplanes hit an Iranian missile launch site on Qeshm "
            "Island. Iran retaliated on Ali Al Salem Air Base in Kuwait "
            "and targets in Bahrain; Houthi drones struck five pumping "
            "stations on Saudi Arabia's East–West pipeline.")
    y += 8
    for ln in wrap(SANS, body, 1.0, 604):
        SANS.draw(cv, 36, y, ln, 1.0, INK)
        y += 25
    # lead graphic: missile and burst over the Gulf
    cv.fill(660, 204, 328, 274, NAVY)
    starburst(cv, 824, 312, 100, 56, 12, ORANGE)
    cv.disc(824, 312, 52, RED)
    cv.disc(824, 312, 28, YELLOW)
    cv.line(668, 448, 696, 425, WHITE, 3)
    cv.line(684, 462, 712, 439, WHITE, 3)
    cv.line(656, 420, 684, 397, WHITE, 3)
    missile(cv, 700, 424, 924, 238, 22, WHITE)
    cv.fill(660, 434, 328, 44, RED)
    cap = "STRIKES IN THE GULF"
    cw = SANSB.text_width(cap, 1.2)
    SANSB.draw(cv, 660 + (328 - cw) // 2, 444, cap, 1.2, WHITE)

    cv.fill(36, 492, W - 72, 1, INK)
    # story grid: 2 columns x 3 rows
    col_x = (36, 520)
    row_y = (506, 654, 802)
    for i, st in enumerate(STORIES):
        draw_cell(cv, col_x[i % 2], row_y[i // 2], 468, *st)
    cv.fill(36, 950, W - 72, 1, INK)
    # market ticker
    cv.fill(36, 958, W - 72, 52, NAVY)
    ty = 962
    for ln in TICKER:
        lw = SANSB.text_width(ln, 0.8)
        SANSB.draw(cv, (W - lw) // 2, ty, ln, 0.8, WHITE)
        ty += 22
    return cv


# ---------------------------------------------------------------- PNG out
def write_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
           chunk(b"IDAT", comp) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    cv = draw_page()
    path = os.path.join(out, "entry.png")
    n = write_png(cv, path)
    print("wrote %s (%d bytes)" % (path, n))


if __name__ == "__main__":
    main()
