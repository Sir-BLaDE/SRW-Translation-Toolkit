# -*- coding: utf-8 -*-
"""Mostrar Strings legibles alrededor de 'Start' en LayoutData."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

p = r"C:/Dev/Default Project/srwv/backup/LayoutData_original.cpk"
cf = load(p)
for r in cf.rows:
    b = b"".join(cf.plain(r) for r in cf.rows) if False else cf.plain(r)
    for m in re.finditer(rb"[ -~]{4,}", b):
        s = m.group(0)
        if re.search(rb"Start|Continue|New|Load|Game|Settings|Options|Quit", s, re.I):
            ctx = b[max(0, m.start()-80):m.end()+80]
            ctx = re.sub(rb"[^\x20-\x7e]", b".", ctx).decode("ascii", "replace")
            print("fila %d @%d %r" % (r["id"], m.start(), s.decode("ascii", "replace")))
            print("   ...%s..." % ctx)
