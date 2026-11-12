#!/usr/bin/env python3
"""Genera post2.html (1080x1350) e historia2.html (1080x1920) de la convocatoria de Málaga."""
import math

PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="#5FB8EC" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.2 4.2L19 7"/></svg>'
WA = '<svg viewBox="0 0 24 24" fill="#25D366" style="width:{s}px;height:{s}px"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
STAR = '<svg class="chispa" viewBox="0 0 24 24" style="{pos}"><path d="M12 0c.9 6.4 4.6 10.6 12 12-7.4 1.4-11.1 5.6-12 12-.9-6.4-4.6-10.6-12-12 7.4-1.4 11.1-5.6 12-12z" fill="{c}"/></svg>'
ICONS = [
    '<path d="M12 20s-6.5-4.1-6.5-9A3.6 3.6 0 0 1 12 8.6 3.6 3.6 0 0 1 18.5 11c0 4.9-6.5 9-6.5 9z"/><path d="M2.5 14.5h3l2 2.5M21.5 14.5h-3l-2 2.5"/>',
    '<path d="M3 7.5a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2V17a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M8 13h8M8 16h5"/>',
    '<path d="M3 11 12 4l9 7"/><path d="M5.5 9.5V20h13V9.5"/><circle cx="12" cy="13.5" r="2"/><path d="M12 15.5V18"/>',
]
CURSOS = [("SSCS0208", "Atención sociosanitaria a personas dependientes"),
          ("ADG305_1", "Operaciones auxiliares administrativas"),
          ("COMT0111", "Gestión comercial inmobiliaria")]


def rayos(r, n=28):
    out = []
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 0.42) / n
        out.append(f'<path d="M{r} {r} L{r + r * math.cos(a0):.1f} {r + r * math.sin(a0):.1f} L{r + r * math.cos(a1):.1f} {r + r * math.sin(a1):.1f}Z"/>')
    return (f'<svg width="{2 * r}" height="{2 * r}" viewBox="0 0 {2 * r} {2 * r}"><defs><radialGradient id="g"><stop offset="0" stop-color="#5FB8EC" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="#5FB8EC" stop-opacity="0"/></radialGradient></defs><g fill="url(#g)">{"".join(out)}</g></svg>')


def pagina(L):
    cursos = "".join(
        f'<div class="curso" style="padding:{L["cp"]}px 24px"><div class="ico" style="width:{L["ico"]}px;height:{L["ico"]}px">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:{L["ico"] * .6:.0f}px;height:{L["ico"] * .6:.0f}px">{ICONS[i]}</svg></div>'
        f'<div><div class="cod" style="font-size:{L["cod"]}px">{c}</div><div class="nom" style="font-size:{L["nom"]}px">{n}</div></div></div>'
        for i, (c, n) in enumerate(CURSOS))
    stars = (STAR.format(pos="left:-40px;top:-46px;width:70px;height:70px", c="#fff")
             + STAR.format(pos="right:-34px;bottom:-30px;width:54px;height:54px", c="#5FB8EC"))
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Space+Mono:wght@700&display=block" rel="stylesheet">
<link rel="stylesheet" href="explosivo.css">
<style>html,body{{height:{L["H"]}px}}
.foto{{height:{L["foto"]}px;object-position:50% 50%}}
.velo{{background:linear-gradient(180deg,rgba(0,38,61,.55) 0px,rgba(0,58,92,.62) {L["foto"] * .35:.0f}px,rgba(0,58,92,.93) {L["foto"] * .72:.0f}px,#003A5C {L["foto"]}px)}}
</style></head><body>
<img class="foto" src="assets/foto2.png" alt="">
<div class="velo"></div>
<div class="rayos" style="top:{L["rayos"]}px">{rayos(L["rr"])}</div>
<div class="logo" style="{L["logo"]}"><img src="assets/logo-alacon-novantis.png" alt="Alacon Formación × Novantis Formación"></div>
<div class="lugar" style="{L["lugar"]}">{PIN}Málaga · Presencial</div>
<div class="hero" style="top:{L["hero"]}px">
  <div class="l1" data-fit="{L["w1"]}">Convocatoria</div>
  <div class="banda">{stars}<span class="l2" data-fit="{L["w2"]}">¡Abierta!</span></div>
</div>
<div class="sub" style="position:absolute;left:0;right:0;top:{L["sub"]}px;font-size:{L["subf"]}px">En estos 3 cursos</div>
<div class="cursos" style="top:{L["cur"]}px;gap:{L["gap"]}px">{cursos}</div>
<div class="pie" style="top:{L["pie"]}px">
  <div class="ok" style="font-size:{L["okf"]}px"><span>{CHECK}Centro oficial presencial</span><span>{CHECK}Prácticas en empresas</span></div>
  <div class="wa" style="font-size:{L["waf"]}px">{WA.format(s=L["waf"] + 8)}611 12 62 64</div>
</div>
<script>
document.fonts.ready.then(()=>{{for(const e of document.querySelectorAll('[data-fit]')){{let s=40;e.style.fontSize=s+'px';
const w=+e.dataset.fit;const r=w/e.getBoundingClientRect().width;e.style.fontSize=(s*r)+'px';
const r2=w/e.getBoundingClientRect().width;e.style.fontSize=(s*r*r2)+'px';}}}});
</script>
</body></html>'''


POST = dict(H=1350, foto=760, rayos=60, rr=480, logo="top:40px;left:48px;width:250px", lugar="top:52px;right:48px",
            hero=250, w1=960, w2=820, sub=700, subf=28, cur=752, gap=16, cp=18, ico=62, cod=19, nom=31,
            pie=1148, okf=28, waf=32)
HIST = dict(H=1920, foto=1080, rayos=330, rr=560, logo="top:190px;left:50%;transform:translateX(-50%);width:400px;padding:16px 24px",
            lugar="top:350px;left:50%;transform:translateX(-50%)",
            hero=500, w1=960, w2=880, sub=972, subf=32, cur=1028, gap=16, cp=20, ico=68, cod=21, nom=31,
            pie=1452, okf=30, waf=36)
open("post2.html", "w").write(pagina(POST))
open("historia2.html", "w").write(pagina(HIST))
print("ok")
