# -*- coding: utf-8 -*-\n"""Vuelca cadenas completas del pool que contienen ingles."""
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = sys.argv[1]
PAT = re.compile(sys.argv[2], re.I)
POOL, PEND = 0x48, 0x1EE10
cf = load(P)
pt = cf.plain(cf.rows[0])
pos = POOL
n = 0
while pos < PEND:
    end = pt.find(b"\0", pos)
    raw = pt[pos:end]
    try:
        s = raw.decode("utf-8")
    except Exception:
        s = None
    if s and PAT.search(s):
        n += 1
        print("=" * 60)
        print("OFF %06X" % (pos - POOL))
        print(repr(s))
    pos = end + 1
print("TOTAL", n)
