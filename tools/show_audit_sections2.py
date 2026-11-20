# -*- coding: utf-8 -*-
import sys
p = r"C:/Dev/Default Project/srwv/datos/audit_all_cpks.txt"
keys = sys.argv[1:]
lines = open(p, encoding="utf-8").read().splitlines()
cur = None
buf = []
sections = {}
for ln in lines:
    if ln.startswith("=" * 70):
        if cur and buf:
            sections[cur] = buf
        cur = None
        buf = []
        continue
    if cur is not None:
        if ln.startswith("OMITIDOS:"):
            if buf:
                sections[cur] = buf
            cur = None
            buf = []
            continue
        buf.append(ln)
        continue
    if ln and not ln.startswith("  ") and ln.endswith("cadenas EN"):
        cur = ln.split(":")[0]
if cur and buf:
    sections[cur] = buf
for k in keys:
    print("\n########", k)
    found = False
    for name, buf in sections.items():
        if k.lower() in name.lower():
            found = True
            print("SECCION:", name)
            for ln in buf[: int(sys.argv[0] and 80)]:
                print(ln)
    if not found:
        print("NO ENCONTRADA")
