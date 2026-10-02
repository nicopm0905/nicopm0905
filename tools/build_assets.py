"""Genera los SVG animados del perfil (claro y oscuro) en assets/.

  hero-*.svg   cabecera: ficha técnica con una fila «EN CARTA» que rota entre proyectos
  stack-*.svg  ingredientes: chips por uso + barras de código real en repos públicos
  flow-*.svg   Skanda por dentro: factura -> IA -> escandallo -> margen

GitHub muestra los SVG como <img>: ejecuta CSS y SMIL, pero no scripts ni fuentes
externas. Las fuentes (DM Serif Display y DM Sans, SIL OFL) van incrustadas en base64.

Uso:  pip install fonttools brotli && python tools/build_assets.py
"""
import base64
import html
import io
import json
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = ROOT / "tools" / ".fonts"
GF = "https://github.com/google/fonts/raw/main/ofl/"
SOURCES = {
    "DMSerifDisplay-Regular.ttf": GF + "dmserifdisplay/DMSerifDisplay-Regular.ttf",
    "DMSerifDisplay-Italic.ttf": GF + "dmserifdisplay/DMSerifDisplay-Italic.ttf",
    "DMSans.ttf": GF + "dmsans/DMSans%5Bopsz,wght%5D.ttf",
}
CHARS = "".join(chr(c) for c in range(32, 127)) + "áéíóúüñÁÉÍÓÚÜÑ¿¡·–—…«»“”’ºª"
USER = "nicopm0905"
REPOS = ["relincho", "scouts", "vision-transformers-mnist", "EndOfLine", "GitMiner"]

THEMES = {
    "light": dict(paper="#fafaf7", ink="#1c1c1a", green="#1c4332", muted="#6b706b",
                  rule="#d6d8cf", line="#b3b9ad", soft="#e4f0e9", onGreen="#fafaf7"),
    "dark": dict(paper="#101814", ink="#f2f2ee", green="#6fcea3", muted="#93a199",
                 rule="#2b3a33", line="#41524a", soft="#202f28", onGreen="#0b110e"),
}

COMMON_CSS = """
.serif{font-family:'F Serif',Georgia,serif}
.italic{font-family:'F Italic',Georgia,serif;font-style:italic}
.sans{font-family:'F Sans','Segoe UI',Helvetica,Arial,sans-serif}
.bold{font-family:'F Bold','Segoe UI',Helvetica,Arial,sans-serif;font-weight:600}
.label{font-family:'F Bold','Segoe UI',Helvetica,Arial,sans-serif;font-weight:600;font-size:11px;letter-spacing:2.2px;fill:{{muted}}}
.ink{fill:{{ink}}}.green{fill:{{green}}}.muted{fill:{{muted}}}
.rule{stroke:{{rule}};stroke-width:1}
.dash{stroke:{{rule}};stroke-width:1;stroke-dasharray:2 4}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
.rise{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
.grow{transform-box:fill-box;transform-origin:left center;animation:grow .9s cubic-bezier(.2,.7,.2,1) both}
.fade{animation:fade .8s ease both}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


# ---------- fuentes ----------
def font_path(name):
    path = FONTS_DIR / name
    if not path.exists():
        FONTS_DIR.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(SOURCES[name], path)
    return path


def load(face):
    if face == "serif":
        return TTFont(font_path("DMSerifDisplay-Regular.ttf"))
    if face == "italic":
        return TTFont(font_path("DMSerifDisplay-Italic.ttf"))
    wght = 400 if face == "sans" else 600
    return instancer.instantiateVariableFont(TTFont(font_path("DMSans.ttf")), {"wght": wght, "opsz": 14})


FAMILY = {"serif": "F Serif", "italic": "F Italic", "sans": "F Sans", "bold": "F Bold"}
_css_cache = {}


def face_css(face):
    if face not in _css_cache:
        font = load(face)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        opts.name_IDs = []
        sub = subset.Subsetter(opts)
        sub.populate(text=CHARS)
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        _css_cache[face] = (
            "@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2')}" % (FAMILY[face], b64)
        )
    return _css_cache[face]


_measure = {}


def tw(face, text, size):
    """Ancho del texto en px para ese tipo y tamaño."""
    if face not in _measure:
        _measure[face] = load(face)
    font = _measure[face]
    cmap, hmtx, upem = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
    return sum(hmtx[cmap.get(ord(ch), cmap[32])][0] for ch in text) * size / upem


def sub(s, c):
    for k, v in c.items():
        s = s.replace("{{%s}}" % k, v)
    assert "{{" not in s, "placeholder sin resolver"
    return s


def wrap(w, h, title, desc, faces, css, body, c):
    fonts = "".join(face_css(f) for f in faces)
    style = sub(COMMON_CSS + css, c)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
        f'aria-labelledby="t d"><title id="t">{html.escape(title)}</title><desc id="d">{html.escape(desc)}</desc>'
        f"<style>{fonts}{style}</style>"
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{c["paper"]}" stroke="{c["rule"]}" stroke-width="1.5"/>'
        f"{sub(body, c)}</svg>"
    )


# ---------- hero ----------
CARTA = [
    "Skanda: escandallos y márgenes reales para catering",
    "Relincho: gestión de yeguadas con facturación Veri*Factu",
    "Plataforma scout: ratios legales de campamento validadas",
    "Vision Transformers: ViT desde cero sobre MNIST",
]


def hero(c):
    css = """
