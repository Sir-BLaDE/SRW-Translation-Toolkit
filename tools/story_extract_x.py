"""story_extract_x.py - Descifra STGEST002_EN.CPK (SRW X) a stg/NNNN.bin y vuelca
los dialogos a datos/story_dialogues.jsonl con el campo pid (genero del heroe:
pid_XMHERO* = masculino, pid_XFHERO* = femenino).
Uso (desde la carpeta de trabajo, con SRW_GAME=X y SRW_EXE definidos):
    python3 story_extract_x.py orig/Data/STAGE/STGEST002_EN.CPK
"""
import json, os, re, sys
from cpk_util import load
from story import find_dialogs, translatable

PID = re.compile(rb'(pid_[A-Za-z0-9_]+)\s*,\s*$')
src = sys.argv[1]
os.makedirs('stg', exist_ok=True); os.makedirs('datos', exist_ok=True)
c = load(src)
with open('datos/story_dialogues.jsonl', 'w', encoding='utf-8') as out:
    for r in c.rows:
        pt = c.plain(r)
        assert len(pt) == r['ex'], r['id']
        open('stg/%04d.bin' % r['id'], 'wb').write(pt)
        for d in find_dialogs(r['id'], pt):
            m = PID.search(pt[max(0, d.start - 120):d.start - 2].rstrip())
            out.write(json.dumps({'entry': r['id'], 'start': d.start, 'end': d.end,
                                  'speaker': d.speaker, 'pid': m.group(1).decode() if m else '',
                                  'text': translatable(d)}, ensure_ascii=False) + '\n')
print('ok', len(c.rows), 'entradas')
