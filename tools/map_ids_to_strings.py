import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def map_ids_to_strings(path, max_entries=200):
    """Map entry IDs to their string content by reading the data2 table."""
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    
    data2_start = hdr[10]
    data2 = x[data2_start:]
    
    mappings = {}
    
    # Read up to max_entries from the data2 table
    for idx in range(min(max_entries, len(data2) // 32)):
        i = 4 + idx * 32  # entries start at offset 4
        if i + 32 > len(data2):
            break
        
        entry = data2[i:i+32]
        # Get the string ID from bytes 8-9 (u16 LE)
        id_val = struct.unpack_from('<H', entry, 8)[0]
        
        # Try to find associated text
        # The ID seems to correlate with position in the file
        # Let's also check if there's text at the entry position or nearby
        
        # Also try reading the "alt" ID: 0x0400 + byte[8]
        byte8 = entry[8]
        id_alt = 0x0400 + byte8
        
        mappings[idx] = {
            'id': id_val,
            'id_alt': id_alt,
            'byte8': byte8,
        }
    
    return mappings

# Map IDs for both versions
print('=== Spanish LT00_EN ID mapping (first 50 entries) ===')
spanish_map = map_ids_to_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', 50)
for idx, info in spanish_map.items():
    print(f'  Entry {idx}: id=0x{info["id"]:04x} ({info["id"]}), alt=0x{info["id_alt"]:04x} ({info["id_alt"]}), byte8=0x{info["byte8"]:02x}')

print()
print('=== English B_LT00_EN ID mapping (first 50 entries) ===')
english_map = map_ids_to_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', 50)
for idx, info in english_map.items():
    print(f'  Entry {idx}: id=0x{info["id"]:04x} ({info["id"]}), alt=0x{info["id_alt"]:04x} ({info["id_alt"]}), byte8=0x{info["byte8"]:02x}')

# Check if the mappings are the same between Spanish and English
print('\n=== Comparison: same IDs? ===')
same = 0
diff = 0
for idx in spanish_map:
    if idx in english_map:
        if spanish_map[idx]['id'] == english_map[idx]['id']:
            same += 1
        else:
            diff += 1
            if diff <= 5:
                print(f'  Entry {idx}: Spanish id=0x{spanish_map[idx]["id"]:04x}, English id=0x{english_map[idx]["id"]:04x}')
print(f'  Same IDs: {same}, Different IDs: {diff}')