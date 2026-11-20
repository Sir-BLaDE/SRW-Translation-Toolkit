# -*- coding: utf-8 -*-
"""Validar TODOS los CPK candidatos construidos antes de instalarlos."""
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

O = r"C:/Dev/Default Project/srwv/outputs"

CANDIDATES = [
    "OP_CK_es.cpk",
    "LayoutData_es.cpk",
    "LayoutImage_es.cpk",
    "SysText_es_final.cpk",
    "LT00_EN_es2.cpk",
    "B_LT00_EN_es.cpk",
    "FontInfo_es7.cpk",
    "MtZkn_Pt_es_acc2.cpk",
    "MtZkn_Rt_es_acc2.cpk",
    "MtZkn_Nm_es_acc.cpk",
    "rpw_jstr_es.cpk",
    "Prologue_es.cpk",
    "STGEST_EN_es.cpk",
    "CMN00_PC_es.cpk",
    "CMN00_CPK_final_es7.cpk",
    "KPACK_P4_LN_EN_es2.cpk",
    "KPACK_P4_LN_EN_es4.cpk",
    "KPACK_P4_RG_EN_es.cpk",
    "LegaZKN_es.cpk",
]

EN_TERMS = [b"Settings", b"Continue", b"Load", b"Start", b"Press Start",
            b"Select", b"Options", b"Beginner", b"Standard Mode", b"Guidance",
            b"First Name", b"Nickname", b"Blood Type", b"End Settings"]


def validate(name):
    path = os.path.join(O, name)
    label = "%-32s" % name
    if not os.path.exists(path):
        print(label + "NO EXISTE")
        return
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        magic = f.read(4)
    if magic != b"CPK ":
        print(label + "%9d  magic=%r  *** NO CPK ***" % (size, magic))
        return
    try:
        cf = load(path)
    except Exception as e:
        print(label + "%9d  LOAD ERROR: %s" % (size, e))
        return
    bad_ex = []
    plain_errors = []
    eng = set()
    acc = 0
    for r in cf.rows:
        try:
            pt = cf.plain(r)
        except Exception as e:
            plain_errors.append("id%d:%s" % (r["id"], e))
            continue
        if r["ex"] != len(pt):
            bad_ex.append("id%d ex=%d len=%d" % (r["id"], r["ex"], len(pt)))
        if any(b in pt for b in b"\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\xb1\xc2\xa1\xc2\xbf"):
            acc += 1
        for t in EN_TERMS:
            if t in pt:
                eng.add(t.decode("ascii"))
    status = "OK" if not (bad_ex or plain_errors) else "*** FALLO ***"
    print(label + "%9d  filas=%2d  acentos=%2d  %s" % (size, len(cf.rows), acc, status))
    if bad_ex:
        print("      EXSIZE MAL: " + "; ".join(bad_ex[:10]))
    if plain_errors:
        print("      PLAIN ERR: " + "; ".join(plain_errors[:10]))
    if eng:
        print("      INGLES: " + ", ".join(sorted(eng)))


print("=" * 96)
print("VALIDACION DE CANDIDATOS EN outputs/")
print("=" * 96)
for n in CANDIDATES:
    validate(n)
