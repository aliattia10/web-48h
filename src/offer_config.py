# -*- coding: utf-8 -*-
"""Single source of truth for brand, prices and legal wording.
Imported by src/build.py (offer page, demos) and by the SEO builder
(/workspace/research/seo/web-48h-integration/build.py + content.py placeholders).
Change a value here, run both builds, redeploy."""
import datetime

BRAND = "Virtualy · Ali Attia"
SITE_URL = "https://ali-webs-48h.netlify.app"
EMAIL = "ali.attia@virtualy.win"
TEL = "+34677372245"
PRICE_RANGE = "29€ - 149€"

# IVA: no statement until Ali decides. One-line change later, e.g. "IVA incluido." or "IVA no incluido."
IVA_NOTE = ""

PROMO_END = datetime.date(2026, 10, 4)          # last day of the launch price for WhatsApp bookings
def promo_active(today=None):
    return (today or datetime.date.today()) <= PROMO_END

def prices(today=None):
    p = promo_active(today)
    return {
        "web":     dict(name="Web en 48 horas", price=99, unit="pago único"),
        "citas":   dict(name="Reservas por WhatsApp", price=79 if p else 99, unit="pago único",
                        note="Precio de lanzamiento hasta el 4 de octubre de 2026; después, 99€." if p else ""),
        "pack":    dict(name="Pack web + reservas", price=149, unit="pago único"),
        "qr":      dict(name="Carta QR para sidrerías", price=49, unit="pago único"),
        "resenas": dict(name="Tarjeta QR de reseñas de Google", price=29, unit="pago único"),
        "care":    dict(name="Mantenimiento opcional (solo web)", price=9, unit="al mes, sin permanencia"),
        "care_citas": dict(name="Mantenimiento opcional (con reservas)", price=19, unit="al mes, sin permanencia"),
    }

DESC = {
    "web": "Web de una página con servicios, fotos, horario, mapa y botón de WhatsApp.",
    "citas": "Página de citas que te envía cada reserva por WhatsApp, ya escrita.",
    "pack": "La web en 48 horas con las reservas por WhatsApp integradas.",
    "qr": "Carta digital para las mesas, con carteles QR listos para imprimir.",
    "resenas": "Tarjeta con código QR para que tus clientes te dejen reseña en Google.",
    "care": "Cambios de horario, precios o fotos en tu web. Sin permanencia.",
    "care_citas": "Lo mismo, incluyendo el mantenimiento de las reservas. Sin permanencia.",
}

MENU_ORDER = ["web", "citas", "pack", "qr", "resenas", "care", "care_citas"]

def fmt(key, today=None):
    """'99€', '79€', '9€ al mes' ... for inline copy."""
    x = prices(today)[key]
    return f"{x['price']}€" + (" al mes" if key.startswith("care") else "")

def placeholders(today=None):
    """Values for {placeholders} used in the SEO content.py copy."""
    return {k: fmt(k, today) for k in MENU_ORDER} | {"iva": IVA_NOTE, "brand": BRAND}

def jsonld_business(today=None, extra=None):
    pr = prices(today)
    d = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "@id": SITE_URL + "/#negocio",
        "name": BRAND, "url": SITE_URL + "/", "image": SITE_URL + "/assets/og.png",
        "description": "Webs de una página en 48 horas, reservas por WhatsApp y cartas QR para pequeños negocios de Oviedo, Gijón y Asturias.",
        "telephone": TEL, "email": EMAIL, "priceRange": PRICE_RANGE,
        "founder": {"@type": "Person", "name": "Ali Attia"},
        "areaServed": [{"@type": "City", "name": "Oviedo"}, {"@type": "City", "name": "Gijón"},
                       {"@type": "AdministrativeArea", "name": "Asturias"}],
        "address": {"@type": "PostalAddress", "addressLocality": "Oviedo", "addressRegion": "Asturias", "addressCountry": "ES"},
        "paymentAccepted": "Bizum, transferencia bancaria",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Servicios", "itemListElement": [
            {"@type": "Offer", "name": pr[k]["name"], "price": str(pr[k]["price"]), "priceCurrency": "EUR",
             **({"priceValidUntil": PROMO_END.isoformat()} if pr[k].get("note") else {})} for k in MENU_ORDER]},
    }
    if extra:
        d.update(extra)
    return d
