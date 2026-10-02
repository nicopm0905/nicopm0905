"""Rellena el bloque «En el pase» del README con los últimos commits propios.

Lee los repos públicos (no forks) de USER, toma los commits más recientes de
cada uno y escribe los N últimos entre los marcadores PASE:START y PASE:END.
Solo usa la API pública de GitHub; con GITHUB_TOKEN sube el límite de peticiones.
Si la API falla, sale con error y no toca el README.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

USER = "nicopm0905"
SKIP = {USER}  # el propio repo de perfil: sus commits son del bot
REPOS = 6  # repos más recientes a consultar
PER_REPO = 2  # máximo por repo, para que el pase no lo acapare uno
SHOW = 4
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- PASE:START -->", "<!-- PASE:END -->"
MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()


def api(path: str):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", f"{USER}-profile-readme")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)


def clean(message: str) -> str:
    line = message.strip().splitlines()[0] if message.strip() else "(sin mensaje)"
    if len(line) > 72:
        line = line[:71].rstrip() + "…"
    # Que un mensaje de commit no pueda romper el markdown ni meter HTML.
    line = line.replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"([\\`*_\[\]|#~])", r"\\\1", line)


def main() -> int:
    repos = api(f"/users/{USER}/repos?type=owner&sort=pushed&per_page=30")
    repos = [r for r in repos if not r["fork"] and not r["private"] and r["name"] not in SKIP][:REPOS]

    commits = []
    for repo in repos:
        if repo["size"] == 0:
            continue
        recent = api(f"/repos/{USER}/{repo['name']}/commits?author={USER}&per_page=10")
        recent = [c for c in recent if len(c["parents"]) < 2][:PER_REPO]  # sin merges
        for c in recent:
            commits.append({
                "repo": repo["name"],
                "url": c["html_url"],
                "date": datetime.fromisoformat(c["commit"]["committer"]["date"].replace("Z", "+00:00")),
                "msg": clean(c["commit"]["message"]),
            })

    commits.sort(key=lambda c: c["date"], reverse=True)
    fecha = lambda d: f"{d.day:02d} {MESES[d.month - 1]}"
    lines = [
        f"- `{fecha(c['date'])}` **{c['repo']}** · [{c['msg']}]({c['url']})"
        for c in commits[:SHOW]
    ] or ["- Sin commits públicos recientes."]
    summary = (
        f"último plato: {commits[0]['repo']}, {fecha(commits[0]['date'])}" if commits else "nada en el pase"
    )

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("Faltan los marcadores PASE en el README", file=sys.stderr)
        return 1
    block = "\n".join([
        START,
        "<details>",
        f"<summary><b>En el pase</b> · {summary}</summary>",
        "",
        "<sub>Mis últimos commits en repos públicos. Una Action lo actualiza cada día.</sub>",
        "",
        *lines,
        "",
        "</details>",
        END,
    ])
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README actualizado")
    else:
        print("Sin cambios")
    return 0


if __name__ == "__main__":
    sys.exit(main())
