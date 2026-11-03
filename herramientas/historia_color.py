#!/usr/bin/env python3
"""Historias con la misma maqueta de siempre pero con paletas de color que van cambiando.
Uso: python3 herramientas/historia_color.py   (genera las de disenos/semana-2026-11-02/)
Cada historia: ilustración SVG arriba, etiqueta, titular, nota, nombre del curso y WhatsApp abajo."""
import os

PALETAS = {
    # nombre: (principal, oscuro, claro, fondo arriba, fondo abajo, marcador)
    "violeta":  ("#6A3FA0", "#4B2A75", "#E6DCF3", "#EFE8F8", "#F8F5FC", "#CDB8EC"),
    "oceano":   ("#00838F", "#005F67", "#CDEFF1", "#DDF3F5", "#F3FBFC", "#9FDDE3"),
    "salvia":   ("#2E7D5B", "#1F5A41", "#D5EDE2", "#E2F2EA", "#F5FBF8", "#A9DBC3"),
    "noche":    ("#7FC4EE", "#FFFFFF", "#1E3A52", "#0D2235", "#13304A", "#2F6F9E"),
    "marca":    ("#006DA6", "#00527E", "#BFDCF0", "#E1EEF7", "#F4F9FC", "#94C6E8"),
}

WA = '<svg width="44" height="44" viewBox="0 0 32 32" aria-hidden="true"><path fill="#25D366" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3z"/><path fill="#fff" d="M22.6 18.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8 0 1.6 1.2 3.2 1.4 3.4.2.2 2.4 3.6 5.8 5 2.8 1.1 3.4.9 4 .8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'
PELIGRO = '<svg width="40" height="40" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 1 21h22L12 2z" fill="#D7362B"/><rect x="11" y="9" width="2" height="6" rx="1" fill="#fff"/><circle cx="12" cy="17.5" r="1.2" fill="#fff"/></svg>'

# Ilustraciones (lienzo 1080×640, se colocan entre y=330 y y=970). P, D, L = principal, oscuro, claro.
def ilu_tension(P, D, L):
    return f'''<circle cx="540" cy="320" r="250" fill="{L}"/>
<rect x="250" y="250" width="250" height="200" rx="40" fill="#fff" stroke="{P}" stroke-width="14"/>
<path d="M500 350 C 600 350, 600 520, 700 520" fill="none" stroke="{D}" stroke-width="12"/>
<circle cx="740" cy="520" r="46" fill="{D}"/>
<circle cx="640" cy="230" r="130" fill="#fff" stroke="{D}" stroke-width="14"/>
<path d="M545 270 A100 100 0 0 1 735 270" fill="none" stroke="{L}" stroke-width="20" stroke-linecap="round"/>
<path d="M690 200 A100 100 0 0 1 735 270" fill="none" stroke="#D7362B" stroke-width="20" stroke-linecap="round"/>
<line x1="640" y1="230" x2="712" y2="182" stroke="{D}" stroke-width="12" stroke-linecap="round"/>
<circle cx="640" cy="230" r="16" fill="{D}"/>
<path d="M300 330 h150 M300 370 h150" stroke="{L}" stroke-width="14" stroke-linecap="round"/>'''

def ilu_tsunami(P, D, L):
    return f'''<path d="M600 560 L760 250 Q790 200 820 250 L980 560 Z" fill="{D}"/>
<rect x="770" y="190" width="80" height="60" fill="#fff"/><path d="M760 195 L810 150 L860 195 Z" fill="{L}"/>
<path d="M120 560 Q 180 300 380 300 Q 520 300 520 420 Q 450 360 400 420 Q 360 480 430 520 L560 560 Z" fill="{P}"/>
<path d="M120 560 Q 180 300 380 300 Q 520 300 520 420" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".7"/>
<path d="M80 600 Q 160 570 240 600 T 400 600 T 560 600 T 720 600 T 880 600 T 1040 600" fill="none" stroke="{P}" stroke-width="14" stroke-linecap="round" opacity=".5"/>
<path d="M600 470 Q 650 330 720 300" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-dasharray="4 30"/>
<path d="M700 282 L748 290 L722 330 Z" fill="#fff"/>'''

def ilu_cama(P, D, L):
    return f'''<rect x="170" y="340" width="740" height="150" rx="28" fill="{L}"/>
<rect x="150" y="250" width="40" height="320" rx="18" fill="{D}"/>
<rect x="890" y="320" width="40" height="250" rx="18" fill="{D}"/>
<rect x="210" y="300" width="160" height="70" rx="34" fill="#fff"/>
<path d="M330 330 Q 600 250 880 330 L880 380 L330 380 Z" fill="{P}"/>
<circle cx="760" cy="150" r="120" fill="#fff" stroke="{P}" stroke-width="14"/>
<text x="760" y="178" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="88" fill="{D}">2 h</text>
<path d="M620 120 A150 150 0 0 1 870 40" fill="none" stroke="{D}" stroke-width="12" stroke-linecap="round"/>
<path d="M858 18 L890 46 L850 60 Z" fill="{D}"/>'''

