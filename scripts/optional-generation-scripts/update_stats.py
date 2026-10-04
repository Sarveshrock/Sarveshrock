#!/usr/bin/env python3
"""Builds the dynamic dashboard SVGs from live GitHub data. Pure stdlib, no secrets needed
(GITHUB_TOKEN is used only to lift the API rate limit when running in Actions).

Outputs (relative to repo root): assets/dynamic/stats.svg, contributions.svg, languages.svg
Every number comes from the GitHub API / public contribution calendar. Nothing is hardcoded.
"""
import json, os, re, sys, urllib.request
from datetime import date
from xml.sax.saxutils import escape

USER = "Sarveshrock"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "dynamic")
BG2 = "#0A1020"; CYAN = "#22E4FF"; VIOLET = "#8B5CF6"; MAGENTA = "#FF2BD6"; GREEN = "#39FF88"
TEXT = "#EAF2FF"; MUTED = "#8FA3BF"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Courier New',monospace"
SANS = "'Space Grotesk','Inter','Segoe UI',Helvetica,Arial,sans-serif"
LANG_COLORS = {"Python": "#3572A5", "JavaScript": "#F1E05A", "Java": "#F89820", "HTML": "#E34C26", "CSS": "#8B5CF6",
               "Dart": "#22E4FF", "Jupyter Notebook": "#DA5B0B", "TypeScript": "#3178C6", "C++": "#F34B7D", "Makefile": "#427819",
               "Shell": "#89E051"}
FALLBACK = ["#8B5CF6", "#22E4FF", "#FF2BD6", "#39FF88", "#FFB020"]


def get(url, accept=None):
    h = {"User-Agent": "profile-stats"}
    if accept: h["Accept"] = accept
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and "api.github.com" in url: h["Authorization"] = f"Bearer {tok}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode("utf-8")


