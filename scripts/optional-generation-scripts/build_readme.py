#!/usr/bin/env python3
"""Generates README.md from data/profile.json so the README, dashboard and website share one verified data model."""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = json.load(open(os.path.join(ROOT, "data", "profile.json"), encoding="utf-8"))
RAW = "https://raw.githubusercontent.com/Sarveshrock/Sarveshrock/main/assets"
I = D["identity"]; P = D["professional"]

lines = []
w = lines.append
w('<div align="center">\n')
w('<picture>')
w(f'  <source media="(max-width: 700px)" srcset="{RAW}/dashboard/mobile.svg">')
w(f'  <img src="{RAW}/dashboard/desktop.svg" width="100%" alt="Sarvesh Shimpi — AI/ML Engineer. Profile dashboard: stats, contributions, languages, tech stack, projects, experience, achievements.">')
w('</picture>\n')
w('<!-- TODO: after you deploy the SARVESH.OS website (see web repo README), replace YOUR_VERIFIED_DOMAIN and uncomment:')
w('<a href="https://YOUR_VERIFIED_DOMAIN"><img src="assets/social/enter.svg" height="48" alt="ENTER SARVESH.OS" /></a>')
w('-->\n')
w(f'<a href="{I["github"]}"><img src="assets/social/github.svg" height="44" alt="GitHub" /></a>')
w(f'<a href="mailto:{I["email"]}"><img src="assets/social/email.svg" height="44" alt="Email" /></a>')
w(f'<a href="{I["linkedin"]}"><img src="assets/social/linkedin.svg" height="44" alt="LinkedIn" /></a>')
w(f'<a href="{I["portfolio"]}"><img src="assets/social/portfolio.svg" height="44" alt="Portfolio" /></a>\n')
w('</div>\n')
w('<details>')
w('<summary>Plain-text profile (screen readers, search, quick scan)</summary>\n')
w(f'**{I["name"]}** — {P["title"]}. {P["currentRole"]} at {P["company"]}.\n')
w(f'{P["summary"]}\n')
w('**Experience**')
for e in D["experience"]:
    w(f'- {e["dates"]} · **{e["company"]}** — {e["role"]}')
w('')
w('**Projects** (resume projects have no public repository unless linked)')
for p in D["projects"]:
    w(f'- [{p["name"]}]({p["repo"]})' if p["repo"] else f'- {p["name"]} — {p["category"]}')
w('')
w('**Achievements**')
for a in D["achievements"]:
    w(f'- {a["org"]}: {a["text"]}')
w('')
s = D["skills"]
w(f'**Skills** — {", ".join(s["languages"])}; {", ".join(s["frameworks"])}; {", ".join(s["tools"])}; {", ".join(s["deployment"])}.\n')
e = D["education"]
w(f'**Education** — {e["degree"]}, {e["institution"]}, {e["years"]}, GPA {e["gpa"]}.\n')
w('</details>')
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("README.md written")
