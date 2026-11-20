"""
story_build.py - Aplica las traducciones de historia y reconstruye STGEST_EN.CPK.

Traducciones: datos/story_es.json  ->  {"<n linea jsonl>": "texto en espanol"}
Solo se sustituye el texto entre 「」; se conserva el nombre del hablante.
"""
import json
import os
import sys

from cpk_util import load
from story import find_dialogs, translatable
from srwv_cpkbuild2 import build_ordered

GAME = 'C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk'
JSONL = 'C:/Dev/Default Project/srwv/datos/story_dialogues.jsonl'
TRANS = 'C:/Dev/Default Project/srwv/datos/story_es.json'
BATCHES = 'C:/Dev/Default Project/srwv/datos/es_batches'
STGQUOTED = 'C:/Dev/Default Project/srwv/datos/stgest_quoted_es.json'
STGBRACKET = 'C:/Dev/Default Project/srwv/datos/stgest_bracket_es.json'
OUT = 'C:/Dev/Default Project/srwv/outputs/STGEST_EN_es.cpk'


def load_translations():
    """Une story_es.json y todos los lotes de datos/es_batches/*.json."""
    trans = {}
    if os.path.isdir(BATCHES):
        for fn in sorted(os.listdir(BATCHES)):
            if not fn.endswith('.json'):
                continue
            with open(os.path.join(BATCHES, fn), encoding='utf-8') as fh:
                for k, v in json.load(fh).items():
                    trans[int(k)] = v
    if os.path.exists(TRANS):
        with open(TRANS, encoding='utf-8') as fh:
            for k, v in json.load(fh).items():
                trans[int(k)] = v
    return trans


def load_tm():
    p = 'C:/Dev/Default Project/srwv/datos/es_tm.json'
    if os.path.exists(p):
        with open(p, encoding='utf-8') as fh:
            return json.load(fh)
    return {}


def load_quoted():
    """Cadenas entre comillas (tips y condiciones) ya traducidas."""
    if not os.path.exists(STGQUOTED):
        return {}
    with open(STGQUOTED, encoding='utf-8') as fh:
        return json.load(fh)


def load_brackets():
    """Bloques [[...]] de historia/monologo ya traducidos."""
    if not os.path.exists(STGBRACKET):
        return {}
    with open(STGBRACKET, encoding='utf-8') as fh:
        return json.load(fh)


def apply_brackets(plain, brackets):
    """Sustituye el contenido de los bloques [[...]] conservando los corchetes."""
    hits = 0
    for en, es in brackets.items():
        old = ('[[' + en + ']]').encode('utf-8')
        new = ('[[' + es + ']]').encode('utf-8')
        if old in plain:
            hits += plain.count(old)
            plain = plain.replace(old, new)
    return plain, hits


def apply_quoted(plain, quoted):
    for en, es in quoted.items():
        old = ('"' + en + '"').encode('utf-8')
        new = ('"' + es + '"').encode('utf-8')
        if old in plain:
            plain = plain.replace(old, new)
    return plain


def load_dialogues():
    """Devuelve {entry: [(id, start, end, speaker, body, text)]}."""
    by_entry = {}
    with open(JSONL, encoding='utf-8') as fh:
        for i, line in enumerate(fh):
            d = json.loads(line)
            by_entry.setdefault(d['entry'], []).append(i)
            d['id'] = i
            by_entry.setdefault('_rec', {})[i] = d
    return by_entry


def build(dry=False):
    trans = load_translations()
    tm = load_tm()
    quoted = load_quoted()
    brackets = load_brackets()
    print('traducciones cargadas:', len(trans), '| memoria de traduccion:', len(tm),
          '| cadenas citadas:', len(quoted), '| bloques [[]]:', len(brackets))

    by_entry = load_dialogues()
    recs = by_entry['_rec']
    per_entry = {}
    for i, d in recs.items():
        per_entry.setdefault(d['entry'], []).append(d)

    cf = load(GAME)
    new_files = {}
    replaced = 0
    bracket_hits = 0
    for f in cf.rows:
        pt = cf.plain(f)
        plain = pt
        ds = per_entry.get(f['id'])
        changed_dialog = False
        if ds:
            dialogs = find_dialogs(f['id'], pt)
            # emparejar por start
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
            if hits:
                out = bytearray()
                last = 0
                for dlg, es in sorted(hits, key=lambda x: x[0].start):
                    from story import rebuild_block
                    out += pt[last:dlg.start]
                    out += rebuild_block(dlg.speaker, es)
                    last = dlg.end
                    replaced += 1
                out += pt[last:]
                plain = bytes(out)
                changed_dialog = True
        plain1, n = apply_brackets(plain, brackets) if brackets else (plain, 0)
        bracket_hits += n
        plain2 = apply_quoted(plain1, quoted) if quoted else plain1
        if changed_dialog or plain2 != plain:
            new_files[f['id']] = (cf.cipher(f, plain2), len(plain2))

    print('bloques sustituidos:', replaced, '| bloques [[]]:', bracket_hits,
          '| entradas modificadas:', len(new_files))
    if dry:
        return
    out = build_ordered(GAME, new_files)
    open(OUT, 'wb').write(out)
    print('escrito', len(out), 'bytes ->', OUT)

    # verificacion
    c2 = load(OUT)
    bad = 0
    for fid in list(new_files)[:5]:
        f = [r for r in c2.rows if r['id'] == fid][0]
        pt = c2.plain(f)
        ds = find_dialogs(fid, pt)
        print('  id', fid, 'bloques', len(ds), '->', repr(ds[0].body[:60]) if ds else '')
    return out


if __name__ == '__main__':
    build(dry='--dry' in sys.argv)