def wrap(w, h, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs><filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient></defs>
<style>text{{font-family:{SANS}}} .m{{font-family:{MONO}}}
@keyframes pulse{{0%,100%{{opacity:.4}}50%{{opacity:1}}}} @keyframes spin{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
{body}
</svg>'''


def card(w, h, accent):
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="#0B1325" stroke="{accent}" stroke-opacity=".5" stroke-width="2"/>')


def save(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f: f.write(content)
    print("wrote", name)


def tiles(user, total):
    W, H = 1200, 120
    items = [("Repositories", user["public_repos"], CYAN, "▣"), ("Contributions · 1y", total, GREEN, "∿"),
             ("Followers", user["followers"], VIOLET, "◉"), ("Following", user["following"], MAGENTA, "◎")]
    tw, gap = 228, 15
    b = []
    for i, (label, val, c, g) in enumerate(items):
        x = i * (tw + gap)
        b.append(f'<g transform="translate({x},0)">{card(tw, H, c)}<circle cx="46" cy="60" r="26" fill="{BG2}" stroke="{c}" stroke-width="2"/>'
                 f'<text x="46" y="70" text-anchor="middle" font-size="26" fill="{c}" filter="url(#glow)">{g}</text>'
                 f'<text x="88" y="64" font-size="42" font-weight="800" fill="{TEXT}">{val}</text>'
                 f'<text x="90" y="92" font-size="{15 if len(label)>14 else 18}" fill="{MUTED}">{escape(label)}</text></g>')
    x = 4 * (tw + gap)
    b.append(f'<g transform="translate({x},0)">{card(tw, H, CYAN)}<text x="24" y="52" font-size="40" fill="{CYAN}" filter="url(#glow)">“</text>'
             f'<text class="m" x="64" y="48" font-size="13" fill="{TEXT}">Turning ideas into</text>'
             f'<text class="m" x="64" y="72" font-size="13" fill="{TEXT}">real-world intelligent</text>'
             f'<text class="m" x="64" y="96" font-size="13" fill="{TEXT}">solutions.</text></g>')
    return wrap(W, H, "\n".join(b), f"GitHub: {user['public_repos']} repositories, {total} contributions in the last year, {user['followers']} followers, {user['following']} following")


def contributions(cells, total):
    W, H = 900, 262
    lv = ["#101A2C", "#0E4A33", "#13854E", "#22C066", "#39FF88"]
    cells = sorted(cells)
    first = date.fromisoformat(cells[0][0])
    off = (first.weekday() + 1) % 7  # Sunday = 0
    cs, gp, x0, y0 = 12, 3, 70, 96
    b = [card(W, H, CYAN),
         f'<text class="m" x="28" y="44" font-size="20"><tspan fill="{CYAN}">&gt;_ </tspan><tspan fill="{GREEN}">sarveshrock@github:~$</tspan><tspan fill="{TEXT}"> contributions</tspan></text>']
    months, last_m = [], None
    for i, (d, l) in enumerate(cells):
        idx = i + off
        wk, dy = idx // 7, idx % 7
        x, y = x0 + wk * (cs + gp), y0 + dy * (cs + gp)
        b.append(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" rx="2" fill="{lv[l]}"/>')
        m = d[5:7]
        if m != last_m and dy < 7:
            months.append((x, ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(m)-1])); last_m = m
    prev = -99
    for x, name in months:
        if x - prev >= 44:
            b.append(f'<text class="m" x="{x}" y="{y0-12}" font-size="13" fill="{MUTED}">{name}</text>'); prev = x
    for r, nm in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b.append(f'<text class="m" x="24" y="{y0 + r*(cs+gp) + 10}" font-size="12" fill="{MUTED}">{nm}</text>')
    b.append(f'<text class="m" x="28" y="{H-24}" font-size="16" fill="{TEXT}">{total} contributions in the last year</text>')
    lx = W - 250
    b.append(f'<text class="m" x="{lx}" y="{H-24}" font-size="14" fill="{MUTED}">Less</text>')
    for i, c in enumerate(lv):
        b.append(f'<rect x="{lx+44+i*18}" y="{H-36}" width="13" height="13" rx="2" fill="{c}"/>')
    b.append(f'<text class="m" x="{lx+44+5*18+6}" y="{H-24}" font-size="14" fill="{MUTED}">More</text>')
    return wrap(W, H, "\n".join(b), f"{total} GitHub contributions in the last year")


def lang_rows(repos):
    """Top-5 languages + Other by code size across non-fork public repos. Raises on API failure."""
    tot = {}
    for r in repos:
        if r["fork"]: continue
        data = json.loads(get(r["languages_url"]))  # raises on rate limit: better no update than partial data
        for k, v in data.items(): tot[k] = tot.get(k, 0) + v
    s = sum(tot.values()) or 1
    top = sorted(tot.items(), key=lambda kv: -kv[1])
    rows = top[:5]
    other = sum(v for _, v in top[5:])
    if other: rows.append(("Other", other))
    return rows, s


def languages(repos):
    W, H = 900, 300
    rows, s = lang_rows(repos)
    b = [card(W, H, VIOLET), f'<text x="28" y="46" font-size="22" font-weight="700" fill="{TEXT}">Most Used Languages</text>']
    x = 28; bw = 470
    for i, (k, v) in enumerate(rows):
        w = max(2, bw * v / s)
        b.append(f'<rect x="{x:.1f}" y="66" width="{w:.1f}" height="10" rx="3" fill="{LANG_COLORS.get(k, FALLBACK[i % 5])}"/>'); x += w
    for i, (k, v) in enumerate(rows):
        y = 122 + i * 27
        c = LANG_COLORS.get(k, FALLBACK[i % 5])
        b.append(f'<circle cx="38" cy="{y-5:.0f}" r="7" fill="{c}"/><text x="58" y="{y:.0f}" font-size="19" fill="{TEXT}">{escape(k)}</text>'
                 f'<text x="{28+bw}" y="{y:.0f}" font-size="19" fill="{MUTED}" text-anchor="end">{100*v/s:.1f}%</text>')
    b.append(f'<text class="m" x="28" y="{H-16}" font-size="12" fill="{MUTED}">by code size, non-fork public repositories</text>')
    cx, cy = 720, 160
    b.append(f'<circle cx="{cx}" cy="{cy}" r="96" fill="none" stroke="url(#neon)" stroke-width="3" stroke-dasharray="6 10" style="transform-origin:{cx}px {cy}px;animation:spin 40s linear infinite"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="68" fill="{BG2}" stroke="url(#neon)" stroke-width="4" filter="url(#glow)"/>')
    b.append(f'<text x="{cx}" y="{cy+16}" text-anchor="middle" font-size="46" font-weight="800" fill="{CYAN}" filter="url(#glow)">AI</text>')
    return wrap(W, H, "\n".join(b), "Most used languages: " + ", ".join(f"{k} {100*v/s:.1f}%" for k, v in rows))


def collect():
    user = json.loads(get(f"https://api.github.com/users/{USER}"))
    repos = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100"))
    html = get(f"https://github.com/users/{USER}/contributions")
    cells = []
    for tag in re.findall(r"<td [^>]*data-date=[^>]*>", html):
        d = re.search(r'data-date="([\d-]+)"', tag); l = re.search(r'data-level="(\d)"', tag)
        if d and l: cells.append((d.group(1), int(l.group(1))))
    tm = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", html)
    if not cells or not tm: sys.exit("could not parse contribution calendar; leaving existing assets untouched")
    return user, repos, cells, int(tm.group(1).replace(",", ""))


def main():
    user = json.loads(get(f"https://api.github.com/users/{USER}"))
    repos = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100"))
    html = get(f"https://github.com/users/{USER}/contributions")
    cells = []
    for tag in re.findall(r"<td [^>]*data-date=[^>]*>", html):
        d = re.search(r'data-date="([\d-]+)"', tag); l = re.search(r'data-level="(\d)"', tag)
        if d and l: cells.append((d.group(1), int(l.group(1))))
    tm = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", html)
    if not cells or not tm: sys.exit("could not parse contribution calendar; leaving existing assets untouched")
    total = int(tm.group(1).replace(",", ""))
    save("stats.svg", tiles(user, total))
    save("contributions.svg", contributions(cells, total))
    save("languages.svg", languages(repos))


if __name__ == "__main__":
    main()
