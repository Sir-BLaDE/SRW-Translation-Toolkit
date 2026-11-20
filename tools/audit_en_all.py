# -*- coding: utf-8 -*-\n"""Muestra TODOS los residuales EN de la auditoria, por CPK."""
import io
import re

P = r"C:/Dev/Default Project/srwv/datos/audit_untranslated.txt"
t = io.open(P, encoding="utf-8").read()
parts = re.split(r"\n=+\n", t)
for part in parts:
    m = re.match(r"\n?(\w+)\s+\(([^)]+)\)", part)
    if not m:
        continue
    name = m.group(1)
    mm = re.search(r"  --- EN \((\d+)\), primeros \d+ ---\n(.*?)(?:\n  ---|\Z)", part, re.S)
    if not mm:
        continue
    n = int(mm.group(1))
    lines = [x.strip() for x in mm.group(2).splitlines() if x.strip()]
    print("===", name, "EN=", n, "mostrados", len(lines))
    for line in lines:
        print("   ", line[:150])
