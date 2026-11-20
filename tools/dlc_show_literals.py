# -*- coding: utf-8 -*-
"""Muestra literales de cadena de los Lua de un DLC."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

path = sys.argv[1]
rows = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [1, 2]
c = load(path)
for rid in rows:
    row = [r for r in c.rows if r["id"] == rid][0]
    txt = c.plain(row).decode("utf-8", "replace")
    print("=== row", rid, "len", len(txt))
    seen = 0
    for m in re.finditer(r'"([^"\\]{4,200})"', txt):
        s = m.group(1)
        if re.search(r"[A-Za-z]", s) and not re.search(r"[{}();=]", s):
            print("   ", repr(s))
            seen += 1
            if seen > 80:
                break
    print("   (mostrados %d)" % seen)
