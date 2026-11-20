# -*- coding: utf-8 -*-
"""Verificación directa de los CPK reconstruidos con el glosario."""
import struct
import sys
from pathlib import Path

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_bltu import load as load_bltu

OUT = Path(r"C:/Dev/Default Project/srwv/outputs")


def check(cpk_path: Path, label: str) -> None:
    cf = load(str(cpk_path))
    bad = [r["id"] for r in cf.rows if r["ex"] != len(cf.plain(r))]
    print(f"{label}: filas={len(cf.rows)} ex_mismatch={bad} size={cpk_path.stat().st_size}")


def systext_bank() -> None:
    cf = load(str(OUT / "SysText_es.cpk"))
    row = [r for r in cf.rows if r["id"] == 2][0]
    pt = cf.plain(row)
    base = struct.unpack_from("<I", pt, 0x18)[0]
    tab = struct.unpack_from("<I", pt, 0x20)[0]
    cnt = struct.unpack_from("<I", pt, 0x24)[0]
    vals = []
    for i in range(cnt):
        v = struct.unpack_from("<I", pt, tab + i * 4)[0]
        vals.append(pt[base + v:].split(b"\x00")[0].decode("utf-8", "ignore"))
    for i in (16, 23, 24, 25, 27, 30, 31, 63):
        print(f"  SysText[{i}] = {vals[i][:100]!r}")
    leftovers = [
        s for s in vals
        if any(x in s.lower() for x in ("newtype", "mobile suit", "martian successor", "captain"))
    ]
    print("  restos EN en banco SysText:", leftovers)
    print("  terminos ES presentes:", sum("Nuevo Tipo" in s for s in vals),
          "Nuevo Tipo |", sum("traje móvil" in s.lower() for s in vals), "traje móvil")


def cmn00_terms() -> None:
    cf = load(str(OUT / "CMN00_CPK_final_es7.cpk"))
    row = [r for r in cf.rows if r["id"] == 1][0]
    t = load_bltu(cf.plain(row))
    alls = [x[3] for x in t.all_strings()]
    for term in ("Campo AT", "Dr. Infierno", "Barón Ashler", "Bestia Mecánica", "Súper Aleación Z"):
        print(f"  CMN00 {term}: {sum(term in s for s in alls)}")


def profile_terms() -> None:
    for name in ("MtZkn_Pt_es_acc2.cpk", "MtZkn_Rt_es_acc2.cpk"):
        cf = load(str(OUT / name))
        texts = []
        for r in cf.rows:
            texts.append(cf.plain(r).decode("utf-8", "ignore"))
        blob = "\n".join(texts)
        print(f"  {name}: mobile suit={blob.count('mobile suit')} traje móvil={blob.count('traje móvil')} Newtype={blob.count('Newtype')}")


def dlc_checks() -> None:
    dlc = OUT / "dlc_es"
    files = sorted(dlc.glob("dlc*.cpk"))
    bad = []
    nblocks = 0
    for p in files:
        cf = load(str(p))
        mism = [r["id"] for r in cf.rows if r["ex"] != len(cf.plain(r))]
        if mism:
            bad.append("%s:%s" % (p.name, mism))
        for r in cf.rows:
            try:
                nblocks += cf.plain(r).count(b"[[")
            except Exception:
                pass
    print("DLC: ficheros=%d bloques=%d ex_mismatch=%s"
          % (len(files), nblocks, bad or "ninguno"))


def main() -> None:
    for name, label in [
        ("SysText_es.cpk", "SysText"),
        ("Prologue_es.cpk", "Prologue"),
        ("CMN00_CPK_final_es7.cpk", "CMN00"),
        ("MtZkn_Pt_es_acc2.cpk", "MtZkn_Pt"),
        ("MtZkn_Rt_es_acc2.cpk", "MtZkn_Rt"),
        ("KPACK_P4_LN_EN_full_stable2.cpk", "KPACK_LN"),
        ("rpw_jstr_es.cpk", "rpw_jstr"),
    ]:
        check(OUT / name, label)
    systext_bank()
    cmn00_terms()
    profile_terms()
    dlc_checks()


if __name__ == "__main__":
    main()
