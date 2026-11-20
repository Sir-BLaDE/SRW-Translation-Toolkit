import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data

def extract_all_printable_strings(path, min_len=3):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
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
        if len(s) >= min_len:
            try:
                strings.append(s.decode('ascii'))
            except:
                pass
    return strings

spanish = extract_all_printable_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')
english = extract_all_printable_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk')

print('Spanish printable strings:', len(spanish))
print('English printable strings:', len(english))

spanish_set = set(spanish)
english_set = set(english)
only_english = english_set - spanish_set
only_spanish = spanish_set - english_set

print(f'Strings only in English: {len(only_english)}')
print(f'Strings only in Spanish: {len(only_spanish)}')

# Write English-only strings to a file for translation
with open('C:/Dev/Default Project/srwv/datos/english_only_lt00.txt', 'w') as f:
    for s in sorted(only_english):
        f.write(s + '\n')

print('\nFirst 30 English-only strings:')
for s in sorted(only_english)[:30]:
    print(f'  {repr(s[:60])}')

print('\nFirst 30 Spanish-only strings:')
for s in sorted(only_spanish)[:30]:
    print(f'  {repr(s[:60])}')
