#!/usr/bin/env python3
"""Renders the whole profile as ONE cinematic dashboard image in two layouts:
  assets/dashboard/desktop.svg  (1200 px wide, 3 columns)
  assets/dashboard/mobile.svg   (600 px wide, 1 column)
Live numbers (repos, contributions, followers, following, heatmap, languages) come from GitHub.
Resume facts come from DATA below. Art (assets/art) and icons (assets/icons) are embedded as data URIs.
"""
import base64, json, os, textwrap
from datetime import date
from xml.sax.saxutils import escape

import update_stats as us
from build_assets import PROJECTS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = os.path.join(ROOT, "assets")
BG, PANEL = "#05070D", "#0A1224"
CYAN, VIOLET, MAGENTA, GREEN, AMBER = "#22E4FF", "#8B5CF6", "#FF2BD6", "#39FF88", "#FFB020"
TEXT, MUTED = "#EAF2FF", "#8FA3BF"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Courier New',monospace"

# ───────────── shared, source-tagged data model (data/profile.json) ─────────────
D = json.load(open(os.path.join(ROOT, "data", "profile.json"), encoding="utf-8"))
EXPERIENCE = [(e["dates"], e["company"], e["role"], e["accent"], e["short"]) for e in D["experience"]]
ACHIEVEMENTS = [(a["org"], a["text"], a["accent"]) for a in D["achievements"]]
ICONS = [(i["id"], i["label"]) for i in D["icons"]]
MORE_TECH = D["moreTech"]
TAGS = D["focus"]
CURRENT = D["currentlyBuilding"]


def b64(path, mime):
    with open(path, "rb") as f: return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def wrapt(s, width_px, size, mono=True):
    cols = max(8, int(width_px / (size * (0.6 if mono else 0.55))))
    return textwrap.wrap(s, cols) or [""]


def T(x, y, s, size=15, fill=TEXT, weight=400, anchor="start", mono=True, extra=""):
    cls = ' class="m"' if mono else ""
    return f'<text{cls} x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(s))}</text>'


def box(w, h, cmd, accent=CYAN):
    head = ""
    if cmd:
        pre = f'<tspan fill="{GREEN}">sarveshrock@github:~</tspan><tspan fill="{MUTED}"> $ </tspan>' if w >= 400 else f'<tspan fill="{GREEN}">~</tspan><tspan fill="{MUTED}"> $ </tspan>'
        head = (f'<text class="m" x="16" y="27" font-size="14.5">{pre}<tspan fill="{TEXT}">{escape(cmd)}</tspan></text>'
                f'<text x="{w-16}" y="27" font-size="16" fill="{MUTED}" text-anchor="end">⋮</text>')
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{PANEL}" stroke="{accent}" stroke-opacity=".55" stroke-width="1.6"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="none" stroke="{accent}" stroke-opacity=".18" stroke-width="6"/>' + head)


def finish(w, cmd, accent, y, parts):
    h = y + 16
    return box(w, h, cmd, accent) + "".join(parts), h


# ───────────── panels: each returns (svg_fragment, height) for a given width ─────────────
def p_welcome(w):
    size = min(64, (w - 40) / 4.3)
    parts = [f'<text class="m" x="18" y="32" font-size="15" fill="{MUTED}">Welcome to </text><rect x="116" y="15" width="124" height="24" fill="{MAGENTA}"/>'
             f'<text class="m" x="122" y="32" font-size="15" font-weight="700" fill="#fff">SARVESHROCK</text>']
    y = 36 + size
    for word in ("SARVESH", "SHIMPI"):
        parts.append(T(18, y + 14, word, size, "url(#neon)", 800, extra='filter="url(#glow)" letter-spacing="1"'))
        y += size * 1.05
    y += 20
    parts.append(f'<path d="M23 {y-8} V{y+len(TAGS)*27-24}" stroke="{CYAN}" stroke-opacity=".5"/>')
    for i, t in enumerate(TAGS):
        parts.append(f'<circle cx="23" cy="{y-5}" r="5" fill="{CYAN if i == 0 else BG}" stroke="{CYAN}" filter="url(#glow)"/>')
        parts.append(T(42, y, t, 16, TEXT if i == 0 else "#C9D6EA", 700 if i == 0 else 400)); y += 27
    y += 14
    for ln in wrapt("Building AI solutions for a better tomorrow.", w - 60, 15, False):
        parts.append(T(18, y, ("“ " if ln == "Building AI solutions for" or y == y else "") + ln if False else ln, 15, CYAN, 400, mono=False, extra='font-style="italic"')); y += 22
    parts.append(T(18, y + 8, ">", 16, GREEN, 700, extra='style="animation:blink 1s infinite"') + T(32, y + 8, "_", 16, GREEN, 700, extra='style="animation:blink 1s infinite"'))
    return finish(w, None, CYAN, y + 18, parts)


