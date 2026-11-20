import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
from lt00 import load

BASE = 'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/'


def plaintext(path):
    return decrypt_data(maybe_decompress(Cpk(path).read_file(0)))


en = load(plaintext(BASE + 'B_LT00_EN.cpk'))
cur = load(plaintext(BASE + 'LT00_EN.cpk'))
bak = load(plaintext(r'C:/Dev/Default Project/srwv/backup/LT00_EN_instalado_antes.cpk'))
es = load(plaintext(r'C:/Dev/Default Project/srwv/outputs/LT00_EN_es.cpk'))
print('counts', en.count, cur.count, bak.count, es.count)
print('cur==bak', cur.strings == bak.strings)
print('cur==en', cur.strings == en.strings)
print('es==cur', es.strings == cur.strings)
print('len es blob', es.blob_end - es.blob_start, 'cur', cur.blob_end - cur.blob_start)
diff = [(i, en.strings[i], cur.strings[i]) for i in range(min(en.count, cur.count))
        if en.strings[i] != cur.strings[i]]
print('diferencias en vs cur:', len(diff))
for d in diff[:8]:
    print(d[0], repr(d[1])[:60], '->', repr(d[2])[:60])
dif2 = [(i, cur.strings[i], es.strings[i]) for i in range(min(cur.count, es.count))
        if cur.strings[i] != es.strings[i]]
print('diferencias cur vs es:', len(dif2))
for d in dif2[:8]:
    print(d[0], repr(d[1])[:60], '->', repr(d[2])[:60])
