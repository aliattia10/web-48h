# Web48h — Tu web en 48 horas por 99€

Static offer page (ES/EN) + 3 fictional demo one-pagers for small businesses in Oviedo/Asturias.

- Live: https://ali-webs-48h.netlify.app
- Demos: `/demo-peluqueria/`, `/demo-sidreria/`, `/demo-fisioterapia/` (fictional businesses, `noindex`)
- `site/` is deployed as-is (no build step). `gen_demos.py` regenerates the demo pages.
- Contact: all CTAs are `mailto:info@virtualy.win` (subject prefilled). A WhatsApp `https://wa.me/...` link can be added later.

Deploy: `npx netlify-cli deploy --prod --dir site`
