# -*- coding: utf-8 -*-
"""Busca prosa en ingles (frases) en los CPK de DLC."""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

# literales de cadena Lua o C: "..." sin caracteres de codigo
LIT = re.compile(r'"([^"\\\r\n]{10,300})"')
PROSE = re.compile(r"^[A-Z0-9¡¿][^=<>{}()]*[.!?…]$")


def strings_of(path):
    c = load(path)
    out = {}
    for r in c.rows:
        try:
            txt = c.plain(r).decode("utf-8")
        except Exception:
            continue
        for m in LIT.finditer(txt):
            s = m.group(1)
            if " " in s and PROSE.match(s) and not re.search(r"[_\[\]|$%^&*\\]", s):
                out[s] = out.get(s, 0) + 1
    return out


def main():
    files = sorted(glob.glob(r"C:/Dev/Default Project/srwv/backup/dlc_en/dlc*.cpk"))
    allfound = {}
    for p in files:
        d = strings_of(p)
        print("%-16s frases=%d" % (os.path.basename(p), len(d)))
        for k, v in d.items():
            allfound[k] = allfound.get(k, 0) + v
    print("\nfrases unicas:", len(allfound))
    json.dump(allfound, io.open(r"C:/Dev/Default Project/srwv/datos/dlc_prose.json", "w",
                                encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0, sort_keys=True)
    for s in sorted(allfound, key=lambda x: (-len(x), x))[:80]:
        print("  %3d %r" % (allfound[s], s[:120]))


if __name__ == "__main__":
    main()
