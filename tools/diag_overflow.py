import json, os, sys
from cpk_util import load

GAME = 'C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk'
JSONL = 'C:/Dev/Default Project/srwv/datos/story_dialogues.jsonl'
BATCHES = 'C:/Dev/Default Project/srwv/datos/es_batches'
TRANS = 'C:/Dev/Default Project/srwv/datos/story_es.json'
TM = 'C:/Dev/Default Project/srwv/datos/es_tm.json'

from story import find_dialogs

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
print('filas:', len(cf.rows))
# distribucion de tablas
from collections import Counter
print(Counter(f['table'] for f in cf.rows))

# solo entradas de tabla L
for f in cf.rows:
    if f['table'] != 'CpkItocL':
        continue
    ds = by_entry.get(f['id'])
    if not ds:
        continue
    pt = cf.plain(f)
    dialogs = find_dialogs(f['id'], pt)
    by_start = {d.start: d for d in dialogs}
    hits = []
    for d in ds:
        if d['start'] not in by_start:
            continue
        es = trans.get(d['id'])
        if es is None:
            es = tm.get(d['text'])
        if es is not None:
            hits.append((by_start[d['start']], es))
    if not hits:
        continue
    from story import rebuild_block
    out = bytearray()
    last = 0
    for dlg, es in sorted(hits, key=lambda x: x[0].start):
        out += pt[last:dlg.start]
        out += rebuild_block(dlg.speaker, es)
        last = dlg.end
    out += pt[last:]
    plain = bytes(out)
    blob = cf.cipher(f, plain)
    fs = len(blob)
    ex = len(plain)
    if fs > 65535 or ex > 65535:
        print('OVERFLOW id', f['id'], 'tabla L | FileSize', fs, '| ExtractSize', ex)