def ilu_convulsion(P, D, L):
    return f'''<circle cx="380" cy="320" r="190" fill="{L}" stroke="{P}" stroke-width="14"/>
<rect x="355" y="100" width="50" height="40" rx="10" fill="{P}"/>
<path d="M380 320 L380 190" stroke="{P}" stroke-width="16" stroke-linecap="round"/>
<path d="M380 320 L470 380" stroke="{P}" stroke-width="16" stroke-linecap="round"/>
<circle cx="380" cy="320" r="18" fill="{P}"/>
<text x="380" y="460" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="64" fill="{P}">5 min</text>
<rect x="640" y="150" width="230" height="380" rx="40" fill="#fff"/>
<rect x="665" y="200" width="180" height="250" rx="16" fill="{L}"/>
<text x="755" y="355" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="84" fill="{P}">112</text>
<circle cx="755" cy="490" r="18" fill="{L}"/>'''

def ilu_rayosx(P, D, L):
    blando = 'fill="#fff" opacity=".22"'
    hueso = 'stroke="#fff" stroke-linecap="round" fill="none" stroke-width="20"'
    # dedos: (x de la base, y de la base, largo, giro)
    dedos = [(445, 380, 150, -8), (505, 360, 200, -3), (565, 355, 215, 2), (625, 365, 190, 7)]
    piel, huesos = "", ""
    for x, y, largo, g in dedos:
        piel += f'<rect x="{x-30}" y="{y-largo}" width="60" height="{largo+40}" rx="30" {blando} transform="rotate({g} {x} {y})"/>'
        t = largo / 3
        segs = "".join(f'<line x1="{x}" y1="{y - i*t - 10:.0f}" x2="{x}" y2="{y - (i+1)*t + 12:.0f}" {hueso}/>' for i in range(3))
        huesos += f'<g transform="rotate({g} {x} {y})">{segs}</g>'
    return f'''<rect x="250" y="10" width="580" height="620" rx="36" fill="{D}"/>
<rect x="250" y="10" width="580" height="620" rx="36" fill="none" stroke="{P}" stroke-width="12"/>
{piel}
<path d="M410 380 Q 400 520 440 620 L 650 620 Q 690 520 660 380 Z" {blando}/>
<rect x="640" y="300" width="58" height="200" rx="29" {blando} transform="rotate(38 670 480)"/>
<line x1="450" y1="400" x2="465" y2="560" {hueso}/><line x1="505" y1="390" x2="510" y2="560" {hueso}/>
<line x1="565" y1="385" x2="560" y2="560" {hueso}/><line x1="622" y1="395" x2="605" y2="560" {hueso}/>
{huesos}
<g transform="rotate(38 670 480)"><line x1="670" y1="470" x2="670" y2="400" {hueso}/><line x1="670" y1="385" x2="670" y2="320" {hueso}/></g>
<line x1="470" y1="600" x2="620" y2="600" stroke="#fff" stroke-width="22" stroke-linecap="round"/>
<g transform="rotate(-3 505 360)"><rect x="475" y="262" width="60" height="18" rx="9" fill="none" stroke="#FFD34D" stroke-width="10"/></g>
<text x="290" y="70" font-family="Space Mono" font-weight="700" font-size="34" fill="#fff" opacity=".8">1895</text>'''

HISTORIAS = [
    dict(fecha="2026-11-04", tema="tension", paleta="violeta", ilu=ilu_tension,
         kicker="Tensión arterial", titular='Cruzar las piernas te <span class="marca">sube la tensión</span>',
         nota="Mídela sentado y tras 5 minutos de reposo", curso="Curso de Auxiliar de Enfermería"),
    dict(fecha="2026-11-05", tema="tsunamis", paleta="oceano", ilu=ilu_tsunami,
         kicker="Día Mundial de los Tsunamis", titular='¿Se retira el mar? <span class="marca">Sube a zona alta</span>',
         nota="Un tsunami son varias olas, no una", curso="Formación en Emergencias Sanitarias"),
    dict(fecha="2026-11-06", tema="ulceras", paleta="salvia", ilu=ilu_cama,
         kicker="Personas encamadas", titular='Cambia de postura <span class="marca">cada 2 horas</span>',
         nota="Así se previenen las úlceras por presión",
         curso="Certificado SSCS0108<br><small>Atención sociosanitaria a personas en el domicilio</small>"),
    dict(fecha="2026-11-07", tema="convulsiones", paleta="noche", ilu=ilu_convulsion, peligro=True,
         kicker="Convulsiones", titular='Nunca le metas <span class="marca">nada en la boca</span>',
         nota="La lengua no se traga.<br>Más de 5 minutos: llama al 112", curso="Formación en Emergencias Sanitarias"),
    dict(fecha="2026-11-08", tema="radiologia", paleta="marca", ilu=ilu_rayosx,
         kicker="Día Internacional de la Radiología", titular='La 1.ª radiografía: <span class="marca">una mano con anillo</span>',
         nota="Röntgen descubrió los rayos X el 8 de noviembre de 1895", curso="Curso de Auxiliar de Enfermería"),
]

