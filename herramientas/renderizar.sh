#!/bin/zsh
# Convierte un diseño HTML (1080×1920) en JPEG listo para Instagram.
# Uso: herramientas/renderizar.sh disenos/historia.html contenido/2026-10-26/historia-alacon.jpg
set -e
entrada="$1"; salida="$2"
[ -z "$entrada" ] || [ -z "$salida" ] && { echo "Uso: $0 entrada.html salida.jpg"; exit 1; }
CHROME="${CHROME:-$(find ~/.cache/hyperframes/chrome -name chrome-headless-shell -type f -perm +111 | head -1)}"
tmp="$(mktemp -d)"
"$CHROME" --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --virtual-time-budget=8000 --window-size=1080,1920 \
  --screenshot="$tmp/captura.png" \
  "file://$(cd "$(dirname "$entrada")" && pwd)/$(basename "$entrada")" >/dev/null 2>&1
mkdir -p "$(dirname "$salida")"
sips -s format jpeg -s formatOptions 92 "$tmp/captura.png" --out "$salida" >/dev/null
rm -rf "$tmp"
echo "Listo: $salida"
