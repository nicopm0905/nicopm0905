# NOTAS: README de perfil `nicopm0905/nicopm0905`

## Estructura y por qué (boceto)

1. **Cabecera SVG (ficha técnica) + TL;DR en inglés.** En 3 segundos se sabe quién es, qué construye (Skanda), de dónde viene y qué busca. El sello de finalista es el único adorno con dato.
2. **Ahora mismo.** Tres frases en primera persona: la historia del camarero que monta la solución, la carrera, el TFG y lo que busca. Con esto basta la primera pantalla.
3. **Elaboración.** 4 proyectos principales, cada uno con qué es, para quién, un hecho verificable y el stack en `<sub>`. El resto va en «Fuera de carta» (`<details>`).
4. **Ingredientes.** El stack agrupado por uso. La «cantidad» no es un porcentaje: dice en qué proyectos se usa de verdad. Base = sostiene Skanda y Relincho.
5. **Coste y margen.** Coste = lo invertido (carrera, conservatorio, sala de catering). Margen = lo que ha salido (premio, certificados). **En el pase** va plegado al final y su resumen se actualiza solo.

## Decisiones de diseño

- **Concepto aplicado al ~70 %.** Los términos de cocina están solo en títulos y etiquetas (Elaboración, Ingredientes, Coste y margen, Fuera de carta, En el pase). El contenido es normal y se entiende sin conocer la metáfora.
- **Fuentes incrustadas.** GitHub sirve los SVG como `<img>` y no carga fuentes externas. Por eso DM Serif Display y DM Sans (OFL) van incrustadas en base64 y recortadas a los glifos usados (~24 KB por SVG). Se regeneran con `python tools/build_ficha.py` (requiere `pip install fonttools brotli`; las fuentes se descargan de google/fonts a `tools/.fonts/`, ignorada en git).
- **Colores de Skanda.** Verde `oklch(0.348 0.054 163)` en claro y `oklch(0.78 0.11 163)` en oscuro, convertidos a hex. El fondo es el papel de su tema.
- **Claro/oscuro.** `<picture>` con `prefers-color-scheme`. En github.com lo resuelve su elemento `themed-picture` según el tema elegido. Revisado en local en ambos temas, a 800 px y a 375 px. En móvil, el texto pequeño de la ficha se lee justo, pero todo está repetido en el markdown de debajo.
- **«Nº 0905»** de la cabecera sale del usuario `nicopm0905`. Es un guiño, no un dato.
- **Lema** «Hago software para oficios que no se hacen sentado.» Es retórico, no un dato: vale para catering, yeguadas y scouts. Cámbialo si no te convence.
- **Medidas.** ~2.070 px de alto a 800 px de ancho, unas 2,3 pantallas de 900 px. Si quieres llegar a 2 justas, plega «Coste y margen» o «Ingredientes».
- **Sin** stats cards, contador, typing SVG, muro de badges ni serpiente. Lo he comprobado con grep.

## «En el pase» (Action)

- `scripts/update_pase.py` (solo stdlib) lee tus repos públicos que no son forks. Toma hasta 2 commits tuyos por repo, sin merges, y escribe los 4 últimos entre `<!-- PASE:START -->` y `<!-- PASE:END -->`. El resumen del `<details>` muestra el último plato.
- `.github/workflows/update-readme.yml` corre a diario a las 06:17 UTC y también a mano (`workflow_dispatch`). Solo usa el `GITHUB_TOKEN` por defecto con `contents: write` y solo hace commit si cambia algo.
- Los mensajes de commit se escapan (markdown y `<>`) y se cortan a 72 caracteres. Si la API falla, el script sale con error y no toca el README.
- Ojo: **tus mensajes de commit públicos salen en el perfil**. Ahora mismo aparecen 2 de relincho y 2 de scouts.
- GitHub desactiva los cron de un repo público tras 60 días sin actividad. Si deja de actualizarse, reactívalo en la pestaña Actions.
- Probado en local con y sin token. Es idempotente: la segunda ejecución da «Sin cambios».

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
git add README.md NOTAS.md .gitignore assets scripts tools/build_ficha.py tools/ficha.svg.tpl tools/preview.sh .github
gh repo create nicopm0905/nicopm0905 --public --source . --push
```

- `PROMPT.md` no lo añado. Decide tú si lo subes; probablemente no. `NOTAS.md` se puede quedar fuera también.
- Después, en GitHub: Actions → «Actualizar «En el pase»» → *Run workflow* para la primera ejecución.
- Preview local antes de subir: `sh tools/preview.sh` y abre `tools/.render-light.html` o `.render-dark.html` con un servidor estático. Usa la API de render de GitHub, que no publica nada.
