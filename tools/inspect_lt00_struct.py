import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from lt00 import load
pt = open(r'C:/Dev/Default Project/srwv/outputs/lt00_plain.bin','rb').read()
t = load(pt)
print('hdr', [hex(x) for x in t.header])
print('blob', hex(t.blob_start), hex(t.blob_end), 'off_start', hex(t.off_start), 'count', t.count,
      'id_start', hex(t.id_start), 'id_count', t.id_count)
print('len', len(pt))
print('slice before blob_end', pt[t.blob_end-24:t.blob_end+8].hex(' '))
print('slice at off_start', pt[t.off_start-8:t.off_start+16].hex(' '))
print('slice at id_start', pt[t.id_start:t.id_start+64].hex(' '))
print('ids[:10]', t.ids[:10])
print('max id a', max(a for a,b,c in t.ids), 'min', min(a for a,b,c in t.ids))
print('distinct a', len(set(a for a,b,c in t.ids)))
# comprobar tabla de offsets
offs = list(struct.unpack_from(f'<{t.count}I', pt, t.off_start))
print('offs[:5]', offs[:5], 'max', max(offs))
print('len blob real', t.blob_end - t.blob_start)
# ¿coinciden los offsets con las posiciones reales?
pos = t.blob_start
ok = 0
for i in range(t.count):
    if offs[i] == pos - t.blob_start:
        ok += 1
    nul = pt.find(b'\0', pos)
    pos = nul + 1
print('offsets coinciden', ok, 'de', t.count)
print('ultima pos', hex(pos))
print('bytes entre fin blob y off_start', pt[t.blob_end:t.off_start].hex(' '))
print('tail despues de ids', len(pt) - (t.id_start + t.id_count*32))
