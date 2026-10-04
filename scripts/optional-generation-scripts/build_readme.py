#!/usr/bin/env python3
"""Generates README.md from data/profile.json so the README, dashboard and website share one verified data model.

Interactivity that GitHub allows in a README:
  - tab-like nav: pill images linking to #section anchors
  - click-to-expand sections via <details> (nested for projects and roles)
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = json.load(open(os.path.join(ROOT, "data", "profile.json"), encoding="utf-8"))
RAW = "https://raw.githubusercontent.com/Sarveshrock/Sarveshrock/main/assets"
I = D["identity"]; P = D["professional"]

lines = []
w = lines.append
NL = "\n"

# ── dashboard + link buttons ──
w('<div align="center">' + NL)
w('<picture>')
w(f'  <source media="(max-width: 700px)" srcset="{RAW}/dashboard/mobile.svg">')
w(f'  <img src="{RAW}/dashboard/desktop.svg" width="100%" alt="Sarvesh Shimpi — AI/ML Engineer. Profile dashboard: stats, contributions, languages, tech stack, projects, experience, achievements.">')
w('</picture>' + NL)
w('<!-- TODO: after you deploy the SARVESH.OS website (see web repo README), replace YOUR_VERIFIED_DOMAIN and uncomment:')
w('<a href="https://YOUR_VERIFIED_DOMAIN"><img src="assets/social/enter.svg" height="48" alt="ENTER SARVESH.OS" /></a>')
w('-->' + NL)
w(f'<a href="{I["github"]}"><img src="assets/social/github.svg" height="44" alt="GitHub" /></a>')
w(f'<a href="mailto:{I["email"]}"><img src="assets/social/email.svg" height="44" alt="Email" /></a>')
w(f'<a href="{I["linkedin"]}"><img src="assets/social/linkedin.svg" height="44" alt="LinkedIn" /></a>')
w(f'<a href="{I["portfolio"]}"><img src="assets/social/portfolio.svg" height="44" alt="Portfolio" /></a>' + NL)

# ── tab-like navigation (anchors) ──
for sl in ("projects", "experience", "achievements", "skills", "contact"):
    w(f'<a href="#{sl}"><img src="assets/social/nav-{sl}.svg" height="40" alt="{sl}" /></a>')
w(NL + '</div>' + NL)

# ── expandable sections ──
w('## Projects' + NL)
w('<details>')
w(f'<summary><b>Open all {len(D["projects"])} projects</b> · click a project to expand</summary>' + NL)
for p in D["projects"]:
    w('<details>')
    w(f'<summary><b>{p["name"]}</b> · <i>{p["category"]}</i></summary>' + NL)
    w(p["description"] + NL)
    w(f'**Stack:** {" · ".join(p["stack"])}' + NL)
    w((f'**Source:** [{p["repo"]}]({p["repo"]})' if p["repo"] else '**Source:** resume (no public repository)') + NL)
    w('</details>' + NL)
w('</details>' + NL)

w('## Experience' + NL)
w('<details>')
w('<summary><b>Open work history</b> · click a role to expand</summary>' + NL)
for e in D["experience"]:
    w('<details>')
    w(f'<summary><b>{e["company"]}</b> — {e["role"]} · <i>{e["dates"]}</i></summary>' + NL)
    for bl in e["bullets"]:
        w(f'- {bl}')
    w(NL + '</details>' + NL)
ed = D["education"]
w(f'_{ed["degree"]}, {ed["institution"]}, {ed["years"]} · GPA {ed["gpa"]}_' + NL)
w('</details>' + NL)

w('## Achievements' + NL)
w('<details>')
w('<summary><b>Open achievements</b> · as listed on my resume</summary>' + NL)
for a in D["achievements"]:
    w(f'- **{a["org"]}** — {a["text"]}')
w(NL + '</details>' + NL)

w('## Skills' + NL)
w('<details>')
w('<summary><b>Open technical skills</b> · from my resume</summary>' + NL)
labels = {"languages": "Languages", "frameworks": "ML/DL frameworks", "domains": "AI domains", "tools": "Tools & libraries",
          "deployment": "Deployment & MLOps", "expertise": "Core expertise"}
for k, lb in labels.items():
    w(f'- **{lb}:** {", ".join(D["skills"][k])}')
w(NL + '</details>' + NL)

w('## Contact' + NL)
w('<details>')
w('<summary><b>Open contact links</b></summary>' + NL)
w(f'- Email: [{I["email"]}](mailto:{I["email"]})')
w(f'- LinkedIn: [{I["linkedin"].replace("https://www.", "")}]({I["linkedin"]})')
w(f'- Portfolio: [{I["portfolio"]}]({I["portfolio"]})')
w(f'- GitHub: [github.com/{I["username"]}]({I["github"]})')
w(NL + '</details>' + NL)
w(f'<sub>{P["summary"]}</sub>')

open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(NL.join(lines) + NL)
print("README.md written")
