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


# ───────────────────────── HERO ─────────────────────────
def hero():
    random.seed(7)
    W, H = 1200, 600
    b = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<ellipse cx="600" cy="430" rx="700" ry="170" fill="{MAGENTA}" opacity=".16"/>',
         f'<ellipse cx="300" cy="400" rx="420" ry="120" fill="{VIOLET}" opacity=".18"/>']
    for _ in range(70):
        b.append(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,300)}" r="{random.choice([1,1,1.5,2])}" fill="#fff" opacity=".6" style="animation:pulse {random.uniform(2,6):.1f}s infinite {random.uniform(0,4):.1f}s"/>')
    # skyline (two layers) with windows
    for layer, (col, base, hmax, op) in enumerate([("#0B1226", 470, 230, 1), ("#070C1B", 520, 300, 1)]):
        x = -20
        while x < W:
            bw = random.randint(46, 110); bh = random.randint(70, hmax)
            b.append(f'<rect x="{x}" y="{base-bh}" width="{bw}" height="{bh+200}" fill="{col}"/>')
            if layer == 1:
                for wy in range(base-bh+12, base-6, 22):
                    for wx in range(x+8, x+bw-10, 18):
                        if random.random() < .22:
                            c = random.choice([CYAN, MAGENTA, AMBER, VIOLET])
                            b.append(f'<rect x="{wx}" y="{wy}" width="7" height="10" fill="{c}" opacity=".85" style="animation:pulse {random.uniform(3,9):.1f}s infinite {random.uniform(0,6):.1f}s"/>')
            x += bw + random.randint(2, 10)
    # desk + developer + laptop (right)
    b.append(f'<rect x="760" y="520" width="440" height="80" fill="#04060B"/>')
    b.append(f'<path d="M880 520 q0 -70 60 -90 q60 20 60 90z" fill="#02040A"/><circle cx="940" cy="408" r="30" fill="#02040A"/>')
    b.append(f'<path d="M840 530 L1030 530 L1010 450 L860 450z" fill="#0D1530" stroke="{CYAN}" stroke-opacity=".7" stroke-width="2"/>')
    b.append(f'<rect x="868" y="458" width="134" height="62" fill="{CYAN}" opacity=".12"/><path d="M880 480 h50 M880 494 h86 M880 508 h30" stroke="{CYAN}" stroke-width="3" opacity=".8"/>')
    b.append(f'<path d="M800 530 H1070" stroke="{MAGENTA}" stroke-width="3" filter="url(#glow)"/>')
    # scanline overlay
    b.append(f'<rect width="{W}" height="40" fill="{CYAN}" opacity=".05" style="animation:scan 6s linear infinite"/>')
    # title
    b.append(f'<text x="60" y="170" font-size="104" font-weight="800" letter-spacing="6" fill="url(#neon)" filter="url(#glow)">SARVESH</text>')
    b.append(f'<text x="60" y="270" font-size="104" font-weight="800" letter-spacing="6" fill="url(#neon)" filter="url(#glow)">SHIMPI</text>')
    b.append(f'<text x="64" y="320" font-size="30" font-weight="700" letter-spacing="5" fill="{CYAN}">AI/ML ENGINEER</text>')
    b.append(f'<text x="64" y="356" font-size="22" letter-spacing="3" fill="{TEXT}">BUILDING INTELLIGENT SYSTEMS FOR THE REAL WORLD</text>')
    b.append(f'<rect x="40" y="378" width="520" height="222" rx="14" fill="{BG}" opacity=".78"/>')
    lines = ["initializing...", "AI systems online", "generative AI online", "computer vision online", "agentic systems online", "ready to build"]
    for i, l in enumerate(lines):
        col = GREEN if i == len(lines)-1 else MUTED
        b.append(f'<text class="m" x="64" y="{405+i*26}" font-size="19" fill="{col}" opacity="0" style="animation:fade .4s forwards {0.6+i*0.7:.1f}s">&gt; {l}</text>')
    b.append(f'<rect x="64" y="{405+6*26-14}" width="11" height="20" fill="{GREEN}" style="animation:blink 1s infinite 5s"/>')
    b.append(f'<text x="64" y="578" font-size="20" font-style="italic" fill="{MUTED}">“Building AI solutions for a better tomorrow.”</text>')
    return svg(W, H, "\n".join(b), "Sarvesh Shimpi — AI/ML Engineer. Building intelligent systems for the real world.")


