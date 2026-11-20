# -*- coding: utf-8 -*-
"""MtZkn_Pt 100% in-situ: mismos tamanos de fila y de cada nombre.

El juego crashea al crear partida nueva si cambia el tamano de las filas de
MtZkn_Pt (tiene offsets internos fijos). Esta version solo sustituye bytes
dentro del espacio exacto que ocupaba cada nombre, rellenando con 0x00.

Uso: python mtzkn_pt_fixedlen.py [salida.cpk]
"""
import io, json, sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/MtZkn_Pt_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/MtZkn_Pt_es_fixedlen.cpk"
NAMES = r"C:/Dev/Default Project/srwv/datos/mtzkn_names_es.json"
NAME_TAGS = (b"CHFN", b"CHNN", b"PRDC")

names = json.load(io.open(NAMES, encoding="utf-8"))
cf = load(SRC)
new_rows = {}
changed = truncated = 0
for f in cf.rows:
    # capa XOR 0x5E adicional sobre el contenido descifrado con Blowfish
    pt = bytearray(b ^ 0x5E for b in cf.plain(f))
    orig_len = len(pt)
    pos = 0
    while True:
        best = None
        for t in NAME_TAGS:
            i = pt.find(t, pos)
            if i >= 0 and (best is None or i < best[0]):
                best = (i, t)
        if best is None:
            break
        i, t = best
        p = i + 4
        if p >= orig_len or pt[p+1:p+4] != b"^^^":
            pos = i + 4
            continue
        ln = pt[p]
        start = p + 4
        end = start + ln
        if end > orig_len:
            pos = i + 4
            continue
        try:
            txt = bytes(pt[start:end]).decode("utf-8")
        except UnicodeDecodeError:
            pos = i + 4
            continue
        es = names.get(txt)
        if es is None or es == txt:
            pos = end
            continue
        eb = es.encode("utf-8")
        if len(eb) > ln:
            # recortar por palabras, sin partir caracteres UTF-8
            words = es.split()
            while words and len(" ".join(words).encode("utf-8")) > ln:
                words.pop()
            es2 = " ".join(words)
            if not es2:
                # una sola palabra demasiado larga: recortar a bytes seguros
                while True:
                    try:
                        es2 = es.encode("utf-8")[:ln].decode("utf-8")
                        break
                    except UnicodeDecodeError:
                        ln2 = ln - 1
                        es2 = es.encode("utf-8")[:ln2].decode("utf-8", "ignore")
                        break
            eb = es2.encode("utf-8")[:ln]
            truncated += 1
        block = bytearray(ln)
        block[:len(eb)] = eb
        pt[start:end] = block
        if len(eb) < ln:
            # rellenar con espacios en vez de ceros, mas seguro para el juego
            for k in range(len(eb), ln):
                pt[start + k] = 0x20
        changed += 1
        pos = end
    assert len(pt) == orig_len
    enc = bytes(b ^ 0x5E for b in pt)
    new_rows[f["id"]] = (cf.cipher(f, enc), orig_len)

blob = build_ordered(SRC, new_rows)
open(OUT, "wb").write(blob)
chk = load(OUT)
print("nombres reescritos:", changed, "recortados:", truncated)
print("longitudes iguales:", all(len(chk.plain(r)) == len(cf.plain(next(q for q in cf.rows if q['id']==r['id']))) for r in chk.rows))
print("magic:", chk.cpk.raw[:4], "diagnose:", chk.cpk.diagnose() or "ok")
print("ExtractSize OK:", all(r['ex'] == len(chk.plain(r)) for r in chk.rows))
print("escrito", OUT)