def p_whoami(w):
    por = b64(os.path.join(A, "art", "portrait.jpg"), "image/jpeg")
    pw = min(w - 32, 330); ph = pw * 132 / 236
    y = 42
    parts = [f'<clipPath id="pc"><rect x="16" y="{y}" width="{pw}" height="{ph:.0f}" rx="8"/></clipPath>',
             f'<image href="{por}" x="16" y="{y}" width="{pw}" height="{ph:.0f}" clip-path="url(#pc)" preserveAspectRatio="xMidYMid slice"/>']
    y += ph + 30
    parts.append(T(16, y, "Sarvesh Shimpi", 21, TEXT, 700, mono=False)); y += 28
    for ln in wrapt("Python Automation & AI Platform Developer @ Infosys", w - 60, 14):
        parts.append(T(36, y, ln, 14, MUTED)); y += 20
    parts.insert(-1, "")
    for t in ("AI/ML Engineer", "Problem Solver", "Open Source Enthusiast", "Lifelong Learner"):
        parts.append(f'<circle cx="23" cy="{y-5}" r="3.5" fill="{VIOLET}"/>' + T(36, y, t, 14, MUTED)); y += 22
    y += 8
    parts.append(f'<path d="M16 {y-10} H{w-16}" stroke="{CYAN}" stroke-opacity=".25"/>'); y += 14
    for g, t, c in (("✉", "sarveshshimpi18@gmail.com", CYAN), ("in", "in/shimpi-ss-150186389", VIOLET), ("◈", "portfolio · netlify.app", GREEN), ("⌥", "github.com/Sarveshrock", MAGENTA)):
        parts.append(T(24, y, g, 15, c, 700, "middle") + T(42, y, t, 13.5, TEXT)); y += 25
    return finish(w, "whoami", CYAN, y, parts)


