import sys, io, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_crypto import encrypt_data

SRC = r'C:/Dev/Default Project/srwv/backup/MtZkn_Nm_original.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/MtZkn_Nm_es_acc.cpk'
TM = r'C:/Dev/Default Project/srwv/datos/mtzkn_nm_es_accent.json'
TM2 = r'C:/Dev/Default Project/srwv/datos/mtzkn_nm_dsc2_es.json'

trans = json.load(io.open(TM, encoding='utf-8'))
try:
    trans2 = json.load(io.open(TM2, encoding='utf-8'))
except:
    trans2 = {}

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

def translate_dsc2(tail):
    """Sustituye el texto util de DSC2, conservando KANA y el relleno."""
    i = tail.find(b'DSC2')
    if i < 0 or i + 6 > len(tail):
        return tail, 0
    size = struct.unpack_from('<H', tail, i + 4)[0]
    start = i + 6
    end = start + size
    blob = tail[start:end]
    k = blob.find(b'KANA')
    text = (blob[:k] if k >= 0 else blob).decode('utf-8', 'replace')
    es = trans2.get(text, text)
    if es == text:
        return tail, 0
    rest = blob[len(text.encode('utf-8')):]
    new_blob = es.encode('utf-8') + rest
    new_tail = tail[:i + 4] + struct.pack('<H', len(new_blob)) + new_blob + tail[end:]
    return new_tail, 1

cf = load(SRC)
new_files = {}
changed = 0
changed2 = 0
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
    tail, n2 = translate_dsc2(tail)
    changed2 += n2
    new_dec = build_mtzkn(desc_es.encode('utf-8'), tail)
    new_enc = bytes(b ^ 0x5E for b in new_dec)
    blob = encrypt_data(new_enc)
    new_files[f['id']] = (blob, len(new_enc))

print('changed DSCR', changed, 'DSC2', changed2, 'of', len(cf.rows))
out = build_ordered(SRC, new_files)
open(OUT, 'wb').write(out)
print('written', len(out))

cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows[:3]:
    p = cf2.plain(f)
    print(' id', f['id'], 'ex', f['ex'], 'plain', len(p), 'OK' if f['ex']==len(p) else 'BAD')