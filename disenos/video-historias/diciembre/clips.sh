#!/bin/zsh
# Uso: clips.sh salida.jpg "destino url" ... → descarga los clips y hace una tira por clip (7 fotogramas) apilada
out=$1; shift; tiras=()
for par in "$@"; do dst=${par%% *}; u=${par#* }; curl -s -o "$dst" "$u"; t="${dst%.mp4}-tira.jpg"; ffmpeg -loglevel error -y -i "$dst" -vf "fps=1.15,scale=210:-1,tile=7x1" -frames:v 1 "$t"; tiras+=$t; done
args=(); i=0; f=""; for t in $tiras; do args+=(-i "$t"); f="${f}[${i}]"; i=$((i+1)); done
ffmpeg -loglevel error -y $args -filter_complex "${f}vstack=$i" "$out" && echo "$out"