# ───────────────────────── SECTION HEADERS ─────────────────────────
def header(slug, label, sub, accent):
    W, H = 1000, 90
    b = (f'<rect width="{W}" height="{H}" fill="none"/>'
         f'<path d="M0 70 H{W}" stroke="{accent}" stroke-opacity=".35" stroke-width="2"/>'
         f'<path d="M0 70 H260" stroke="{accent}" stroke-width="3" filter="url(#glow)" stroke-dasharray="14 6" style="animation:drift 2s linear infinite"/>'
         f'<text class="m" x="4" y="22" font-size="17" fill="{accent}" letter-spacing="3">// {escape(sub)}</text>'
         f'<text x="2" y="62" font-size="40" font-weight="800" letter-spacing="4" fill="{TEXT}">{escape(label)}</text>')
    write(f"headers/{slug}.svg", svg(W, H, b, label))


# ───────────────────────── IDENTITY PANEL ─────────────────────────
def identity():
    W, H = 900, 400
    items = ["AI/ML Engineer", "Generative AI", "Agentic AI", "Computer Vision", "LLM Systems", "Real-time AI"]
    b = [panel(W, H, CYAN),
         f'<text class="m" x="40" y="62" font-size="24" fill="{CYAN}" letter-spacing="2">SARVESHROCK // AI ENGINEER</text>',
         f'<path d="M40 82 H{W-40}" stroke="{CYAN}" stroke-opacity=".3"/>']
    for i, t in enumerate(items):
        col, row = i % 2, i // 2
        x, y = 40 + col * 400, 140 + row * 62
        c = [CYAN, VIOLET, MAGENTA][row]
        b.append(f'<circle cx="{x+8}" cy="{y-8}" r="6" fill="{c}" filter="url(#glow)" style="animation:pulse 3s infinite {i*.4:.1f}s"/>')
        b.append(f'<text x="{x+28}" y="{y}" font-size="32" font-weight="600" fill="{TEXT}">{t}</text>')
    b.append(f'<path d="M40 {H-70} H{W-40}" stroke="{CYAN}" stroke-opacity=".3"/>')
    b.append(f'<text class="m" x="40" y="{H-28}" font-size="23" fill="{GREEN}">Problem Solver • Builder • Learner</text>')
    write("hero/identity-panel.svg", svg(W, H, "\n".join(b), "Identity panel: AI/ML Engineer, Generative AI, Agentic AI, Computer Vision, LLM Systems, Real-time AI"))


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
        b.append(f'<rect x="{x-w/2}" y="{y-26}" width="{w}" height="52" rx="26" fill="rgba(15,25,45,.92)" stroke="{c}" stroke-width="2.5"/>')
        b.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="22" font-weight="700" letter-spacing="1" fill="{c}">{t}</text>')
    write("animations/ai-core.svg", svg(W, H, "\n".join(b), "AI Core connected to Computer Vision, LLMs, Generative AI and Agentic AI"))


# ───────────────────────── PROJECT CARDS ─────────────────────────
PROJECTS = [  # slug, name, category, accent, description, stack
    ("voice-agent", "AI VOICE AGENT", "GENERATIVE AI · VOICE", MAGENTA,
     "Autonomous multi-turn voice agent for doctor appointment booking. Cut manual booking workload by 70%.", "Whisper • LLM • TTS • Intent"),
    ("deepfake", "DEEPFAKE DETECTION", "COMPUTER VISION", CYAN,
     "Hybrid CNN-RNN spatial-temporal detector with MTCNN preprocessing and low-latency inference.", "CNN • LSTM • Transformer • MTCNN"),
    ("ml-platform", "MULTI-MODEL ML PLATFORM", "ML SYSTEMS", AMBER,
     "Multi-task placement delay, salary and risk prediction. Optuna tuning, A/B testing, Dockerized REST API.", "Optuna • Docker • Flask • Gunicorn"),
    ("draggan", "DRAGGAN", "GENERATIVE AI", MAGENTA,
     "Point-based real-time image editing with custom losses for better training stability and fewer artifacts.", "GAN • Custom Loss • Image Editing"),
    ("pothole", "POTHOLE DETECTION", "COMPUTER VISION · EDGE", CYAN,
     "Real-time pothole and road-damage detection deployed on edge devices for smart-city monitoring.", "YOLOv8 • EfficientDet • Edge"),
    ("rag-qa", "LLM RECOMMENDATION & Q&A", "LLM · RAG", VIOLET,
     "RAG plus fine-tuned LLM for domain-specific question answering with hybrid vector search.", "RAG • FAISS • Chroma • Fine-tuning"),
    ("travel-planner", "AI TRAVEL PLANNER", "AGENTIC AI", GREEN,
     "Multi-agent itinerary generator with a responsive full-stack web app and dynamic visualizations.", "LangChain • OpenAI • Next.js • TypeScript"),
    # public repository (GitHub-verified description only)
    ("unmaskai", "UNMASKAI", "HACKATHON · PUBLIC REPO", AMBER,
     "SEED Hackathon submission.", "Python"),
]


