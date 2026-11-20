import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def extract_all_ids(path, language='unknown'):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    
    data2_start = hdr[10]
    data2 = x[data2_start:]
    
    # Parse ALL entries regardless of ID value
    table_entries = []
    i = 4  # skip first 4 bytes
    entry_num = 0
    max_entries = 1000
    
    while i + 32 <= len(data2) and entry_num < max_entries:
        entry = data2[i:i+32]
        count_val = struct.unpack_from('<I', entry, 1)[0]
        id_val = struct.unpack_from('<I', entry, 5)[0]
        
        table_entries.append((entry_num, id_val, count_val))
        
        i += 32
        entry_num += 1
    
    print(f'{language}: {len(table_entries)} entries')
    print(f'  IDs (first 30): {[e[1] for e in table_entries[:30]]}')
    if len(table_entries) > 30:
        print(f'  IDs (last 30): {[e[1] for e in table_entries[-30:]]}')
    
    # Also print ID ranges
    if table_entries:
        all_ids = [e[1] for e in table_entries]
        print(f'  Range: {min(all_ids)} - {max(all_ids)}')
        # Count unique ID prefixes (0x04XX)
        prefixes = set(h >> 8 for h in all_ids)
        print(f'  Prefijos 0x04: {sorted(prefixes)}')
    
    return table_entries

# Extract from both versions
print('=== SPANISH LT00_EN ===')
spanish_ids = extract_all_ids(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', 'Spanish')

print()
print('=== ENGLISH B_LT00_EN ===')
english_ids = extract_all_ids(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', 'English')