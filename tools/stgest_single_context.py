# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
p = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK"
c = load(p)
d = c.plain([x for x in c.rows if x["id"] == 9][0]).decode("utf-8", "replace")
needle = "'ll bet she'"
i = d.find(needle)
print(i)
print(repr(d[max(0, i - 600):i + 600]))
