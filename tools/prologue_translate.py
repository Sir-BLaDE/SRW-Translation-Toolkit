# -*- coding: utf-8 -*-
"""prologue_translate.py - traduccion del Prologue al espanol de Espana.

Estrategia: reemplazo in-place manteniendo el tamano exacto de cada cadena
(incluido su 0x00 terminador). Si la traduccion es mas corta se rellena con
0x00; si es mas larga se acorta. Asi no se rompen los offsets de los slots.
"""
import sys, struct, json, copy
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
BACKUP = r'C:/Dev/Default Project/srwv/backup/Prologue_EN_original.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk'
DATA = r'C:/Dev/Default Project/srwv/datos/prologue_full.json'
TRANS = r'C:/Dev/Default Project/srwv/datos/prologue_trans.json'

d = json.load(open(DATA, encoding='utf-8'))
T = json.load(open(TRANS, encoding='utf-8')) if __import__('os').path.exists(TRANS) else {}

# --- utilidades -------------------------------------------------------------
def split_slot(b, meta_start):
    """Devuelve (prefijo, [ (start,end,texto) ], sufijo) usando meta_start."""
    text = b[:meta_start]
    parts = []
    i = 0
    while i < len(text):
        j = text.find(b'\x00', i)
        if j < 0: break
        if j > i:
            parts.append((i, j, text[i:j].decode('utf-8','ignore')))
        i = j + 1
    return parts

def esc(s):
    return s.encode('utf-8')

def fit(es, nbytes):
    """Ajusta una traduccion a exactamente nbytes (sin contar el 0x00)."""
    b = esc(es)
    if len(b) == nbytes:
        return es, True
    if len(b) < nbytes:
        return es + ' ' * (nbytes - len(b)), True
    # demasiado larga: recortar por palabras
    words = es.split()
    while words and len(esc(' '.join(words))) > nbytes:
        # quitar la palabra mas larga
        idx = max(range(len(words)), key=lambda k: len(words[k]))
        words.pop(idx)
    out = ' '.join(words)
    if len(esc(out)) > nbytes:
        out = esc(out)[:nbytes].decode('utf-8','ignore')
    return out + ' ' * (nbytes - len(esc(out))), False

# --- aplicar ----------------------------------------------------------------
c = load(ORIG)
newrows = {}
stats = {'ok':0, 'shrunk':0, 'missing':0, 'same':0}
for r in c.rows:
    pt = bytearray(c.plain(r))
    rid = r['id']
    rd = d.get(str(rid))
    if not rd:
        newrows[r['id']] = (c.cipher(r, bytes(pt)), len(pt))
        continue
    cnt = rd['count']; slot = rd['slot']
    for si in range(cnt):
        base = 24 + si*slot
        b = bytes(pt[base:base+slot])
        # encontrar meta_start: usar el guardado
        sinfo = rd['rows'][si]
        ms = sinfo['meta']
        parts = split_slot(b, ms)
        replacement = []
        for (a,z,txt) in parts:
            key = txt.strip()
            n = z - a
            if key in T and T[key].strip():
                es,ok = fit(T[key].strip(), n)
                stats['ok' if ok else 'shrunk'] += 1
                if es == txt: stats['same'] += 1
            else:
                es = txt
                stats['missing'] += 1
            replacement.append((a,z,esc(es)))
        # reescribir cada cadena en su sitio, rellenando el hueco con 0x00
        for (a,z,nb) in replacement:
            pt[base+a:base+z] = nb
    newrows[r['id']] = (c.cipher(r, bytes(pt)), len(pt))
print('stats:', stats)

blob = build_ordered(ORIG, newrows)
open(OUT,'wb').write(blob)
c2 = load(OUT)
for rr in c2.rows:
    assert rr['ex'] == len(c2.plain(rr)), rr
print('escrito', OUT, len(blob), 'verificado')
