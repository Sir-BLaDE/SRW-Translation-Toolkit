from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

c = Cpk('C:/Dev/Default Project/srwv/outputs/LT00_EN_rebuilt.cpk')
raw = c.read_file(0)
dec = maybe_decompress(raw)
x = decrypt_data(dec)

# Search for some Spanish strings we translated
search_strings = [
    b'Gana 50 Enfoque al ser sorteado.',
    b'Activa el comando espiritual Instinto.',
    b'El Enfoque es superior a 140.',
    b'Ignora la barrera de la unidad enemiga al atacar.',
    b'Buena Suerte ',
    b'Accion Doble',
]

print('=== Searching for Spanish strings in rebuilt CPK ===')
for s in search_strings:
    pos = x.find(s)
    found = pos >= 0
    pos_str = hex(pos) if found else 'N/A'
    s_name = s[:25].decode('latin-1', 'replace')
    print(f'  {s_name:25s}: found={found} at position {pos_str}')

# Also check the first few entries in the data2 table
header = struct.unpack_from('<12I', x, 0)
data2_start = header[10]
print('\\n=== First 5 entries in data2 ===')
for i in range(5):
    offset = 4 + i * 32
    if offset + 32 > len(x):
        break
    entry = x[offset:offset+32]
    id_low = entry[8]
    id_val = 0x0400 + id_low
    print(f'Entry {i}: id=0x{id_val:04x} (byte8=0x{id_low:02x})')

print('\\n=== Verification complete ===')