import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def extract_lt00_strings_detailed(path, language='unknown'):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    
    data2_start = hdr[10]
    data2 = x[data2_start:]
    
    print(f'{language}: data2 size = {len(data2)} bytes, starts at 0x{data2_start:x}')
    
    # The data2 has:
    # - 4 bytes header (00 00 00 00)
    # - entries at intervals of 32 bytes starting at offset 4
    # - each entry: [byte0] [count: 4 bytes] [id: 4 bytes] [24 bytes padding]
    # - string data follows
    
    # Let's parse ALL entries in the table section
    table_entries = []
    i = 4  # skip first 4 bytes
    entry_num = 0
    while i + 32 <= len(data2):
        entry = data2[i:i+32]
        # Byte 0 is usually 0 or 1
        # Bytes 1-4: count as u32 LE
        count_val = struct.unpack_from('<I', entry, 1)[0]
        # Bytes 5-8: id as u32 LE (the 0x04XX value)
        id_val = struct.unpack_from('<I', entry, 5)[0]
        
        # Check if valid
        if count_val >= 1 and 0x0400 <= id_val <= 0x0500:
            table_entries.append((entry_num, id_val, count_val))
        
        i += 32
        entry_num += 1
        if entry_num > 500:  # safety
            break
    
    print(f'  Table entries found: {len(table_entries)} (first 10: {table_entries[:10]})')
    
    # Now look at the string data section
    # String data starts after the table
    table_size = 4 + len(table_entries) * 32
    print(f'  Table ends at offset {table_size} from data2 start')
    
    # Extract strings from the string data section
    strings_found = []
    pos = table_size
    string_idx = 0
    
    while pos + 8 <= len(data2) and string_idx < 200:
        # Read the entry at current position
        if pos + 32 > len(data2):
            break
        
        entry = data2[pos:pos+32]
        count_val = struct.unpack_from('<I', entry, 1)[0]
        id_val = struct.unpack_from('<I', entry, 5)[0]
        
        if count_val == 1 and 0x0400 <= id_val <= 0x0500:
            # This is a valid entry - the ID seems to map to a string
            # But we need to find the actual text
            # Let's look at what follows this entry
            
            # First, check if there's a null-terminated string right after
            # (within the 32-byte entry or immediately after)
            # The entry itself has bytes 8-31 which might be relevant
            
            # Let's look at bytes 8-31 of this entry
            extra_bytes = entry[8:32]
            # Check if there's a string starting at pos + 32
            # Look for printable ASCII starting at pos + 32
            j = pos + 32
            # Skip zeros
            while j < len(data2) and data2[j] == 0:
                j += 1
            
            # Check if we have printable text
            if j < len(data2) and 32 <= data2[j] < 127:
                # Found start of string
                k = j
                while k < len(data2) and k < j + 100 and 32 <= data2[k] < 127:
                    k += 1
                if k > j:
                    s = data2[j:k].decode('ascii')
                    # Only record if it looks like meaningful text (not just symbols)
                    if len(s) >= 3 and any(c.isalpha() for c in s):
                        strings_found.append((string_idx, id_val, s, pos))
                        print(f'  String {string_idx}: id=0x{id_val:x} ({id_val}), texto="{s[:60]}" at pos 0x{pos:x}')
                        string_idx += 1
                        # Move past this string
                        pos = k
                        continue
            
            # If no string found immediately, just move to next entry
            pos += 32
        else:
            pos += 32
    
    return table_entries, strings_found

# Extract from both versions
print('=== EXTRACTING FROM SPANISH LT00_EN ===')
spanish_table, spanish_strings = extract_lt00_strings_detailed(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', 'Spanish')

print()
print('=== EXTRACTING FROM ENGLISH B_LT00_EN ===')
english_table, english_strings = extract_lt00_strings_detailed(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', 'English')

print(f'\n=== RESULTADOS ===')
print(f'Spanish: {len(spanish_table)} entradas de tabla, {len(spanish_strings)} strings con texto')
print(f'English: {len(english_table)} entradas de tabla, {len(english_strings)} strings con texto')

# Show first 20 strings from each
print('\n=== Primeras 20 strings Spanish ===')
for s in spanish_strings[:20]:
    print(f'  id=0x{s[1]:x}: {s[2][:60]}')

print('\n=== Primeras 20 strings English ===')
for s in english_strings[:20]:
    print(f'  id=0x{s[1]:x}: {s[2][:60]}')