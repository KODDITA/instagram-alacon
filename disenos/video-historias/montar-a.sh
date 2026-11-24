#!/bin/zsh
# Formato A: clip (con sonido ambiente) + capa + música. Uso: montar-a.sh carpeta salida.mp4 inicio fin velocidad musica.mp3
set -e
d=$1; out=$2; t0=$3; t1=$4; lento=${5:-1}; mus=${6:-../musica/ligera-diaria.mp3}
V="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p,setsar=1"
dur=$(python3 -c "print(round(($t1-$t0)*$lento,2))")
fo=$(python3 -c "print(round($dur-0.8,2))")
tempo=$(python3 -c "print(round(1/$lento,4))")
cd $d
ffmpeg -loglevel error -y -i clip.mp4 -loop 1 -t $dur -i capa.png -i $mus -filter_complex "[0:v]trim=$t0:$t1,setpts=${lento}*(PTS-STARTPTS),${V}[v];[1:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1[t];[v][t]overlay=shortest=1,trim=0:${dur},format=yuv420p[o];[0:a]atrim=$t0:$t1,asetpts=PTS-STARTPTS,atempo=${tempo},volume=0.5[amb];[2:a]atrim=0:${dur},asetpts=PTS-STARTPTS,volume=0.9[mus];[amb][mus]amix=inputs=2:duration=longest:normalize=0,atrim=0:${dur},afade=out:st=${fo}:d=0.8,loudnorm=I=-16:TP=-1.5:LRA=11[m]" -map "[o]" -map "[m]" -c:v libx264 -crf 20 -preset slow -r 30 -c:a aac -b:a 160k -ar 48000 -movflags +faststart $out
echo "$out $(ffprobe -v error -show_entries format=duration -of csv=p=0 $out)s"
