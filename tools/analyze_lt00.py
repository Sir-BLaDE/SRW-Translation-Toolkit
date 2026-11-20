import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def analyze_path(path):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    
    print('Header:', [hex(h) for h in hdr])
    print(f'data1: 0x{hdr[7]:x}, offsets1: 0x{hdr[8]:x}, data2: 0x{hdr[10]:x}')
    print(f'names2: 0x{hdr[9]:x}, names3: 0x{hdr[11]:x}')
    
    # Print data section 1 (from data1 to offsets1)
    data1_size = hdr[8] - hdr[7]
    print(f'data1 size: {data1_size}')
    print(f'data1 first 128 bytes: {x[hdr[7]:hdr[7]+128].hex()}')
    
    # Print data2 section
    data2_size = len(x) - hdr[10]
    print(f'data2 size: {data2_size}')
    print(f'data2 first 128 bytes: {x[hdr[10]:hdr[10]+128].hex()}')
    
    # The actual text seems to be around data1 offset
    # Let's look at the section around 0x15185 for Spanish
    print()
    print('=== Section around 0x15185 (Spanish) ===')
    for i in range(0x15180, min(0x15180+256, len(x)), 16):
        hexpart = x[i:i+16].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in x[i:i+16])
        print(f'{i:04x}  {hexpart:<47}  {asc}')
    
    print()
    print('=== Section around 0x131e2 (English) ===')
    for i in range(0x131e0, min(0x131e0+256, len(x)), 16):
        hexpart = x[i:i+16].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in x[i:i+16])
        print(f'{i:04x}  {hexpart:<47}  {asc}')

print('=== LT00_EN (Spanish) ===')
analyze_path('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')

print()
print('=== B_LT00_EN (English) ===')
analyze_path('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk')