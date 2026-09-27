"""Shared palette, fonts and SVG helpers for the profile graphics.

Fonts (Archivo, IBM Plex Sans, IBM Plex Mono; SIL OFL) are subset to the
characters each image uses and embedded as base64 woff2, so every SVG renders
the same on any machine without loading anything from the network.
"""
import base64
import io
from html import escape
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).parent / "fonts"
FONTS = {
    "display": ("Archivo", 800, "archivo-latin-800-normal.woff2", "Arial Black, Helvetica, sans-serif"),
    "body": ("IBM Plex Sans", 400, "ibm-plex-sans-latin-400-normal.woff2", "Helvetica, Arial, sans-serif"),
    "strong": ("IBM Plex Sans", 600, "ibm-plex-sans-latin-600-normal.woff2", "Helvetica, Arial, sans-serif"),
    "mono": ("IBM Plex Mono", 500, "ibm-plex-mono-latin-500-normal.woff2", "Menlo, Consolas, monospace"),
}

THEMES = {
    "dark": dict(bg="#0b0e14", surface="#10141c", line="#232a36", text="#e8ecf2", muted="#8b95a5",
                 faint="#171c26", accent="#5b9cff", accent2="#a9c8ff", chip="#151a23"),
    "light": dict(bg="#f7f9fc", surface="#ffffff", line="#dfe4ec", text="#0f1623", muted="#5a6475",
                  faint="#eef2f8", accent="#1f5fd6", accent2="#123f94", chip="#f1f4f9"),
}

_tt = {k: TTFont(FONT_DIR / f[2]) for k, f in FONTS.items()}


def width(text, font, size, tracking=0.0):
    f = _tt[font]
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    adv = sum(hmtx[cmap.get(ord(ch), cmap[ord("?")])][0] for ch in text)
    return adv * size / upm + tracking * len(text)


def wrap(text, font, size, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and width(trial, font, size) > max_width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


class Canvas:
    """Collects SVG elements and the text used per font (for subsetting)."""

    def __init__(self, w, h, theme):
        self.w, self.h, self.c = w, h, THEMES[theme]
        self.body, self.defs, self.css = [], [], []
        self.used = {}

    def add(self, s):
        self.body.append(s)

    def text(self, x, y, s, font="body", size=16, fill=None, anchor=None, tracking=0, cls=None, extra=""):
        fam, wt, _, fb = FONTS[font]
        self.used.setdefault(font, set("0123456789")).update(s)
        attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f"font-family=\"'{fam}', {fb}\"", f'font-weight="{wt}"',
                 f'font-size="{size}"', f'fill="{fill or self.c["text"]}"']
        if anchor:
            attrs.append(f'text-anchor="{anchor}"')
        if tracking:
            attrs.append(f'letter-spacing="{tracking}"')
        if cls:
            attrs.append(f'class="{cls}"')
        if extra:
            attrs.append(extra)
        self.add(f'<text {" ".join(attrs)}>{escape(s)}</text>')

    def chip(self, x, y, label, size=12.5, h=30):
        w = width(label, "mono", size) + 26
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
                 f'fill="{self.c["chip"]}" stroke="{self.c["line"]}"/>')
        self.text(x + 13, y + h / 2 + size * 0.36, label, "mono", size)
        return w

    def arrow(self, x, y, size=11, stroke=None, sw=2):
        """North-east arrow drawn as a path (no glyph needed). (x, y) is the bottom-left."""
        s = stroke or self.c["accent"]
        self.add(f'<path d="M{x} {y} L{x + size} {y - size} M{x + 3} {y - size} H{x + size} V{y - size + 8}" '
                 f'fill="none" stroke="{s}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

    def render(self):
        faces = []
        for key, chars in self.used.items():
            fam, wt, fname, _ = FONTS[key]
            opts = subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["kern", "liga", "tnum"]
            font = TTFont(FONT_DIR / fname)
            sub = subset.Subsetter(opts)
            sub.populate(text="".join(sorted(chars)) + " ")
            sub.subset(font)
            buf = io.BytesIO()
            font.flavor = "woff2"
            font.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            faces.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};"
                         f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
        css = "".join(faces) + "".join(self.css)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}"><defs>{"".join(self.defs)}<style>{css}</style></defs>'
                f'{"".join(self.body)}</svg>\n')
