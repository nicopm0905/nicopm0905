"""Genera assets/ficha-light.svg y assets/ficha-dark.svg desde tools/ficha.svg.tpl.

GitHub muestra los SVG del README como <img>: no carga fuentes externas.
Por eso las fuentes van incrustadas en base64, recortadas a los glifos usados.

Uso:  pip install fonttools brotli && python tools/build_ficha.py
Fuentes: DM Serif Display y DM Sans (SIL Open Font License), de github.com/google/fonts.
"""
import base64
import html
import io
import re
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

THEMES = {
    "light": {"paper": "#fafaf7", "ink": "#1c1c1a", "green": "#1c4332", "muted": "#6b706b", "rule": "#d6d8cf"},
    "dark": {"paper": "#101814", "ink": "#f2f2ee", "green": "#6fcea3", "muted": "#93a199", "rule": "#2b3a33"},
}


def font_path(name: str) -> Path:
    path = FONTS_DIR / name
    if not path.exists():
        FONTS_DIR.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(SOURCES[name], path)
    return path


def woff2_b64(font: TTFont, text: str) -> str:
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def texts_with(tpl: str, cls: str) -> str:
    """Texto de todos los <text> cuyo atributo class contiene `cls`."""
    found = re.findall(r'<text[^>]*class="[^"]*\b%s\b[^"]*"[^>]*>(.*?)</text>' % cls, tpl)
    return html.unescape("".join(found))


def main() -> None:
    tpl = (ROOT / "tools" / "ficha.svg.tpl").read_text(encoding="utf-8")

    def sans(wght: int) -> TTFont:
        return instancer.instantiateVariableFont(TTFont(font_path("DMSans.ttf")), {"wght": wght, "opsz": 14})

    faces = [
        ("Ficha Serif", TTFont(font_path("DMSerifDisplay-Regular.ttf")), texts_with(tpl, "serif")),
        ("Ficha Serif Italic", TTFont(font_path("DMSerifDisplay-Italic.ttf")), texts_with(tpl, "italic")),
        ("Ficha Sans", sans(400), texts_with(tpl, "sans")),
        ("Ficha Sans Bold", sans(600), texts_with(tpl, "label")),
    ]
    css = "\n    ".join(
        "@font-face { font-family: '%s'; src: url(data:font/woff2;base64,%s) format('woff2'); }"
        % (family, woff2_b64(font, text))
        for family, font, text in faces
    )

    for theme, colors in THEMES.items():
        out = tpl.replace("{{FONTS}}", css)
        for key, value in colors.items():
            out = out.replace("{{%s}}" % key, value)
        assert "{{" not in out, "placeholder sin resolver"
        dest = ROOT / "assets" / f"ficha-{theme}.svg"
        dest.write_text(out, encoding="utf-8")
        print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
