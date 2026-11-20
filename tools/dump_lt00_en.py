# -*- coding: utf-8 -*-\n"""Vuelca cadenas completas de un LT00 que contengan ingles."""
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from lt00 import load as load_lt

P = sys.argv[1]
PAT = re.compile(sys.argv[2], re.I)
cf = load(P)
t = load_lt(cf.plain(cf.rows[0]))
for i, s in enumerate(t.strings):
    if PAT.search(s):
        print("IDX %d %r" % (i, s[:400]))
