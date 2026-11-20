import sys, struct, time
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import story_build as sb
from story import find_dialogs, rebuild_block
from cpk_util import load, inflate, CpkFiles
from srwv_crypto import encrypt_data, decrypt_data
import crilayla_compress_c as slow
import crilayla_compress_fast as fast
from crilayla import decompress

fid = int(sys.argv[1]) if len(sys.argv) > 1 else 122
trans = sb.load_translations(); tm = sb.load_tm()
recs = sb.load_dialogues()['_rec']
per = {}
for i, d in recs.items(): per.setdefault(d['entry'], []).append(d)
cf = load(sb.GAME)
f = [x for x in cf.rows if x['id'] == fid][0]
pt = cf.plain(f)
by_start = {d.start: d for d in find_dialogs(fid, pt)}
out = bytearray(); last = 0
hits = []
for d in per.get(fid, []):
    if d['start'] not in by_start: continue
    es = trans.get(d['id'])
    if es is None: es = tm.get(d['text'])
    if es is not None: hits.append((by_start[d['start']], es))
for dlg, es in sorted(hits, key=lambda x: x[0].start):
    out += pt[last:dlg.start]; out += rebuild_block(dlg.speaker, es); last = dlg.end
out += pt[last:]
plain = bytes(out)
enc = encrypt_data(plain)
print('id', fid, 'plain', len(plain), 'enc', len(enc), flush=True)

new = load(r'C:/Dev/Default Project/srwv/outputs/STGEST_EN_es.cpk')
nf = [x for x in new.rows if x['id'] == fid][0]
stored = new.raw(nf)
print('stored size', len(stored), 'header', stored[:16].hex(), flush=True)

for name, comp in (('slow', slow), ('fast', fast)):
    t = time.time(); blob = comp.compress(enc)
    print(name, 'len', len(blob), 'same_as_stored', blob == stored, 'time %.1f' % (time.time()-t), flush=True)
    body, csize = struct.unpack_from('<II', blob, 8)
    for dn, dec in (('inflate', lambda b: inflate(b[16:16+csize], b[16+csize:16+csize+256], body)),
                    ('decompress', decompress)):
        try:
            got = dec(blob)
            print('  ', dn, 'ok', got == enc, flush=True)
        except Exception as e:
            print('  ', dn, 'FAIL', e, flush=True)
