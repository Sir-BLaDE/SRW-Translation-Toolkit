import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
from srwv_bltu import BltuTable
import struct

# Load English CPK
c = Cpk('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk')
raw = c.read_file(1)
dec = maybe_decompress(raw)
x = decrypt_data(dec)

# Try BLTU parse
try:
    t = BltuTable(x)
    print('BLTU chunks:', len(t.chunks), 'strings:', len(t))
    for i, ch in enumerate(t.chunks[:5]):
        s = ch.strings[:3] if ch.strings else []
        print('  Chunk', i, ':', s)
except Exception as e:
    print('Not BLTU format:', e)

# Check data1 and data2 structure
data2_start = struct.unpack_from('<12I', x, 0)[10]
print('\\ndata2 starts at:', hex(data2_start), 'size:', len(x) - data2_start)

# Check data1
header = struct.unpack_from('<12I', x, 0)
data1_start = header[7]
data1_size = header[8] - data1_start
print('data1 starts at:', hex(data1_start), 'size:', data1_size)

# Print data1 content
print('\\ndata1 content:')
for i in range(0, min(data1_size, 128), 16):
    end = min(i+16, data1_size)
    chunk = data1_start + i
    hexpart = x[chunk:chunk+16].hex(' ')
    asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in x[chunk:chunk+16])
    print('  ', hex(chunk), hexpart, asc)