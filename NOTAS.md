# NOTAS: README de perfil `nicopm0905/nicopm0905`

## Estructura y por qué (boceto)

1. **Cabecera SVG (ficha técnica) + TL;DR en inglés.** En 3 segundos se sabe quién es, qué construye (Skanda), de dónde viene y qué busca. El sello de finalista es el único adorno con dato.
2. **Ahora mismo.** Tres frases en primera persona: la historia del camarero que monta la solución, la carrera, el TFG y lo que busca. Con esto basta la primera pantalla.
3. **Elaboración.** 4 proyectos principales, cada uno con qué es, para quién, un hecho verificable y el stack en `<sub>`. El resto va en «Fuera de carta» (`<details>`).
4. **Ingredientes.** El stack agrupado por uso. La «cantidad» no es un porcentaje: dice en qué proyectos se usa de verdad. Base = sostiene Skanda y Relincho.
5. **Coste y margen.** Coste = lo invertido (carrera, conservatorio, sala de catering). Margen = lo que ha salido (premio, certificados). **En el pase** va plegado al final y su resumen se actualiza solo.

## Decisiones de diseño (v2, animada)

- **Todo el diseño es SVG propio y animado.** GitHub ejecuta CSS y SMIL dentro de un `<img>`, pero no scripts ni fuentes externas. Generados con `python tools/build_assets.py` (`pip install fonttools brotli`): `hero`, `stack` y `flow`, cada uno en claro y oscuro, con DM Serif Display y DM Sans (OFL) incrustadas en base64.
- **hero:** la ficha con el sello que «cae» al cargar, un punto que late en «Buscando primer puesto» y una fila «EN CARTA» que rota cada 4 s entre Skanda, Relincho, plataforma scout y ViT. Incluye una fila CON con el stack principal.
- **stack:** chips por uso. Relleno = lo uso en Skanda y Relincho; borde = otros proyectos. Debajo, barras con los bytes de código por lenguaje en tus repos públicos (datos de la API de GitHub en el momento de generar). Skanda es privado y no cuenta; está dicho en el propio SVG. Para refrescar las barras, vuelve a ejecutar `build_assets.py` y haz commit.
- **flow:** «Skanda, por dentro»: factura, IA (Gemini), escandallo y margen real, con un punto que recorre el flujo e ilumina cada paso. Solo dice lo que dicen tus datos, sin cifras.
- **pase:** una comanda monoespaciada con tus últimos commits que genera la Action (`scripts/update_pase.py`, solo stdlib). Ya no toca el README: solo regenera `assets/pase-*.svg` y hace commit si hay commits nuevos.
- `prefers-reduced-motion` desactiva las animaciones CSS (el punto del flujo, que usa SMIL, no se desactiva).
- **Sin** stats cards, contador, typing SVG, muro de badges ni serpiente.
- Los SVG no tienen enlaces clicables, por eso hay una fila de enlaces bajo la cabecera y los enlaces de cada proyecto siguen en texto.
- Pesan ~55-70 KB cada uno (las fuentes son casi todo).

## Datos que faltan o no pude verificar

- **185 tests en Pest (scouts).** En el clon local cuento 240 llamadas `it(`/`test(` en 59 ficheros de `tests/`. Puede que la cifra esté desactualizada. Ejecuta `php artisan test` y corrige el número si toca.
- **97,86 % en test (ViT).** Coincide con `0.97858…` en `notebooks/01_modelo1_vit_baseline.ipynb`. No he confirmado si es accuracy o F1; en el README pone «97,86 % en test» sin métrica.
- **Vectores AEAT (Relincho):** verificado en `tests/verifactu.test.ts`.
- **Next.js:** el README de Relincho dice Next.js 15. En el perfil pongo «Next.js» a secas, como en los datos.
- **Scrum:** viene en los datos, pero no sé en qué proyecto lo usaste. Lo he puesto como «trabajo en equipo».
- **LinkedIn** responde 999 (su anti-bot bloquea curl). El enlace es el de los datos; ábrelo en el navegador para confirmarlo.
- **Email:** no está incluido. En el pie hay un comentario HTML sin la dirección. Si lo confirmas, añade `· [email](mailto:...)`. Recuerda que el comentario se ve en el código fuente público.
- **Skanda** sin enlace a código porque es privado. «cerebro» y el TFG van sin enlace.

## Publicar

```bash
cd C:/PROYECTOS/github-profile-readme
git init -b main
git add README.md NOTAS.md .gitignore assets scripts tools/build_assets.py tools/preview.sh .github
gh repo create nicopm0905/nicopm0905 --public --source . --push
```

- `PROMPT.md` no lo añado. Decide tú si lo subes; probablemente no. `NOTAS.md` se puede quedar fuera también.
- Después, en GitHub: Actions → «Actualizar «En el pase»» → *Run workflow* para la primera ejecución.
- Preview local antes de subir: `sh tools/preview.sh` y abre `tools/.render-light.html` o `.render-dark.html` con un servidor estático. Usa la API de render de GitHub, que no publica nada.
