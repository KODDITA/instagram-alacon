#!/usr/bin/env python3
"""Genera la capa transparente (HTML) de una historia en vídeo. Uso: capa.py salida.html JSON"""
import sys, json
WA = '<svg width="46" height="46" viewBox="0 0 32 32" aria-hidden="true"><path fill="#25D366" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3z"/><path fill="#fff" d="M22.6 18.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8 0 1.6 1.2 3.2 1.4 3.4.2.2 2.4 3.6 5.8 5 2.8 1.1 3.4.9 4 .8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'
c = json.loads(sys.argv[2])
partes = []
if c.get("pre"): partes.append(f'<div class="pre" style="{c.get("pre_estilo","")}">{c["pre"]}</div>')
for l in c.get("lineas", []): partes.append(f'<div class="linea" style="font-size:{c.get("tam",58)}px">{l}</div>')
if c.get("sub"): partes.append(f'<div class="sub">{c["sub"]}</div>')
if c.get("curso"): partes.append(f'<div class="curso">{c["curso"]}</div>')
sticker = f'<div class="sticker" style="top:{c.get("y_wa",1565)}px">{WA}<span>Pide info</span><b>611 12 62 64</b></div>' if c.get("wa", True) else ""
html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=block" rel="stylesheet"><link rel="stylesheet" href="../capa.css"></head><body>
<div class="logo"><img src="../logo-alacon-novantis.png" alt="Alacon Formación × Novantis Formación"></div>
<div class="bloque" style="top:{c.get("y",1150)}px">{"".join(partes)}</div>{sticker}</body></html>'''
open(sys.argv[1], "w").write(html)
