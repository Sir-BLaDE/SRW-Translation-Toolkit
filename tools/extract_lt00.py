import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct, re

def get_strings(path):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    data2 = hdr[10]
    strings = []
    pos = data2
    while pos < len(x):
        end = x.find(b'\x00', pos)
        if end < 0:
            break
        if end > pos:
            s = x[pos:end]
            if all(32 <= b < 127 or b >= 0xC0 for b in s):
                strings.append(s.decode('utf-8', 'replace'))
        pos = end + 1
    return strings

# Extract Spanish strings from LT00_EN.cpk
spanish = get_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')
english = get_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk')

print('Spanish strings:', len(spanish))
print('English strings:', len(english))

# Find strings that are only in English (need translation)
english_set = set(english)
spanish_set = set(spanish)
only_english = english_set - spanish_set
print('English strings not in Spanish:', len(only_english))

# Show some examples
for s in list(only_english)[:30]:
    print(' ', repr(s[:80]))