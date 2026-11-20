import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def parse_lt00_en(path):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    
    hdr = struct.unpack_from('<12I', x, 0)
    print('Header:', [hex(h) for h in hdr])
    print(f'data1: 0x{hdr[7]:x}, size: {hdr[8] - hdr[7]}')
    print(f'offsets1: 0x{hdr[8]:x}')
    print(f'data2: 0x{hdr[10]:x}, size: {len(x) - hdr[10]}')
    print(f'names2: 0x{hdr[9]:x}')
    print(f'names3: 0x{hdr[11]:x}')
    
    # Parse data1 section - it has strings followed by offsets
    data1_start = hdr[7]
    data1_end = hdr[8]
    data1 = x[data1_start:data1_end]
    print(f'\ndata1 ({len(data1)} bytes):')
    # Print as hex + ASCII
    for i in range(0, len(data1), 16):
        end = min(i+16, len(data1))
        hexpart = data1[i:end].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data1[i:end])
        print(f'  {data1_start+i:04x}  {hexpart:<47}  {asc}')
    
    # The offsets1 array starts at hdr[8]
    offsets_start = hdr[8]
    # How many offsets are there? They go from offsets_start to data1_end
    # But data1_end is also where data2 starts... no, data2 is at hdr[10]
    # Let me check the range
    print(f'\noffsets1 starts at 0x{offsets_start:x}, data1 ends at 0x{data1_end:x}')
    print(f'So offsets section is {data1_end - offsets_start} bytes')
    
    # Number of u32 offsets
    n_offsets = (data1_end - offsets_start) // 4
    print(f'Number of offsets: {n_offsets}')
    
    # Read the offsets
    offsets = []
    for i in range(n_offsets):
        off = struct.unpack_from('<I', x, offsets_start + i*4)[0]
        offsets.append(off)
        print(f'  offset[{i}]: 0x{off:x} ({off})')
    
    # The actual strings are at these offsets within data1
    print(f'\nStrings at offsets within data1:')
    for i, off in enumerate(offsets):
        if off < len(data1):
            # Find end of string (null terminator)
            s_end = data1.find(b'\x00', off)
            if s_end < 0:
                s_end = off + 40  # fallback
            s = data1[off:s_end].decode('utf-8', 'replace')
            print(f'  [{i}] offset 0x{off:x}: "{s}"')

parse_lt00_en('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')