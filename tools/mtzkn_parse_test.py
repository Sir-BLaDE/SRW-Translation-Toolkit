import sys, io, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

def parse_mtzkn(data):
    pos = 0
    assert data[:8] == b'ZKANPDNM', 'bad magic'
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
    return dsiz, dsize, dscr, desc, tail

def build_mtzkn(dsiz, dsize, desc, tail):
    dscr = len(desc) + 2
    body = b'ZKANPDNM' + bytes([0x5E]) + b'\x01' + b'^^' + b'\x0c' + b'^^^DSIZ' + struct.pack('<H', dsiz) + b'^^DATA' + struct.pack('<H', dsize) + b'^^DSCR' + struct.pack('<H', dscr) + b'^^' + desc + tail
    return body

c = load(r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Nm.cpk')
f0 = c.rows[0]
pt = c.plain(f0)
dec = bytes(b ^ 0x5E for b in pt)
dsiz, dsize, dscr, desc, tail = parse_mtzkn(dec)
print('dsiz', dsiz, 'dsize', dsize, 'dscr', dscr, 'desc_len', len(desc), 'tail', len(tail))
dsiz2 = len(dec) - 24
dsize2 = dsiz2 - 8
new_dec = build_mtzkn(dsiz2, dsize2, desc, tail)
print('rebuilt len', len(new_dec), 'orig', len(dec), 'match', new_dec == dec)