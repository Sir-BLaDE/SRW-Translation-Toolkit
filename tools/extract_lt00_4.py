import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def get_strings(path, min_len=1):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    data2 = hdr[10]
    strings = []
    pos = data2
    count = 0
    while pos < len(x) and count < 100:
        end = x.find(b'\x00', pos)
        if end < 0:
            break
        if end > pos:
            s = x[pos:end]
            print(f'String {count}: len={len(s)}, bytes={s.hex()}, chars={s.decode("utf-8", "replace") if all(32 <= b < 127 for b in s) else "non-printable"}')
        else:
            print(f'String {count}: empty')
        pos = end + 1
        count += 1
    print(f'Total strings found: {count}')

print('=== LT00_EN (Spanish) ===')
get_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', min_len=1)

print()
print('=== B_LT00_EN (English) ===')
get_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', min_len=1)