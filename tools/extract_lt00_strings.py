import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
import struct, re

def extract_all_printable_strings(path, min_len=3):
    """Extract all printable ASCII strings from the decrypted CPK file."""
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    
    strings = []
    # Find sequences of printable ASCII characters
    i = 0
    while i < len(x):
        # Skip non-printable bytes
        if not (32 <= x[i] < 127):
            i += 1
            continue
        
        # Start of a potential string
        start = i
        while i < len(x) and 32 <= x[i] < 127:
            i += 1
        
        s = x[start:i]
        if len(s) >= min_len:
            try:
                strings.append(s.decode('ascii'))
            except:
                pass
    
    return strings

# Extract from both versions
spanish = extract_all_printable_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')
english = extract_all_printable_strings(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk')

print('Spanish printable strings:', len(spanish))
print('English printable strings:', len(english))

# Show first 30 from each
print('\n=== First 30 Spanish strings ===')
for s in spanish[:30]:
    print(f'  {repr(s[:60])}')

print('\n=== First 30 English strings ===')
for s in english[:30]:
    print(f'  {repr(s[:60])}')

# Find strings only in English
spanish_set = set(spanish)
english_set = set(english)
only_english = english_set - spanish_set
only_spanish = spanish_set - english_set

print(f'\nStrings only in English: {len(only_english)}')
print(f'Strings only in Spanish: {len(only_spanish)}')

# Show some only in English
print('\n=== Only in English (first 20) ===')
for s in list(only_english)[:20]:
    print(f'  {repr(s[:60])}')

# Show some only in Spanish
print('\n=== Only in Spanish (first 20) ===')
for s in list(only_spanish)[:20]:
    print(f'  {repr(s[:60])}')