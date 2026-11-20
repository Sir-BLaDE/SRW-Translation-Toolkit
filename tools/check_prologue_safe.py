# -*- coding: utf-8 -*-
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

FILES = [
    ("ORIGINAL", r"C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk"),
    ("REBUILD (crashea)", r"C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk"),
    ("INPLACE SEGURO", r"C:/Dev/Default Project/srwv/outputs/Prologue_es_inplace_v7.cpk"),
]
EN = [b"the ", b"you ", b"our ", b"will ", b"have ", b"This ", b"that ", b"with ",
      b"them ", b"their ", b"because ", b"attack ", b"mission ", b"enemy ", b" Earth ",
      b" of ", b" and ", b" to "]
ACC = re.compile(rb"[\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\xb1\xc2\xbf\xc2\xa1]")

for label, path in FILES:
    cf = load(path)
    b = b"".join(cf.plain(r) for r in cf.rows)
    print("%-20s len=%-8d EN=%-6d acentos=%d" % (label, len(b), sum(b.count(w) for w in EN), len(ACC.findall(b))))
