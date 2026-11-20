import json, os
from cpk_util import load
from story import find_dialogs

GAME = 'C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk'
JSONL = 'C:/Dev/Default Project/srwv/datos/story_dialogues.jsonl'
BATCHES = 'C:/Dev/Default Project/srwv/datos/es_batches'
TRANS = 'C:/Dev/Default Project/srwv/datos/story_es.json'
TM = 'C:/Dev/Default Project/srwv/datos/es_tm.json'

def load_translations():
    trans = {}
    for fn in sorted(os.listdir(BATCHES)):
        if fn.endswith('.json'):
            with open(os.path.join(BATCHES, fn), encoding='utf-8') as fh:
                for k, v in json.load(fh).items():
                    trans[int(k)] = v
    if os.path.exists(TRANS):
        with open(TRANS, encoding='utf-8') as fh:
            for k, v in json.load(fh).items():
                trans[int(k)] = v
    return trans

def load_tm():
    if os.path.exists(TM):
        with open(TM, encoding='utf-8') as fh:
            return json.load(fh)
    return {}

def load_dialogues():
    by_entry = {}
    with open(JSONL, encoding='utf-8') as fh:
        for i, line in enumerate(fh):
            d = json.loads(line)
            d['id'] = i
            by_entry.setdefault(d['entry'], []).append(d)
    return by_entry

trans = load_translations()
tm = load_tm()
by_entry = load_dialogues()

cf = load(GAME)
f = [r for r in cf.rows if r['id'] == 374][0]
pt = cf.plain(f)
dialogs = find_dialogs(374, pt)
by_start = {d.start: d for d in dialogs}
ds = by_entry.get(374, [])
rows = []
for d in ds:
    if d['start'] not in by_start:
        continue
    es = trans.get(d['id'])
    if es is None:
        es = tm.get(d['text'])
    if es is not None:
        dlg = by_start[d['start']]
        rows.append((d['id'], len(dlg.body), len(es), len(es)-len(dlg.body), es))

rows.sort(key=lambda x: -x[3])
total_delta = sum(r[3] for r in rows)
print('total delta', total_delta, '| bloques', len(rows))
for rid, o, n, delta, es in rows[:40]:
    print(rid, 'orig', o, 'nuevo', n, 'delta', delta, '|', es[:60].replace('\\r\\n',' '))
