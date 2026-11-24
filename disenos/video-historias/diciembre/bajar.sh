#!/bin/zsh
# Uso: bajar.sh ext "clave url" "clave url" ...  → descarga y crea hoja de contacto hoja-<primera clave>.jpg
ext=$1; shift
claves=()
for par in "$@"; do k=${par%% *}; u=${par#* }; curl -s -o "$k.$ext" "$u"; claves+=$k; done
if [ "$ext" = png ]; then
  args=(); f=""; i=0
  for k in $claves; do args+=(-i "$k.png"); f="${f}[${i}]scale=240:-1[v${i}];"; i=$((i+1)); done
  inputs=""; for j in $(seq 0 $((i-1))); do inputs="${inputs}[v${j}]"; done
  ffmpeg -loglevel error -y $args -filter_complex "${f}${inputs}hstack=$i" "hoja-${claves[1]}.jpg" && echo "hoja-${claves[1]}.jpg"
fi
