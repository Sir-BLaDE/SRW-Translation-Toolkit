import sys, glob, os
sys.path.insert(0, r"C:\Dev\Default Project\srwv\tools")
from srwv_cpk import Cpk

base = r"D:\Juegos\-SPARROW-\Super Robot Wars V"
targets = [
    r"Data\BTLC\EN0\1_CMN00.CPK",
    r"Data\BTLC\EN0\CMN00.CPK",
    r"Data\AIDDATA\EN\SysText - copia.cpk",
    r"Data\AIDDATA\EN\SysText.cpk",
    r"Data\AIDDATA\EN\M_FontInfo.cpk",
    r"Data\AIDDATA\EN\FontInfo.cpk",
    r"Data\AIDDATA\EN\Prologue.cpk",
    r"CommonData\ShiroData\LanguageData\EN\LT00_EN.cpk",
    r"CommonData\ShiroData\LanguageData\EN\B_LT00_EN.cpk",
    r"CommonData\ShiroData\LanguageData\JP\LT00_JP.cpk",
    r"Data\KURODATA\EN\1_KPACK_P4_RG_EN.CPK",
    r"Data\KURODATA\EN\KPACK_P4_RG_EN.CPK",
    r"Data\KURODATA\JP\KPACK_P4_LN_JP.CPK",
    r"Data\BTLC\EN0\OP.cpk",
]
for t in targets:
    p = os.path.join(base, t)
    if not os.path.exists(p):
        print(f"--- {t}: NO EXISTE")
        continue
    try:
        c = Cpk(p)
    except Exception as e:
        print(f"--- {t}: ERROR {e}")
        continue
    probs = c.diagnose()
    print(f"--- {t}  ({os.path.getsize(p)} bytes)")
    print("    content:", c.content_offset, c.content_offset and c.h.get("ContentSize"),
          "| packed:", c.h.get("EnabledPackedSize"), "| data:", c.h.get("EnabledDataSize"))
    print("    ficheros:", [(f["id"], f["size"], f["extract_size"]) for f in c.file_list()])
    print("    PROBLEMAS:", probs if probs else "ninguno")