def construir(h):
    P, D, L, B1, B2, M = PALETAS[h["paleta"]]
    oscuro = h["paleta"] == "noche"
    texto = "#FFFFFF" if oscuro else "#4C4C4C"
    titular = "#FFFFFF" if oscuro else P
    nota = "#CFE3F2" if oscuro else D
    icono = PELIGRO if h.get("peligro") else ""
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Space+Mono:wght@700&display=block" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; }}
body {{ font-family: "Montserrat", sans-serif; color: {texto}; position: relative;
  background: linear-gradient(180deg, {B1} 0%, {B2} 100%); }}
.circulo {{ position: absolute; border-radius: 50%; background: {L}; opacity: .55; }}
.ilu {{ position: absolute; top: 310px; left: 0; }}
.logo {{ position: absolute; top: 160px; left: 50%; transform: translateX(-50%); width: 380px; padding: 18px 26px;
  background: #fff; border-radius: 26px; box-shadow: 0 14px 40px rgba(0,0,0,.10); }}
.logo img {{ width: 100%; display: block; }}
.bloque {{ position: absolute; top: 975px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; }}
.kicker {{ text-align: center; }}
.chip {{ display: inline-flex; align-items: center; gap: 14px; background: #fff; border-radius: 999px; padding: 14px 30px;
  font-family: "Space Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 3px; text-transform: uppercase;
  color: {"#B02A21" if h.get("peligro") else "#4C4C4C"}; box-shadow: 0 10px 30px rgba(0,0,0,.10); }}
.titular {{ margin: 28px 70px 0; text-align: center; font-weight: 900; font-size: 78px;
  line-height: 1.07; letter-spacing: -1px; color: {titular}; }}
.marca {{ background: linear-gradient(transparent 62%, {M} 62%, {M} 92%, transparent 92%); padding: 0 6px; }}
.nota {{ margin: 22px 110px 0; text-align: center; font-weight: 700; font-size: 38px;
  line-height: 1.3; color: {nota}; }}
.curso {{ margin-top: 30px; text-align: center; }}
.curso span {{ display: inline-block; background: {D if not oscuro else P}; color: {"#fff" if not oscuro else "#0D2235"};
  font-weight: 900; font-size: 34px; padding: 14px 34px; border-radius: 22px; line-height: 1.2; max-width: 900px; }}
.curso small {{ font-weight: 700; font-size: 26px; }}
.wa {{ margin-top: 22px; display: inline-flex; align-items: center;
  gap: 16px; background: #fff; border-radius: 999px; padding: 14px 34px; border: 4px solid {P};
  box-shadow: 0 12px 34px rgba(0,0,0,.12); white-space: nowrap; }}
.wa b {{ font-weight: 900; font-size: 50px; color: {P if not oscuro else "#0D2235"}; letter-spacing: 1px; }}
.wa span {{ font-family: "Space Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 2px; color: #4C4C4C; text-transform: uppercase; }}
</style></head><body>
<div class="circulo" style="width:520px;height:520px;left:-200px;top:820px"></div>
<div class="circulo" style="width:380px;height:380px;right:-140px;top:260px"></div>
<svg class="ilu" width="1080" height="640" viewBox="0 0 1080 640" aria-hidden="true">{h["ilu"](P, D, L)}</svg>
<div class="logo"><img src="../assets/logo-alacon-novantis.png" alt="Alacon Formación × Novantis Formación"></div>
<div class="bloque"><div class="kicker"><span class="chip">{icono}<span>{h["kicker"]}</span></span></div>
<div class="titular">{h["titular"]}</div>
<div class="nota">{h["nota"]}</div>
<div class="curso"><span>{h["curso"]}</span></div>
<div class="wa">{WA}<span>Pide info</span><b>611 12 62 64</b></div></div>
</body></html>
'''

if __name__ == "__main__":
    carpeta = os.path.join(os.path.dirname(__file__), "..", "disenos", "semana-2026-11-02")
    os.makedirs(carpeta, exist_ok=True)
    for h in HISTORIAS:
        ruta = os.path.join(carpeta, f'{h["fecha"]}-{h["tema"]}.html')
        open(ruta, "w").write(construir(h))
        print(ruta)
