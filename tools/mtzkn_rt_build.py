import sys, io, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_crypto import encrypt_data

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/MtZkn_Rt_es.cpk'
TM = r'C:/Dev/Default Project/srwv/datos/mtzkn_rt_es.json'

trans = {}
try:
    trans = json.load(io.open(TM, encoding='utf-8'))
except:
    print('No translation file, using identity')

def parse_rt(data):
    idx = data.find(b'DSCR')
    assert idx >= 0, 'no DSCR'
    size = struct.unpack_from('<H', data, idx+4)[0]
    desc_start = idx + 6  # 'DSCR' (4) + size (2)
    desc = data[desc_start:desc_start+size]
    prefix = data[:idx]
    tail = data[desc_start+size:]
    return prefix, desc, tail, idx

def build_rt(prefix, desc_bytes, tail):
    # update DSIZ in prefix
    dsiz_pos = prefix.find(b'^^^DSIZ')
    assert dsiz_pos >= 0
    new_total = len(prefix) + len(desc_bytes) + len(tail) + 4  # +4 for 'DSCR' marker? 
    # Wait: prefix includes everything up to 'DSCR'. The 'DSCR' marker (4 bytes) + size (2) are between prefix and desc.
    # Actually parse_rt: prefix = data[:idx] where idx is position of 'DSCR'. So prefix doesn't include 'DSCR'.
    # The output should be: prefix + b'DSCR' + size(2) + desc + tail
    new_total = len(prefix) + 4 + 2 + len(desc_bytes) + len(tail)
    new_dsiz = new_total - 24
    new_data_pos = prefix.find(b'^^DATA')
    # update DSIZ
    prefix = prefix[:dsiz_pos+7] + struct.pack('<H', new_dsiz) + prefix[dsiz_pos+9:]
    # update DATA
    data_pos = prefix.find(b'^^DATA')
    new_data = new_dsiz - 8
    prefix = prefix[:data_pos+6] + struct.pack('<H', new_data) + prefix[data_pos+8:]
    # build
    new_dscr_size = len(desc_bytes)
    body = prefix + b'DSCR' + struct.pack('<H', new_dscr_size) + desc_bytes + tail
    return body

cf = load(SRC)
new_files = {}
changed = 0
for f in cf.rows:
    pt = cf.plain(f)
    dec = bytes(b ^ 0x5E for b in pt)
    prefix, desc, tail, idx = parse_rt(dec)
    desc_en = desc.decode('utf-8', 'replace')
    full_es = trans.get(desc_en, desc_en)
    if full_es != desc_en:
        changed += 1
    new_dec = build_rt(prefix, full_es.encode('utf-8'), tail)
    new_enc = bytes(b ^ 0x5E for b in new_dec)
    blob = encrypt_data(new_enc)
    new_files[f['id']] = (blob, len(new_enc))

print('changed', changed, 'of', len(cf.rows))
out = build_ordered(SRC, new_files)
open(OUT, 'wb').write(out)
print('written', len(out))

cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
bad = sum(1 for f in cf2.rows if f['ex'] != len(cf2.plain(f)))
print('files with ex mismatch:', bad)