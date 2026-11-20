#!/usr/bin/env python3
"""Extract strings from Prologue.cpk to begin story translation"""

from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data

pro = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data\\AIDDATA/EN/Prologue.cpk'

c = Cpk(pro)
print('Files in Prologue.cpk:', c.files_count)

# Extract strings from each file
for f in c.file_list():
    fid = f['id']
    raw = c.read_file(fid)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    # Extract printable ASCII strings
    strings = []
    i = 0
    while i < len(x):
        if not (32 <= x[i] < 127):
            i += 1
            continue
        start = i
        while i < len(x) and 32 <= x[i] < 127:
            i += 1
        s = x[start:i]
        if len(s) >= 3:
            try:
                strings.append(s.decode('ascii'))
            except:
                pass
    
    print(f'File {fid}: {len(strings)} strings')
    if len(strings) > 0:
        for s in strings[:10]:
            print(f'  {repr(s[:60])}')

print('\nPrologue extraction complete.')
