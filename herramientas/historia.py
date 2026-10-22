#!/usr/bin/env python3
"""Genera el HTML de una historia a partir de unos pocos campos (misma plantilla para todas)."""
import sys, json, html
WA = '<svg width="44" height="44" viewBox="0 0 32 32" aria-hidden="true"><path fill="#25D366" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3z"/><path fill="#fff" d="M22.6 18.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8 0 1.6 1.2 3.2 1.4 3.4.2.2 2.4 3.6 5.8 5 2.8 1.1 3.4.9 4 .8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'
PELIGRO = '<svg width="40" height="40" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 1 21h22L12 2z" fill="#D7362B"/><rect x="11" y="9" width="2" height="6" rx="1" fill="#fff"/><circle cx="12" cy="17.5" r="1.2" fill="#fff"/></svg>'

def construir(c):
    icono = PELIGRO if c.get("peligro") else ""
    color = ' style="color:#B02A21"' if c.get("peligro") else ""
    kicker = ""
    if c.get("kicker") or icono:
        texto = f'<span{color}>{c["kicker"]}</span>' if c.get("kicker") else ""
        pad = "" if c.get("kicker") else ' style="padding:18px"'
        kicker = f'<div class="kicker" style="top:{c["y_kicker"]}px"><span class="chip etiqueta"{pad}>{icono}{texto}</span></div>'
    grande = f'<div class="grande" style="top:{c["y_grande"]}px">{c["grande"]}</div>' if c.get("grande") else ""
    nota = f'<div class="nota" style="top:{c["y_nota"]}px;{c.get("estilo_nota","")}">{c["nota"]}</div>' if c.get("nota") else ""
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Space+Mono:wght@700&display=block" rel="stylesheet">
<link rel="stylesheet" href="estilo-historia.css">
<style>:root{{--subir:{c.get("subir",110)}px}} .velo{{height:{c.get("velo",900)}px;{c.get("velo_extra","")}}}
.titular{{top:{c["y_titular"]}px;font-size:{c.get("tam",88)}px}}
.grande{{position:absolute;left:0;right:0;text-align:center;font-weight:900;font-size:{c.get("tam_grande",200)}px;line-height:1;color:var(--brand);letter-spacing:-4px}}</style></head><body>
<img class="fondo" src="fondos/{c["fondo"]}" alt=""><div class="velo"></div>
<div class="logo"><img src="assets/logo-alacon-novantis.png" alt="Alacon Formación × Novantis Formación"></div>
{kicker}
{grande}
<div class="titular">{c["titular"]}</div>
{nota}
<div class="wa-chip" style="top:{c.get("y_cta",1470)}px">{WA}<span>{c.get("cta","Pide info")}</span><b>611 12 62 64</b></div>
</body></html>
'''

if __name__ == "__main__":
    c = json.load(open(sys.argv[1]))
    open(sys.argv[2], "w").write(construir(c))