def p_aicore(w):
    h = 270; cx, cy = w / 2, 142
    nodes = [("COMPUTER VISION", cx, 62, CYAN), ("LLMs", 50, cy, VIOLET), ("GENERATIVE AI", w - 74, cy, MAGENTA), ("AGENTIC AI", cx, 232, GREEN)]
    parts = []
    for t, x, y, c in nodes:
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{c}" stroke-width="2" stroke-dasharray="8 6" style="animation:drift 1.5s linear infinite"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="{BG}" stroke="url(#neon)" stroke-width="4" filter="url(#glow)" style="animation:pulse 3s infinite"/>' + T(cx, cy + 5, "AI", 18, CYAN, 800, "middle"))
    for t, x, y, c in nodes:
        tw = 9 * len(t) + 22
        parts.append(f'<rect x="{x-tw/2}" y="{y-14}" width="{tw}" height="28" rx="14" fill="{PANEL}" stroke="{c}" stroke-width="1.8"/>' + T(x, y + 5, t, 12.5, c, 700, "middle"))
    return box(w, h, "ai.core", CYAN) + "".join(parts), h


def p_init(w):
    lines = ["Identity loaded", "GitHub stats synced", "Projects indexed", "Skills mapped", "Contributions fetched", "AI systems online", "Ready to build"]
    y = 52
    parts = [T(16, y, "[OK] Initializing SarveshOS...", 14, GREEN)]
    y += 24
    for i, t in enumerate(lines):
        parts.append(T(16, y, "[✓]", 14, GREEN, 700) + T(52, y, t, 14, TEXT, extra=f'style="animation:pulse 4s infinite {i*.25:.2f}s"')); y += 22
    y += 6
    parts.append(f'<rect x="16" y="{y}" width="{w-90}" height="12" rx="6" fill="{BG}" stroke="{CYAN}" stroke-opacity=".4"/>'
                 f'<rect x="16" y="{y}" width="{w-90}" height="12" rx="6" fill="url(#neon)" style="transform-origin:16px 0;animation:fill 2.5s ease-out both"/>' + T(w - 16, y + 11, "100%", 13, MUTED, anchor="end"))
    y += 34
    parts.append(T(16, y, "Welcome to SARVESHROCK!", 14.5, CYAN, 700))
    return finish(w, "system.init", CYAN, y, parts)


def p_experience(w):
    y = 52; parts = []
    for dates, co, role, c, bullets in EXPERIENCE:
        parts.append(f'<circle cx="24" cy="{y-5}" r="6" fill="{BG}" stroke="{c}" stroke-width="2" filter="url(#glow)"/>' + T(40, y, dates, 14, c, 700)); y += 24
        parts.append(T(40, y, co, 17, TEXT, 700, mono=False)); y += 20
        for ln in wrapt(role, w - 62, 13.5): parts.append(T(40, y, ln, 13.5, MUTED)); y += 18
        y += 4
        for b in bullets:
            ls = wrapt(b, w - 82, 13)
            for j, ln in enumerate(ls): parts.append(T(46, y, ("› " if j == 0 else "  ") + ln, 13, "#C9D6EA")); y += 17
        y += 14
    parts.append(f'<path d="M24 {52} V{y-26}" stroke="{CYAN}" stroke-opacity=".3" stroke-dasharray="4 5"/>')
    for ln in wrapt("MIT-WPU · B.Tech Computer Engineering · 2021–2025 · GPA 8.49/10", w - 32, 12):
        parts.append(T(16, y - 2, ln, 12, MUTED)); y += 16
    return finish(w, "cat experience.log", CYAN, y - 6, parts)


def p_achievements(w):
    y = 52; parts = []
    for name, d, c in ACHIEVEMENTS:
        parts.append(f'<circle cx="32" cy="{y+6}" r="15" fill="{BG}" stroke="{c}" stroke-width="2" filter="url(#glow)"/>' + T(32, y + 12, "★", 15, c, 700, "middle"))
        parts.append(T(60, y, name, 15.5, c, 700, mono=False)); y += 20
        for ln in wrapt(d, w - 78, 13): parts.append(T(60, y, ln, 13, MUTED)); y += 17
        y += 14
    return finish(w, "achievements", AMBER, y - 8, parts)


def p_current(w):
    y = 52; parts = []
    for i, t in enumerate(CURRENT):
        parts.append(f'<circle cx="24" cy="{y-5}" r="5" fill="{GREEN}" filter="url(#glow)" style="animation:pulse 2s infinite {i*.3:.1f}s"/>' + T(40, y, t, 14.5)); y += 25
    return finish(w, "currently_building", GREEN, y - 6, parts)


def p_nowplaying(w):
    h = 120
    parts = [f'<rect x="16" y="46" width="58" height="58" rx="10" fill="url(#neon)" opacity=".85"/>' + T(45, 84, "♪", 28, "#fff", 700, "middle"),
             T(88, 66, "Building the Future", 16, TEXT, 700, mono=False), T(88, 86, "ai-world.ost", 12, MUTED),
             f'<rect x="88" y="97" width="{w-110}" height="5" rx="2.5" fill="{BG}" stroke="{MAGENTA}" stroke-opacity=".4"/>'
             f'<rect x="88" y="97" width="0" height="5" rx="2.5" fill="url(#neon)"><animate attributeName="width" from="0" to="{w-110}" dur="24s" repeatCount="indefinite"/></rect>']
    return box(w, h, "now_playing", MAGENTA) + "".join(parts), h


def p_hero(w):
    art = b64(os.path.join(A, "art", "hero.jpg"), "image/jpeg")
    h = w * 256 / 890
    return (f'<clipPath id="hc"><rect width="{w}" height="{h:.0f}" rx="14"/></clipPath><image href="{art}" width="{w}" height="{h:.0f}" clip-path="url(#hc)" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2:.0f}" rx="14" fill="none" stroke="{MAGENTA}" stroke-opacity=".5" stroke-width="2"/>'), h


def p_stats(w, user, total):
    items = [("Repositories", user["public_repos"], CYAN, "▣"), ("Contributions · 1y", total, GREEN, "∿"), ("Followers", user["followers"], VIOLET, "◉"), ("Following", user["following"], MAGENTA, "◎")]
    gap = 10; tw = (w - 32 - gap * 3) / 4; parts = []
    for i, (lab, val, c, g) in enumerate(items):
        x = 16 + i * (tw + gap)
        parts.append(f'<g transform="translate({x:.0f},46)"><rect width="{tw:.0f}" height="62" rx="10" fill="{BG}" stroke="{c}" stroke-opacity=".5"/>'
                     + T(18, 26, g, 17, c, 700, "middle", extra='filter="url(#glow)"') + T(34, 30, val, 26 if tw > 100 else 22, TEXT, 800, mono=False)
                     + T(10, 52, lab, 11.5 if tw < 125 else 13, MUTED) + '</g>')
    return box(w, 124, "stats --overview", CYAN) + "".join(parts), 124


def p_contrib(w, cells, total):
    lv = ["#101A2C", "#0E4A33", "#13854E", "#22C066", "#39FF88"]
    cells = sorted(cells); off = (date.fromisoformat(cells[0][0]).weekday() + 1) % 7
    left = 44; pitch = (w - left - 16) / 54; cs = pitch - 2
    y0 = 62; parts = []; months = []; last = None
    for i, (d, l) in enumerate(cells):
        idx = i + off; wk, dy = idx // 7, idx % 7
        x, y = left + wk * pitch, y0 + dy * pitch
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cs:.1f}" height="{cs:.1f}" rx="1.5" fill="{lv[l]}"/>')
        if d[5:7] != last: months.append((x, ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(d[5:7]) - 1])); last = d[5:7]
    prev = -99
    for x, n in months:
        if x - prev >= 40: parts.append(T(f"{x:.0f}", y0 - 7, n, 11.5, MUTED)); prev = x
    for r, nm in ((1, "Mon"), (3, "Wed"), (5, "Fri")): parts.append(T(14, f"{y0 + r*pitch + cs - 1:.0f}", nm, 11, MUTED))
    yb = y0 + 7 * pitch + 22
    parts.append(T(16, yb, f"{total} contributions in the last year", 14, TEXT))
    lx = w - 230
    parts.append(T(lx, yb, "Less", 12, MUTED))
    for i, c in enumerate(lv): parts.append(f'<rect x="{lx+38+i*17}" y="{yb-11}" width="12" height="12" rx="2" fill="{c}"/>')
    parts.append(T(lx + 38 + 5 * 17 + 4, yb, "More", 12, MUTED))
    return finish(w, "git contributions", CYAN, yb, parts)


