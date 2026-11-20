import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def parse_data2(path):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    
    data2_start = hdr[10]
    data2 = x[data2_start:]
    print(f'data2: {len(data2)} bytes, starts at 0x{data2_start:x}')
    
    # Print first 256 bytes of data2
    print('\n=== First 256 bytes of data2 ===')
    for i in range(0, min(256, len(data2)), 16):
        end = min(i+16, len(data2))
        hexpart = data2[i:end].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data2[i:end])
        print(f'  0x{data2_start+i:04x}  {hexpart:<47}  {asc}')
    
    # Look for patterns: u32 values followed by strings
    # From the hex dump, we see patterns like:
    # 01 00 00 00 XX 04 00 00
    # where XX increments: 2e, 2f, 30, 31, 32, 33, 34, 35
    # 0x042e = 1070, 0x042f = 1071, etc.
    
    # Let's look for the pattern u32_count u32_value
    print('\n=== Looking for u32 patterns ===')
    i = 0
    count = 0
    while i < len(data2) - 8 and count < 30:
        # Try to read as two u32 values
        val1 = struct.unpack_from('<I', data2, i)[0]
        val2 = struct.unpack_from('<I', data2, i+4)[0]
        # Check if val2 looks like an offset (0x04xx = 1070-1099 range)
        if 0x0420 <= val2 <= 0x0450 and val1 in (0, 1, 2):
            print(f'  pos 0x{data2_start+i:x}: val1={val1}, val2=0x{val2:x} ({val2})')
            i += 8
            count += 1
        else:
            i += 1

parse_data2('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')