@keyframes stamp{0%{opacity:0;transform:scale(2.1) rotate(-22deg)}55%{opacity:1;transform:scale(.93) rotate(-8deg)}100%{opacity:1;transform:scale(1) rotate(-9deg)}}
@keyframes pulse{0%{transform:scale(1);opacity:.55}100%{transform:scale(3.2);opacity:0}}
@keyframes cycle{0%{opacity:0;transform:translateY(8px)}3%{opacity:1;transform:none}24%{opacity:1;transform:none}27%{opacity:0;transform:translateY(-8px)}100%{opacity:0}}
.stamp{animation:stamp .9s cubic-bezier(.3,1.4,.5,1) 1s both}
.ring{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}
.cyc{opacity:0;animation:cycle 16s linear infinite both}
.cyc.first{opacity:1}
"""
    rows = [("ORIGEN", "De camarero en caterings a cofundador y desarrollador"),
            ("BUSCA", "Primer puesto junior en IT o en investigación en IA aplicada"),
            ("CON", "TypeScript · Next.js · PostgreSQL · Python · Java · Laravel")]
    b = [
        '<text class="label" x="36" y="40">FICHA TÉCNICA · Nº 0905</text>',
        '<circle cx="518" cy="36" r="4" fill="{{green}}"/><circle class="ring" cx="518" cy="36" r="4" fill="{{green}}"/>',
        '<text class="label" x="724" y="40" text-anchor="end">BUSCANDO PRIMER PUESTO</text>',
        '<line class="rule" x1="36" y1="54" x2="724" y2="54"/>',
        '<text class="serif ink rise" x="34" y="108" font-size="50" style="animation-delay:.1s">Nicolás Pérez Martín</text>',
        '<text class="italic green rise" x="36" y="140" font-size="21" style="animation-delay:.3s">'
        "Hago software para oficios que no se hacen sentado.</text>",
        '<g transform="translate(650 108)"><g class="stamp">'
        '<circle r="48" fill="none" stroke="{{green}}" stroke-width="1.6"/>'
        '<circle r="42" fill="none" stroke="{{green}}" stroke-width=".8"/>'
        '<text class="label" y="-13" text-anchor="middle" style="fill:{{green}};font-size:8px;letter-spacing:2px">FINALISTA</text>'
        '<text class="serif green" y="6" font-size="14" text-anchor="middle">Santander X</text>'
        '<text class="label" y="21" text-anchor="middle" style="fill:{{green}};font-size:8.5px;letter-spacing:1.4px">AWARD 2026</text>'
        "</g></g>",
    ]
    ys = [164, 200, 236, 272]
    b.append(f'<line class="dash fade" x1="36" y1="{ys[0]}" x2="724" y2="{ys[0]}" style="animation-delay:.5s"/>')
    b.append(f'<text class="label fade" x="36" y="{ys[0] + 24}" style="animation-delay:.5s">EN CARTA</text>')
    for i, t in enumerate(CARTA):
        first = " first" if i == 0 else ""
        b.append(
            f'<text class="sans ink cyc{first}" x="150" y="{ys[0] + 24}" font-size="16.5" '
            f'style="animation-delay:{1.2 + i * 4}s">{html.escape(t)}</text>'
        )
    for n, (label, val) in enumerate(rows, start=1):
        y = ys[n]
        d = 0.5 + n * 0.15
        b.append(f'<line class="dash fade" x1="36" y1="{y}" x2="724" y2="{y}" style="animation-delay:{d}s"/>')
        b.append(f'<text class="label fade" x="36" y="{y + 24}" style="animation-delay:{d}s">{label}</text>')
        b.append(f'<text class="sans ink rise" x="150" y="{y + 24}" font-size="16.5" style="animation-delay:{d}s">{html.escape(val)}</text>')
    desc = ("Nicolás Pérez Martín. Hago software para oficios que no se hacen sentado. Finalista del Santander X Award 2026. "
            "En carta: Skanda, Relincho, plataforma scout y Vision Transformers. Origen: de camarero en caterings a cofundador y "
            "desarrollador. Busca su primer puesto junior en IT o en investigación en IA aplicada. "
            "Con TypeScript, Next.js, PostgreSQL, Python, Java y Laravel.")
    return wrap(760, 316, "Ficha técnica de Nicolás Pérez Martín", desc, ["serif", "italic", "sans", "bold"], css, "".join(b), c)


# ---------- stack ----------
GROUPS = [
    ("Producto web", [("TypeScript", 1), ("Next.js", 1), ("React", 1), ("Tailwind", 1), ("shadcn/ui", 1), ("tRPC", 1), ("Vue 3 + Inertia", 0)]),
    ("Backend y datos", [("PostgreSQL", 1), ("Prisma", 1), ("Supabase (RLS)", 1), ("Node.js", 1), ("Laravel", 0), ("PHP", 0), ("Java", 0), ("Spring Boot", 0)]),
    ("IA", [("Gemini API", 1), ("Python", 0), ("PyTorch", 0), ("Hugging Face", 0), ("Claude Code", 0), ("MCP", 0), ("Agentes", 0)]),
    ("Infra y calidad", [("Git", 1), ("Vercel", 1), ("Stripe", 1), ("Cloudflare R2", 1), ("Docker", 0), ("GitHub Actions", 0), ("Pest", 0), ("JUnit", 0), ("Scrum", 0)]),
]
BAR_LANGS = ["TypeScript", "Java", "PHP", "Vue", "JavaScript", "Python"]


def code_bytes():
    totals = {}
    for repo in REPOS:
        req = urllib.request.Request(f"https://api.github.com/repos/{USER}/{repo}/languages",
                                     headers={"User-Agent": "profile-readme", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=20) as res:
            for lang, n in json.load(res).items():
                totals[lang] = totals.get(lang, 0) + n
    return {k: totals.get(k, 0) for k in BAR_LANGS}


def mb(n):
    return f"{n / 1_000_000:.2f}".replace(".", ",") + " MB" if n < 100_000 else f"{n / 1_000_000:.1f}".replace(".", ",") + " MB"


def stack(c, langs):
    css = ".chip{animation:rise .6s cubic-bezier(.2,.7,.2,1) both}"
    b = ['<text class="label" x="30" y="40">INGREDIENTES</text>']
    # leyenda
    lx = 440
    b.append(f'<rect x="{lx}" y="28" width="16" height="14" rx="7" fill="{{{{green}}}}"/>')
    b.append(f'<text class="sans muted" x="{lx + 22}" y="40" font-size="12">En Skanda y Relincho</text>')
    lx2 = lx + 22 + tw("sans", "En Skanda y Relincho", 12) + 22
    b.append(f'<rect x="{lx2}" y="28.5" width="16" height="13" rx="6.5" fill="none" stroke="{{{{line}}}}" stroke-width="1.3"/>')
    b.append(f'<text class="sans muted" x="{lx2 + 22}" y="40" font-size="12">En otros proyectos</text>')
    y = 58
    idx = 0
    for name, items in GROUPS:
        b.append(f'<line class="dash" x1="30" y1="{y}" x2="730" y2="{y}"/>')
        x, cy, lines = 190, y + 14, 1
        chips = []
        for text, filled in items:
            face = "bold" if filled else "sans"
            w = tw(face, text, 13) + 24
            if x + w > 730:
                x, cy, lines = 190, cy + 34, lines + 1
            d = 0.15 + idx * 0.045
            idx += 1
            if filled:
                chips.append(
                    f'<g class="chip" style="animation-delay:{d:.2f}s"><rect x="{x:.1f}" y="{cy}" width="{w:.1f}" height="26" rx="13" fill="{{{{green}}}}"/>'
                    f'<text class="bold" x="{x + w / 2:.1f}" y="{cy + 17.5}" font-size="13" text-anchor="middle" fill="{{{{onGreen}}}}">{html.escape(text)}</text></g>')
            else:
                chips.append(
                    f'<g class="chip" style="animation-delay:{d:.2f}s"><rect x="{x:.1f}" y="{cy + .5}" width="{w:.1f}" height="25" rx="12.5" fill="none" stroke="{{{{line}}}}" stroke-width="1.3"/>'
                    f'<text class="sans ink" x="{x + w / 2:.1f}" y="{cy + 17.5}" font-size="13" text-anchor="middle">{html.escape(text)}</text></g>')
            x += w + 8
        h = lines * 34 + 12
        b.append(f'<text class="serif ink" x="30" y="{y + 33}" font-size="18">{html.escape(name)}</text>')
        b.extend(chips)
        y += h + 14
    # barras
    b.append(f'<line class="dash" x1="30" y1="{y}" x2="730" y2="{y}"/>')
    b.append(f'<text class="label" x="30" y="{y + 28}">DÓNDE ESCRIBO MÁS CÓDIGO</text>')
    top = max(langs.values())
    by = y + 48
    for i, lang in enumerate(BAR_LANGS):
        n = langs[lang]
        w = max(3, 430 * n / top)
        yy = by + i * 24
        b.append(f'<text class="sans ink" x="30" y="{yy + 11}" font-size="13">{lang}</text>')
        b.append(f'<rect x="130" y="{yy}" width="430" height="12" rx="6" fill="{{{{soft}}}}"/>')
        b.append(f'<rect class="grow" x="130" y="{yy}" width="{w:.1f}" height="12" rx="6" fill="{{{{green}}}}" style="animation-delay:{.5 + i * .12:.2f}s"/>')
        b.append(f'<text class="sans muted fade" x="{130 + w + 10:.1f}" y="{yy + 11}" font-size="12" style="animation-delay:{.9 + i * .12:.2f}s">{mb(n)}</text>')
    fy = by + len(BAR_LANGS) * 24 + 14
    b.append(f'<text class="sans muted" x="30" y="{fy}" font-size="11.5">Bytes por lenguaje en mis repos públicos, según GitHub. '
             "Skanda es privado y no cuenta; Python son sobre todo notebooks.</text>")
    h = fy + 22
    stack_txt = "; ".join(f"{n}: " + ", ".join(t for t, _ in it) for n, it in GROUPS)
    desc = f"Stack por uso. {stack_txt}. Relleno: usado en Skanda y Relincho. Borde: usado en otros proyectos."
    return wrap(760, h, "Ingredientes: stack por uso", desc, ["serif", "sans", "bold"], css, "".join(b), c)


# ---------- flow ----------
def flow(c):
    css = """
