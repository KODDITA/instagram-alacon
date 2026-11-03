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
    "indigo":   ("#3949AB", "#283593", "#D9DDF5", "#E6E9F8", "#F6F7FD", "#B5BEEE"),
    "petroleo": ("#1F6F8B", "#154E63", "#D2E7EF", "#DFEEF3", "#F4FAFC", "#A6CFDD"),
    "ciruela":  ("#8E3B78", "#662955", "#F1DDEB", "#F5E7F1", "#FCF7FA", "#E2B9D6"),
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

def ficha(P, D, etiqueta, dentro):
    """Marco tipo placa (el estilo de la radiografía) con una etiqueta arriba a la izquierda."""
    fondo = "#0A1A29" if D == "#FFFFFF" else D  # en la paleta oscura, la placa va más oscura que el fondo
    return f'''<rect x="250" y="10" width="580" height="620" rx="36" fill="{fondo}"/>
<rect x="250" y="10" width="580" height="620" rx="36" fill="none" stroke="{P}" stroke-width="12"/>
{dentro}
<text x="290" y="70" font-family="Space Mono" font-weight="700" font-size="34" fill="#fff" opacity=".8">{etiqueta}</text>'''

def ilu_avion_ola(P, D, L):
    return ficha(P, D, "800 km/h", f'''
<g transform="translate(540 220) rotate(-8)" fill="#fff">
  <path d="M-190 0 Q-190 -22 -160 -22 L150 -22 Q200 -22 210 0 Q200 22 150 22 L-160 22 Q-190 22 -190 0 Z"/>
  <path d="M-20 -18 L-90 -120 L-50 -120 L60 -18 Z"/><path d="M-20 18 L-90 120 L-50 120 L60 18 Z"/>
  <path d="M-170 -10 L-200 -70 L-175 -70 L-130 -10 Z"/>
</g>
<path d="M300 520 Q 360 380 470 380 Q 560 380 560 450 Q 510 420 480 455 Q 455 490 500 520 Z" fill="{L}"/>
<path d="M280 560 Q 340 535 400 560 T 520 560 T 640 560 T 760 560 T 800 560" fill="none" stroke="{L}" stroke-width="12" stroke-linecap="round" opacity=".6"/>
<path d="M600 470 h150 M640 510 h110 M600 430 h90" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".7"/>''')

def ilu_musica(P, D, L):
    return ficha(P, D, "MEMORIA", f'''
<circle cx="520" cy="350" r="200" fill="#111"/>
<circle cx="520" cy="350" r="170" fill="none" stroke="#333" stroke-width="4"/>
<circle cx="520" cy="350" r="140" fill="none" stroke="#333" stroke-width="4"/>
<circle cx="520" cy="350" r="110" fill="none" stroke="#333" stroke-width="4"/>
<path d="M420 240 A150 150 0 0 1 560 205" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".35"/>
<circle cx="520" cy="350" r="62" fill="{L}"/><circle cx="520" cy="350" r="10" fill="#111"/>
<g fill="#fff"><ellipse cx="720" cy="230" rx="30" ry="22" transform="rotate(-20 720 230)"/><rect x="742" y="110" width="12" height="122"/>
<path d="M742 110 L790 130 L790 160 L754 145 Z"/>
<ellipse cx="760" cy="430" rx="24" ry="18" transform="rotate(-20 760 430)"/><rect x="777" y="330" width="10" height="102"/></g>''')

