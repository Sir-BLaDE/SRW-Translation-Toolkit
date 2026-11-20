# -*- coding: utf-8 -*-
"""Auditoria del estado REAL instalado: CPK valido, ExtractSize, inglés residual."""
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"

TARGETS = {
    "OP.CPK INSTALADO": G + r"/Data/BTLC/EN0/OP.CPK",
    "OP.CPK ORIGINAL BACKUP": r"C:/Dev/Default Project/srwv/backup/OP_CK_original.cpk",
    "output/OP_CK_es.cpk": r"C:/Dev/Default Project/srwv/output/OP_CK_es.cpk",
    "output/OP_CK_es_real.cpk": r"C:/Dev/Default Project/srwv/output/OP_CK_es_real.cpk",
    "output/OP_CK_es_real_null.cpk": r"C:/Dev/Default Project/srwv/output/OP_CK_es_real_null.cpk",
    "outputs/OP_CK_es.cpk": r"C:/Dev/Default Project/srwv/outputs/OP_CK_es.cpk",
    "SysText INSTALADO": G + r"/Data/AIDDATA/EN/SysText.cpk",
    "SysText ORIGINAL": r"C:/Dev/Default Project/srwv/backup/SysText_EN_original.cpk",
    "LT00 INSTALADO": G + r"/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk",
    "LT00 ORIGINAL": r"C:/Dev/Default Project/srwv/backup/LT00_EN_instalado_antes.cpk",
    "B_LT00 INSTALADO": G + r"/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk",
    "B_LT00 ORIGINAL": r"C:/Dev/Default Project/srwv/backup/B_LT00_EN_original.cpk",
    "MtZkn_Pt INSTALADO": G + r"/CommonData/MtData/EN/MtZkn_Pt.cpk",
    "MtZkn_Pt ORIGINAL": r"C:/Dev/Default Project/srwv/backup/MtZkn_Pt_original.cpk",
    "FontInfo INSTALADO": G + r"/Data/AIDDATA/EN/FontInfo.cpk",
    "FontInfo ORIGINAL": r"C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk",
    "LayoutData INSTALADO": G + r"/Data/AIDDATA/EN/LayoutData.cpk",
    "CMN00 INSTALADO?": G + r"/Data/BTLC/EN0/CMN00.CPK",
    "CMN00 ORIGINAL": r"C:/Dev/Default Project/srwv/backup/CMN00_CPK_original.cpk",
    "KPACK_LN INSTALADO": G + r"/KURODATA/EN/KPACK_P4_LN_EN.CPK",
    "KPACK_LN .es INSTALADO": G + r"/Data/KURODATA/KPACK_P4_LN.es",
    "MTZKN_NM .es INSTALADO": G + r"/Data/MTDATA/MtZkn_Nm.es",
}

UI_EN = [b"Settings", b"Continue", b"Load Game", b"Start", b"New Game",
         b"Press Start", b"PRESS START", b"Select", b"Language", b"Options",
         b"Beginner", b"Standard Mode", b"Guidance", b"First Name", b"Nickname"]


def check(label, path):
    head = "%-28s " % label
    if not os.path.exists(path):
        print(head + "NO EXISTE: " + path)
        return
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        magic = f.read(4)
    okmagic = magic == b"CPK "
    line = head + "%9d bytes  magic=%r %s" % (size, magic, "OK" if okmagic else "*** NO CPK ***")
    if not okmagic:
        print(line)
        return
    try:
        cf = load(path)
    except Exception as e:
        print(line + "  LOAD ERROR: %s" % e)
        return
    bad = []
    eng = set()
    spa = 0
    total = 0
    for r in cf.rows:
        try:
            pt = cf.plain(r)
        except Exception as e:
            bad.append("row%d plain error %s" % (r["id"], e))
            continue
        total += 1
        if r["ex"] != len(pt):
            bad.append("row%d ex=%d len=%d" % (r["id"], r["ex"], len(pt)))
        if any(b in pt for b in b"\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\xb1\xc2\xa1\xc2\xbf"):
            spa += 1
        for term in UI_EN:
            if term in pt:
                eng.add(term.decode())
    print(line + "  filas=%d conAcentos=%d" % (total, spa))
    if bad:
        print("      EXSIZE/PLAIN: " + "; ".join(bad[:12]))
    if eng:
        print("      INGLES UI: " + ", ".join(sorted(eng)))


print("=" * 100)
print("AUDITORIA DEL ESTADO INSTALADO")
print("=" * 100)
for label, path in TARGETS.items():
    check(label, path)