@keyframes glow{0%{opacity:0}3%{opacity:1}16%{opacity:0}100%{opacity:0}}
@keyframes dashmove{to{stroke-dashoffset:-14}}
.glow{animation:glow 8s linear infinite both}
.flowline{stroke-dasharray:4 5;animation:dashmove .9s linear infinite}
"""
    nodes = [
        ("Factura", "del proveedor", "", "invoice"),
        ("IA (Gemini)", "extrae los datos", "de la factura", "ai"),
        ("Escandallo", "ingredientes,", "cantidades y coste", "recipe"),
        ("Margen real", "calculado en", "tiempo real", "margin"),
    ]
    nw, gap, x0, ny, nh = 136, 52, 30, 96, 138
    centers = [x0 + i * (nw + gap) + nw / 2 for i in range(4)]
    cy = ny + 40
    b = ['<text class="label" x="30" y="40">SKANDA, POR DENTRO</text>',
         '<text class="italic green" x="30" y="72" font-size="21">De la factura del proveedor al margen real del evento.</text>']
    b.append(f'<line class="flowline" x1="{centers[0]}" y1="{cy}" x2="{centers[-1]}" y2="{cy}" stroke="{{{{line}}}}" stroke-width="2"/>')
    icons = {
        "invoice": '<path d="M-14 -20h20l10 10v30h-30z" fill="none" stroke="{{green}}" stroke-width="2" stroke-linejoin="round"/>'
                   '<path d="M6 -20v10h10M-8 0h16M-8 7h16M-8 14h9" fill="none" stroke="{{green}}" stroke-width="2" stroke-linecap="round"/>',
        "ai": '<path d="M0 -22l5 15 15 5-15 5-5 15-5-15-15-5 15-5z" fill="{{green}}"/>'
              '<circle cx="17" cy="-17" r="3" fill="{{green}}"/><circle cx="-17" cy="17" r="2.5" fill="{{green}}"/>',
        "recipe": '<path d="M-20 -14h20M-20 0h26M-20 14h14" stroke="{{green}}" stroke-width="3.5" stroke-linecap="round"/>'
                  '<path d="M8 -14h12M12 0h8M2 14h18" stroke="{{green}}" stroke-width="2" stroke-linecap="round" opacity=".45"/>',
        "margin": '<rect x="-20" y="2" width="9" height="18" rx="2" fill="{{green}}" opacity=".45"/>'
                  '<rect x="-5" y="-6" width="9" height="26" rx="2" fill="{{green}}" opacity=".7"/>'
                  '<rect x="10" y="-20" width="9" height="40" rx="2" fill="{{green}}"/>',
    }
    for i, (title, l1, l2, icon) in enumerate(nodes):
        x = x0 + i * (nw + gap)
        b.append(f'<g class="rise" style="animation-delay:{.2 + i * .18:.2f}s">'
                 f'<rect x="{x}" y="{ny}" width="{nw}" height="{nh}" rx="12" fill="{{{{paper}}}}" stroke="{{{{rule}}}}" stroke-width="1.5"/>'
                 f'<rect class="glow" style="animation-delay:{i * 2}s" x="{x}" y="{ny}" width="{nw}" height="{nh}" rx="12" fill="{{{{soft}}}}" stroke="{{{{green}}}}" stroke-width="2"/>'
                 f'<g transform="translate({centers[i]} {cy})">{icons[icon]}</g>'
                 f'<text class="serif ink" x="{centers[i]}" y="{ny + 94}" font-size="17" text-anchor="middle">{html.escape(title)}</text>'
                 f'<text class="sans muted" x="{centers[i]}" y="{ny + 108}" font-size="11.5" text-anchor="middle">{html.escape((l1 + " " + l2).strip()) if not l2 else html.escape(l1)}</text>'
                 + (f'<text class="sans muted" x="{centers[i]}" y="{ny + 121}" font-size="11.5" text-anchor="middle">{html.escape(l2)}</text>' if l2 else "")
                 + "</g>")
    b.append(f'<circle r="6" fill="{{{{green}}}}"><animateMotion dur="8s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.75;1" '
             f'calcMode="linear" path="M{centers[0]} {cy} L{centers[-1]} {cy}"/>'
             '<animate attributeName="opacity" dur="8s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.03;.74;.78;1"/></circle>')
    desc = ("Cómo funciona Skanda: la factura del proveedor entra, una IA (Gemini) extrae los datos, se calcula el escandallo "
            "con ingredientes, cantidades y coste, y sale el margen real en tiempo real.")
    return wrap(760, 254, "Skanda por dentro: de la factura al margen", desc, ["serif", "italic", "sans"], css, "".join(b), c)


def main():
    langs = code_bytes()
    print("bytes:", langs)
    for theme, c in THEMES.items():
        for name, fn in (("hero", lambda c=c: hero(c)), ("stack", lambda c=c: stack(c, langs)), ("flow", lambda c=c: flow(c))):
            dest = ROOT / "assets" / f"{name}-{theme}.svg"
            dest.write_text(fn(), encoding="utf-8")
            print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
