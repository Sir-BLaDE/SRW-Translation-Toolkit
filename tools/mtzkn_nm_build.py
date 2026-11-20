import sys, io, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_crypto import encrypt_data

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Nm.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/MtZkn_Nm_es.cpk'
TM = r'C:/Dev/Default Project/srwv/datos/mtzkn_nm_es.json'

trans = json.load(io.open(TM, encoding='utf-8'))

def parse_mtzkn(data):
    pos = 0
    assert data[:8] == b'ZKANPDNM'
    pos = 8
    assert data[pos] == 0x5E; pos += 1
    assert data[pos] == 1; pos += 1
    assert data[pos:pos+2] == b'^^'; pos += 2
    assert data[pos] == 0x0c; pos += 1
    assert data[pos:pos+7] == b'^^^DSIZ'; pos += 7
    dsiz = struct.unpack_from('<H', data, pos)[0]; pos += 2
    assert data[pos:pos+6] == b'^^DATA'; pos += 6
    dsize = struct.unpack_from('<H', data, pos)[0]; pos += 2
    assert data[pos:pos+6] == b'^^DSCR'; pos += 6
    dscr = struct.unpack_from('<H', data, pos)[0]; pos += 2
    assert data[pos:pos+2] == b'^^'; pos += 2
    desc = data[pos:pos+dscr-2]
    pos += dscr - 2
    tail = data[pos:]
    return desc, tail

def build_mtzkn(desc_bytes, tail):
    dscr = len(desc_bytes) + 2
    prefix_len = 8 + 1 + 1 + 2 + 1 + 7 + 2 + 6 + 2 + 6 + 2 + 2
    total = prefix_len + len(desc_bytes) + len(tail)
    dsiz = total - 24
    dsize = dsiz - 8
    body = b'ZKANPDNM' + bytes([0x5E]) + b'\x01' + b'^^' + b'\x0c' + b'^^^DSIZ' + struct.pack('<H', dsiz) + b'^^DATA' + struct.pack('<H', dsize) + b'^^DSCR' + struct.pack('<H', dscr) + b'^^' + desc_bytes + tail
    return body

cf = load(SRC)
new_files = {}
changed = 0
for f in cf.rows:
    pt = cf.plain(f)
    dec = bytes(b ^ 0x5E for b in pt)
    desc_bytes, tail = parse_mtzkn(dec)
    desc_en = desc_bytes.decode('utf-8', 'replace')
    full_en = '^^' + desc_en
    full_es = trans.get(full_en, full_en)
    desc_es = full_es[2:] if full_es.startswith('^^') else full_es
    if full_es != full_en:
        changed += 1
    new_dec = build_mtzkn(desc_es.encode('utf-8'), tail)
    new_enc = bytes(b ^ 0x5E for b in new_dec)
    blob = encrypt_data(new_enc)
    new_files[f['id']] = (blob, len(new_enc))

print('changed', changed, 'of', len(cf.rows))
out = build_ordered(SRC, new_files)
open(OUT, 'wb').write(out)
print('written', len(out))

cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows[:3]:
    p = cf2.plain(f)
    print(' id', f['id'], 'ex', f['ex'], 'plain', len(p), 'OK' if f['ex']==len(p) else 'BAD')