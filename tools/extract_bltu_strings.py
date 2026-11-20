#!/usr/bin/env python3
"""Extract all BLTU strings from CMN00 CPK and save to file"""

from srwv_cpk import Cpk
from srwv_bltu import BltuTable
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data

cpk = Cpk('C:/Dev/Default Project/srwv/outputs/CMN00_CPK_traducido.cpk')

raw = cpk.read_file(1)
dec = maybe_decompress(raw)
x = decrypt_data(dec)
bltu = BltuTable(x)

all_strings = bltu.all_strings()
with open('C:/Dev/Default Project/srwv/datos/bltu_strings.txt', 'w', encoding='utf-8') as f:
    for gid, ch_idx, str_idx, s in all_strings:
        f.write(f'{gid}\t{s}\n')

print(f'Extracted {len(all_strings)} BLTU strings')
print('Saved to: C:/Dev/Default Project/srwv/datos/bltu_strings.txt')
