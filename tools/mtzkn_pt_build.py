import sys, io, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_crypto import encrypt_data

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Pt.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/MtZkn_Pt_es.cpk'
TM = r'C:/Dev/Default Project/srwv/datos/mtzkn_pt_es.json'

trans = {}
try:
    trans = json.load(io.open(TM, encoding='utf-8'))
except:
    print('No translation file, using identity')

def find_field(data, marker):
    idx = data.find(marker.encode() if isinstance(marker, str) else marker)
    return idx

def parse_pt(data):
    # find DSCR
    idx = data.find(b'^^^DSCR')
    assert idx >= 0
    size = struct.unpack_from('<H', data, idx+7)[0]
    desc_start = idx + 9
    desc = data[desc_start:desc_start+size]
    tail = data[desc_start+size:]
    # prefix before desc (everything up to desc_start)
    prefix = data[:desc_start]
    return prefix, desc, tail, idx

def build_pt(prefix, desc_bytes, tail):
    # prefix contains DSIZ and DATA sizes that need updating
    # Rebuild: prefix with updated DSIZ and DATA, then desc, then tail
    # DSIZ at position in prefix: find ^^^DSIZ
    dsiz_pos = prefix.find(b'^^^DSIZ')
    data_pos = prefix.find(b'^^DATA')
    new_total = len(prefix) + len(desc_bytes) + len(tail)
    new_dsiz = new_total - 24
    new_data = new_dsiz - 8
    new_dscr = len(desc_bytes)
    # rebuild prefix with updated sizes
    prefix = prefix[:dsiz_pos+7] + struct.pack('<H', new_dsiz) + prefix[dsiz_pos+9:]
    data_pos = prefix.find(b'^^DATA')
    prefix = prefix[:data_pos+6] + struct.pack('<H', new_data) + prefix[data_pos+8:]
    # DSCR size is in prefix? No, DSCR marker is at desc_start-9..desc_start-2, which is in prefix.
    # Actually desc_start = idx+9, and prefix = data[:desc_start], so DSCR marker+size is in prefix.
    dscr_pos = prefix.find(b'^^^DSCR')
    prefix = prefix[:dscr_pos+7] + struct.pack('<H', new_dscr) + prefix[dscr_pos+9:]
    body = prefix + desc_bytes + tail
    return body

cf = load(SRC)
new_files = {}
changed = 0
for f in cf.rows:
    pt = cf.plain(f)
    dec = bytes(b ^ 0x5E for b in pt)
    prefix, desc, tail, idx = parse_pt(dec)
    desc_en = desc.decode('utf-8', 'replace')
    full_en = desc_en  # desc already includes '^^' prefix
    full_es = trans.get(full_en, full_en)
    if full_es != full_en:
        changed += 1
    new_dec = build_pt(prefix, full_es.encode('utf-8'), tail)
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