from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

# Spanish FontInfo.cpk
c = Cpk('D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk')
raw = c.read_file(0)
dec = maybe_decompress(raw)
dec2 = decrypt_data(dec)

print('Spanish FontInfo.cpk:')
print('  Raw size:', len(raw))
print('  Decompressed size:', len(dec))
print('  Decrypted size:', len(dec2))
print('  Decrypted first 32 bytes:', dec2[:32].hex())

print('\\nHeader (12 u32):')
header = struct.unpack_from('<12I', dec2, 0)
for i, h in enumerate(header):
    print(f'  [{i}]: 0x{h:08x} ({h})')

print('\\nFile list:')
for f in c.file_list():
    print(f'  id={f["id"]} size={f["size"]} extract={f["extract_size"]}')

# Check each file
for fid in range(len(c.file_list())):
    fid_data = c.read_file(f["id"])
    fdec = maybe_decompress(fid_data)
    fdec2 = decrypt_data(fdec)
    print(f'\\nFile {f["id"]}: size={len(fdec2)}')
    print(f'  First 32 bytes: {fdec2[:32].hex()}')
    # Try as UTF table
    try:
        from cri_utf import UtfTable
        t = UtfTable(fdec2, base=0)
        print(f'  UTF table: {t.name}, rows: {t.rows_count}, cols: {[c.name for c in t.columns]}')
    except Exception as e:
        print(f'  Not UTF: {str(e)[:60]}')