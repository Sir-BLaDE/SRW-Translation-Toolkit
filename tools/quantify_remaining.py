# -*- coding: utf-8 -*-\n"""Cuantifica texto restante: rpw_jstr, nombres MTZKN y CPK DLC."""
import glob
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/"
JP = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")

# --- rpw_jstr ---
c = load(G + "CommonData/MtData/EN/rpw_jstr.cpk")
pt = c.plain(c.rows[0])
parts = [p for p in pt.split(b"\0") if p]
jp = sum(1 for p in parts if JP.search(p.decode("utf-8", "replace")))
print("rpw_jstr: trozos nulos", len(parts), "con japones", jp)
sample = [p.decode("utf-8", "replace") for p in parts if not JP.search(p.decode("utf-8", "replace"))
          and re.search(r"[A-Za-z]{4}", p.decode("utf-8", "replace"))]
print("  trozos ASCII con letras", len(sample))
for s in sample[:20]:
    print("    ", repr(s[:90]))

# --- DLC ---
dlc = sorted(glob.glob(G + "Data/DLCDIRE/EN/dlc*.cpk"))
print("DLC CPK:", len(dlc))
tot = 0
for p in dlc:
    c = load(p)
    for f in c.rows:
        tot += len(c.plain(f))
print("  bytes plain totales DLC:", tot)

# --- nombres MTZKN por fichero ---
for fn in ("MtZkn_Rt.cpk", "MtZkn_Pt.cpk", "MtZkn_Nm.cpk"):
    c = load(G + "CommonData/MtData/EN/" + fn)
    names = set()
    for f in c.rows:
        d = bytes(b ^ 0x5E for b in c.plain(f))
        for tag in (b"RBTN", b"RBN2", b"CHFN", b"CHNN"):
            pos = 0
            while True:
                i = d.find(tag, pos)
                if i < 0:
                    break
                pos = i + 4
                if pos + 4 > len(d):
                    break
                n = d[pos]
                if d[pos + 1:pos + 4] != b"^^^":
                    continue
                raw = d[pos + 4:pos + 4 + n]
                try:
                    s = raw.decode("utf-8")
                except Exception:
                    continue
                if len(s) >= 3 and re.search(r"[A-Za-z]{2}", s):
                    names.add(s)
    print(fn, "nombres unicos ASCII:", len(names))
