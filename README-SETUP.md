# README-SETUP — GitHub profile (entry point of the hybrid)

Architecture: this repo is **Layer 1** (static terminal-style profile). **Layer 2** is the interactive website in `sarvesh-os/` (Next.js). Both read `data/profile.json`.

## What's here
- `assets/dashboard/desktop.svg` (1200 px, 3 columns) and `mobile.svg` (600 px, 1 column). One image holds every panel, switched by `<picture>` at 700 px. GitHub removes CSS and JS from READMEs, so a single image is the only way to get the multi-panel layout. Text inside it cannot be clicked, so link buttons sit underneath.
- `assets/art/` — city/hoodie banner and portrait, cropped from your reference image (low resolution, 890 px wide). Replace `hero.jpg` / `portrait.jpg` with the original high-resolution art for a sharper result.
- `assets/icons/` — official devicon SVGs, embedded into the dashboard.
- `data/profile.json` — the single verified data model (every item tagged resume / github / brief).
- `scripts/optional-generation-scripts/` — `build_dashboard.py` (renders both SVGs), `build_readme.py` (README from the data model), `build_assets.py` (link buttons), `update_stats.py` (GitHub data helpers).

## Deploy
1. Copy `README.md`, `assets/`, `data/`, `scripts/`, `.github/` into the root of `Sarveshrock/Sarveshrock`, push to `main`.
2. **Settings → Actions → General → Workflow permissions → Read and write.**
3. **Actions → Update profile dashboard → Run workflow** (also runs daily at 03:17 UTC and on pushes that touch the scripts or data).
4. Set your GitHub bio at github.com/settings/profile: "AI/ML Engineer at Infosys. Computer Vision, Generative AI, LLMs."

## Live vs static
| Element | Source | Refresh |
|---|---|---|
| Repositories, followers, following | GitHub API | daily Action |
| Contributions (last year) + heatmap | public contribution calendar | daily Action |
| Language shares | GitHub languages API, by code size, non-fork repos | daily Action |
| Everything else | `data/profile.json` | when you edit it and re-run the scripts |

If GitHub is unreachable the script exits without touching existing files, so you never get partial numbers. Locally, `DASH_CACHED=1` reuses the last fetched numbers (cache file `.stats-cache.json`, not for commit) so you can iterate on layout without calling the API.

## ENTER SARVESH.OS button
`README.md` contains a commented-out button. After deploying the website, put its **verified** URL in place of `YOUR_VERIFIED_DOMAIN`, uncomment it, and (if you regenerate the README) edit the same line in `build_readme.py`.

## Maintenance
- New job/project/achievement: edit `data/profile.json`, copy it to `sarvesh-os/data/`, run `build_dashboard.py` and `build_readme.py`, rebuild the website.
- When a resume project gets a public repo, set its `"repo"` in `profile.json`.

## Facts and limits (read this)
- Resume-sourced: roles, dates, education, skills, 7 project descriptions, achievements. Cards say "SOURCE: RESUME · NO PUBLIC REPO" and have no links. UnmaskAI is the only linked repo (its GitHub description is just "SEED HACKATHON Submission").
- From your brief, not resume/GitHub: tagline, motto, "Open Source Enthusiast", "currently building" list, "now playing" panel (visual only).
- Omitted: phone number, location (not set on GitHub), AURA, AI-Contract and every repo not verified.
- The reference image's numbers, repos and URLs are placeholders and are not used.
- `<picture media>` switching on GitHub is untested here; if the mobile image does not switch on your phone, tell me and I'll replace it with a single responsive layout.
- Repo hygiene is yours: NASA, Max-num and Intern have unprofessional descriptions.
