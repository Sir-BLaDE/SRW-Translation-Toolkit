"""
tm.py - Memoria de traduccion (texto ingles -> espanol) a partir de los lotes.

Uso:
    python tm.py            # reconstruye datos/es_tm.json
    python tm.py a b        # muestra registros [a,b) SIN traducir todavia
"""
import glob
import json
import os
import sys

JSONL = 'C:/Dev/Default Project/srwv/datos/story_dialogues.jsonl'
BATCHES = 'C:/Dev/Default Project/srwv/datos/es_batches'
TM = 'C:/Dev/Default Project/srwv/datos/es_tm.json'


def load_records():
    with open(JSONL, encoding='utf-8') as fh:
        return [json.loads(line) for line in fh]


def load_batches():
    trans = {}
    if os.path.isdir(BATCHES):
        for p in sorted(glob.glob(BATCHES + '/*.json')):
            with open(p, encoding='utf-8') as fh:
                for k, v in json.load(fh).items():
                    trans[int(k)] = v
    return trans


def build_tm(recs=None, trans=None):
    recs = recs if recs is not None else load_records()
    trans = trans if trans is not None else load_batches()
    tm = {}
    for i, d in enumerate(recs):
        if i in trans:
            tm[d['text']] = trans[i]
    with open(TM, 'w', encoding='utf-8') as fh:
        json.dump(tm, fh, ensure_ascii=False, indent=0, sort_keys=True)
    return tm


def load_tm():
    if os.path.exists(TM):
        with open(TM, encoding='utf-8') as fh:
            return json.load(fh)
    return {}


def show_pending(a, b):
    recs = load_records()
    trans = load_batches()
    tm = {}
    for i, d in enumerate(recs):
        if i in trans:
            tm[d['text']] = trans[i]
    n = 0
    for i in range(a, min(b, len(recs))):
        d = recs[i]
        if i in trans or d['text'] in tm:
            continue
        if d['speaker'].strip().startswith('-----'):
            continue
        n += 1
        print('%d\t%s\t%s' % (i, d['speaker'], json.dumps(d['text'], ensure_ascii=False)))
    sys.stderr.write('pendientes en [%d,%d): %d\n' % (a, b, n))


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        show_pending(int(sys.argv[1]), int(sys.argv[2]))
    else:
        recs = load_records()
        trans = load_batches()
        tm = build_tm(recs, trans)
        real = [d for d in recs if not d['speaker'].strip().startswith('-----')]
        print('registros', len(recs), 'generados', len(trans), 'textos en TM', len(tm))
        print('cubiertos por id o TM:',
              sum(1 for i, d in enumerate(recs)
                  if i in trans or d['text'] in tm))
