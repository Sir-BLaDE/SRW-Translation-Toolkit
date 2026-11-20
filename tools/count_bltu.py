#!/usr/bin/env python3
"""Count English vs Spanish strings in BLTU"""

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

english_count = 0
spanish_count = 0
english_only_list = []
spanish_only_list = []
system_terms = []

spanish_chars = set('áéíóúñÁÉÍÓÚÑüÜ¿¡')
english_count_ids = set()
spanish_count_ids = set()

for gid, ch_idx, str_idx, s in all_strings:
    has_spanish = any(c in s for c in spanish_chars)
    is_ascii_only = all(ord(c) < 128 for c in s)
    if is_ascii_only and any(c.isalpha() for c in s):
        english_count += 1
        english_only_list.append((gid, s))
    elif has_spanish or not is_ascii_only:
        spanish_count += 1
        spanish_only_list.append((gid, s))
    # Check for system terms
    lower_s = s.lower()
    if any(k in lower_s for k in ['dummy', 'barrier', 'field', 'armor', 'coat', 'bits', 'driver', 'ammo', 'count', 'mode', 'slot']):
        system_terms.append((gid, s))

print(f'ASCII-only strings (likely English/system): {english_count}')
print(f'Strings with Spanish chars or non-ASCII: {spanish_count}')
print(f'Total: {len(all_strings)}')
print()
print(f'First 30 English-like strings:')
for gid, s in english_only_list[:30]:
    print(f'  {gid}: {repr(s[:60])}')
print()
print(f'First 30 Spanish-like strings:')
for gid, s in spanish_only_list[:30]:
    print(f'  {gid}: {repr(s[:60])}')
print()
print(f'System term-like strings (first 30):')
for gid, s in system_terms[:30]:
    print(f'  {gid}: {repr(s[:60])}')