def ilu_gato(P, D, L):
    return ficha(P, D, "GEN TAS1R2", f'''
<path d="M330 260 L360 120 L440 210 Z" fill="#fff"/><path d="M640 210 L720 120 L750 260 Z" fill="#fff"/>
<ellipse cx="540" cy="330" rx="230" ry="190" fill="#fff"/>
<path d="M362 160 L415 210 L375 228 Z M718 160 L665 210 L705 228 Z" fill="#F4B6C2"/>
<ellipse cx="460" cy="310" rx="26" ry="36" fill="#0D2235"/><ellipse cx="620" cy="310" rx="26" ry="36" fill="#0D2235"/>
<path d="M525 380 L555 380 L540 400 Z" fill="{P}"/>
<path d="M540 400 Q 520 430 495 420 M540 400 Q 560 430 585 420" fill="none" stroke="#0D2235" stroke-width="6" stroke-linecap="round"/>
<path d="M440 385 L330 370 M440 400 L330 410 M640 385 L750 370 M640 400 L750 410" stroke="#9AA9B6" stroke-width="5" stroke-linecap="round"/>
<g transform="translate(700 540)"><path d="M-70 0 L-100 -25 L-100 25 Z M70 0 L100 -25 L100 25 Z" fill="{L}"/>
<ellipse cx="0" cy="0" rx="72" ry="44" fill="{P}"/><path d="M-40 -30 L-10 30 M0 -40 L30 40" stroke="#fff" stroke-width="10" opacity=".6"/></g>
<text x="700" y="470" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="64" fill="#fff">?</text>''')


def ilu_nariz(P, D, L):
    puntos = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{D}" opacity=".55"/>'
                     for x in range(380, 720, 34) for y in range(250, 470, 30)
                     if ((x-540)/170)**2 + ((y-350)/115)**2 < 1)
    return ficha(P, D, "HUELLA NASAL", f"""
<path d="M540 470 Q 360 470 350 340 Q 345 230 450 225 Q 500 222 540 260 Q 580 222 630 225 Q 735 230 730 340 Q 720 470 540 470 Z" fill="{L}"/>
{puntos}
<path d="M420 330 Q 440 290 480 300 Q 500 340 470 360 Q 430 370 420 330 Z" fill="{D}"/>
<path d="M660 330 Q 640 290 600 300 Q 580 340 610 360 Q 650 370 660 330 Z" fill="{D}"/>
<path d="M540 380 L540 470" stroke="{D}" stroke-width="10" stroke-linecap="round"/>
<text x="540" y="580" text-anchor="middle" font-family="Space Mono" font-weight="700" font-size="34" fill="#fff" opacity=".8">ID ÚNICO</text>""")

def ilu_altura(P, D, L):
    marcas = "".join(f'<line x1="300" y1="{y}" x2="{335 if y % 50 else 360}" y2="{y}" stroke="#fff" stroke-width="5" opacity=".7"/>' for y in range(110, 600, 25))
    def persona(x, y0, c):
        return f'<circle cx="{x}" cy="{y0+40}" r="38" fill="{c}"/><rect x="{x-55}" y="{y0+90}" width="110" height="200" rx="50" fill="{c}"/><rect x="{x-45}" y="{y0+270}" width="38" height="{560-y0-270}" rx="18" fill="{c}"/><rect x="{x+7}" y="{y0+270}" width="38" height="{560-y0-270}" rx="18" fill="{c}"/>'
    return ficha(P, D, "−1 CM", f"""
<rect x="290" y="100" width="80" height="500" fill="none"/>{marcas}
{persona(500, 140, "#fff")}{persona(680, 168, L)}
<line x1="440" y1="140" x2="740" y2="140" stroke="#fff" stroke-width="4" stroke-dasharray="10 10" opacity=".7"/>
<circle cx="500" cy="105" r="0"/>
<g transform="translate(500 600)"><circle r="0"/></g>
<text x="500" y="615" text-anchor="middle" font-family="Space Mono" font-weight="700" font-size="30" fill="#fff">8:00</text>
<text x="680" y="615" text-anchor="middle" font-family="Space Mono" font-weight="700" font-size="30" fill="{L}">22:00</text>""")

def ilu_aire(P, D, L):
    return ficha(P, D, "1902", f"""
<rect x="330" y="130" width="420" height="150" rx="24" fill="#fff"/>
<rect x="360" y="230" width="360" height="22" rx="11" fill="{L}"/>
<path d="M370 170 h200" stroke="{L}" stroke-width="12" stroke-linecap="round"/>
<circle cx="690" cy="180" r="14" fill="{P}"/>
<path d="M400 300 q 20 40 0 80 M540 300 q 20 40 0 80 M680 300 q 20 40 0 80" fill="none" stroke="{L}" stroke-width="10" stroke-linecap="round"/>
<g transform="translate(400 420) rotate(-10)"><rect width="150" height="190" rx="8" fill="#fff"/><path d="M25 40 h100 M25 75 h100 M25 110 h70" stroke="{L}" stroke-width="10" stroke-linecap="round"/></g>
<g transform="translate(560 430) rotate(8)"><rect width="150" height="180" rx="8" fill="#fff"/><path d="M25 40 h100 M25 75 h100 M25 110 h70" stroke="{L}" stroke-width="10" stroke-linecap="round"/></g>""")

