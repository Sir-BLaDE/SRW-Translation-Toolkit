import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

def parse_data2_full(path):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    hdr = struct.unpack_from('<12I', x, 0)
    
    data2_start = hdr[10]
    data2 = x[data2_start:]
    
    # Print first entry in detail (32 bytes starting at offset 4)
    print('=== First 32-byte entry (offset 4 from data2 start) ===')
    entry = data2[4:4+32]
    for i in range(0, 32, 16):
        hexpart = entry[i:i+16].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in entry[i:i+16])
        print(f'  {i:02x}  {hexpart:<47}  {asc}')
    
    # Print second entry
    print('\n=== Second 32-byte entry (offset 36 from data2 start) ===')
    entry = data2[36:36+32]
    for i in range(0, 32, 16):
        hexpart = entry[i:i+16].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in entry[i:i+16])
        print(f'  {i:02x}  {hexpart:<47}  {asc}')
    
    # Print third entry
    print('\n=== Third 32-byte entry (offset 68 from data2 start) ===')
    entry = data2[68:68+32]
    for i in range(0, 32, 16):
        hexpart = entry[i:i+16].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in entry[i:i+16])
        print(f'  {i:02x}  {hexpart:<47}  {asc}')
    
    # Now look for strings after the table
    # The string data might follow after the table
    table_size = 4 + 32 * 30  # 4 byte header + 30 entries × 32 bytes = 964
    print(f'\n=== String data starting at offset {table_size} from data2 start ===')
    strings_section = data2[table_size:table_size+256]
    for i in range(0, min(256, len(strings_section)), 16):
        end = min(i+16, len(strings_section))
        hexpart = strings_section[i:end].hex(' ')
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in strings_section[i:end])
        print(f'  0x{table_size+i:04x}  {hexpart:<47}  {asc}')

parse_data2_full('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')