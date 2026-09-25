#!/usr/bin/env python3
"""Static build for web-48h.

Layout = one shared <head> (title / description / canonical / OG / robots / JSON-LD slots)
+ partials (offer header/footer, demo header/footer). Pages are plain dicts.

Adding a page:
  * drop a JSON file in src/pages/<slug>.json  (see src/pages/_example.json.txt), or
  * let the SEO worker drop files into /workspace/research/seo/web-48h-integration/
    (pages/*.json, sitemap.xml, robots.txt, jsonld/*.json) and re-run this script.
Run:  python3 src/build.py   -> writes ../site/
"""
import json, os, re, shutil, html, glob
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "site")
SITE_URL = "https://ali-webs-48h.netlify.app"
SEO_DIR = "/workspace/research/seo/web-48h-integration"
EMAIL = "ali.attia@virtualy.win"
MAILTO = "mailto:ali.attia@virtualy.win?subject=Quiero%20mi%20web%20en%2048h"
WA = "https://wa.me/34677372245?text=" + quote("Hola Ali, quiero mi web en 48h por 99€. Mi negocio es: ", safe="")
e = html.escape

# ---------- icons (monochrome SVG) ----------
WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.9-4.45 9.9-9.91A9.86 9.86 0 0 0 12.04 2zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24a8.2 8.2 0 0 1 8.24 8.25c0 4.54-3.7 8.23-8.24 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.13-.56-1.35-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.29z"/></svg>')
MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x=".5" y=".5" width="31" height="31" fill="none" stroke="currentColor"/>'
        '<path d="M9 9l7 14 7-14" fill="none" stroke="currentColor" stroke-width="2"/></svg>')
ARROW = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'

REVEAL_JS = """<script>
(function(){var d=document.documentElement;d.classList.add('js');
if(!('IntersectionObserver' in window)){d.classList.remove('js');return}
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)})});
})();</script>"""

# ---------- shared layout ----------
def layout(p):
    """p: dict(path, title, description, body, css=[...], noindex=False, og_image, jsonld=[...], theme, head_extra)"""
    canon = p.get("canonical") or SITE_URL + p["path"]
    og = p.get("og_image", "/assets/og.png")
    og = og if og.startswith("http") else SITE_URL + og
    robots = '<meta name="robots" content="noindex, follow">' if p.get("noindex") else '<meta name="robots" content="index, follow">'
    css = "\n".join(f'<link rel="stylesheet" href="{c}">' for c in ["/assets/css/base.css"] + p.get("css", []))
    ld = "\n".join('<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + "</script>"
                   for j in p.get("jsonld", []))
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['description'])}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="{p.get('theme', '#0a0e1a')}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Virtualy · Webs en 48 horas">
<meta property="og:title" content="{e(p.get('og_title', p['title']))}">
<meta property="og:description" content="{e(p['description'])}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/montserrat.woff2" as="font" type="font/woff2" crossorigin>
{css}
{p.get('head_extra', '')}
{ld}
{REVEAL_JS}
</head>
<body class="{p.get('body_class', '')}">
<a class="skip" href="#main">Saltar al contenido</a>
{p['body']}
</body>
</html>
"""

# ---------- offer partials ----------
def offer_header(home=True):
    pre = "" if home else "/"
    return f"""<header class="hdr">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Virtualy, inicio">{MARK}<span>Virtualy</span></a>
    <nav class="nav" aria-label="Principal">
      <a href="{pre}#ejemplos">Ejemplos</a><a href="{pre}#incluye">Qué incluye</a><a href="{pre}#proceso">Proceso</a><a href="{pre}#preguntas">Preguntas</a>
    </nav>
    <a class="btn btn--light" href="{WA}" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp</span></a>
  </div>
</header>"""

def offer_footer():
    return f"""<footer class="ftr">
  <div class="wrap">
    <a class="brand" href="/">{MARK}<span>Virtualy</span></a>
    <span>Ali Attia · Webs para negocios locales · Oviedo, Asturias</span>
    <a href="{MAILTO}">{EMAIL}</a>
    <span>© 2026</span>
  </div>
</footer>
<a class="fab" href="{WA}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{WA_ICON}</a>"""