def ilu_pulmones(P, D, L):
    return ficha(P, D, "MENORES DE 5", f"""
<rect x="525" y="110" width="30" height="170" rx="15" fill="#fff"/>
<path d="M540 270 Q 500 300 470 300 M540 270 Q 580 300 610 300" stroke="#fff" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M500 230 Q 370 220 340 380 Q 320 560 460 570 Q 505 570 505 520 L505 290 Q 505 240 500 230 Z" fill="{L}"/>
<path d="M580 230 Q 710 220 740 380 Q 760 560 620 570 Q 575 570 575 520 L575 290 Q 575 240 580 230 Z" fill="{L}"/>
<path d="M470 300 Q 430 360 430 440 M470 330 Q 420 400 390 460 M610 300 Q 650 360 650 440 M610 330 Q 660 400 690 460" stroke="{D}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".6"/>""")

def ilu_ascensor(P, D, L):
    botones = ""
    for i, n in enumerate(["15", "14", "12", "11"]):
        y = 140 + i * 115
        botones += f'<circle cx="540" cy="{y}" r="44" fill="#fff"/><text x="540" y="{y+16}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="44" fill="#0D2235">{n}</text>'
    return ficha(P, D, "VIERNES 13", f"""
<rect x="430" y="80" width="220" height="510" rx="30" fill="{L}"/>
{botones}
<g transform="translate(720 300)"><circle r="56" fill="none" stroke="#D7362B" stroke-width="12"/><text y="20" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="54" fill="#fff">13</text><line x1="-40" y1="40" x2="40" y2="-40" stroke="#D7362B" stroke-width="12" stroke-linecap="round"/></g>""")

def ilu_insulina(P, D, L):
    return ficha(P, D, "14·11·1891", f"""
<circle cx="450" cy="340" r="160" fill="none" stroke="{L}" stroke-width="44"/>
<g transform="translate(650 200)">
<rect x="0" y="40" width="110" height="250" rx="22" fill="#fff"/>
<rect x="15" y="0" width="80" height="50" rx="12" fill="{L}"/>
<rect x="0" y="150" width="110" height="80" fill="{L}"/>
<text x="55" y="203" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="30" fill="{D}">INS</text></g>""")

def ilu_pata(P, D, L):
    gotas = "".join(f'<path d="M{x} {y} q -18 30 0 42 q 18 -12 0 -42 Z" fill="{L}"/>' for x, y in [(330, 160), (760, 230), (720, 470), (360, 470)])
    return ficha(P, D, "ALMOHADILLAS", f"""
<ellipse cx="540" cy="420" rx="140" ry="120" fill="#fff"/>
<ellipse cx="400" cy="270" rx="52" ry="68" fill="#fff" transform="rotate(-20 400 270)"/>
<ellipse cx="490" cy="200" rx="52" ry="70" fill="#fff"/>
<ellipse cx="590" cy="200" rx="52" ry="70" fill="#fff"/>
<ellipse cx="680" cy="270" rx="52" ry="68" fill="#fff" transform="rotate(20 680 270)"/>
{gotas}""")

