import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct, re

def get_strings(path, min_len=2):
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
            if len(s) >= min_len and all(32 <= b < 127 or b >= 0xC0 for b in s):
                strings.append(s.decode('utf-8', 'replace'))
        pos = end + 1
    return strings

# Extract Spanish strings from LT00_EN.cpk with min length 3
spanish = get_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', min_len=3)
english = get_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', min_len=3)

print('Spanish strings (len>=3):', len(spanish))
print('English strings (len>=3):', len(english))

# Find strings only in English
english_set = set(english)
spanish_set = set(spanish)
only_english = english_set - spanish_set
print('English strings not in Spanish:', len(only_english))

# Show some only in English
print()
print('=== Only in English (first 30) ===')
for s in list(only_english)[:30]:
    print(' ', repr(s[:80]))

# Show some only in Spanish
only_spanish = spanish_set - english_set
print()
print('=== Only in Spanish (first 30) ===')
for s in list(only_spanish)[:30]:
    print(' ', repr(s[:80]))