def final_cta(title="¿Hablamos de tu web?", text="Cuéntame qué haces y te enseño una propuesta en 48 horas. Si no te convence, no pagas nada."):
    return f"""<section class="final" id="contacto">
  <div class="wrap reveal">
    <span class="eyebrow">Contacto</span>
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="ctas">
      <a class="btn btn--solid" href="{WA}" target="_blank" rel="noopener">{WA_ICON}<span>Escribir por WhatsApp</span></a>
      <a class="link" href="{MAILTO}">{EMAIL}</a>
    </div>
  </div>
</section>"""

# ---------- offer page ----------
DEMOS = [
    ("demo-peluqueria", "Peluquería", "Peluquería Demo", "Salón con cita previa, carta de servicios y galería."),
    ("demo-sidreria", "Sidrería", "Sidrería Demo", "Carta completa, menú del día y reservas de grupo."),
    ("demo-fisioterapia", "Fisioterapia", "Fisioterapia Demo", "Tratamientos, tarifas claras y primera valoración."),
]
INCLUDES = [
    ("Diseño a medida", "Una página cuidada, con tu logo, tus colores y tus fotos."),
    ("Servicios y precios", "Tu carta o lista de servicios, clara y fácil de actualizar."),
    ("Horario y ubicación", "Horario, dirección y enlace directo a Google Maps."),
    ("WhatsApp y llamada", "Botones para que te escriban o llamen con un toque."),
    ("Preparada para Google", "Título, descripción y datos del negocio bien configurados."),
    ("Perfecta en el móvil", "Rápida y legible en cualquier teléfono."),
    ("Hosting incluido", "Publicada en Netlify, sin cuotas de alojamiento."),
    ("Una ronda de cambios", "Ajustamos textos y fotos hasta que te guste."),
]
FAQ = [
    ("¿De verdad está en 48 horas?", "Sí. Cuando me envías el texto básico y algunas fotos, en 48 horas tienes la web lista para revisar. Si no tienes fotos, usamos imágenes profesionales con licencia libre."),
    ("¿Cómo se paga?", "Pago por Bizum o transferencia. Pagas al aprobar la web, no antes."),
    ("¿Tengo que pagar algo cada mes?", "No. El alojamiento es gratuito. Si quieres que me ocupe de los cambios y el mantenimiento, hay una cuota opcional de 9€ al mes."),
    ("¿Puedo tener mi propio dominio?", "Sí. Puedo conectar un dominio tuyo (tunegocio.es). El dominio se paga aparte al registrador, normalmente entre 10€ y 15€ al año."),
    ("¿Y si ya tengo Facebook o Instagram?", "Perfecto: los enlazamos. La web te da un sitio propio, que aparece en Google y que tú controlas."),
]

