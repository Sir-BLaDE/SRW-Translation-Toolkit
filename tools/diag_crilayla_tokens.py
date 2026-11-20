import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from crilayla import ReverseBitReader, _read_match_length, PREFIX_SIZE
from srwv_crypto import encrypt_data
import story_build as sb
from story import find_dialogs, rebuild_block
import crilayla_compress_fast as fast

fid = int(sys.argv[1]) if len(sys.argv) > 1 else 122
# reconstruir el plano igual que story_build
trans = sb.load_translations(); tm = sb.load_tm()
recs = sb.load_dialogues()['_rec']; per = {}
for i, d in recs.items(): per.setdefault(d['entry'], []).append(d)
cf = load(sb.GAME); f = [x for x in cf.rows if x['id'] == fid][0]
pt = cf.plain(f); by_start = {d.start: d for d in find_dialogs(fid, pt)}
out = bytearray(); last = 0
for d in per.get(fid, []):
    if d['start'] not in by_start: continue
    es = trans.get(d['id'])
    if es is None: es = tm.get(d['text'])
    if es is not None:
        dlg = by_start[d['start']]
        out += pt[last:dlg.start]; out += rebuild_block(dlg.speaker, es); last = dlg.end
out += pt[last:]
enc = encrypt_data(bytes(out))
blob = fast.compress(enc)
body, csize = struct.unpack_from('<II', blob, 8)
payload = blob[16:16+csize]
print('body', body, 'csize', csize, 'payload', len(payload), 'prefix', blob[16+csize:16+csize+8].hex())

# decoder instrumentado
reader = ReverseBitReader(payload)
written = 0
tokens = []
try:
    while written < body:
        marker = reader.read(1)
        if marker == 0:
            reader.read(8); written += 1; tokens.append(('L', written))
            continue
        off = reader.read(13)
        ln = _read_match_length(reader)
        tokens.append(('M', off, ln, written))
        written += ln
except Exception as e:
    import traceback
    traceback.print_exc()
    print('DECODE FAIL', e, 'written', written, 'de', body, 'tokens', len(tokens),
          'reader.index', reader.index, 'bit_count', reader.bit_count)
    print('ultimos tokens', tokens[-8:])
else:
    print('DECODE OK written', written, 'tokens', len(tokens))

# comprimir registrando longitud maxima de la cola de bits
def compress_tokens(src):
    srclen = len(src); pos = {}
    for p in range(srclen - 2):
        pos.setdefault(src[p:p+3], []).append(p)
    buflen = srclen * 2 + 0x100; dest = bytearray(buflen)
    n = srclen - 1; m = buflen - 1; d = 0; T = 0; maxt = 0; toks = []
    while n >= 0x100:
        j = min(srclen, n + 3 + 0x2000)
        p = q = 0
        for pp in pos.get(src[n-2:n+1], []):
            i = pp + 2
            if not (n + 1 <= pp < j - 2): continue
            k = 0
            while k <= n - 0x100 and src[n-k] == src[i-k]: k += 1
            if k > p: p, q = k, i - n - 3
        if p < 3:
            d = (d << 9) | src[n]; n -= 1; T += 9; toks.append(('L', src[n] if False else None))
        else:
            d = (((d << 1) | 1) << 13) | q; T += 14; n -= p
            if p < 6: d = (d << 2) | (p-3); T += 2
            elif p < 13: d = (((d << 2) | 3) << 3) | (p-6); T += 5
            elif p < 44: d = (((d << 5) | 0x1f) << 5) | (p-13); T += 10
            else:
                d = (d << 10) | 0x3ff; T += 10; p -= 44
                while True:
                    while T >= 8:
                        dest[m] = (d >> (T-8)) & 0xff; m -= 1; T -= 8
                        d &= (1 << T) - 1 if T else 0
                    if p < 255: break
                    d = (d << 8) | 0xff; T += 8; p -= 0xff
                d = (d << 8) | p; T += 8
            toks.append(('M', q, p))
        maxt = max(maxt, T)
        while T >= 8:
            dest[m] = (d >> (T-8)) & 0xff; m -= 1; T -= 8
            d &= (1 << T) - 1 if T else 0
    return toks, maxt

toks, maxt = compress_tokens(enc)
print('COMPRESS tokens', len(toks), 'maxT', maxt, 'ultimos', toks[-8:])
