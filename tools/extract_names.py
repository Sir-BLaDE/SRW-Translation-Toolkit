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
    
    # Start at the given offset
    pos = offset
    names = []
    count = 0
    
    while pos < len(x) and count < 100:
        # Find null terminator
        end = x.find(b'\x00', pos)
        if end < 0:
            # Try to find end based on next entry
            # The names table might have fixed-size entries
            # From earlier: names2 at 0xaed, names3 at 0x42e
            # Let's check the gap
            break
        
        name = x[pos:end].decode('ascii', 'replace')
        if name.strip():  # skip empty names
            names.append((count, name))
        else:
            names.append((count, f'[empty:{pos:x}]'))
        
        pos = end + 1
        count += 1
    
    return names

# Extract names from Spanish LT00_EN at offset 0xaed
print('=== Spanish LT00_EN names (from 0xaed) ===')
spanish_names = extract_names_from_offset(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', 0xaed, 'Spanish')

print(f'Found {len(spanish_names)} names')
for i, (idx, name) in enumerate(spanish_names[:30]):
    print(f'  [{i}] {repr(name[:50])}')

print()

# Extract names from English B_LT00_EN at offset 0xaed
print('=== English B_LT00_EN names (from 0xaed) ===')
english_names = extract_names_from_offset(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', 0xaed, 'English')

print(f'Found {len(english_names)} names')
for i, (idx, name) in enumerate(english_names[:30]):
    print(f'  [{i}] {repr(name[:50])}')