# web-48h · Tu web profesional en 48 horas por 99€

Página de oferta (100% en español de España) + 3 demos de negocios ficticios de Oviedo.

- Live: https://ali-webs-48h.netlify.app
- Demos (`noindex`, negocios ficticios): `/demo-peluqueria/`, `/demo-sidreria/`, `/demo-fisioterapia/`
  (`/demo-fisioterapeuta/` redirige a `/demo-fisioterapia/`).
- CTA principal: WhatsApp (wa.me/34677372245 con mensaje prellenado). Secundario: ali.attia@virtualy.win.
- Pago: Bizum o transferencia, al aprobar la web (el número de Bizum no se publica).

## Estructura

```
src/build.py        layout compartido (head con title/description/canonical/OG/robots + slot JSON-LD),
                    parciales (cabecera/pie de la oferta y de las demos), páginas y plantilla de landing
src/assets/         css (base, offer, demo), fuentes autoalojadas, imágenes WebP, capturas, og.png
src/static/         favicon, apple-touch-icon, _redirects (se copian a la raíz)
src/pages/*.json    páginas extra (landings SEO) -> plantilla landing_page(); ver _example.json.txt
site/               salida generada (lo que se despliega)
```

## Añadir páginas / integración SEO

1. Crea `src/pages/<slug>.json` (ver `src/pages/_example.json.txt`), o deja que el worker SEO escriba en
   `/workspace/research/seo/web-48h-integration/`: `pages/*.json` (mismo formato), `jsonld/<slug>.json`
   (o `index.json` para la portada), `sitemap.xml`, `robots.txt`.
2. `python3 src/build.py` — genera `site/` con el diseño común; si hay sitemap/robots del worker se usan esos,
   si no, se generan automáticamente (las demos quedan fuera del sitemap).
3. `npx netlify-cli deploy --prod --dir site`

Diseño: lenguaje visual hermano de virtualy.win (Montserrat + Lora, azul real #4169e1 sobre neutros,
eyebrows en mayúsculas espaciadas, botones rectos). Créditos de imágenes en `CREDITS.md`.
