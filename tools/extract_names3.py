import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def extract_names_from_offset(path, offset, name='unknown'):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    
    pos = offset
    names = []
    count = 0
    
    while pos < len(x) and count < 100:
        end = x.find(b'\x00', pos)
        if end < 0:
            break
        
        name = x[pos:end].decode('ascii', 'replace')
        if name.strip():
            names.append((count, name))
        else:
            names.append((count, f'[empty:{pos:x}]'))
        
        pos = end + 1
        count += 1
    
    return names

# Extract names3 from Spanish LT00_EN at offset 0x42e
print('=== Spanish LT00_EN names3 (from 0x42e) ===')
spanish_names3 = extract_names_from_offset(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', 0x42e, 'Spanish')

print(f'Found {len(spanish_names3)} names3')
for i, (idx, name) in enumerate(spanish_names3[:30]):
    print(f'  [{i}] {repr(name[:60])}')

print()

# Extract names3 from English B_LT00_EN at offset 0x42e
print('=== English B_LT00_EN names3 (from 0x42e) ===')
english_names3 = extract_names_from_offset(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', 0x42e, 'English')

print(f'Found {len(english_names3)} names3')
for i, (idx, name) in enumerate(english_names3[:30]):
    print(f'  [{i}] {repr(name[:60])}')