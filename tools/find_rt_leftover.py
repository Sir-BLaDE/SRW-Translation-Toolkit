import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

p = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk"
cf = load(p)
for r in cf.rows:
    d = bytes(x ^ 0x5E for x in cf.plain(r))
    i = d.find(b"size than regular")
    if i >= 0:
        print("row", r["id"], repr(d[max(0, i-400):i+250]))
