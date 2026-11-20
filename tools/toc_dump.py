import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from srwv_cpk import Cpk, UtfTable
p=sys.argv[1]
c=Cpk(p); h=c.header.row(0)
blob=c.raw[h['TocOffset']:h['TocOffset']+h['TocSize']]
print('magic',blob[:4])
idx=blob.find(b'@UTF',0,64)
print('utf at',idx)
t=UtfTable(blob[idx:],base=h['TocOffset']+idx)
print('columns',t.columns)
for i in range(t.rows_count):
    r=t.row(i)
    print(i, {k:(v[:60] if isinstance(v,bytes) else v) for k,v in r.items()})
