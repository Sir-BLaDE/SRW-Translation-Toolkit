# -*- coding: utf-8 -*-
import ast
import re

lines = open(r"C:/Dev/Default Project/srwv/datos/audit_all_cpks.txt", encoding="utf-8").read().splitlines()
cur = False
out = []
for l in lines:
    if l.startswith("=" * 70):
        cur = False
    if l and not l.startswith("  ") and l.endswith("cadenas EN"):
        cur = "LayoutData" in l
        continue
    if cur and l.startswith("  "):
        # forma: "     4  'texto'"
        m = re.match(r"^\s*\d+\s+(.*)$", l)
        if m:
            raw = m.group(1)
            try:
                s = ast.literal_eval(raw)
            except Exception:
                continue
            if isinstance(s, str):
                out.append(s)
print(len(out))
for s in out:
    print(repr(s))
