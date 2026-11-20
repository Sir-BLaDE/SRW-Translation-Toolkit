import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def extract_lt00_strings(path, language='unknown'):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    
    data2_start = hdr[10]
    data2 = x[data2_start:]
    
    # The data2 section has a table of entries, then string data
    # Each entry is 32 bytes: 4 bytes (00 or 01) + 4 bytes (count) + 4 bytes (0x04XX ID) + 20 bytes padding
    # Then string data follows
    
    # Let's parse the table first
    table_entries = []
    i = 4  # skip first 4 bytes (possibly a count/marker)
    entry_count = 0
    while i + 32 <= len(data2):
        entry = data2[i:i+32]
        # Read the u32 values
        count_val = struct.unpack_from('<I', entry, 1)[0]  # bytes 1-4
        id_val = struct.unpack_from('<I', entry, 5)[0]  # bytes 5-8: 0x04XX
        
        # Check if this is a valid entry (count=1 and id in reasonable range)
        if count_val == 1 and 0x0420 <= id_val <= 0x0450:
            table_entries.append((id_val, entry_count))
            entry_count += 1
        
        i += 32
        if entry_count >= 50:  # safety limit
            break
    
    print(f'{language}: {len(table_entries)} table entries (IDs {table_entries[0][0] if table_entries else "N/A"} - {table_entries[-1][0] if table_entries else "N/A"})')
    
    # Now extract strings from the string data section
    # String data starts after the table
    table_size = 4 + len(table_entries) * 32
    
    strings = []
    pos = table_size
    string_count = 0
    while pos + 8 <= len(data2) and string_count < 100:
        # Read entry at current position
        entry = data2[pos:pos+32]
        count_val = struct.unpack_from('<I', entry, 1)[0]
        id_val = struct.unpack_from('<I', entry, 5)[0]
        
        if count_val != 1:
            # Maybe this is padding or end of table
            # Try to find a null-terminated string
            # Look for printable ASCII
            j = pos
            while j < len(data2) and j < pos + 256:
                if data2[j] == 0:
                    # Null terminator found
                    s = data2[pos:j]
                    if s and all(32 <= b < 127 for b in s):
                        try:
                            strings.append(s.decode('ascii'))
                            string_count += 1
                            print(f'  String {string_count}: "{s.decode("ascii")}" at 0x{pos:x}')
                            pos = j + 1
                            break
                        except:
                            pass
                    pos = j + 1
                    break
                j += 1
            else:
                pos += 1
        else:
            # Has valid entry, move past it
            pos += 32
    
    return strings

# Extract from both versions
spanish_strings = extract_lt00_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk', 'Spanish')
english_strings = extract_lt00_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk', 'English')

print(f'\nTotal Spanish strings extracted: {len(spanish_strings)}')
print(f'Total English strings extracted: {len(english_strings)}')

# Show first 20 from each
print('\n=== First 20 Spanish strings ===')
for s in spanish_strings[:20]:
    print(f'  {repr(s[:60])}')

print('\n=== First 20 English strings ===')
for s in english_strings[:20]:
    print(f'  {repr(s[:60])}')