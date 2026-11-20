import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

# Spanish
c = Cpk('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')
raw = c.read_file(0)
dec = maybe_decompress(raw)
x = decrypt_data(dec)
data2_start = struct.unpack_from('<12I', x, 0)[10]
data2 = x[data2_start:]

print('Spanish data2 first 128 bytes:')
for i in range(0, 128, 16):
    hexpart = data2[i:i+16].hex(' ')
    asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data2[i:i+16])
    print(f'  {data2_start+i:04x}  {hexpart:<47}  {asc}')

# Parse first 5 entries
print('\n=== First 5 entries (32 bytes each) ===')
for idx in range(5):
    i = idx * 32
    entry = data2[i:i+32]
    print(f'\nEntry {idx} at data2 offset {i}:')
    for j in range(32):
        b = entry[j]
        print(f'  byte[{j}]: 0x{b:02x} ({b})', end='')
        if (j+1) % 8 == 0:
            print()
        else:
            print(' ', end='')

# Read the u32 values as my code does
print('\n\n=== Reading u32 values ===')
for idx in range(5):
    i = idx * 32
    entry = data2[i:i+32]
    count_val = struct.unpack_from('<I', entry, 1)[0]
    id_val = struct.unpack_from('<I', entry, 5)[0]
    print(f'Entry {idx}: count={count_val}, id={id_val} (0x{id_val:x})')
    
    # Also try reading from different offsets
    for offset in [0, 1, 4, 5]:
        val = struct.unpack_from('<I', entry, offset)[0]
        print(f'  u32 at offset {offset}: {val} (0x{val:x})')