def project_cards():
    W, H = 600, 270
    for slug, name, cat, c, desc, stack in PROJECTS:
        b = [panel(W, H, c)]
        b.append(f'<text x="30" y="58" font-size="28" font-weight="800" fill="{TEXT}">◈ {escape(name)}</text>')
        b.append(f'<text class="m" x="30" y="90" font-size="16" letter-spacing="2" fill="{c}">{escape(cat)}</text>')
        for i, ln in enumerate(textwrap.wrap(desc, 46)[:3]):
            b.append(f'<text x="30" y="{128+i*27}" font-size="19" fill="{MUTED}">{escape(ln)}</text>')
        b.append(f'<text class="m" x="30" y="{H-48}" font-size="16" fill="{TEXT}">{escape(stack)}</text>')
        b.append(f'<path d="M30 {H-34} H{W-30}" stroke="{c}" stroke-opacity=".3"/>')
        tag = "SOURCE: GITHUB" if "PUBLIC REPO" in cat else "SOURCE: RESUME · NO PUBLIC REPO"
        b.append(f'<text class="m" x="30" y="{H-12}" font-size="13" letter-spacing="1" fill="{MUTED}">{tag}</text>')
        b.append(f'<rect x="0" y="0" width="{W}" height="30" fill="{c}" opacity=".07" style="animation:scan 5s linear infinite"/>')
        write(f"projects/{slug}.svg", svg(W, H, "\n".join(b), f"{name} — {cat}. {desc}"))


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
                     f'<rect width="{w}" height="48" rx="12" fill="rgba(15,25,45,.85)" stroke="{c}" stroke-opacity=".7" stroke-width="2"/>'
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


def button(slug, label, glyph, c):
    W, H = 200, 64
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="rgba(15,25,45,.9)" stroke="{c}" stroke-width="2"/>',
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
    b.append(f'<rect x="300" y="40" width="600" height="190" rx="18" fill="rgba(15,25,45,.8)" stroke="url(#neon)" stroke-width="2.5"/>')
    b.append(f'<text x="600" y="108" text-anchor="middle" font-size="34" font-weight="800" letter-spacing="4" fill="{TEXT}" filter="url(#glow)">KEEP BUILDING. KEEP LEARNING.</text>')
    b.append(f'<text x="600" y="150" text-anchor="middle" font-size="21" fill="{MUTED}">Turning ideas into real-world intelligent solutions.</text>')
    b.append(f'<text class="m" x="600" y="202" text-anchor="middle" font-size="19" letter-spacing="3" fill="{CYAN}">SARVESHROCK // 2026</text>')
    write("backgrounds/footer.svg", svg(W, H, "\n".join(b), "Keep building. Keep learning. Sarveshrock 2026"))


def frame():
    """Contribution-matrix frame: header strip shown above the dynamic activity graph."""
    W, H = 900, 80
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="rgba(15,25,45,.85)" stroke="{CYAN}" stroke-opacity=".5" stroke-width="2"/>',
         f'<text class="m" x="28" y="48" font-size="22" fill="{CYAN}">&gt; contributions<tspan style="animation:blink 1s infinite">_</tspan></text>',
         f'<text class="m" x="{W-28}" y="48" font-size="17" fill="{MUTED}" text-anchor="end">LESS ░▒▓█ MORE</text>']
    write("backgrounds/contrib-frame.svg", svg(W, H, "\n".join(b), "Contribution matrix: less to more"))


if __name__ == "__main__":
    write("hero/hero.svg", hero())
    for slug, label, sub, c in [("identity", "IDENTITY", "who", CYAN), ("terminal", "TERMINAL", "shell", VIOLET), ("stats", "SYSTEM STATS", "live telemetry", GREEN),
                                ("matrix", "CONTRIBUTION MATRIX", "activity", CYAN), ("stack", "TECHNOLOGY CONSTELLATION", "stack", VIOLET),
                                ("projects", "FEATURED PROJECTS", "builds", MAGENTA), ("ai", "AI SYSTEMS", "core", CYAN),
                                ("experience", "EXPERIENCE", "system log", CYAN), ("vault", "ACHIEVEMENT VAULT", "unlocked", AMBER),
                                ("status", "STATUS", "live", GREEN), ("contact", "CONTACT", "open channel", MAGENTA)]:
        header(slug, label, sub, c)
    identity(); terminal(); ai_core(); project_cards(); tech(); experience(); achievements(); status(); now_playing(); footer(); frame()
    button("github", "GitHub", "⌥", CYAN); button("email", "Email", "✉", MAGENTA)
    button("linkedin", "LinkedIn", "in", VIOLET); button("portfolio", "Portfolio", "◈", GREEN)
