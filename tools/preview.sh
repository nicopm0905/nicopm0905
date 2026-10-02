#!/bin/sh
# Preview local (no se publica nada): renderiza README.md con la API de GitHub (modo README) y genera tools/.render-{light,dark}.html
cd "$(dirname "$0")/.." || exit 1
gh api markdown -f mode=markdown -f text="$(cat README.md)" \
  | sed 's#"assets/#"../assets/#g; s#<a target="_blank" rel="noopener noreferrer" href="[^"]*ficha[^"]*"><img#<img#; s#\(alt="Ficha[^>]*>\)</a>#\1#' > tools/.render-body.html
for theme in light dark; do
  bg='#ffffff'; [ "$theme" = dark ] && bg='#0d1117'
  { printf '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    printf '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-%s.css">' "$theme"
    printf '<style>body{margin:0;background:%s}.markdown-body{box-sizing:border-box;max-width:880px;margin:0 auto;padding:24px 16px}</style></head><body><article class="markdown-body">' "$bg"
    cat tools/.render-body.html; printf '</article></body></html>'; } > tools/.render-$theme.html
done
