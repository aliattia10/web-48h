# Web48h — Tu web en 48 horas por 99€

Static offer page (100% Spanish) + 3 fictional demo one-pagers for small businesses in Oviedo/Asturias.

- Live: https://ali-webs-48h.netlify.app
- Demos: `/demo-peluqueria/`, `/demo-sidreria/`, `/demo-fisioterapia/` (fictional businesses, `noindex`)
- `site/` is deployed as-is (no build step). `gen_demos.py` regenerates the demo pages.
- Contact: all CTAs are `mailto:ali.attia@virtualy.win` (subject prefilled). A WhatsApp `https://wa.me/...` link can be added later.

Deploy: `npx netlify-cli deploy --prod --dir site`
- Payment: Bizum or bank transfer on approval (phone number intentionally NOT published on the page).
