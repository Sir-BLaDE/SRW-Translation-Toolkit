import sys, time
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import story_build as sb
from story import find_dialogs, rebuild_block
from cpk_util import load, inflate
from crilayla import ReverseBitReader
import crilayla_compress_c as slow
import crilayla_compress_fast as fast

IDS = [122, 255, 303, 546]
trans = sb.load_translations()
tm = sb.load_tm()
recs = sb.load_dialogues()['_rec']
per = {}
for i, d in recs.items():
    per.setdefault(d['entry'], []).append(d)
cf = load(sb.GAME)

for fid in IDS:
    f = [x for x in cf.rows if x['id'] == fid][0]
    pt = cf.plain(f)
    dialogs = find_dialogs(fid, pt)
    by_start = {d.start: d for d in dialogs}
    hits = []
    for d in per.get(fid, []):
        if d['start'] not in by_start:
            continue
        es = trans.get(d['id'])
        if es is None:
            es = tm.get(d['text'])
        if es is not None:
            hits.append((by_start[d['start']], es))
    out = bytearray()
    last = 0
    for dlg, es in sorted(hits, key=lambda x: x[0].start):
        out += pt[last:dlg.start]
        out += rebuild_block(dlg.speaker, es)
        last = dlg.end
    out += pt[last:]
    plain = bytes(out)
    print('id', fid, 'hits', len(hits), 'plain', len(plain), flush=True)
    for name, comp in (('slow', slow), ('fast', fast)):
        t = time.time()
        blob = comp.compress(plain)
        body, csize = __import__('struct').unpack_from('<II', blob, 8)
        try:
            data = inflate(blob[16:16+csize], blob[16+csize:16+csize+256], body)
            ok = data == plain
            err = ''
        except Exception as e:
            ok = False
            err = str(e)
        print('  %s len=%d time=%.1fs roundtrip=%s %s' % (name, len(blob), time.time()-t, ok, err), flush=True)
