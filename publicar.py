#!/usr/bin/env python3
"""Publica en Instagram lo que toca hoy.

Lee contenido/AAAA-MM-DD/plan.json y publica sus historias y posts en las
cuentas indicadas, con la API oficial de Instagram (Graph API).

Uso:
    python publicar.py                      # publica lo de hoy
    python publicar.py --fecha 2026-10-26   # publica lo de otro día
    python publicar.py --prueba             # enseña qué haría, sin publicar
    python publicar.py --desde-hora 9       # no publica antes de las 9:00 (Madrid)

Las claves salen de variables de entorno (en GitHub, de los Secrets) o, en el
Mac, del archivo .env. Nunca se escriben en pantalla.
"""

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parent
CONTENIDO = RAIZ / "contenido"
API = "https://graph.facebook.com"
ZONA = ZoneInfo("Europe/Madrid")

# Dirección pública donde GitHub Pages sirve las imágenes y vídeos.
URL_PUBLICA = os.environ.get("URL_PUBLICA", "https://koddita.github.io/instagram-alacon")

# Una entrada por cuenta. El identificador de Instagram no es secreto; el token sí.
CUENTAS = {
    "alacon": {"ig_id": "17841450053831841", "token_env": "META_TOKEN_ALACON"},
    # "novantis": {"ig_id": "...", "token_env": "META_TOKEN_NOVANTIS"},
}

VIDEO = {".mp4", ".mov"}


def cargar_env():
    archivo = RAIZ / ".env"
    if not archivo.exists():
        return
    for linea in archivo.read_text().splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            clave, valor = linea.split("=", 1)
            os.environ.setdefault(clave.strip(), valor.strip())


class ErrorAPI(Exception):
    pass


def llamar(metodo, ruta, token, **params):
    params["access_token"] = token
    datos = urllib.parse.urlencode(params).encode()
    if metodo == "GET":
        peticion = urllib.request.Request(f"{API}/{ruta}?{datos.decode()}")
    else:
        peticion = urllib.request.Request(f"{API}/{ruta}", data=datos, method="POST")
    try:
        with urllib.request.urlopen(peticion, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            error = json.load(e).get("error", {})
        except Exception:
            error = {"message": str(e)}
        raise ErrorAPI(error.get("error_user_msg") or error.get("message") or str(error)) from None


def esperar_listo(contenedor, token, tope=300):
    """Instagram procesa los vídeos antes de dejar publicarlos."""
    inicio = time.time()
    while True:
        estado = llamar("GET", contenedor, token, fields="status_code,status").get("status_code")
        if estado in (None, "FINISHED"):
            return
        if estado in ("ERROR", "EXPIRED"):
            raise ErrorAPI(f"Instagram no pudo procesar el archivo (estado {estado})")
        if time.time() - inicio > tope:
            raise ErrorAPI("Instagram tarda demasiado en procesar el archivo")
        time.sleep(5)


def media(ig_id, token, fecha, archivo, **extra):
    url = f"{URL_PUBLICA}/contenido/{fecha}/{archivo}"
    clave = "video_url" if Path(archivo).suffix.lower() in VIDEO else "image_url"
    contenedor = llamar("POST", f"{ig_id}/media", token, **{clave: url}, **extra)["id"]
    esperar_listo(contenedor, token)
    return contenedor


def publicar_contenedor(ig_id, token, contenedor):
    return llamar("POST", f"{ig_id}/media_publish", token, creation_id=contenedor)["id"]


def publicar_historia(ig_id, token, fecha, item):
    return publicar_contenedor(ig_id, token, media(ig_id, token, fecha, item["archivo"], media_type="STORIES"))


def publicar_post(ig_id, token, fecha, item):
    archivos, texto = item["archivos"], item.get("texto", "")
    if len(archivos) > 1:
        hijos = []
        for a in archivos:
            extra = {"is_carousel_item": "true"}
            if Path(a).suffix.lower() in VIDEO:
                extra["media_type"] = "VIDEO"
            hijos.append(media(ig_id, token, fecha, a, **extra))
        contenedor = llamar("POST", f"{ig_id}/media", token, media_type="CAROUSEL",
                            children=",".join(hijos), caption=texto)["id"]
        esperar_listo(contenedor, token)
    elif Path(archivos[0]).suffix.lower() in VIDEO:
        contenedor = media(ig_id, token, fecha, archivos[0], media_type="REELS",
                           caption=texto, share_to_feed="true")
    else:
        contenedor = media(ig_id, token, fecha, archivos[0], caption=texto)
    return publicar_contenedor(ig_id, token, contenedor)


def tareas(plan):
    """Convierte el plan del día en una lista de (clave, tipo, cuenta, item)."""
    lista = []
    for i, h in enumerate(plan.get("historias", [])):
        lista.append((f"{h['cuenta']}:historia:{i}", "historia", h["cuenta"], h))
    for i, p in enumerate(plan.get("posts", [])):
        for cuenta in p["cuentas"]:
            lista.append((f"{cuenta}:post:{i}", "post", cuenta, p))
    return lista


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fecha")
    parser.add_argument("--prueba", action="store_true")
    parser.add_argument("--desde-hora", type=int)
    parser.add_argument("--solo", help="publicar solo esta cuenta (p. ej. alacon)")
    args = parser.parse_args()

    cargar_env()
    ahora = dt.datetime.now(ZONA)
    fecha = args.fecha or ahora.date().isoformat()

    if args.desde_hora is not None and not args.fecha and ahora.hour < args.desde_hora:
        print(f"Son las {ahora:%H:%M} en Madrid; se publica a partir de las {args.desde_hora}:00.")
        return 0

    carpeta = CONTENIDO / fecha
    archivo_plan = carpeta / "plan.json"
    if not archivo_plan.exists():
        print(f"No hay nada programado para el {fecha}.")
        return 0

    plan = json.loads(archivo_plan.read_text())
    registro_ruta = carpeta / "publicado.json"
    registro = json.loads(registro_ruta.read_text()) if registro_ruta.exists() else {}

    fallos = 0
    for clave, tipo, cuenta, item in tareas(plan):
        if args.solo and cuenta != args.solo:
            continue
        if clave in registro:
            print(f"✓ {clave}: ya publicado antes")
            continue
        datos = CUENTAS.get(cuenta)
        token = os.environ.get(datos["token_env"], "") if datos else ""
        if not datos or not token:
            print(f"✗ {clave}: falta la cuenta o su token; se salta")
            fallos += 1
            continue
        nombres = item.get("archivo") or ", ".join(item["archivos"])
        for nombre in ([item["archivo"]] if "archivo" in item else item["archivos"]):
            if not (carpeta / nombre).exists():
                print(f"✗ {clave}: no encuentro {nombre}")
                fallos += 1
                break
        else:
            if args.prueba:
                print(f"· {clave}: publicaría {nombres}")
                continue
            try:
                funcion = publicar_historia if tipo == "historia" else publicar_post
                media_id = funcion(datos["ig_id"], token, fecha, item)
                registro[clave] = {"id": media_id, "hora": dt.datetime.now(ZONA).isoformat(timespec="seconds")}
                registro_ruta.write_text(json.dumps(registro, indent=2, ensure_ascii=False) + "\n")
                print(f"✓ {clave}: publicado ({nombres})")
            except ErrorAPI as e:
                print(f"✗ {clave}: {e}")
                fallos += 1

    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
