# -*- coding: utf-8 -*-
"""Dump SysText row-2 bank: original EN, installed ES, and translation status."""
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

ROOT = Path(r"C:/Dev/Default Project/srwv")
ORIG = ROOT / "backup" / "SysText_EN_original.cpk"
INST = ROOT / "outputs" / "SysText_es.cpk"
TRANS = ROOT / "datos" / "systext_trans.json"


def bank(path: Path) -> list[str]:
    cpk = load(str(path))
    row = [x for x in cpk.rows if x["id"] == 2][0]
    pt = cpk.plain(row)
    base = struct.unpack_from("<I", pt, 0x18)[0]
    tab = struct.unpack_from("<I", pt, 0x20)[0]
    cnt = struct.unpack_from("<I", pt, 0x24)[0]
    out = []
    for i in range(cnt):
        v = struct.unpack_from("<I", pt, tab + i * 4)[0]
        out.append(pt[base + v:].split(b"\x00")[0].decode("utf-8", "ignore"))
    return out


def main() -> None:
    orig = bank(ORIG)
    inst = bank(INST)
    trans = json.loads(TRANS.read_text(encoding="utf-8"))
    for i, (en, es) in enumerate(zip(orig, inst)):
        mark = "OK " if en in trans else "-- "
        print(f"{i:3d} {mark} EN={en[:90]!r} | ES={es[:90]!r}")


if __name__ == "__main__":
    main()