def p_langs(w, rows, s):
    palette = dict(us.LANG_COLORS); parts = []
    y = 52; bw = w - 190 if w > 400 else w - 150
    x = 16
    for i, (k, v) in enumerate(rows):
        seg = max(2, bw * v / s); parts.append(f'<rect x="{x:.1f}" y="{y}" width="{seg:.1f}" height="9" rx="3" fill="{palette.get(k, us.FALLBACK[i % 5])}"/>'); x += seg
    y += 32
    for i, (k, v) in enumerate(rows):
        c = palette.get(k, us.FALLBACK[i % 5])
        parts.append(f'<circle cx="24" cy="{y-5}" r="6" fill="{c}"/>' + T(40, y, k, 14.5) + T(16 + bw, y, f"{100*v/s:.1f}%", 14, MUTED, anchor="end")); y += 25
    cx, cy, r = w - 78, 96, 46
    import math
    circ = 2 * math.pi * r; acc = 0
    for i, (k, v) in enumerate(rows):
        c = palette.get(k, us.FALLBACK[i % 5]); seg = circ * v / s
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="14" stroke-dasharray="{seg:.1f} {circ-seg:.1f}" stroke-dashoffset="{-acc:.1f}" transform="rotate(-90 {cx} {cy})"/>'); acc += seg
    parts.append(T(cx, cy + 7, "AI", 20, CYAN, 800, "middle", extra='filter="url(#glow)"'))
    parts.append(T(16, max(y, 190) + 4, "by code size · non-fork public repositories", 11, MUTED))
    return finish(w, "languages", VIOLET, max(y, 190) + 6, parts)


