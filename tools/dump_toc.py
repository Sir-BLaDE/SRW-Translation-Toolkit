import sys, struct
sys.path.insert(0, r"C:\Dev\Default Project\srwv\tools")
from cri_utf import UtfTable

c = open(r"D:\Juegos\-SPARROW-\Super Robot Wars V\Data\AIDDATA\COMMON\ButtonHintsSTEAM.cpk", "rb").read()
blob = c[2048:2048+864]
idx = blob.find(b"@UTF")
size = struct.unpack_from("<I", blob, idx+4)[0] + 8
tab = UtfTable(blob[idx:idx+size], base=2048+idx)
print(tab)
print("cols:", [(x.name, hex(x.type)) for x in tab.columns])
for r in range(min(tab.rows_count, 5)):
    row = tab.row(r)
    print("  ", {k: (v[:60] if isinstance(v, str) else v) for k, v in row.items()})
print("total rows:", tab.rows_count)
