#!/usr/bin/env python3
"""Extract and save BLTU strings from CMN00 CPK"""

from srwv_cpk import Cpk
from srwv_bltu import BltuTable
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct

cpk = Cpk('C:/Dev/Default Project/srwv/outputs/CMN00_CPK_traducido.cpk')

# Check both files
for fid in [0, 1]:
    try:
        raw = cpk.read_file(fid)
        dec = maybe_decompress(raw)
        x = decrypt_data(dec)
        print(f'File {fid}: decrypted len={len(x)}')
        # Try BLTU parse
        bltu = BltuTable(x)
        print(f'  BLTU chunks: {len(bltu.chunks)}')
        print(f'  BLTU strings: {len(bltu)}')
        # Print first few strings
        all_strings = bltu.all_strings()
        for i, (gid, ch_idx, str_idx, s) in enumerate(all_strings[:20]):
            print(f'    {i}: gid={gid} chunk={ch_idx} str={str_idx}: {repr(s[:60])}')
    except Exception as e:
        print(f'File {fid}: ERROR - {e}')