def p_tech(w):
    per = max(5, int((w - 20) // 70)); y = 48; parts = []
    for i, (fid, label) in enumerate(ICONS):
        col, row = i % per, i // per
        x = 16 + col * ((w - 32) / per); yy = y + row * 74
        icon = b64(os.path.join(A, "icons", fid + ".svg"), "image/svg+xml")
        parts.append(f'<rect x="{x:.0f}" y="{yy}" width="{(w-32)/per-8:.0f}" height="66" rx="10" fill="{BG}" stroke="{CYAN}" stroke-opacity=".25"/>'
                     + (f'<rect x="{x + ((w-32)/per-8)/2 - 19:.0f}" y="{yy+4}" width="38" height="38" rx="9" fill="#DCE6F7"/>' if fid in ("flask", "pandas") else "") + f'<image href="{icon}" x="{x + ((w-32)/per-8)/2 - 16:.0f}" y="{yy+7}" width="32" height="32"/>' + T(f"{x + ((w-32)/per-8)/2:.0f}", yy + 56, label, 11.5, MUTED, anchor="middle"))
    y += ((len(ICONS) - 1) // per + 1) * 74 + 6
    parts.append(T(16, y + 8, "also", 12, CYAN))
    px, py = 16, y + 22
    for t in MORE_TECH:
        tw = 8.2 * len(t) + 22
        if px + tw > w - 16: px = 16; py += 30
        parts.append(f'<rect x="{px:.0f}" y="{py}" width="{tw:.0f}" height="24" rx="12" fill="{BG}" stroke="{VIOLET}" stroke-opacity=".6"/>' + T(f"{px+tw/2:.0f}", py + 16, t, 12, TEXT, anchor="middle")); px += tw + 7
    return finish(w, "tech --stack", VIOLET, py + 30, parts)


def p_projects(w, cols):
    gap = 10; cw = (w - 32 - gap * (cols - 1)) / cols; ch = 150; parts = []
    for i, (slug, name, cat, c, desc, stack, glyph) in enumerate(PROJECTS):
        col, row = i % cols, i // cols
        x, y = 16 + col * (cw + gap), 46 + row * (ch + gap)
        pub = "PUBLIC REPO" in cat
        g = [f'<g transform="translate({x:.0f},{y})"><rect width="{cw:.0f}" height="{ch}" rx="10" fill="{BG}" stroke="{c}" stroke-opacity=".55"/>',
             T(14, 28, glyph, 18, c, 700, extra='filter="url(#glow)"')]
        yy = 26
        for ln in wrapt(name, cw - 60, 13.5, False)[:2]: g.append(T(38, yy, ln, 14, c, 700, mono=False)); yy += 17
        yy = max(yy, 46) + 4
        for ln in wrapt(desc, cw - 28, 12)[:3]: g.append(T(14, yy, ln, 12, MUTED)); yy += 16
        g.append(T(14, ch - 24, stack, 11.5, TEXT))
        g.append(T(14, ch - 8, "SOURCE: " + ("GITHUB" if pub else "RESUME · NO PUBLIC REPO"), 9.5, MUTED, extra='letter-spacing=".5"'))
        g.append('</g>'); parts += g
    rows_n = (len(PROJECTS) + cols - 1) // cols
    h = 46 + rows_n * (ch + gap) + 6
    return box(w, h, "ls projects/", MAGENTA) + "".join(parts), h


def p_build(w):
    h = 150
    parts = [T(16, 56, "build --future", 14.5, CYAN), T(16, 84, "SYSTEM ONLINE ✓", 18, GREEN, 700, extra='filter="url(#glow)"'),
             T(16, 116, "ready to build", 13.5, MUTED), T(16, 136, "> _", 14, GREEN, extra='style="animation:blink 1s infinite"')]
    return box(w, h, "./initialize", GREEN) + "".join(parts), h


def p_quote(w):
    y = 54; parts = [T(16, y + 6, "“", 34, MAGENTA, 700, extra='filter="url(#glow)"')]
    for ln in wrapt("Turning ideas into real-world intelligent solutions.", w - 70, 15, False):
        parts.append(T(52, y, ln, 15, TEXT, 400, mono=False, extra='font-style="italic"')); y += 22
    for k, t in enumerate(("KEEP BUILDING.", "KEEP LEARNING.")):
        parts.append(T(52, y + 8 + k * 16, t, 11.5, CYAN, 700, extra='letter-spacing="1.5"'))
    return finish(w, "motto", MAGENTA, y + 22, parts)


def topbar(w, compact):
    items = [] if compact else ["~/profile", "~/about", "~/projects", "~/experience", "~/skills", "~/achievements", "~/stats", "~/contact"]
    parts = [f'<rect x="1" y="1" width="{w-2}" height="46" rx="12" fill="{PANEL}" stroke="{CYAN}" stroke-opacity=".4" stroke-width="1.4"/>',
             f'<circle cx="26" cy="24" r="11" fill="none" stroke="{TEXT}" stroke-width="2"/><circle cx="26" cy="24" r="4" fill="{TEXT}"/>',
             T(48, 29, "sarveshrock@github:~", 15, GREEN if compact else TEXT, 700)]
    x = 232
    for i, t in enumerate(items):
        parts.append(T(x, 29, t, 14, CYAN if i == 0 else MUTED, 700 if i == 0 else 400)); x += 10 + 8.4 * len(t) + 14
    parts.append(f'<circle cx="{w-92}" cy="24" r="5" fill="{GREEN}" filter="url(#glow)" style="animation:pulse 2s infinite"/>' + T(w - 78, 29, "ONLINE", 13.5, GREEN, 700))
    return "".join(parts), 48


# ───────────── layouts ─────────────
def wrap_svg(W, H, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs><filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
<radialGradient id="bgg" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#14123a"/><stop offset="1" stop-color="{BG}"/></radialGradient></defs>
<style>text{{font-family:'Space Grotesk','Inter','Segoe UI',Helvetica,Arial,sans-serif}} .m{{font-family:{MONO}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}} @keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
@keyframes drift{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-28}}}} @keyframes fill{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
<rect width="{W}" height="{H}" fill="url(#bgg)"/>
{body}
</svg>'''


def place(frag, x, y): return f'<g transform="translate({x},{y})">{frag}</g>'


def desktop(user, total, cells, rows, s):
    W, M, G = 1200, 10, 10
    lw, cw_, rw = 250, 640, 270
    xl, xc, xr = M, M + lw + G, M + lw + G + cw_ + G
    tb, th = topbar(W - 2 * M, False)
    body = [place(tb, M, 8)]
    top = 8 + th + G
    cols = {xl: top, xc: top, xr: top}
    def add(x, fn, *a):
        frag, h = fn(*a); body.append(place(frag, x, cols[x])); cols[x] += h + G
    add(xl, p_welcome, lw); add(xl, p_whoami, lw); add(xl, p_aicore, lw); add(xl, p_current, lw); add(xl, p_quote, lw)
    add(xc, p_hero, cw_); add(xc, p_stats, cw_, user, total); add(xc, p_contrib, cw_, cells, total); add(xc, p_langs, cw_, rows, s)
    add(xc, p_tech, cw_); add(xc, p_projects, cw_, 2)
    add(xr, p_init, rw); add(xr, p_experience, rw); add(xr, p_achievements, rw); add(xr, p_nowplaying, rw); add(xr, p_build, rw)
    H = max(cols.values())
    return wrap_svg(W, H, "\n".join(body), "Sarvesh Shimpi — AI/ML Engineer profile dashboard"), H


def mobile(user, total, cells, rows, s):
    W, M, G = 600, 8, 10
    pw = W - 2 * M
    tb, th = topbar(pw, True)
    body = [place(tb, M, 6)]; y = 6 + th + G
    for fn, args in ((p_hero, (pw,)), (p_welcome, (pw,)), (p_stats, (pw, user, total)), (p_contrib, (pw, cells, total)), (p_langs, (pw, rows, s)), (p_tech, (pw,)),
                     (p_projects, (pw, 1)), (p_experience, (pw,)), (p_achievements, (pw,)), (p_whoami, (pw,)), (p_aicore, (pw,)), (p_init, (pw,)), (p_current, (pw,)), (p_nowplaying, (pw,)), (p_quote, (pw,)), (p_build, (pw,))):
        frag, h = fn(*args); body.append(place(frag, M, y)); y += h + G
    return wrap_svg(W, y, "\n".join(body), "Sarvesh Shimpi — AI/ML Engineer profile dashboard (mobile)"), y


def main():
    cache = os.path.join(os.path.dirname(__file__), ".stats-cache.json")
    if os.environ.get("DASH_CACHED") and os.path.exists(cache):  # layout iteration without hitting the API
        user, cells, total, rows, s = json.load(open(cache, encoding="utf-8"))
        cells = [tuple(c) for c in cells]; rows = [tuple(r) for r in rows]
    else:
        user, repos, cells, total = us.collect()
        rows, s = us.lang_rows(repos)
        json.dump([user, cells, total, rows, s], open(cache, "w", encoding="utf-8"))
    os.makedirs(os.path.join(A, "dashboard"), exist_ok=True)
    for name, fn in (("desktop", desktop), ("mobile", mobile)):
        svg, h = fn(user, total, cells, rows, s)
        with open(os.path.join(A, "dashboard", name + ".svg"), "w", encoding="utf-8") as f: f.write(svg)
        print(name, f"{len(svg)/1024:.0f} KB", f"1200x{h:.0f}" if name == "desktop" else f"600x{h:.0f}")


if __name__ == "__main__":
    main()
