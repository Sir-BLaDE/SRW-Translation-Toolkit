import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def extract_data2_strings(path):
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
            # Only keep strings with actual text content
            if all(32 <= b < 127 or b >= 0xC0 for b in s) and len(s) > 1:
                strings.append(s.decode('utf-8', 'replace'))
        pos = end + 1
    return strings, len(strings)

# Extract from Spanish LT00_EN
spanish_strings, spanish_count = extract_data2_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')
# Extract from English B_LT00_EN
english_strings, english_count = extract_data2_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk')

print('Spanish data2 strings:', spanish_count)
print('English data2 strings:', english_count)

# Show first 20 Spanish strings
print()
print('=== First 20 Spanish data2 strings ===')
for s in spanish_strings[:20]:
    print(' ', repr(s[:80]))

# Show first 20 English strings
print()
print('=== First 20 English data2 strings ===')
for s in english_strings[:20]:
    print(' ', repr(s[:80]))

# Find strings only in English
english_set = set(english_strings)
spanish_set = set(spanish_strings)
only_english = english_set - spanish_set
print()
print('English strings not in Spanish:', len(only_english))

# Show some only in English
print()
print('=== Only in English (first 20) ===')
for s in list(only_english)[:20]:
    print(' ', repr(s[:80]))

# Show some only in Spanish
only_spanish = spanish_set - english_set
print()
print('=== Only in Spanish (first 20) ===')
for s in list(only_spanish)[:20]:
    print(' ', repr(s[:80]))