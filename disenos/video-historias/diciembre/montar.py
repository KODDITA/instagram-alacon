#!/usr/bin/env python3
"""Monta la historia de un día de diciembre. Uso: montar.py DD [t0 t1 lento] (A) o montar.py DD [fin1 fin2 fin3] (C)."""
import json, subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = sys.argv[1]; c = json.load(open('spec.json'))[d]
V = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p,setsar=1"
mus = f"../musica/{c['mus']}.mp3"; out = f"d{d}/historia-{d}-dic.mp4"
enc = ['-c:v','libx264','-crf','20','-preset','slow','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart']
if c['f'] == 'A':
    t0, t1, lento = (float(x) for x in (sys.argv[2:5] if len(sys.argv) > 4 else (0, 6, 1)))
    dur = round((t1 - t0) * lento, 3); fo = round(dur - 0.8, 3); tempo = round(1 / lento, 4)
    f = (f"[0:v]trim={t0}:{t1},setpts={lento}*(PTS-STARTPTS),{V}[v];[1:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1[t];"
         f"[v][t]overlay=shortest=1,trim=0:{dur},format=yuv420p[o];"
         f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,atempo={tempo},volume=0.45[amb];[2:a]atrim=0:{dur},asetpts=PTS-STARTPTS,volume=0.9[m0];"
         f"[amb][m0]amix=inputs=2:duration=longest:normalize=0,atrim=0:{dur},afade=out:st={fo}:d=0.8,loudnorm=I=-16:TP=-1.5:LRA=11[m]")
    cmd = ['ffmpeg','-loglevel','error','-y','-i',f'd{d}/clip.mp4','-loop','1','-t',str(dur),'-i',f'd{d}/capa1.png','-i',mus,'-filter_complex',f,'-map','[o]','-map','[m]',*enc,out]
else:
    fins = [float(x) for x in sys.argv[2:5]] if len(sys.argv) > 4 else [5, 5, 5]
    # cada clip se estira a 5 s si se recorta antes
    seg = []
    for i, fin in enumerate(fins):
        lento = round(5 / fin, 4)
        seg.append(f"[{i}:v]trim=0:{fin},setpts={lento}*(PTS-STARTPTS),{V},trim=0:5[s{i}]")
    f = (";".join(seg) + ";[s0][s1]xfade=transition=fade:duration=0.5:offset=4.5[ab];[ab][s2]xfade=transition=fade:duration=0.5:offset=9[v];"
         "[3:v]format=rgba,fade=in:st=0.4:d=0.5:alpha=1,fade=out:st=4.3:d=0.4:alpha=1[t1];"
         "[4:v]format=rgba,fade=in:st=4.7:d=0.5:alpha=1,fade=out:st=8.8:d=0.4:alpha=1[t2];"
         "[5:v]format=rgba,fade=in:st=9.2:d=0.5:alpha=1[t3];"
         "[v][t1]overlay=shortest=1[v1];[v1][t2]overlay=shortest=1[v2];[v2][t3]overlay=shortest=1,trim=0:14,format=yuv420p[o];"
         "[6:a]atrim=0:14,asetpts=PTS-STARTPTS,afade=in:st=0:d=0.6,afade=out:st=12.6:d=1.4,loudnorm=I=-16:TP=-1.5:LRA=11[m]")
    ins = []
    for i in (1, 2, 3): ins += ['-i', f'd{d}/clip{i}.mp4']
    for i in (1, 2, 3): ins += ['-loop', '1', '-t', '14', '-i', f'd{d}/capa{i}.png']
    cmd = ['ffmpeg','-loglevel','error','-y',*ins,'-i',mus,'-filter_complex',f,'-map','[o]','-map','[m]',*enc,out]
subprocess.run(cmd, check=True)
dur = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip()
print(out, dur)