def offer_page():
    demos = "\n".join(f"""      <a class="demo reveal" href="/{s}/">
        <div class="frame"><picture><source media="(max-width:600px)" srcset="/assets/shots/{s}-m.webp"><img src="/assets/shots/{s}.webp" width="800" height="1000" alt="Captura de la web de ejemplo {e(n)}" loading="lazy" decoding="async"></picture></div>
        <div class="meta"><h3>{e(n)}</h3><span class="kind">{e(k)}</span></div>
        <p class="muted">{e(d)}</p>
        <div class="go">Ver ejemplo</div>
      </a>""" for s, k, n, d in DEMOS)
    incl = "\n".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in INCLUDES)
    faq = "\n".join(f"<details><summary>{e(q)}<i aria-hidden=\"true\"></i></summary><p>{e(a)}</p></details>" for q, a in FAQ)
    body = f"""{offer_header()}
<main id="main">
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Webs para negocios de Oviedo y Asturias</span>
    <h1>Tu web profesional<br> en 48 horas. <span>99€.</span></h1>
    <p class="lead">Una página clara y rápida con tus servicios, fotos, horario, mapa y botón de WhatsApp. Pagas al aprobarla.</p>
    <div class="ctas">
      <a class="btn btn--solid" href="{WA}" target="_blank" rel="noopener">{WA_ICON}<span>Pedir mi web</span></a>
      <a class="link" href="#ejemplos">Ver ejemplos {ARROW}</a>
    </div>
    <div class="facts">
      <div><b>48 horas</b>Desde que me envías tus datos.</div>
      <div><b>99€, pago único</b>Hosting incluido, sin permanencia.</div>
      <div><b>Bizum o transferencia</b>Pagas al aprobar la web.</div>
    </div>
  </div>
</section>

<section id="ejemplos">
  <div class="wrap">
    <div class="shead reveal">
      <div><span class="eyebrow">Ejemplos</span><h2 style="margin-top:20px">Así puede quedar la tuya.</h2></div>
      <p>Tres negocios ficticios de Oviedo, tres estilos. Cada web se adapta a tu marca, tus fotos y tu forma de trabajar.</p>
    </div>
    <div class="demos">
{demos}
    </div>
  </div>
</section>

<section id="incluye" class="alt">
  <div class="wrap incl">
    <div class="reveal">
      <span class="eyebrow">Qué incluye</span>
      <h2 style="margin-top:20px">Todo lo necesario. Nada que sobre.</h2>
      <p class="intro">Una sola página, bien hecha, con lo que tus clientes buscan antes de llamarte.</p>
      <div class="price">
        <div class="amt">99€<small>pago único</small></div>
        <p>Pago por Bizum o transferencia. <strong>Pagas al aprobar la web.</strong></p>
        <p>Mantenimiento opcional: 9€/mes para cambios de horario, precios o fotos.</p>
        <a class="btn btn--solid" href="{WA}" target="_blank" rel="noopener">{WA_ICON}<span>Pedir mi web</span></a>
      </div>
    </div>
    <ul class="list reveal">
{incl}
    </ul>
  </div>
</section>

<section id="proceso">
  <div class="wrap">
    <div class="shead reveal">
      <div><span class="eyebrow">Proceso</span><h2 style="margin-top:20px">Tres pasos. Sin complicaciones.</h2></div>
      <p>Tú sigues con tu negocio. Yo me encargo del resto.</p>
    </div>
    <ol class="steps">
      <li class="reveal"><span class="n">01</span><h3>Me escribes</h3><p>Por WhatsApp: nombre del negocio, servicios, horario y unas fotos. Diez minutos.</p></li>
      <li class="reveal"><span class="n">02</span><h3>La preparo en 48 horas</h3><p>Diseño, textos y fotos optimizadas. Te envío el enlace para revisarla en tu móvil.</p></li>
      <li class="reveal"><span class="n">03</span><h3>La apruebas y se publica</h3><p>Hacemos los cambios que necesites. Cuando te guste, pagas y queda online.</p></li>
    </ol>
  </div>
</section>

<section id="preguntas" class="alt">
  <div class="wrap">
    <div class="shead reveal">
      <div><span class="eyebrow">Preguntas</span><h2 style="margin-top:20px">Lo que suelen preguntarme.</h2></div>
    </div>
    <div class="faq reveal">
{faq}
    </div>
  </div>
</section>
{final_cta()}
</main>
{offer_footer()}"""
    jsonld = [{
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Virtualy · Webs en 48 horas", "url": SITE_URL + "/", "image": SITE_URL + "/assets/og.png",
        "description": "Diseño de webs de una página para negocios locales en Oviedo y Asturias. 99€, entrega en 48 horas.",
        "email": EMAIL, "founder": {"@type": "Person", "name": "Ali Attia"},
        "areaServed": [{"@type": "City", "name": "Oviedo"}, {"@type": "AdministrativeArea", "name": "Asturias"}],
        "address": {"@type": "PostalAddress", "addressLocality": "Oviedo", "addressRegion": "Asturias", "addressCountry": "ES"},
        "priceRange": "99€",
        "makesOffer": {"@type": "Offer", "name": "Web de una página en 48 horas", "price": "99", "priceCurrency": "EUR"},
    }]
    return dict(path="/", title="Tu web profesional en 48 horas por 99€ · Oviedo y Asturias",
                og_title="Tu web profesional en 48 horas. 99€.",
                description="Webs de una página para negocios locales de Oviedo y Asturias: servicios, fotos, horario, mapa y WhatsApp. 99€, lista en 48 horas. Pagas al aprobarla.",
                css=["/assets/css/offer.css"], jsonld=jsonld, body=body)

