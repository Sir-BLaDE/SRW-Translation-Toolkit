import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def inspect_data2(path):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    data2 = hdr[10]
    
    print(f'data2 starts at: 0x{data2:x}')
    print(f'data2 section size: {len(x) - data2}')
    print()
    
    # Print first 256 bytes of data2
    print('=== First 256 bytes of data2 ===')
    for i in range(data2, min(data2+256, len(x)), 16):
        hexpart = x[i:i+16].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in x[i:i+16])
        print(f'{i:04x}  {hexpart:<47}  {asc}')
    
    print()
    # Print bytes around the first few potential string starts
    print('=== Looking for string patterns ===')
    # Look for sequences that look like text (printable ASCII)
    for i in range(data2, min(data2+128, len(x))):
        b = x[i:i+1]
        if 32 <= b < 127:
            # This is printable ASCII
            end = i + 1
            while end < len(x) and 32 <= x[end] < 127:
                end += 1
            s = x[i:end].decode('ascii')
            if len(s) >= 3:
                print(f'  Printable string at 0x{i:x}: "{s}" (len={len(s)})')
                i = end
            else:
                i = end - 1
        else:
            i += 1 - 1  # just move one forward

inspect_data2('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')