# Web48h — Tu web en 48 horas por 99€

Static offer page (ES/EN) + 3 fictional demo one-pagers for small businesses in Oviedo/Asturias.

- Live: https://ali-webs-48h.netlify.app
- Demos: `/demo-peluqueria/`, `/demo-sidreria/`, `/demo-fisioterapia/` (fictional businesses, `noindex`)
- `site/` is deployed as-is (no build step). `gen_demos.py` regenerates the demo pages.
- Contact buttons use the placeholder `#CONTACT` — replace with a real `https://wa.me/34XXXXXXXXX` / `mailto:` link before outreach.

Deploy: `npx netlify-cli deploy --prod --dir site`
