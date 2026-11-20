# -*- coding: utf-8 -*-
"""Extrae los bloques [[...]] de los DLC (dialogo de evento)."""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

BLOCK = re.compile(r"\[\[(.*?)\]\]", re.S)


def main():
    files = sorted(glob.glob(r"C:/Dev/Default Project/srwv/backup/dlc_en/dlc*.cpk"))
    texts = {}
    per = {}
    for p in files:
        c = load(p)
        base = os.path.basename(p)
        n = 0
        for r in c.rows:
            try:
                txt = c.plain(r).decode("utf-8")
            except Exception:
                continue
            for m in BLOCK.finditer(txt):
                body = m.group(1)
                # solo bloques con texto latino visible (dialogo traducido al EN)
                if not re.search(r"[A-Za-z]{3}", body):
                    continue
                texts[body] = texts.get(body, 0) + 1
                n += 1
        per[base] = n
    print("bloques [[...]] con texto:", sum(per.values()), "unicos:", len(texts))
    for k in sorted(per):
        print("  %-16s %d" % (k, per[k]))
    json.dump(texts, io.open(r"C:/Dev/Default Project/srwv/datos/dlc_dialogue_en.json", "w",
                             encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0, sort_keys=True)
    print("escrito datos/dlc_dialogue_en.json")


if __name__ == "__main__":
    main()
