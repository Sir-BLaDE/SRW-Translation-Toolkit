# -*- coding: utf-8 -*-
"""Extrae las cadenas de texto visibles de los CPK de DLC."""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

DLC = r"C:/Dev/Default Project/srwv/backup/dlc_en/dlc*.cpk"
OUT = r"C:/Dev/Default Project/srwv/datos/dlc_strings.json"

# texto imprimible: ASCII basico + latin-1 util; evita basura binaria
TXT = re.compile(rb"[\x20-\x7e]{4,}")


def main():
    files = sorted(glob.glob(DLC))
    print("CPK:", len(files))
    found = {}
    per_file = {}
    for p in files:
        c = load(p)
        strs = []
        for r in c.rows:
            pt = c.plain(r)
            for m in TXT.finditer(pt):
                s = m.group().decode("ascii")
                strs.append((r["id"], s))
                found[s] = found.get(s, 0) + 1
        per_file[os.path.basename(p)] = len(strs)
        print("%-16s filas=%d textos=%d" % (os.path.basename(p), len(c.rows), len(strs)))

    print("\ncadenas unicas:", len(found))
    json.dump(found, io.open(OUT, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0, sort_keys=True)
    print("escrito", OUT)
    for s in sorted(found, key=lambda x: (-len(x), x))[:60]:
        print("  %4d %r" % (found[s], s[:110]))


if __name__ == "__main__":
    main()
