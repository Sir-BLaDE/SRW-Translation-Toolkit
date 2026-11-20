"""prologue_meta_compare.py - compara la cola de metadatos de slots EN vs JP.

Si los metadatos coinciden (o casi), no dependen del texto y es seguro
reutilizar el espacio de padding de cada slot.
"""
import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full.json', encoding='utf-8'))
raw = {}
for lang in ['EN','JP']:
    p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/%s/Prologue.cpk' % lang
    c = load(p)
    raw[lang] = {}
    for r in c.rows:
        pt = c.plain(r)
        cnt = struct.unpack_from('<H', pt, 0)[0]
        if not cnt or len(pt) < 24 or (len(pt)-24) % cnt: continue
        slot = (len(pt)-24)//cnt
        raw[lang][r['id']] = (cnt, slot, pt)

# para cada fila EN, comparar la cola de metadatos (en bytes absolutos desde el final del slot)
for rid in sorted(d.keys(), key=int):
    if rid not in raw['EN'] or rid not in raw['JP']: continue
    ec, es, ep = raw['EN'][rid]
    jc, js, jp = raw['JP'][rid]
    if ec != jc: 
        print('fila %-3s count difiere EN=%d JP=%d' % (rid, ec, jc)); continue
    same = 0; diff = 0
    for si in range(min(ec, 12)):
        eb = ep[24+si*es : 24+(si+1)*es]
        jb = jp[24+si*js : 24+(si+1)*js]
        # comparar ultimos 22 bytes
        if eb[-22:] == jb[-22:]: same += 1
        else: diff += 1
    print('fila %-3s ENslot=%-4d JPslot=%-4d cola igual=%d distinta=%d' % (rid, es, js, same, diff))
