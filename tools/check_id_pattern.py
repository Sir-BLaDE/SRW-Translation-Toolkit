import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

c = Cpk('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')
raw = c.read_file(0)
dec = maybe_decompress(raw)
x = decrypt_data(dec)
data2_start = struct.unpack_from('<12I', x, 0)[10]
data2 = x[data2_start:]

# Check entries at wider intervals to see the ID pattern
print('=== ID pattern across entries ===')
for idx in range(0, 1070, 100):  # every 100 entries
    i = idx * 32
    if i + 32 > len(data2):
        break
    entry = data2[i:i+32]
    # Read the string ID: bytes 8-9 as u16 LE, but really just 0x0400 + byte[8]
    # Actually, from the data: the ID seems to be constructed from bytes 8-9
    # byte[8] varies, byte[9] is usually 0x04
    id_high = entry[9]  # usually 4
    id_low = entry[8]   # varies
    id_value = (id_high << 8) | id_low  # u16 LE
    # Also try: 0x0400 + id_low
    id_alt = 0x0400 + id_low
    
    print(f'Entry {idx}: byte[8]=0x{id_low:02x}({id_low}), byte[9]=0x{id_high:02x}({id_high}), ID u16=0x{id_value:04x}({id_value}), ID alt=0x{id_alt:04x}({id_alt})')

print()
print('=== Last 10 entries ===')
for idx in range(1060, 1070):
    i = idx * 32
    if i + 32 > len(data2):
        break
    entry = data2[i:i+32]
    id_high = entry[9]
    id_low = entry[8]
    id_value = (id_high << 8) | id_low
    id_alt = 0x0400 + id_low
    print(f'Entry {idx}: byte[8]=0x{id_low:02x}({id_low}), byte[9]=0x{id_high:02x}({id_high}), ID u16=0x{id_value:04x}({id_value}), ID alt=0x{id_alt:04x}({id_alt})')