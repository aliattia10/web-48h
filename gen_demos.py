import os, html
BASE = os.path.join(os.path.dirname(__file__), "site")
demos = [
 dict(slug="demo-peluqueria", name="Peluquería Demo", kind="Peluquería unisex", emoji="✂️",
      c1="#db2777", c2="#7c3aed", tagline="Cortes, color y peinados con cita previa en el centro de Oviedo.",
      address="Calle Ejemplo 1, Oviedo (dirección ficticia)",
      services=[("Corte mujer","desde 18€"),("Corte hombre","12€"),("Color / tinte","desde 30€"),("Mechas / balayage","desde 45€"),("Peinado evento","25€"),("Tratamiento hidratante","15€")],
      gallery=[("💇‍♀️","Corte y peinado"),("🎨","Color"),("💈","Barbería"),("✨","Tratamientos"),("👰","Novias"),("🪞","Nuestro salón")],
      hours=[("Lunes","Cerrado"),("Martes – Viernes","9:30 – 13:30 · 16:00 – 20:00"),("Sábado","9:00 – 14:00"),("Domingo","Cerrado")],
      about="Somos un salón de barrio con más de 10 años cuidando el pelo de nuestros vecinos. Trabajamos con cita previa para que no tengas que esperar.",
      cta="Pide cita por WhatsApp", extra_title="Por qué elegirnos", extra=[("Con cita previa","Sin esperas"),("Productos profesionales","Cuidamos tu pelo")]),
 dict(slug="demo-sidreria", name="Sidrería Demo", kind="Sidrería · cocina asturiana", emoji="🍏",
      c1="#b45309", c2="#65a30d", tagline="Sidra bien escanciada, cachopos y cocina asturiana de siempre.",
      address="Calle Gascona (zona), Oviedo (negocio ficticio)",
      services=[("Menú del día (L–V)","14€"),("Cachopo de ternera","22€"),("Fabada asturiana","13€"),("Tabla de quesos asturianos","14€"),("Pixín a la sidra","18€"),("Botella de sidra natural","3,50€")],
      gallery=[("🍏","Sidra natural"),("🥘","Fabada"),("🥩","Cachopo"),("🧀","Quesos"),("🍻","Terraza"),("🎉","Grupos y celebraciones")],
      hours=[("Lunes – Jueves","12:00 – 16:30 · 20:00 – 23:30"),("Viernes – Sábado","12:00 – 00:30"),("Domingo","12:00 – 17:00"),("Martes","Cerrado por descanso")],
      about="Sidrería familiar en el corazón del bulevar de la sidra. Reservas para grupos, comidas de empresa y celebraciones.",
      cta="Reserva mesa por WhatsApp", extra_title="Para grupos", extra=[("Menús de grupo desde 25€/persona","Consulta disponibilidad"),("Comedor privado hasta 30 personas","Con reserva previa")]),
 dict(slug="demo-fisioterapia", name="Fisioterapia Demo", kind="Clínica de fisioterapia", emoji="🩺",
      c1="#0284c7", c2="#0f766e", tagline="Fisioterapia deportiva, dolor de espalda y rehabilitación en Oviedo.",
      address="Avenida Ejemplo 10, Oviedo (dirección ficticia)",
      services=[("Sesión de fisioterapia (45 min)","35€"),("Bono 5 sesiones","160€"),("Fisioterapia deportiva","40€"),("Punción seca","+10€"),("Drenaje linfático","35€"),("Pilates terapéutico (grupo reducido)","50€/mes")],
      gallery=[("🦴","Espalda y cuello"),("🏃","Deportiva"),("🧘","Pilates"),("💆","Terapia manual"),("🦵","Rehabilitación"),("🏥","Nuestra clínica")],
      hours=[("Lunes – Viernes","9:00 – 14:00 · 15:30 – 21:00"),("Sábado","Con cita previa"),("Domingo","Cerrado")],
      about="Fisioterapeutas colegiados (ejemplo). Primera valoración para entender tu caso y un plan de tratamiento claro desde el primer día.",
      cta="Pide cita por WhatsApp", extra_title="Nuestro equipo", extra=[("Fisioterapeuta A (ejemplo)","Deportiva y punción seca"),("Fisioterapeuta B (ejemplo)","Suelo pélvico y pilates")]),
]
TPL = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} · {kind} en Oviedo (web de demostración)</title>
<meta name="description" content="{tagline} — Web de demostración de un negocio ficticio.">
<meta name="robots" content="noindex">
<style>
:root{{--c1:{c1};--c2:{c2};--ink:#1f2937;--muted:#6b7280;--line:#e5e7eb}}
*{{box-sizing:border-box}}body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);line-height:1.6;background:#fafafa}}
.demo-bar{{background:#111827;color:#fde68a;text-align:center;font-size:.85rem;padding:8px 12px}}
.demo-bar a{{color:#fff}}
.wrap{{max-width:980px;margin:0 auto;padding:0 20px}}
.hero{{background:linear-gradient(135deg,var(--c1),var(--c2));color:#fff;padding:70px 0 80px;text-align:center}}
.hero .e{{font-size:3.5rem}}.hero h1{{font-size:clamp(2rem,6vw,3.2rem);margin:.2em 0;letter-spacing:-.02em}}
.hero p{{font-size:1.15rem;opacity:.95;max-width:620px;margin:0 auto 20px}}
.btn{{display:inline-block;padding:13px 22px;border-radius:999px;font-weight:700;text-decoration:none;margin:6px}}
.wa{{background:#25d366;color:#fff}}.call{{background:#fff;color:var(--c1)}}
section{{padding:56px 0}}h2{{font-size:1.8rem;margin:0 0 20px;letter-spacing:-.01em}}
.svc{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.svc div{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 18px;display:flex;justify-content:space-between;gap:10px}}
.svc b{{color:var(--c1);white-space:nowrap}}
.gal{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}}
.ph{{aspect-ratio:4/3;border-radius:14px;background:linear-gradient(160deg,var(--c1),var(--c2));color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:2.4rem;opacity:.92}}
.ph span{{font-size:.85rem;margin-top:6px}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;border:1px solid var(--line)}}
td{{padding:12px 16px;border-bottom:1px solid var(--line)}}td:last-child{{text-align:right;color:var(--muted)}}
iframe{{width:100%;height:280px;border:0;border-radius:12px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
.cards div{{background:#fff;border-left:4px solid var(--c1);border-radius:10px;padding:14px 18px}}
.cards small{{color:var(--muted)}}
.float{{position:fixed;right:18px;bottom:18px;background:#25d366;color:#fff;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.7rem;text-decoration:none;box-shadow:0 6px 20px rgba(0,0,0,.25)}}
footer{{background:#111827;color:#9ca3af;padding:30px 0;text-align:center;font-size:.9rem}}footer a{{color:#fff}}
</style></head><body>
<div class="demo-bar">🧪 Web de demostración · negocio ficticio · <a href="../">¿Quieres una así para tu negocio? 99€ en 48 h →</a> · <a href="mailto:info@virtualy.win?subject=Quiero%20mi%20web%20en%2048h">info@virtualy.win</a></div>
<header class="hero"><div class="wrap">
<div class="e">{emoji}</div><h1>{name}</h1><p>{tagline}</p>
<a class="btn wa" href="#" onclick="alert('Demo: aquí iría el enlace a tu WhatsApp');return false">💬 {cta}</a>
<a class="btn call" href="#" onclick="alert('Demo: aquí iría tu teléfono');return false">📞 Llamar</a>
</div></header>
<section><div class="wrap"><h2>Sobre nosotros</h2><p>{about}</p></div></section>
<section style="background:#fff"><div class="wrap"><h2>Servicios y precios</h2><div class="svc">{services}</div>
<p style="color:#6b7280;font-size:.85rem;margin-top:12px">Precios de ejemplo.</p></div></section>
<section><div class="wrap"><h2>Galería</h2><div class="gal">{gallery}</div>
<p style="color:#6b7280;font-size:.85rem;margin-top:12px">En tu web irían tus fotos reales.</p></div></section>
<section style="background:#fff"><div class="wrap"><h2>{extra_title}</h2><div class="cards">{extra}</div></div></section>
<section><div class="wrap two">
<div><h2>Horario</h2><table>{hours}</table></div>
<div><h2>Dónde estamos</h2><p style="margin-top:0">{address}</p>
<iframe loading="lazy" title="Mapa Oviedo" src="https://www.google.com/maps?q=Oviedo,+Asturias&output=embed"></iframe></div>
</div></section>
<footer><div class="wrap">{name} · Oviedo, Asturias · Web de demostración creada por <a href="../">Web48h</a> · <a href="mailto:info@virtualy.win?subject=Quiero%20mi%20web%20en%2048h">info@virtualy.win</a></div></footer>
<a class="float" href="#" aria-label="WhatsApp" onclick="alert('Demo: aquí iría el enlace a tu WhatsApp');return false">💬</a>
</body></html>
"""
for d in demos:
    e = html.escape
    out = TPL.format(
        name=e(d["name"]), kind=e(d["kind"]), tagline=e(d["tagline"]), c1=d["c1"], c2=d["c2"], emoji=d["emoji"],
        about=e(d["about"]), cta=e(d["cta"]), address=e(d["address"]), extra_title=e(d["extra_title"]),
        services="".join(f"<div><span>{e(a)}</span><b>{e(b)}</b></div>" for a,b in d["services"]),
        gallery="".join(f'<div class="ph">{a}<span>{e(b)}</span></div>' for a,b in d["gallery"]),
        hours="".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a,b in d["hours"]),
        extra="".join(f"<div><b>{e(a)}</b><br><small>{e(b)}</small></div>" for a,b in d["extra"]),
    )
    os.makedirs(os.path.join(BASE, d["slug"]), exist_ok=True)
    open(os.path.join(BASE, d["slug"], "index.html"), "w").write(out)
    print("wrote", d["slug"])
