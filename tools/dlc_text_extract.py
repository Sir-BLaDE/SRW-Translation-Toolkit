# -*- coding: utf-8 -*-
"""Extrae literales 'tipo texto' de los DLC con un filtro laxo."""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

LIT = re.compile(r'"([^"\\\r\n]{6,300})"')
CODE = re.compile(r"[_=<>{}()\[\]|$%^&*\\]|\b(pid|rid)_")


def looks_text(s):
    if CODE.search(s):
        return False
    words = s.split()
    if len(words) < 2:
        return False
    letters = sum(ch.isalpha() for ch in s)
    if letters < 0.6 * len(s.replace(" ", "")):
        return False
    # descarta rutas y nombres de fichero
    if re.search(r"\.(lua|h|cpp|dds|bin|xae|xml)\b", s):
        return False
    return True


def main():
    files = sorted(glob.glob(r"C:/Dev/Default Project/srwv/backup/dlc_en/dlc*.cpk"))
    found = {}
    where = {}
    for p in files:
        c = load(p)
        base = os.path.basename(p)
        for r in c.rows:
            try:
                txt = c.plain(r).decode("utf-8")
            except Exception:
                continue
            for m in LIT.finditer(txt):
                s = m.group(1)
                if looks_text(s):
                    found[s] = found.get(s, 0) + 1
                    where.setdefault(s, set()).add(base)
    print("literales tipo texto unicos:", len(found))
    json.dump(found, io.open(r"C:/Dev/Default Project/srwv/datos/dlc_text_literals.json", "w",
                             encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0, sort_keys=True)
    json.dump({k: sorted(v) for k, v in where.items()},
              io.open(r"C:/Dev/Default Project/srwv/datos/dlc_text_where.json", "w",
                      encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0, sort_keys=True)
    for s in sorted(found, key=lambda x: (-found[x], x)):
        print("  %3d %-30s %r" % (found[s], ",".join(sorted(where[s]))[:28], s[:110]))


if __name__ == "__main__":
    main()
