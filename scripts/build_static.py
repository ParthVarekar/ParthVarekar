#!/usr/bin/env python3
"""Build the static profile graphics into assets/ (header, project cards, stack, buttons).

    pip install fonttools brotli pillow
    python scripts/build_static.py
"""
import base64
import io
from pathlib import Path

from PIL import Image, ImageOps

from theme import Canvas, width, wrap

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def portrait_b64(size=520):
    """Duotone crop of assets/hero-banner.png (the ASCII-on-CRT portrait)."""
    im = Image.open(ASSETS / "hero-banner.png").convert("L")
    im = ImageOps.autocontrast(im.crop((250, 95, 1070, 875)).resize((size, size), Image.LANCZOS), cutoff=1)
    hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    stops = [(0, hx("#0c0c0e")), (0.35, hx("#2a1208")), (0.7, hx("#ff5a1f")), (1, hx("#ffe6d6"))]
    lut = []
    for i in range(256):
        t = i / 255
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if a <= t <= b:
                u = (t - a) / (b - a)
                lut.append(tuple(round(ca[k] + (cb[k] - ca[k]) * u) for k in range(3)))
                break
    rgb = Image.merge("RGB", [im.point([c[k] for c in lut]) for k in range(3)])
    buf = io.BytesIO()
    rgb.save(buf, "JPEG", quality=78, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode()


def header(theme, photo):
    cv = Canvas(1200, 480, theme)
    c = cv.c
    cv.defs.append(f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
                   f'<circle cx="1.5" cy="1.5" r="1.1" fill="{c["line"]}"/></pattern>')
    cv.add(f'<rect width="1200" height="480" rx="24" fill="{c["bg"]}"/>')
    cv.add('<rect width="1200" height="480" rx="24" fill="url(#dots)"/>')
    cv.add(f'<rect x=".5" y=".5" width="1199" height="479" rx="24" fill="none" stroke="{c["line"]}"/>')

    x = 64
    cv.add(f'<circle cx="{x + 6}" cy="80" r="5" fill="{c["accent"]}"/>'
           f'<circle cx="{x + 6}" cy="80" r="5" fill="none" stroke="{c["accent"]}" stroke-width="2" class="ping"/>')
    cv.text(x + 24, 85, "OPEN TO COLLABS AND HACKATHONS", "mono", 13.5, c["muted"], tracking=1.6)
    cv.text(x - 3, 176, "Parth Varekar", "display", 86, tracking=-2.5)

    size, y = 27, 238
    a, b, rest = "I build ", "local-first AI", "software:"
    cv.text(x, y, a, "body", size)
    xb = x + width(a, "body", size)
    cv.text(xb, y, b, "strong", size, c["accent"])
    cv.add(f'<rect x="{xb:.1f}" y="{y + 7}" width="{width(b, "strong", size):.1f}" height="2" fill="{c["accent"]}" opacity=".5"/>')
    cv.text(xb + width(b, "strong", size) + width(" ", "body", size), y, rest, "body", size)
    cv.text(x, y + 38, "retrieval engines, voice tools and developer", "body", size, c["muted"])
    cv.text(x, y + 76, "platforms that run on your own hardware.", "body", size, c["muted"])

    cx = x
    for lab in ["PYTHON", "TYPESCRIPT", "LLM + RAG", "REACT / NEXT.JS", "LOCAL INFERENCE"]:
        cx += cv.chip(cx, 352, lab, 12.5) + 10

    lx = x
    for lab in ["parthvarekar.in", "github.com/ParthVarekar"]:
        cv.arrow(lx, 430, 10)
        cv.text(lx + 22, 430, lab, "mono", 15)
        lx += 22 + width(lab, "mono", 15) + 40

    px, py, ps = 776, 52, 376
    cv.defs.append(f'<clipPath id="pclip"><rect x="{px}" y="{py}" width="{ps}" height="{ps}" rx="18"/></clipPath>'
                   f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">'
                   f'<stop offset="0" stop-color="{c["accent"]}" stop-opacity="0"/>'
                   f'<stop offset=".9" stop-color="{c["accent"]}" stop-opacity=".25"/>'
                   f'<stop offset="1" stop-color="#ffb38a" stop-opacity=".9"/></linearGradient>')
    cv.add(f'<g clip-path="url(#pclip)"><image x="{px}" y="{py}" width="{ps}" height="{ps}" '
           f'href="data:image/jpeg;base64,{photo}"/>'
           f'<rect x="{px}" y="{py - 60}" width="{ps}" height="60" fill="url(#scan)" class="sweep"/></g>')
    cv.add(f'<rect x="{px + .5}" y="{py + .5}" width="{ps - 1}" height="{ps - 1}" rx="18" fill="none" stroke="{c["line"]}"/>')
    L, o = 18, 10
    for bx, by, dx, dy in [(px - o, py - o, 1, 1), (px + ps + o, py - o, -1, 1),
                           (px - o, py + ps + o, 1, -1), (px + ps + o, py + ps + o, -1, -1)]:
        cv.add(f'<path d="M{bx} {by + dy * L} V{by} H{bx + dx * L}" fill="none" stroke="{c["accent"]}" stroke-width="2"/>')

    cv.css.append(f"""
.ping{{transform-box:fill-box;transform-origin:center;animation:ping 2.2s cubic-bezier(0,0,.2,1) infinite}}
@keyframes ping{{0%{{transform:scale(1);opacity:.9}}80%,100%{{transform:scale(2.6);opacity:0}}}}
.sweep{{animation:sweep 5s cubic-bezier(.45,0,.55,1) infinite}}
@keyframes sweep{{0%{{transform:translateY(0)}}70%,100%{{transform:translateY({ps + 60}px)}}}}
@media (prefers-reduced-motion:reduce){{.ping,.sweep{{animation:none}}}}""")
    return cv.render()


PROJECTS = [
    dict(slug="eka", n="01", tag="FLAGSHIP", cat="RAG / SECURITY / LOCAL LLM",
         title="Enterprise Knowledge Assistant",
         desc="Slack-native RAG engine that answers from company docs, and declines when it cannot back an answer with evidence.",
         pills=["Zero-trust ACL", "BM25 + vector RRF", "NLI grounding"],
         stack="TypeScript · Node.js · llama.cpp (CUDA) · Vitest"),
    dict(slug="whisperflow", n="02", tag="SHIPPED", cat="VOICE / ON-DEVICE AI",
         title="WhisperFlow",
         desc="Offline dictation for any app. On-device speech recognition plus LLM cleanup, pasted back as polished text.",
         pills=["Fully offline", "Qwen3-ASR + Gemma", "Global hotkey"],
         stack="Python · llama.cpp · Qwen3-ASR · Gemma"),
    dict(slug="codeframe", n="03", tag="IN PROGRESS", cat="DEV TOOLS / DESIGN TO CODE",
         title="Codeframe",
         desc="Figma-style design canvas whose frames export as clean, editable React and Tailwind projects.",
         pills=["Scene graph to code", "Live prototyping", "shadcn/ui library"],
         stack="TypeScript · React · Vite · Tailwind · Node.js"),
    dict(slug="agent-safety-net", n="04", tag="SECURITY", cat="AI SAFETY / BROWSER",
         title="Agent Safety Net",
         desc="Runtime safety layer for AI browser agents. Flags prompt injection and PII exfiltration before a request leaves the page.",
         pills=["Chrome MV3", "Under 2 ms overhead", "4-tier interventions"],
         stack="TypeScript · React · Vite · Chrome APIs"),
]


def card(p, theme):
    W, H = 600, 318
    cv = Canvas(W, H, theme)
    c = cv.c
    cv.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{c["surface"]}" stroke="{c["line"]}"/>')
    cv.text(W - 26, 124, p["n"], "display", 128, c["faint"], anchor="end", tracking=-6)
    cv.add(f'<rect x="32" y="30" width="44" height="4" rx="2" fill="{c["accent"]}" class="bar"/>')
    top = f'{p["n"]} / {p["tag"]}'
    cv.text(32, 62, top, "mono", 12.5, c["accent"], tracking=1.2)
    cv.text(32 + width(top, "mono", 12.5, 1.2) + 14, 62, p["cat"], "mono", 12.5, c["muted"], tracking=1.2)
    tsize = 32 if width(p["title"], "display", 32, -0.8) < W - 64 else 28
    cv.text(32, 110, p["title"], "display", tsize, tracking=-0.8)
    y = 146
    for line in wrap(p["desc"], "body", 17, W - 72)[:3]:
        cv.text(32, y, line, "body", 17, c["muted"])
        y += 25
    cx = 32
    for pl in p["pills"]:
        cx += cv.chip(cx, 214, pl, 12) + 8
    cv.add(f'<line x1="32" y1="264" x2="{W - 32}" y2="264" stroke="{c["line"]}"/>')
    cv.text(32, 292, p["stack"], "mono", 12.5, c["muted"])
    lab = "View repository"
    lw = width(lab, "strong", 14.5)
    cv.add('<g class="nudge">')
    cv.text(W - 50 - lw, 292, lab, "strong", 14.5, c["accent"])
    cv.arrow(W - 43, 291, 9)
    cv.add('</g>')
    cv.css.append("""
.nudge{animation:nudge 2.6s ease-in-out infinite}
@keyframes nudge{0%,60%,100%{transform:translate(0,0)}30%{transform:translate(3px,-2px)}}
@media (prefers-reduced-motion:reduce){.nudge{animation:none}}""")
    return cv.render()


STACK = [
    ("LANGUAGES", ["Python", "TypeScript", "JavaScript", "Java", "SQL"]),
    ("AI / ML", ["llama.cpp", "GGUF models", "RAG: BM25 + vectors", "NLI grounding", "Gemini API", "NVIDIA NIM", "PyTorch"]),
    ("FRONTEND", ["React", "Next.js", "Tailwind CSS", "Vite", "shadcn/ui", "Chrome extensions (MV3)"]),
    ("BACKEND & DATA", ["Node.js", "Flask", "Spring Boot", "Prisma", "SQLite", "Supabase"]),
    ("TOOLING", ["Git", "Linux", "Docker", "Vitest", "GitHub Actions"]),
]


def stack(theme):
    W = 1200
    rows, row_h, top = len(STACK), 50, 40
    cv = Canvas(W, top + (rows - 1) * row_h + 32 + top - 4, theme)
    c = cv.c
    cv.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{cv.h - 1}" rx="20" fill="{c["surface"]}" stroke="{c["line"]}"/>')
    y = top
    for i, (label, items) in enumerate(STACK):
        cv.text(40, y + 20, label, "mono", 12.5, c["accent"], tracking=1.4)
        cx = 240
        for it in items:
            cx += cv.chip(cx, y, it, 13, 32) + 8
        if i < rows - 1:
            cv.add(f'<line x1="40" y1="{y + row_h - 9}" x2="{W - 40}" y2="{y + row_h - 9}" stroke="{c["line"]}" stroke-dasharray="2 5"/>')
        y += row_h
    return cv.render()


BUTTONS = [("portfolio", "parthvarekar.in", True), ("follow", "Follow on GitHub", False), ("hello", "Say hello", False)]


def button(label, primary, theme):
    lw = width(label, "strong", 15)
    W, H = int(lw + 72), 46
    cv = Canvas(W, H, theme)
    c = cv.c
    fill, ink, stroke = (c["accent"], "#ffffff", c["accent"]) if primary else (c["surface"], c["text"], c["line"])
    cv.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{(H - 1.5) / 2}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    cv.text(24, 29, label, "strong", 15, ink)
    cv.arrow(W - 36, 28, 9, ink if primary else c["accent"])
    return cv.render()


def main():
    photo = portrait_b64()
    for theme in ("dark", "light"):
        (ASSETS / f"header-{theme}.svg").write_text(header(theme, photo))
        for p in PROJECTS:
            (ASSETS / f"card-{p['slug']}-{theme}.svg").write_text(card(p, theme))
        (ASSETS / f"stack-{theme}.svg").write_text(stack(theme))
        for slug, label, primary in BUTTONS:
            (ASSETS / f"btn-{slug}-{theme}.svg").write_text(button(label, primary, theme))
    print("built", sorted(p.name for p in ASSETS.glob("*.svg")))


if __name__ == "__main__":
    main()
