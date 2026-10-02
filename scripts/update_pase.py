"""Genera la comanda «En el pase» (assets/pase-{light,dark}.svg) con mis últimos commits públicos.

Lee los repos públicos (no forks) de USER, toma los commits propios más recientes
(sin merges, máximo PER_REPO por repo) y dibuja un ticket animado. Solo stdlib y la
API pública de GitHub; con GITHUB_TOKEN sube el límite de peticiones. Si la API
falla, sale con error y no toca nada. El SVG solo cambia si hay commits nuevos.
"""
import html
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import urllib.request

USER = "nicopm0905"
SKIP = {USER}  # el propio repo de perfil: sus commits son del bot
REPOS = 6
PER_REPO = 2
SHOW = 5
ASSETS = Path(__file__).resolve().parent.parent / "assets"
MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "light": dict(paper="#fafaf7", ink="#1c1c1a", green="#1c4332", muted="#6b706b", rule="#d6d8cf", soft="#e4f0e9"),
    "dark": dict(paper="#101814", ink="#f2f2ee", green="#6fcea3", muted="#93a199", rule="#2b3a33", soft="#202f28"),
}


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", f"{USER}-profile-readme")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)


def cut(text, n):
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def fecha(d):
    return f"{d.day:02d} {MESES[d.month - 1]}"


def fetch():
    repos = api(f"/users/{USER}/repos?type=owner&sort=pushed&per_page=30")
    repos = [r for r in repos if not r["fork"] and not r["private"] and r["name"] not in SKIP][:REPOS]
    commits = []
    for repo in repos:
        if repo["size"] == 0:
            continue
        recent = api(f"/repos/{USER}/{repo['name']}/commits?author={USER}&per_page=10")
        for c in [c for c in recent if len(c["parents"]) < 2][:PER_REPO]:
            msg = (c["commit"]["message"].strip().splitlines() or ["(sin mensaje)"])[0]
            commits.append({
                "repo": repo["name"],
                "date": datetime.fromisoformat(c["commit"]["committer"]["date"].replace("Z", "+00:00")),
                "msg": msg,
            })
    commits.sort(key=lambda c: c["date"], reverse=True)
    return commits[:SHOW]


def render(commits, c):
    row = 30
    top = 96
    h = top + max(len(commits), 1) * row + 62
    last = fecha(commits[0]["date"]).upper() if commits else "SIN DATOS"
    z = h - 14  # borde inferior en dientes de sierra, como un ticket
    teeth = " l-8 10 l-8 -10" * 46
    css = f"""
@keyframes feed{{from{{opacity:0;transform:translateX(-14px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.m{{font-family:{MONO};font-size:13px}}
.l{{font-family:{MONO};font-size:11px;letter-spacing:2.2px;font-weight:600;fill:{c['muted']}}}
.row{{animation:feed .55s cubic-bezier(.2,.7,.2,1) both}}
.live{{animation:blink 1.6s ease-in-out infinite}}
.fade{{animation:fade .8s ease both}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""
    b = [
        f'<text class="l" x="36" y="42">COMANDA · EN EL PASE</text>',
        f'<circle class="live" cx="{724 - 8.4 * (len(last) + 16) - 14:.0f}" cy="38" r="4" fill="{c["green"]}"/>',
        f'<text class="l" x="724" y="42" text-anchor="end">ÚLTIMO PLATO · {last}</text>',
        f'<line x1="36" y1="58" x2="724" y2="58" stroke="{c["rule"]}" stroke-dasharray="2 4"/>',
        f'<text class="m" x="36" y="82" fill="{c["muted"]}" font-size="11">FECHA</text>',
        f'<text class="m" x="104" y="82" fill="{c["muted"]}" font-size="11">REPO</text>',
        f'<text class="m" x="280" y="82" fill="{c["muted"]}" font-size="11">COMMIT</text>',
    ]
    for i, k in enumerate(commits):
        y = top + 14 + i * row
        b.append(
            f'<g class="row" style="animation-delay:{0.3 + i * 0.4:.2f}s">'
            f'<rect x="28" y="{y - 17}" width="704" height="24" rx="5" fill="{c["soft"]}" opacity="{0.55 if i % 2 == 0 else 0}"/>'
            f'<text class="m" x="36" y="{y}" fill="{c["muted"]}">{fecha(k["date"])}</text>'
            f'<text class="m" x="104" y="{y}" fill="{c["green"]}" font-weight="700">{html.escape(cut(k["repo"], 22))}</text>'
            f'<text class="m" x="280" y="{y}" fill="{c["ink"]}">{html.escape(cut(k["msg"], 56))}</text></g>'
        )
    if not commits:
        b.append(f'<text class="m" x="36" y="{top + 14}" fill="{c["muted"]}">Sin commits públicos recientes.</text>')
    fy = top + max(len(commits), 1) * row + 12
    b.append(f'<line x1="36" y1="{fy}" x2="724" y2="{fy}" stroke="{c["rule"]}" stroke-dasharray="2 4"/>')
    b.append(f'<text class="l fade" x="36" y="{fy + 24}" style="animation-delay:2.4s">REPOS PÚBLICOS DE GITHUB.COM/{USER.upper()} · SE ACTUALIZA A DIARIO</text>')
    alt = "En el pase: " + "; ".join(f"{fecha(k['date'])}, {k['repo']}: {k['msg']}" for k in commits)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {h}" width="760" height="{h}" role="img" aria-labelledby="t d">'
        f'<title id="t">En el pase: últimos commits de Nicolás</title><desc id="d">{html.escape(alt)}</desc><style>{css}</style>'
        f'<path d="M12 12 H748 V{z}{teeth} Z" fill="{c["paper"]}" stroke="{c["rule"]}" stroke-width="1.5" stroke-linejoin="round"/>'
        + "".join(b)
        + "</svg>"
    )


def main():
    commits = fetch()
    changed = False
    ASSETS.mkdir(exist_ok=True)
    for theme, colors in THEMES.items():
        dest = ASSETS / f"pase-{theme}.svg"
        svg = render(commits, colors)
        if not dest.exists() or dest.read_text(encoding="utf-8") != svg:
            dest.write_text(svg, encoding="utf-8")
            changed = True
    print("Pase actualizado" if changed else "Sin cambios")
    return 0


if __name__ == "__main__":
    sys.exit(main())