HISTORIAS = [
    dict(fecha="2026-11-04", tema="tension", paleta="violeta", ilu=ilu_tension,
         kicker="Tensión arterial", titular='Cruzar las piernas te <span class="marca">sube la tensión</span>',
         nota="Mídela sentado y tras 5 minutos de reposo", curso="Curso de Auxiliar de Enfermería"),
    dict(fecha="2026-11-05", tema="tsunamis", paleta="oceano", ilu=ilu_avion_ola,
         kicker="Día Mundial de los Tsunamis", titular='Un tsunami viaja <span class="marca">tan rápido como un avión</span>',
         nota="En alta mar va a unos 800 km/h", curso="Formación en Emergencias Sanitarias"),
    dict(fecha="2026-11-06", tema="musica-alzheimer", paleta="salvia", ilu=ilu_musica, top=940,
         kicker="Alzhéimer", titular='Su música favorita <span class="marca">despierta recuerdos</span>',
         nota="La memoria musical resiste al alzhéimer",
         curso="Certificado SSCS0208<br><small>Atención sociosanitaria a personas dependientes en instituciones sociales</small>"),
    dict(fecha="2026-11-07", tema="gatos-dulce", paleta="noche", ilu=ilu_gato,
         kicker="Gatos", titular='Los gatos <span class="marca">no notan el sabor dulce</span>',
         nota="Les falta el receptor del dulce", curso="Curso de Auxiliar de Veterinaria"),
    dict(fecha="2026-11-08", tema="radiologia", paleta="marca", ilu=ilu_rayosx,
         kicker="Día Internacional de la Radiología", titular='La 1.ª radiografía: <span class="marca">una mano con anillo</span>',
         nota="Röntgen descubrió los rayos X el 8 de noviembre de 1895", curso="Curso de Auxiliar de Enfermería"),
]

SEMANA_2 = [
    dict(fecha="2026-11-09", tema="nariz-perro", paleta="indigo", ilu=ilu_nariz,
         kicker="Perros", titular='Su nariz es única, <span class="marca">como una huella</span>',
         nota="No hay dos perros con el mismo dibujo", curso="Curso de Auxiliar de Veterinaria"),
    dict(fecha="2026-11-10", tema="altura", paleta="violeta", ilu=ilu_altura,
         kicker="Cuerpo humano", titular='Por la noche mides <span class="marca">hasta 1 cm menos</span>',
         nota="Los discos de la columna se aplastan durante el día", curso="Curso de Auxiliar de Enfermería"),
    dict(fecha="2026-11-11", tema="aire-acondicionado", paleta="petroleo", ilu=ilu_aire,
         kicker="Aire acondicionado", titular='Se inventó <span class="marca">para una imprenta</span>',
         nota="Carrier lo creó en 1902 para cuidar el papel",
         curso="Curso de Técnico de Climatización y Mantenimiento"),
    dict(fecha="2026-11-12", tema="neumonia", paleta="salvia", ilu=ilu_pulmones,
         kicker="Día Mundial de la Neumonía", titular='La infección que <span class="marca">más niños mata</span>',
         nota="Es la neumonía, en menores de 5 años",
         curso="Curso de Auxiliar de Enfermería"),
    dict(fecha="2026-11-13", tema="planta-13", paleta="noche", ilu=ilu_ascensor,
         kicker="Viernes 13", titular='Muchos hoteles <span class="marca">no tienen planta 13</span>',
         nota="Del 12 se pasa directamente al 14", curso="Curso de Recepcionista de Hotel"),
    dict(fecha="2026-11-14", tema="diabetes", paleta="marca", ilu=ilu_insulina,
         kicker="Día Mundial de la Diabetes", titular='Hoy nació <span class="marca">el padre de la insulina</span>',
         nota="Frederick Banting nació un 14 de noviembre", curso="Curso de Auxiliar de Enfermería"),
    dict(fecha="2026-11-15", tema="patas-perro", paleta="ciruela", ilu=ilu_pata,
         kicker="Perros", titular='Los perros sudan <span class="marca">por las patas</span>',
         nota="Sus almohadillas tienen glándulas del sudor", curso="Curso de Auxiliar de Veterinaria"),
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
.bloque {{ position: absolute; top: {h.get("top", 975)}px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; }}
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
.curso small {{ font-weight: 700; font-size: 24px; }}
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
    base = os.path.join(os.path.dirname(__file__), "..", "disenos")
    for semana, lista in (("semana-2026-11-02", HISTORIAS), ("semana-2026-11-09", SEMANA_2)):
        carpeta = os.path.join(base, semana)
        os.makedirs(carpeta, exist_ok=True)
        for h in lista:
            ruta = os.path.join(carpeta, f'{h["fecha"]}-{h["tema"]}.html')
            open(ruta, "w").write(construir(h))
            print(ruta)
