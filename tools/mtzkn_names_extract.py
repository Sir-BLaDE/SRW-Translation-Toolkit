# -*- coding: utf-8 -*-
"""Extrae los campos de nombre (RBTN/RBN2/CHFN/CHNN/PLTN) de los MtZkn."""
import io
import json
import re
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

FILES = {
    "Pt": r"C:/Dev/Default Project/srwv/backup/MtZkn_Pt_original.cpk",
    "Rt": r"C:/Dev/Default Project/srwv/backup/MtZkn_Rt_original.cpk",
    "Nm": r"C:/Dev/Default Project/srwv/backup/MtZkn_Nm_original.cpk",
}
TAGS = (b"RBTN", b"RBN2", b"CHFN", b"CHNN", b"PLTN", b"PRDC")


def fields(dec):
    """Devuelve [(tag, pos_tag, pos_val, text)] para cada campo TAG+len+^^^+texto."""
    out = []
    for m in re.finditer(rb"(RBTN|RBN2|CHFN|CHNN|PLTN|PRDC)", dec):
        tag = m.group(1)
        p = m.end()
        if p >= len(dec):
            continue
        ln = dec[p]
        if dec[p + 1:p + 4] != b"^^^":
            continue
        val = dec[p + 4:p + 4 + ln]
        if len(val) != ln:
            continue
        try:
            txt = val.decode("utf-8")
        except Exception:
            continue
        out.append((tag.decode(), m.start(), p + 4, txt))
    return out


def main():
    allnames = {}
    per = {}
    for k, p in FILES.items():
        c = load(p)
        cnt = {}
        names = set()
        for f in c.rows:
            dec = bytes(b ^ 0x5E for b in c.plain(f))
            for tag, pt, pv, txt in fields(dec):
                cnt[tag] = cnt.get(tag, 0) + 1
                if tag != "PRDC":
                    names.add(txt)
        per[k] = cnt
        print(k, "filas", len(c.rows), cnt, "nombres unicos", len(names))
        for n in sorted(names):
            allnames.setdefault(n, []).append(k)
    print("\ntotal nombres unicos:", len(allnames))
    json.dump({k: sorted(v) for k, v in allnames.items()},
              io.open(r"C:/Dev/Default Project/srwv/datos/mtzkn_names_worklist.json", "w",
                      encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0)
    print("escrito datos/mtzkn_names_worklist.json")
    for n in sorted(allnames)[:40]:
        print("  ", repr(n))


if __name__ == "__main__":
    main()
