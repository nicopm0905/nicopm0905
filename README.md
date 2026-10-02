<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/ficha-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/ficha-light.svg">
  <img src="assets/ficha-light.svg" width="100%" alt="Ficha técnica de Nicolás Pérez Martín. Plato: Skanda, escandallos y márgenes reales para catering. Origen: de camarero en caterings a cofundador y desarrollador. Busca: primer puesto junior en IT o en investigación en IA aplicada. Sello: finalista del Santander X Award 2026.">
</picture>

**TL;DR** · Software engineering student (University of Seville, 2027) and co-founder of Skanda, a B2B SaaS for catering cost control, Santander X Award 2026 finalist. Looking for a first junior role in software or applied-AI research.

### Ahora mismo

Fui camarero en caterings, vi el problema desde dentro y monté **[Skanda](https://skanda-software.com)**. Estudio Ingeniería del Software en la Universidad de Sevilla (hasta 2027) y hago el TFG sobre seguridad en MCP. Busco mi primer puesto junior en IT o en un equipo de investigación en IA aplicada.

### Elaboración

1. **[Skanda](https://skanda-software.com)**: costes y eventos para catering. Escandallos y márgenes reales en tiempo real; una IA extrae los datos de las facturas de proveedores. Finalista del Santander X Award 2026. Código privado.<br>
   <sub>Next.js 16 · React 19 · TypeScript · Tailwind 4 + shadcn/ui · Clerk · Prisma · PostgreSQL (Supabase) · Stripe · Gemini</sub>

2. **[Relincho](https://github.com/nicopm0905/relincho)** · [demo](https://relincho.vercel.app): gestión multi-tenant de yeguadas de caballo PRE en Andalucía: sanidad, reproducción, alimentación, portal del propietario e IA. Factura con Veri\*Factu, con la huella encadenada validada contra los vectores oficiales de la AEAT. Objetivo: lanzarlo en SICAB 2026.<br>
   <sub>Next.js · TypeScript · tRPC v11 · Prisma · PostgreSQL con RLS (Supabase EU) · Auth.js v5 · Stripe · Cloudflare R2 · Resend · next-intl</sub>

3. **[Plataforma scout](https://github.com/nicopm0905/scouts)**: nace en mi propio grupo, el Grupo Scout San José de Jerez. Miembros, tesorería, actas, inventario y portal de familias con permisos por parentesco. El calendario valida las ratios legales de campamento (Decretos 45/2000 y 89/2018). 185 tests en Pest.<br>
   <sub>Laravel 11 · PHP 8.3 · PostgreSQL · Vue 3 + Inertia · Tailwind · spatie/permission · Pest · Docker · Google Drive API</sub>

4. **[Vision Transformers desde cero](https://github.com/nicopm0905/vision-transformers-mnist)**: 3 arquitecturas ViT entrenadas desde cero sobre MNIST, con validación cruzada de 5 folds. La mejor (patch 7, 6 capas): F1-macro medio de 0,9758 y 97,86 % en test. [Informe técnico](https://github.com/nicopm0905/vision-transformers-mnist/blob/main/docs/memoria.pdf).<br>
   <sub>Python · PyTorch · Hugging Face Transformers</sub>

<details>
<summary><b>Fuera de carta</b> · EndOfLine, GitMiner, cerebro y el TFG</summary>
<br>

- **[EndOfLine](https://github.com/nicopm0905/EndOfLine)**: juego de mesa online de estrategia, en equipo, para Diseño y Pruebas (US, 2025/26). Modos Versus, Battle Royale, Puzzle Solitario y Cooperativo. <sub>Spring Boot 3 (Java 21) · React · Spring Security + JWT · JUnit 5 + Mockito</sub>
- **[GitMiner](https://github.com/nicopm0905/GitMiner)**: API REST que extrae y normaliza proyectos, commits, issues y usuarios de GitHub y Bitbucket (AISS 2025). <sub>Java · Spring Boot</sub>
- **cerebro** (privado): mi orquestador para Claude Code. Memoria en capas sobre un vault de Obsidian, servidor MCP propio, hooks como guardarraíles, evals y subagentes.
- **TFG** (en curso): seguridad en MCP (Model Context Protocol).

</details>

### Ingredientes

| Para | Ingredientes | Cantidad |
| :-- | :-- | :-- |
| Producto web | TypeScript · Next.js · React · Tailwind · shadcn/ui · tRPC | **Base** de Skanda y Relincho |
| Backend y datos | PostgreSQL · Prisma · Supabase (RLS) · Node.js | **Base** de Skanda y Relincho |
| | Laravel · PHP, con Vue 3 + Inertia | La plataforma scout |
| | Java · Spring Boot | Dos proyectos de carrera |
| IA | Claude Code · MCP · agentes | **Base** de cerebro y del TFG |
| | Gemini API · Python · PyTorch · Hugging Face | Skanda (facturas) y el estudio ViT |
| Infra y calidad | Git · Docker · Vercel · GitHub Actions · Stripe · Cloudflare R2 | Despliegue, cobros y ficheros |
| | Pest · JUnit + Mockito · Scrum | Tests y trabajo en equipo |

### Coste y margen

| Coste | Margen |
| :-- | :-- |
| Ingeniería Informática del Software, US · 2023–2027 | Finalista del Santander X Award 2026, con Skanda |
| Título profesional de violonchelo, Conservatorio Joaquín Villatoro · 2012–2023 | Claude Code in Action, Anthropic · agosto&nbsp;de&nbsp;2026 |
| Sala en caterings: Alda y Terry, Terralda, González Byas | MF0950 Construcción de Páginas Web · 60&nbsp;h · abril de 2025 |
| Español nativo · francés básico | Inglés B2, Cambridge English |

<!-- PASE:START -->
<details>
<summary><b>En el pase</b> · último plato: relincho, 01 oct</summary>

<sub>Mis últimos commits en repos públicos. Una Action lo actualiza cada día.</sub>

- `01 oct` **relincho** · [feat: añadir Vercel Analytics en el layout raíz](https://github.com/nicopm0905/relincho/commit/517f31c370c584f48ea299c2fc1c20af18f1ad50)
- `01 oct` **relincho** · [feat: importación CSV/Excel y exportación de caballos, acciones rápidas…](https://github.com/nicopm0905/relincho/commit/f17398491ea6ba55ab34810471fe7d5fd708d5aa)
- `07 sep` **scouts** · [Plan de rama y salidas en el formato oficial MSC](https://github.com/nicopm0905/scouts/commit/c1c3fd528b40d43bd74555a4110252a93b8d960c)
- `07 sep` **scouts** · [Memoria del curso, censo MSC, presupuesto vs real, retención y 'Tu sema…](https://github.com/nicopm0905/scouts/commit/d930abd4dfd95816a19bd49eef867f2a05af0697)

</details>
<!-- PASE:END -->

---

[LinkedIn](https://www.linkedin.com/in/nicol%C3%A1s-p%C3%A9rez-mart%C3%ADn-5773b0355/) · [skanda-software.com](https://skanda-software.com) · Sevilla / Jerez de la Frontera
<!-- Email: añadir solo cuando Nico lo confirme. Formato: · [email](mailto:DIRECCION) -->