# ---------- generic landing template (for SEO pages) ----------
def landing_page(d):
    """d: {slug|path, title, description, h1, eyebrow?, lead?, sections:[{h2, html}] | html, jsonld?:[...], canonical?, noindex?}"""
    path = d.get("path") or "/" + d["slug"].strip("/") + "/"
    secs = d.get("sections") or ([{"h2": "", "html": d["html"]}] if d.get("html") else [])
    content = "\n".join(f'<div class="reveal">{("<h2>" + e(s["h2"]) + "</h2>") if s.get("h2") else ""}{s.get("html", "")}</div>' for s in secs)
    body = f"""{offer_header(home=False)}
<main id="main">
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">{e(d.get('eyebrow', 'Webs en 48 horas · 99€'))}</span>
    <h1>{e(d['h1'])}</h1>
    {('<p class="lead">' + e(d['lead']) + '</p>') if d.get('lead') else ''}
    <div class="ctas">
      <a class="btn btn--solid" href="{WA}" target="_blank" rel="noopener">{WA_ICON}<span>Pedir mi web</span></a>
      <a class="link" href="/#ejemplos">Ver ejemplos {ARROW}</a>
    </div>
  </div>
</section>
<section><div class="wrap prose">
{content}
</div></section>
{final_cta()}
</main>
{offer_footer()}"""
    return dict(path=path, title=d["title"], description=d["description"], canonical=d.get("canonical"),
                noindex=d.get("noindex", False), css=["/assets/css/offer.css"], jsonld=d.get("jsonld", []), body=body)

