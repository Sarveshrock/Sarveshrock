#!/usr/bin/env python3
"""Generates every SVG asset for the profile. Pure stdlib.
Usage (from github-profile/):  python scripts/optional-generation-scripts/build_assets.py
Edit the DATA blocks below, re-run, commit the regenerated assets/ folder.
"""
import os, random, textwrap
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets"))

BG, BG2 = "#05070D", "#0A1020"
CYAN, VIOLET, MAGENTA, GREEN, AMBER = "#22E4FF", "#8B5CF6", "#FF2BD6", "#39FF88", "#FFB020"
TEXT, MUTED = "#EAF2FF", "#8FA3BF"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Courier New',monospace"
SANS = "'Space Grotesk','Inter','Segoe UI',Helvetica,Arial,sans-serif"


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel, f"{len(content)/1024:.1f} KB")


def svg(w, h, body, title, css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="0.55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
</defs>
<style>
text{{font-family:{SANS}}} .m{{font-family:{MONO}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@keyframes drift{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-40}}}}
@keyframes scan{{from{{transform:translateY(-100%)}}to{{transform:translateY(100%)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important;opacity:1!important}}}}
{css}
</style>
{body}
</svg>'''


def panel(w, h, accent, x=0, y=0, r=18):
    return (f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="{r}" fill="rgba(15,25,45,0.85)" stroke="{accent}" stroke-opacity=".55" stroke-width="2"/>'
            f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="6" rx="3" fill="{accent}" opacity=".8"/>')


# ───────────────────────── TERMINAL ─────────────────────────
def terminal():
    W, H = 900, 560
    rows = [("sarvesh@github:~$ whoami", CYAN), ("AI/ML Engineer", TEXT), ("Problem Solver", TEXT), ("Open Source Enthusiast", TEXT), ("Lifelong Learner", TEXT), ("", TEXT),
            ("sarvesh@github:~$ current_focus", CYAN), ("> Generative AI", GREEN), ("> Agentic AI", GREEN), ("> Computer Vision", GREEN), ("> LLM Systems", GREEN), ("> Intelligent Automation", GREEN), ("", TEXT),
            ("sarvesh@github:~$ build --future", CYAN), ("SYSTEM ONLINE ✓", GREEN)]
    b = [panel(W, H, VIOLET)]
    for i, c in enumerate((MAGENTA, AMBER, GREEN)):
        b.append(f'<circle cx="{40+i*26}" cy="30" r="7" fill="{c}"/>')
    b.append(f'<text class="m" x="{W-40}" y="36" font-size="15" fill="{MUTED}" text-anchor="end">zsh — sarveshrock</text>')
    for i, (t, c) in enumerate(rows):
        if t:
            b.append(f'<text class="m" x="40" y="{82+i*29}" font-size="21" fill="{c}" opacity="0" style="animation:fade .3s forwards {0.4+i*0.45:.2f}s">{escape(t)}</text>')
    b.append(f'<rect x="40" y="{82+15*29-18}" width="12" height="22" fill="{GREEN}" style="animation:blink 1s infinite {0.4+15*.45:.1f}s"/>')
    write("animations/terminal.svg", svg(W, H, "\n".join(b), "Terminal: whoami, current_focus, build --future. System online."))


# ───────────────────────── AI CORE ─────────────────────────
def ai_core():
    W, H = 900, 560
    cx, cy = 450, 280
    nodes = [("COMPUTER VISION", 450, 70, CYAN), ("LLMs", 110, 280, VIOLET), ("GENERATIVE AI", 790, 280, MAGENTA), ("AGENTIC AI", 450, 490, GREEN)]
    b = [f'<rect width="{W}" height="{H}" fill="url(#bg)" rx="22"/>']
    for r in (120, 190, 250):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CYAN}" stroke-opacity=".12" stroke-dasharray="4 10"/>')
    for t, x, y, c in nodes:
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{c}" stroke-width="3" stroke-dasharray="10 8" style="animation:drift 1.5s linear infinite" filter="url(#glow)"/>')
    random.seed(3)
    for _ in range(26):
        b.append(f'<circle cx="{random.randint(30,870)}" cy="{random.randint(30,530)}" r="2.5" fill="{VIOLET}" style="animation:pulse {random.uniform(2,5):.1f}s infinite {random.uniform(0,3):.1f}s"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="78" fill="{BG2}" stroke="url(#neon)" stroke-width="5" filter="url(#glow)" style="animation:pulse 3s infinite"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{CYAN}" filter="url(#glow)"/>')
    b.append(f'<text x="{cx}" y="{cy+112}" text-anchor="middle" font-size="26" font-weight="800" letter-spacing="4" fill="{TEXT}">AI CORE</text>')
    for t, x, y, c in nodes:
        w = 14 * len(t) + 36
        b.append(f'<rect x="{x-w/2}" y="{y-26}" width="{w}" height="52" rx="26" fill="#0B1325" stroke="{c}" stroke-width="2.5"/>')
        b.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="22" font-weight="700" letter-spacing="1" fill="{c}">{t}</text>')
    write("animations/ai-core.svg", svg(W, H, "\n".join(b), "AI Core connected to Computer Vision, LLMs, Generative AI and Agentic AI"))


# ───────────────────────── TECH CONSTELLATION ─────────────────────────
TECH = [
    ("AI / ML", CYAN, ["Python", "PyTorch", "TensorFlow", "Keras", "Scikit-learn", "Hugging Face", "OpenCV", "LangChain", "OpenAI API"]),
    ("BACKEND", VIOLET, ["FastAPI", "Flask", "REST APIs"]),
    ("DATA", MAGENTA, ["Pandas", "NumPy", "SQL", "Matplotlib"]),
    ("DEPLOYMENT", GREEN, ["Docker", "ONNX", "Git", "Weights & Biases"]),
    ("ENGINEERING", AMBER, ["AsyncIO", "Multi-threading", "Model Optimization", "Quantization", "Distributed Training", "Real-time Inference"]),
]


def tech():
    W = 900
    for label, c, items in TECH:
        x, y, rows = 0, 0, []
        for t in items:
            w = 16 * len(t) + 44
            if x + w > W - 150:
                x, y = 0, y + 62
            rows.append((x, y, w, t)); x += w + 14
        H = y + 62
        b = []
        for i, (rx, ry, w, t) in enumerate(rows):
            b.append(f'<g transform="translate({rx+150},{ry+4})" style="animation:pulse 5s infinite {i*.3:.1f}s">'
                     f'<rect width="{w}" height="48" rx="12" fill="#0B1325" stroke="{c}" stroke-opacity=".7" stroke-width="2"/>'
                     f'<circle cx="18" cy="24" r="4" fill="{c}" filter="url(#glow)"/>'
                     f'<text x="32" y="32" font-size="21" font-weight="600" fill="{TEXT}">{escape(t)}</text></g>')
        b.append(f'<text class="m" x="0" y="34" font-size="19" letter-spacing="2" fill="{c}">{label}</text>')
        write(f"tech/{label.lower().replace(' / ', '-').replace(' ', '-')}.svg", svg(W, H, "\n".join(b), f"{label}: {', '.join(items)}"))


# ───────────────────────── EXPERIENCE ─────────────────────────
def experience():
    W, H = 900, 760
    b = [panel(W, H, CYAN)]
    b.append(f'<text class="m" x="40" y="60" font-size="20" fill="{MUTED}">AUG 2025 ───────────────────────────────▶ NOW</text>')
    b.append(f'<path d="M60 130 V{H-50}" stroke="{CYAN}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 6"/>')
    blocks = [
        (CYAN, "INFOSYS", "Python Automation & AI Platform Developer", "Aug 2025 – Present",
         ["AI-powered enterprise workflow automation", "Scalable ML pipelines + FastAPI / Flask APIs", "Cross-team AI integration into enterprise systems"]),
        (VIOLET, "CANSPIRIT AI", "AI Developer Intern", "Jun 2024 – Jan 2025",
         ["FileFinder: document intelligence across millions of files", "Metadata extraction, retrieval efficiency 40%+", "Multi-threaded + async processing, end-to-end architecture"]),
        (MAGENTA, "IIT GANDHINAGAR", "AI / Game Development Intern", "Jun 2023 – Aug 2023",
         ["A* pathfinding + NPC behavior (RL concepts, decision trees)", "20% gain in game performance and responsiveness"]),
    ]
    y = 120
    for c, co, role, dates, bullets in blocks:
        b.append(f'<circle cx="60" cy="{y}" r="9" fill="{c}" filter="url(#glow)" style="animation:pulse 3s infinite"/>')
        b.append(f'<text x="90" y="{y+8}" font-size="29" font-weight="800" fill="{c}">{co}</text>')
        b.append(f'<text class="m" x="{W-40}" y="{y+6}" font-size="17" fill="{MUTED}" text-anchor="end">{dates}</text>')
        b.append(f'<text x="90" y="{y+38}" font-size="22" fill="{TEXT}">{escape(role)}</text>')
        for i, t in enumerate(bullets):
            glyph = "└──" if i == len(bullets)-1 else "├──"
            b.append(f'<text class="m" x="90" y="{y+72+i*30}" font-size="18" fill="{MUTED}">{glyph} {escape(t)}</text>')
        y += 72 + len(bullets)*30 + 52
    write("animations/experience.svg", svg(W, H, "\n".join(b), "Experience timeline: Infosys (Aug 2025 – Present), CanSpirit AI (Jun 2024 – Jan 2025), IIT Gandhinagar (Jun 2023 – Aug 2023)"))


# ───────────────────────── ACHIEVEMENTS ─────────────────────────
ACH = [("iisc", "IISc BANGALORE", "3rd Prize", "ML system achieving 20% accuracy improvement", AMBER),
       ("iitb", "IIT BOMBAY", "Robotic Optimization", "Reduced processing time by 30%", CYAN),
       ("iitbhu", "IIT BHU", "5,000+ Active Users", "Built and deployed a platform adopted by 5,000+ active users", GREEN),
       ("iitk", "IIT KANPUR", "Hackathon Finalist", "Finalist among 200+ teams", MAGENTA)]


def achievements():
    W, H = 440, 220
    for slug, inst, head, det, c in ACH:
        b = [panel(W, H, c)]
        b.append(f'<text class="m" x="28" y="52" font-size="17" letter-spacing="3" fill="{c}">★ {inst}</text>')
        b.append(f'<text x="28" y="100" font-size="30" font-weight="800" fill="{TEXT}">{escape(head)}</text>')
        for i, ln in enumerate(textwrap.wrap(det, 36)[:3]):
            b.append(f'<text x="28" y="{138+i*26}" font-size="18" fill="{MUTED}">{escape(ln)}</text>')
        write(f"achievements/{slug}.svg", svg(W, H, "\n".join(b), f"{inst}: {head}. {det}"))


# ───────────────────────── STATUS / NOW PLAYING / SOCIAL / FOOTER ─────────────────────────
def status():
    W, H = 440, 330
    items = ["AI Systems", "Generative AI", "Agentic AI", "Intelligent Automation", "Real-world ML applications", "Open Source"]
    b = [panel(W, H, GREEN), f'<text class="m" x="28" y="52" font-size="19" letter-spacing="3" fill="{GREEN}">CURRENTLY BUILDING</text>']
    for i, t in enumerate(items):
        b.append(f'<circle cx="36" cy="{96+i*38}" r="7" fill="{GREEN}" filter="url(#glow)" style="animation:pulse 2s infinite {i*.35:.2f}s"/>')
        b.append(f'<text class="m" x="58" y="{103+i*38}" font-size="20" fill="{TEXT}">{t}</text>')
    write("animations/status.svg", svg(W, H, "\n".join(b), "Currently building: " + ", ".join(items)))


def now_playing():
    W, H = 440, 330
    b = [panel(W, H, MAGENTA), f'<text class="m" x="28" y="52" font-size="19" letter-spacing="3" fill="{MAGENTA}">NOW PLAYING</text>',
         f'<text x="28" y="130" font-size="33" font-weight="800" fill="{TEXT}">Building the Future</text>',
         f'<text class="m" x="28" y="162" font-size="16" fill="{MUTED}">sarveshrock // ai-world.ost</text>',
         f'<rect x="28" y="200" width="384" height="8" rx="4" fill="{BG}" stroke="{MAGENTA}" stroke-opacity=".4"/>',
         f'<rect x="28" y="200" width="0" height="8" rx="4" fill="url(#neon)"><animate attributeName="width" from="0" to="384" dur="24s" repeatCount="indefinite"/></rect>',
         f'<text x="{W/2-70}" y="276" font-size="34" fill="{MUTED}" text-anchor="middle">◀</text>',
         f'<text x="{W/2}" y="276" font-size="34" fill="{TEXT}" text-anchor="middle">❚❚</text>',
         f'<text x="{W/2+70}" y="276" font-size="34" fill="{MUTED}" text-anchor="middle">▶</text>']
    write("animations/now-playing.svg", svg(W, H, "\n".join(b), "Now playing: Building the Future (visual only, no audio)"))


def button(slug, label, glyph, c, W=200):
    H = 64
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0B1325" stroke="{c}" stroke-width="2"/>',
         f'<text x="26" y="42" font-size="24" fill="{c}" filter="url(#glow)">{glyph}</text>',
         f'<text x="62" y="41" font-size="21" font-weight="700" letter-spacing="1" fill="{TEXT}">{label}</text>']
    write(f"social/{slug}.svg", svg(W, H, "\n".join(b), label))


def footer():
    W, H = 1200, 340
    random.seed(11)
    b = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>', f'<ellipse cx="600" cy="{H}" rx="700" ry="140" fill="{MAGENTA}" opacity=".18"/>']
    x = 0
    while x < W:
        bw = random.randint(40, 100); bh = random.randint(40, 140)
        b.append(f'<rect x="{x}" y="{H-bh}" width="{bw}" height="{bh}" fill="#070C1B"/>')
        for _ in range(3):
            b.append(f'<rect x="{x+random.randint(4,bw-12)}" y="{H-bh+random.randint(8,bh-14)}" width="6" height="9" fill="{random.choice([CYAN,MAGENTA,AMBER])}" opacity=".8" style="animation:pulse {random.uniform(3,8):.1f}s infinite {random.uniform(0,5):.1f}s"/>')
        x += bw + 4
    b.append(f'<rect x="300" y="40" width="600" height="190" rx="18" fill="#0B1325" stroke="url(#neon)" stroke-width="2.5"/>')
    b.append(f'<text x="600" y="108" text-anchor="middle" font-size="34" font-weight="800" letter-spacing="4" fill="{TEXT}" filter="url(#glow)">KEEP BUILDING. KEEP LEARNING.</text>')
    b.append(f'<text x="600" y="150" text-anchor="middle" font-size="21" fill="{MUTED}">Turning ideas into real-world intelligent solutions.</text>')
    b.append(f'<text class="m" x="600" y="202" text-anchor="middle" font-size="19" letter-spacing="3" fill="{CYAN}">SARVESHROCK // 2026</text>')
    write("backgrounds/footer.svg", svg(W, H, "\n".join(b), "Keep building. Keep learning. Sarveshrock 2026"))


def frame():
    """Contribution-matrix frame: header strip shown above the dynamic activity graph."""
    W, H = 900, 80
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0B1325" stroke="{CYAN}" stroke-opacity=".5" stroke-width="2"/>',
         f'<text class="m" x="28" y="48" font-size="22" fill="{CYAN}">&gt; contributions<tspan style="animation:blink 1s infinite">_</tspan></text>',
         f'<text class="m" x="{W-28}" y="48" font-size="17" fill="{MUTED}" text-anchor="end">LESS ░▒▓█ MORE</text>']
    write("backgrounds/contrib-frame.svg", svg(W, H, "\n".join(b), "Contribution matrix: less to more"))


# ───────────────────────── BANNER ─────────────────────────
def banner():
    W, H = 1200, 440
    random.seed(21)
    b = [f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120a33"/><stop offset=".55" stop-color="#5a2a7e"/><stop offset="1" stop-color="#d9507e"/></linearGradient>'
         f'<radialGradient id="moon" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#f2ecff"/><stop offset="1" stop-color="#9a86d8"/></radialGradient>'
         f'<linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG}" stop-opacity=".85"/><stop offset=".55" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    for _ in range(60):
        b.append(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,200)}" r="{random.choice([1,1,1.6])}" fill="#fff" opacity=".7" style="animation:pulse {random.uniform(2,6):.1f}s infinite {random.uniform(0,4):.1f}s"/>')
    b.append('<circle cx="790" cy="110" r="150" fill="url(#moon)" opacity=".92"/>')
    for cx, cy, r in ((740, 90, 26), (830, 150, 20), (780, 60, 14), (860, 70, 18)):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#7d6cc0" opacity=".35"/>')
    b.append(f'<ellipse cx="640" cy="330" rx="520" ry="40" fill="{MAGENTA}" opacity=".25"/>')
    layers = [("#3a1f66", 360, 150, .75, False), ("#1c1040", 400, 190, .95, True), ("#0a0720", 460, 150, 1, True)]
    for col, base, hmax, op, win in layers:
        x = -30
        while x < W:
            bw = random.randint(38, 96); bh = random.randint(40, hmax)
            b.append(f'<rect x="{x}" y="{base-bh}" width="{bw}" height="{bh+120}" fill="{col}" opacity="{op}"/>')
            if win:
                for wy in range(base-bh+10, base-4, 18):
                    for wx in range(x+7, x+bw-9, 15):
                        if random.random() < .2:
                            b.append(f'<rect x="{wx}" y="{wy}" width="6" height="9" fill="{random.choice([CYAN,MAGENTA,AMBER,"#ffd9f0"])}" opacity=".85" style="animation:pulse {random.uniform(3,9):.1f}s infinite {random.uniform(0,6):.1f}s"/>')
            x += bw + random.randint(2, 8)
    b.append(f'<path d="M1010 {H} V120 L1017 120 L1017 {H}z" fill="#0a0720"/><path d="M1013 120 V60" stroke="{MAGENTA}" stroke-width="2"/><circle cx="1013" cy="58" r="4" fill="{MAGENTA}" filter="url(#glow)" style="animation:pulse 2s infinite"/>')
    # ledge + hooded developer seen from behind
    b.append(f'<rect x="470" y="352" width="360" height="{H-352}" fill="#05030f"/><rect x="470" y="352" width="360" height="3" fill="{CYAN}" opacity=".7" filter="url(#glow)"/>')
    body = "M588 352 C586 292 606 252 642 248 C680 252 700 292 698 352Z"
    b.append('<path d="M690 346 q52 -14 88 8 l-4 -18 q-44 -22 -84 0z" fill="#07041a"/>')
    b.append(f'<path d="{body}" fill="#0a0722" stroke="{MAGENTA}" stroke-opacity=".6" stroke-width="2"/>')
    b.append(f'<circle cx="644" cy="222" r="36" fill="#0a0722" stroke="{MAGENTA}" stroke-opacity=".6" stroke-width="2"/>')
    b.append('<path d="M614 204 l-8 -26 l24 14 l8 -30 l14 28 l22 -16 l-4 28z" fill="#0a0722"/>')
    b.append(f'<circle cx="643" cy="298" r="22" fill="none" stroke="{CYAN}" stroke-width="3" filter="url(#glow)"/><text class="m" x="643" y="305" text-anchor="middle" font-size="17" font-weight="700" fill="{CYAN}">&lt;/&gt;</text>')
    # floating code panel
    b.append(f'<g transform="translate(850,48) skewY(-3)"><rect width="250" height="150" rx="10" fill="#101C45" stroke="{CYAN}" stroke-width="2" filter="url(#glow)"/>')
    for i, (t, c) in enumerate([("while (ideas) {", TEXT), ("  build();", GREEN), ("  learn();", AMBER), ("  improve();", MAGENTA), ("}", TEXT), ("// still in progress...", MUTED)]):
        b.append(f'<text class="m" x="16" y="{28+i*22}" font-size="15" fill="{c}">{escape(t)}</text>')
    b.append('</g>')
    for i, (t, c) in enumerate([("CODE", TEXT), ("LEARN", TEXT), ("BUILD", TEXT), ("EXPLORE", TEXT), ("REPEAT", MAGENTA)]):
        b.append(f'<text class="m" x="1170" y="{240+i*26}" font-size="18" letter-spacing="3" fill="{c}" text-anchor="end">{t}</text>')
    b.append(f'<rect width="640" height="{H}" fill="url(#shade)"/>')
    script = "'Segoe Script','Snell Roundhand','Brush Script MT','Lucida Handwriting',cursive"
    b.append(f'<text x="40" y="132" font-family="{script}" font-size="84" fill="#fff" fill-opacity=".9" stroke="url(#neon)" stroke-width="2" filter="url(#glow)">Sarvesh</text>')
    b.append(f'<text x="120" y="222" font-family="{script}" font-size="84" fill="#fff" fill-opacity=".9" stroke="url(#neon)" stroke-width="2" filter="url(#glow)">Shimpi</text>')
    b.append(f'<text class="m" x="44" y="290" font-size="24" font-weight="700" letter-spacing="4" fill="{CYAN}">AI/ML ENGINEER</text>')
    b.append(f'<text class="m" x="44" y="322" font-size="18" letter-spacing="3" fill="{TEXT}">BUILDING INTELLIGENT SYSTEMS</text>')
    b.append(f'<text class="m" x="44" y="348" font-size="18" letter-spacing="3" fill="{TEXT}">FOR THE REAL WORLD<tspan fill="{GREEN}" style="animation:blink 1s infinite"> _</tspan></text>')
    b.append(f'<text x="44" y="410" font-size="19" font-style="italic" fill="{TEXT}" opacity=".85">“Building AI solutions for a better tomorrow.”</text>')
    return svg(W, H, "\n".join(b), "Sarvesh Shimpi — AI/ML Engineer. Building intelligent systems for the real world.")


# ───────────────────────── PANEL TITLES ─────────────────────────
def header(slug, label, sub, accent):
    W, H = 1000, 56
    b = (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="#0B1325" stroke="{accent}" stroke-opacity=".45" stroke-width="2"/>'
         f'<text class="m" x="24" y="37" font-size="22" fill="{accent}">&gt;_ <tspan fill="{TEXT}">{escape(label)}</tspan></text>'
         f'<text class="m" x="{W-24}" y="35" font-size="14" fill="{MUTED}" text-anchor="end">{escape(sub)}</text>')
    write(f"headers/{slug}.svg", svg(W, H, b, label))


# ───────────────────────── PROJECT CARDS (repo-card style) ─────────────────────────
PROJECTS = [  # slug, name, category, accent, description, stack, glyph
    ("voice-agent", "AI Voice Agent for Doctor Appointment Booking", "GENERATIVE AI", MAGENTA,
     "Autonomous multi-turn voice agent. Cut manual booking workload by 70%.", "Whisper • LLM • TTS", "♫"),
    ("deepfake", "Deepfake Video Detection System", "COMPUTER VISION", CYAN,
     "Hybrid CNN-RNN spatial-temporal detector with MTCNN preprocessing.", "CNN • LSTM • Transformer", "◈"),
    ("ml-platform", "Multi-Model ML Prediction Platform", "ML SYSTEMS", AMBER,
     "Placement delay, salary and risk prediction. Optuna, A/B testing, Docker REST API.", "Optuna • Docker • Flask", "▦"),
    ("draggan", "DragGAN", "GENERATIVE AI", MAGENTA,
     "Point-based real-time image editing with custom losses and refinements.", "GAN • Custom Loss", "✦"),
    ("pothole", "Real-Time Pothole Detection", "COMPUTER VISION", CYAN,
     "Road damage detection deployed on edge devices for smart-city monitoring.", "YOLOv8 • EfficientDet", "⌖"),
    ("rag-qa", "LLM Recommendation & Q&A System", "LLM · RAG", VIOLET,
     "RAG plus fine-tuned LLM with hybrid vector search for domain Q&A.", "RAG • FAISS • Chroma", "❖"),
    ("travel-planner", "AI Travel Planner", "AGENTIC AI", GREEN,
     "Multi-agent itinerary generator with a responsive full-stack web app.", "LangChain • OpenAI • Next.js", "✈"),
    ("unmaskai", "UnmaskAI", "HACKATHON · PUBLIC REPO", AMBER,
     "SEED Hackathon submission.", "Python", "◆"),
]


def project_cards():
    W, H = 600, 190
    for slug, name, cat, c, desc, stack, glyph in PROJECTS:
        pub = "PUBLIC REPO" in cat
        b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0B1325" stroke="{c}" stroke-opacity=".6" stroke-width="2"/>',
             f'<text x="34" y="52" font-size="30" fill="{c}" filter="url(#glow)">{glyph}</text>']
        for i, ln in enumerate(textwrap.wrap(name, 34)[:2]):
            b.append(f'<text x="76" y="{48+i*26}" font-size="23" font-weight="700" fill="{c}">{escape(ln)}</text>')
        for i, ln in enumerate(textwrap.wrap(desc, 52)[:2]):
            b.append(f'<text x="30" y="{98+i*24}" font-size="18" fill="{MUTED}">{escape(ln)}</text>')
        px = 30
        for t in stack.split(" • "):
            w = 11 * len(t) + 26
            b.append(f'<rect x="{px}" y="140" width="{w}" height="28" rx="14" fill="{BG}" stroke="{c}" stroke-opacity=".5"/><text class="m" x="{px+13}" y="159" font-size="14" fill="{TEXT}">{escape(t)}</text>')
            px += w + 8
        tag = "GITHUB" if pub else "RESUME · NO PUBLIC REPO"
        b.append(f'<text class="m" x="{W-24}" y="{H-14}" font-size="11" letter-spacing="1" fill="{MUTED}" text-anchor="end">SOURCE: {tag}</text>')
        write(f"projects/{slug}.svg", svg(W, H, "\n".join(b), f"{name} — {cat}. {desc}"))


# ───────────────────────── TECH: chips for items without an official icon ─────────────────────────
TECH = [
    ("MORE AI / ML", CYAN, ["Hugging Face", "LangChain", "OpenAI API", "Albumentations", "Weights & Biases"]),
    ("DATA / APIs", VIOLET, ["SQL", "Matplotlib", "REST APIs", "ONNX"]),
    ("ENGINEERING", AMBER, ["AsyncIO", "Multi-threading", "Model Optimization", "Quantization", "Distributed Training", "Real-time Inference", "A/B Testing", "Feature Engineering"]),
]


if __name__ == "__main__":
    write("hero/banner.svg", banner())
    for slug, label, sub, c in [("contributions", "contributions", "last 12 months · live", CYAN), ("stack", "Tech Stack", "from resume", VIOLET),
                                ("projects", "Projects", "from resume + GitHub", MAGENTA), ("ai", "AI Systems", "core", CYAN),
                                ("terminal", "Terminal", "shell", VIOLET), ("experience", "Experience", "system log", CYAN),
                                ("vault", "Achievement Vault", "from resume", AMBER), ("status", "Status", "live", GREEN), ("contact", "Contact", "open channel", MAGENTA)]:
        header(slug, label, sub, c)
    terminal(); ai_core(); project_cards(); tech(); experience(); achievements(); status(); now_playing(); footer()
    button("github", "GitHub", "⌥", CYAN); button("email", "Email", "✉", MAGENTA)
    button("linkedin", "LinkedIn", "in", VIOLET); button("portfolio", "Portfolio", "◈", GREEN); button("enter", "ENTER SARVESH.OS →", "▶", MAGENTA, 340)