# ---------- demos ----------
def img(name, alt, sizes, big, small, w, h, eager=False, cls=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="/assets/img/{name}-{small}.webp" srcset="/assets/img/{name}-{small}.webp {small}w, /assets/img/{name}-{big}.webp {big}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {load} decoding="async"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>')

def demo_page(D):
    s = D["slug"]
    menu = lambda items: "\n".join(
        f'<li><b>{e(n)}</b><span class="p">{e(p)}</span>{("<span class=" + chr(34) + "d" + chr(34) + ">" + e(d) + "</span>") if d else ""}</li>'
        for n, d, p in items)
    hours = "\n".join(f"<li><span>{e(a)}</span><span>{e(b)}</span></li>" for a, b in D["hours"])
    revs = "\n".join(f"<figure><blockquote>{e(q)}</blockquote><figcaption>{e(w)}</figcaption></figure>" for q, w in D["reviews"])
    g = D["gallery"]
    gal = "\n".join(f'<figure class="g{i+1}">{img(n, a, "(min-width:900px) 60vw, 100vw", 1200, 600, 1200, 800)}</figure>' for i, (n, a) in enumerate(g))
    booking = '<a class="btn btn--solid js-demo" href="#visita">{icon}<span>{t}</span></a>'.format(icon=WA_ICON, t=e(D["cta"]))
    hero_cls = "dhero dhero--full" if D.get("full_hero") else "dhero"
    hn, ha, hb, hs, hw, hh = D["hero"]
    hero_img = img(hn, ha, "100vw" if D.get("full_hero") else "(min-width:960px) 50vw, 100vw", hb, hs, hw, hh, eager=True)
    services_html = D["services_html"](menu) if callable(D.get("services_html")) else f'<ul class="menu reveal">{menu(D["services"])}</ul>'
    body = f"""<div class="demobar">Web de demostración · negocio ficticio. ¿Quieres una así para tu negocio? <a href="/">99€ en 48 horas</a></div>
<header class="dh">
  <div class="wrap">
    <a class="logo" href="#main">{e(D['name'])}<small>Demo</small></a>
    <nav class="dnav" aria-label="Secciones">{''.join(f'<a href="#{a}">{e(b)}</a>' for a, b in D['nav'])}</nav>
    <a class="btn btn--ghost js-demo" href="#visita">{e(D['cta_short'])}</a>
  </div>
</header>
<main id="main">
<section class="{hero_cls}">
  <div class="img">{hero_img}</div>
  <div class="txt">
    <span class="eyebrow">{e(D['eyebrow'])}</span>
    <h1>{D['h1']}</h1>
    <p>{e(D['lead'])}</p>
    <div class="ctas">{booking}<a class="link" href="#{D['nav'][0][0]}">{e(D['secondary'])}</a></div>
  </div>
</section>

<section class="ds">
  <div class="wrap intro reveal">
    <blockquote>{e(D['quote'])}</blockquote>
    <p>{e(D['about'])}</p>
  </div>
</section>

<section class="ds" id="{D['nav'][0][0]}" style="padding-top:0">
  <div class="wrap">
    <div class="dsh reveal"><div><span class="eyebrow">{e(D['svc_eyebrow'])}</span><h2 style="margin-top:18px">{e(D['svc_title'])}</h2></div><p>{e(D['svc_text'])}</p></div>
    {services_html}
  </div>
</section>

<section class="ds" id="galeria" style="padding-top:0">
  <div class="wrap">
    <div class="dsh reveal"><div><span class="eyebrow">Galería</span><h2 style="margin-top:18px">{e(D['gal_title'])}</h2></div></div>
    <div class="gal reveal">{gal}</div>
  </div>
</section>

<section class="ds" id="opiniones" style="background:var(--bg-2)">
  <div class="wrap">
    <div class="dsh reveal"><div><span class="eyebrow">Opiniones</span><h2 style="margin-top:18px">Lo que dicen nuestros clientes.</h2></div><p>Opiniones de ejemplo para esta demostración.</p></div>
    <div class="revs reveal">{revs}</div>
  </div>
</section>

<section class="ds" id="visita">
  <div class="wrap visit">
    <div class="reveal">
      <span class="eyebrow">Visítanos</span>
      <p class="addr" style="margin-top:18px">{D['address']}</p>
      <p class="muted" style="margin-top:12px">Dirección de ejemplo. Negocio ficticio.</p>
      <a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=Oviedo%2C%20Asturias" target="_blank" rel="noopener">Cómo llegar {ARROW}</a>
    </div>
    <div class="reveal">
      <span class="eyebrow">Horario</span>
      <ul class="hours" style="margin-top:18px">{hours}</ul>
    </div>
  </div>
</section>

<section class="ds book">
  <div class="wrap reveal">
    <div><h2>{e(D['book_title'])}</h2><p style="margin-top:20px">{e(D['book_text'])}</p></div>
    <div class="ctas"><a class="btn btn--light js-demo" href="#visita">{WA_ICON}<span>{e(D['cta'])}</span></a></div>
  </div>
</section>
</main>
<footer class="df">
  <div class="wrap">
    <span>{e(D['name'])} · Negocio ficticio creado como ejemplo</span>
    <span>Diseño: <a href="/">Virtualy · Tu web en 48 horas por 99€</a></span>
  </div>
</footer>
<a class="fab js-demo" href="#visita" aria-label="{e(D['cta'])} (demostración)">{WA_ICON}</a>
<div class="toast" role="status" aria-live="polite"></div>
<script>
document.querySelectorAll('.js-demo').forEach(function(a){{a.addEventListener('click',function(ev){{
var t=document.querySelector('.toast');t.textContent='Botón de demostración. En tu web, abrirá tu WhatsApp.';t.classList.add('on');
clearTimeout(window.__t);window.__t=setTimeout(function(){{t.classList.remove('on')}},2600);}})}});
</script>"""
    style = f"<style>:root{{--bg:{D['bg']};--bg-2:{D['bg2']};--ink:{D['ink']};--muted:{D['muted']};--accent:{D['accent']};--accent-deep:{D['accent_deep']}}}</style>"
    return dict(path=f"/{s}/", title=f"{D['name']} · {D['kind']} en Oviedo (web de demostración)",
                description=D["lead"] + " Web de demostración de un negocio ficticio.",
                noindex=True, css=["/assets/css/demo.css"], head_extra=style, theme=D["bg"],
                og_image=f"/assets/shots/{s}-og.jpg", body=body)

PELU = dict(
    slug="demo-peluqueria", name="Peluquería Demo", kind="Peluquería",
    bg="#f6f2ee", bg2="#efe8e1", ink="#1c1917", muted="#6b625c", accent="#8a5442", accent_deep="#6f4234",
    nav=[("servicios", "Servicios"), ("galeria", "Galería"), ("opiniones", "Opiniones"), ("visita", "Horario")],
    cta="Pedir cita por WhatsApp", cta_short="Pedir cita", secondary="Ver servicios",
    eyebrow="Peluquería · Centro de Oviedo",
    h1="Tu pelo, en <em>buenas manos.</em>",
    lead="Corte, color y peinado con cita previa. Un salón tranquilo, sin prisas y con productos profesionales.",
    hero=("pelu-hero", "Interior del salón con espejos redondos, apliques de luz y sillones negros", 1400, 800, 1400, 2119),
    quote="Escuchamos primero. Cortamos después.",
    about="Cada cita empieza con una conversación: cómo llevas el pelo, cuánto tiempo le dedicas y qué te apetece cambiar. Trabajamos con cita previa para dedicarte el tiempo que necesitas.",
    svc_eyebrow="Servicios", svc_title="Servicios y precios.", svc_text="Precios orientativos. El precio final depende del largo y del tipo de pelo; te lo confirmamos antes de empezar.",
    services=[
        ("Corte y peinado", "Asesoramiento, lavado, corte y acabado", "32€"),
        ("Corte caballero", "Corte a tijera o máquina, con lavado", "18€"),
        ("Color raíz", "Cobertura de canas o retoque de tono", "38€"),
        ("Balayage", "Técnica a mano alzada para un tono natural", "desde 85€"),
        ("Tratamiento de hidratación", "Mascarilla profesional y masaje capilar", "25€"),
        ("Peinado de evento", "Ondas, recogidos y acabados especiales", "40€"),
        ("Novias", "Prueba previa incluida", "desde 120€"),
    ],
    gal_title="El salón y nuestro trabajo.",
    gallery=[("pelu-1", "Espejos iluminados del salón"), ("pelu-2", "Estilista cortando el pelo a tijera"), ("pelu-3", "Salón luminoso con tocadores y sillones")],
    reviews=[("Por fin alguien que entiende lo que le pido. El color quedó exactamente como quería.", "Marta G. · Ejemplo"),
             ("Ambiente tranquilo, puntuales con la cita y un trato muy cercano.", "Lucía F. · Ejemplo"),
             ("Me cortan el pelo aquí desde hace años. Siempre salgo contento.", "Javier R. · Ejemplo")],
    address="Calle Ejemplo, 12<br>33001 Oviedo, Asturias",
    hours=[("Lunes", "Cerrado"), ("Martes a viernes", "9:30–13:30 · 16:00–20:00"), ("Sábado", "9:00–14:00"), ("Domingo", "Cerrado")],
    book_title="Reserva tu cita.", book_text="Escríbenos por WhatsApp con el servicio y el día que prefieres. Te respondemos en el día.",
)

def sidra_services(menu):
    carta = [
        ("Para empezar", [("Tabla de quesos asturianos", "Cabrales, Afuega'l Pitu, Gamonéu y Casín", "16€"), ("Chorizo a la sidra", "", "9€"), ("Croquetas caseras de jamón", "Ocho unidades", "11€"), ("Pulpo a la plancha", "Con patata y pimentón de la Vera", "19€")]),
        ("Principales", [("Fabada asturiana", "Con su compango", "15€"), ("Cachopo de ternera asturiana", "Relleno de jamón y queso de la tierra", "26€"), ("Pixín a la sidra", "Rape del Cantábrico", "22€"), ("Chuletón de vaca madurada", "Precio por kilo", "48€")]),
        ("Postres", [("Arroz con leche requemado", "", "6€"), ("Tarta de queso casera", "", "6,50€"), ("Frixuelos", "Con crema y miel", "6€")]),
        ("Sidra y bodega", [("Sidra natural", "Botella, escanciada en mesa", "3,80€"), ("Sidra de nueva expresión", "Botella", "9€"), ("Vino de la casa", "Copa", "2,80€")]),
    ]
    cols = "\n".join(f'<div><h3>{e(t)}</h3><ul class="menu">{menu(items)}</ul></div>' for t, items in carta)
    house = """<ul class="house reveal" style="margin-bottom:88px">
<li><b>Menú del día</b><span>De lunes a viernes, primero, segundo, postre y bebida. 15€.</span></li>
<li><b>Grupos y celebraciones</b><span>Comedor privado hasta 30 personas. Menús desde 28€ por persona.</span></li>
<li><b>Sidra escanciada</b><span>Sidra natural de llagares asturianos, servida en mesa.</span></li>
</ul>"""
    return house + f'<div class="cols reveal">{cols}</div><p class="note reveal">Carta de ejemplo. Consulta alérgenos al personal.</p>'

SIDRA = dict(
    slug="demo-sidreria", name="Sidrería Demo", kind="Sidrería", full_hero=True,
    bg="#f4f0e8", bg2="#ebe5d8", ink="#1b1a16", muted="#6a6456", accent="#7a5a1e", accent_deep="#5f4515",
    nav=[("carta", "Carta"), ("galeria", "Galería"), ("opiniones", "Opiniones"), ("visita", "Horario")],
    cta="Reservar mesa por WhatsApp", cta_short="Reservar", secondary="Ver la carta",
    eyebrow="Sidrería · Calle Gascona, Oviedo",
    h1="Sidra, brasa y <em>cocina de casa.</em>",
    lead="Cocina asturiana de siempre, producto de temporada y sidra natural escanciada en mesa.",
    hero=("sidra-hero", "Comedor de la sidrería con mesas de madera y luz cálida", 1800, 900, 1800, 1200),
    quote="Una mesa larga, una botella de sidra y tiempo para compartir.",
    about="Llevamos la cocina asturiana tradicional al centro de Oviedo: fabada a fuego lento, pescado del Cantábrico y quesos de pequeños productores. Reservamos para grupos, comidas de empresa y celebraciones.",
    svc_eyebrow="La carta", svc_title="Nuestra carta.", svc_text="Cocina de mercado. Algunos platos cambian según la temporada.",
    services_html=sidra_services,
    gal_title="La casa.",
    gallery=[("sidra-5", "Botella de sidra natural y manzanas sobre una tabla de madera"), ("sidra-2", "Tabla de quesos para compartir"), ("sidra-4", "Tabla de embutidos, quesos y aceitunas"), ("sidra-3", "Comedor con lámparas de mimbre y ventanales")],
    reviews=[("La fabada, de las mejores que he probado en Oviedo. Y la sidra, perfecta.", "Pablo M. · Ejemplo"),
             ("Celebramos una comida de empresa de 25 personas. Todo impecable.", "Ana S. · Ejemplo"),
             ("Trato familiar, raciones generosas y un cachopo espectacular.", "Carlos V. · Ejemplo")],
    address="Calle Gascona (zona)<br>33001 Oviedo, Asturias",
    hours=[("Lunes", "Cerrado por descanso"), ("Martes a jueves", "12:00–16:30 · 20:00–23:30"), ("Viernes y sábado", "12:00–00:30"), ("Domingo", "12:00–17:00")],
    book_title="Reserva tu mesa.", book_text="Dinos cuántos sois, el día y la hora. Para grupos de más de diez, mejor con dos días de antelación.",
)

FISIO = dict(
    slug="demo-fisioterapia", name="Fisioterapia Demo", kind="Fisioterapia",
    bg="#f3f5f4", bg2="#e8eeec", ink="#141a19", muted="#5a6663", accent="#2c6964", accent_deep="#1f514d",
    nav=[("tratamientos", "Tratamientos"), ("galeria", "Clínica"), ("opiniones", "Opiniones"), ("visita", "Horario")],
    cta="Pedir cita por WhatsApp", cta_short="Pedir cita", secondary="Ver tratamientos",
    eyebrow="Fisioterapia · Oviedo",
    h1="Muévete <em>sin dolor.</em>",
    lead="Fisioterapia manual, deportiva y rehabilitación. Primera valoración completa y un plan claro desde el primer día.",
    hero=("fisio-hero", "Fisioterapeuta realizando un estiramiento de pierna a una paciente en camilla", 1800, 900, 1800, 1200),
    quote="Entender la causa del dolor es la mitad del tratamiento.",
    about="Sesiones individuales de 45 minutos, siempre con el mismo fisioterapeuta. Te explicamos qué ocurre, qué vamos a hacer y qué puedes hacer tú en casa para recuperarte antes.",
    svc_eyebrow="Tratamientos", svc_title="Tratamientos y tarifas.", svc_text="Sesiones individuales en cabina privada. Aceptamos pago con tarjeta y Bizum.",
    services=[
        ("Primera valoración", "Entrevista, exploración y primera sesión · 60 min", "45€"),
        ("Sesión de fisioterapia", "Terapia manual y ejercicio · 45 min", "40€"),
        ("Fisioterapia deportiva", "Lesiones, prevención y vuelta al deporte", "45€"),
        ("Punción seca", "Complemento a la sesión", "+10€"),
        ("Suelo pélvico", "Valoración y tratamiento especializado", "50€"),
        ("Pilates terapéutico", "Grupos de cuatro personas · cuatro sesiones al mes", "60€"),
        ("Bono de cinco sesiones", "Válido durante tres meses", "180€"),
    ],
    gal_title="La clínica.",
    gallery=[("fisio-1", "Sala de pilates terapéutico con máquinas reformer"), ("fisio-2", "Terapia de percusión en la planta del pie"), ("fisio-3", "Masaje terapéutico de espalda y hombros"), ("fisio-4", "Terapia manual en la zona lumbar")],
    reviews=[("Llegué con una lumbalgia de meses y en cuatro sesiones noté un cambio enorme.", "Elena P. · Ejemplo"),
             ("Te explican todo con claridad y te dan ejercicios útiles para casa.", "Diego A. · Ejemplo"),
             ("Me recuperé de una lesión de rodilla y volví a correr sin molestias.", "Sara L. · Ejemplo")],
    address="Avenida Ejemplo, 10<br>33004 Oviedo, Asturias",
    hours=[("Lunes a viernes", "9:00–14:00 · 15:30–21:00"), ("Sábado", "Con cita previa"), ("Domingo", "Cerrado")],
    book_title="Pide tu primera valoración.", book_text="Cuéntanos brevemente qué te pasa y te proponemos el primer hueco disponible.",
)

# ---------- extra pages ----------
def extra_pages():
    pages = []
    for f in sorted(glob.glob(os.path.join(HERE, "pages", "*.json")) + glob.glob(os.path.join(SEO_DIR, "pages", "*.json")) + glob.glob(os.path.join(SEO_DIR, "*.page.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        for item in (d if isinstance(d, list) else [d]):
            pages.append(landing_page(item))
    return pages

def seo_jsonld():
    """Optional JSON-LD from SEO worker: jsonld/<slug-or-index>.json -> merged into the matching page."""
    m = {}
    for f in glob.glob(os.path.join(SEO_DIR, "jsonld", "*.json")) + glob.glob(os.path.join(SEO_DIR, "*.jsonld")):
        key = os.path.splitext(os.path.basename(f))[0].replace(".jsonld", "")
        key = "/" if key in ("index", "home", "root") else "/" + key.strip("/") + "/"
        with open(f, encoding="utf-8") as fh:
            j = json.load(fh)
        m.setdefault(key, []).extend(j if isinstance(j, list) else [j])
    return m

def write(path, text):
    fp = os.path.join(OUT, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as fh:
        fh.write(text)

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"))
    for f in os.listdir(os.path.join(HERE, "static")):
        shutil.copy(os.path.join(HERE, "static", f), OUT)
    pages = [offer_page(), demo_page(PELU), demo_page(SIDRA), demo_page(FISIO)] + extra_pages()
    extra_ld = seo_jsonld()
    for p in pages:
        if p["path"] in extra_ld and not p.get("noindex"):
            p["jsonld"] = extra_ld[p["path"]]  # SEO worker's JSON-LD replaces default for that page
        write(p["path"], layout(p))
    # sitemap / robots: SEO worker's versions win, else generate
    for name in ("sitemap.xml", "robots.txt"):
        src = os.path.join(SEO_DIR, name)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(OUT, name))
    if not os.path.isfile(os.path.join(OUT, "sitemap.xml")):
        urls = "".join(f"<url><loc>{SITE_URL}{p['path']}</loc></url>" for p in pages if not p.get("noindex"))
        write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    if not os.path.isfile(os.path.join(OUT, "robots.txt")):
        write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("built", len(pages), "pages:", ", ".join(p["path"] for p in pages))

if __name__ == "__main__":
    main()
