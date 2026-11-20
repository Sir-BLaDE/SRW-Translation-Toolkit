"""
story_extract.py - Extrae todos los dialogos de STGEST a JSONL y estadisticas.
"""
import json
import re

from cpk_util import load
from story import find_dialogs, translatable

PATH = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
OUT = 'C:/Dev/Default Project/srwv/datos/story_dialogues.jsonl'
OUT_STATS = 'C:/Dev/Default Project/srwv/datos/story_stats.txt'
BLOCK = re.compile(rb'\[\[(.*?)\]\]', re.S)


def main():
    c = load(PATH)
    n = 0
    with open(OUT, 'w', encoding='utf-8') as fh:
        for f in c.rows:
            pt = c.plain(f)
            ds = find_dialogs(f['id'], pt)
            for d in ds:
                fh.write(json.dumps({
                    'entry': f['id'], 'start': d.start, 'end': d.end,
                    'speaker': d.speaker, 'body': d.body,
                    'text': translatable(d),
                }, ensure_ascii=False) + '\n')
                n += 1
    # bloques sin comillas japonesas que parezcan texto natural
    plain_blocks = 0
    plain_text = 0
    for f in c.rows:
        pt = c.plain(f)
        for m in BLOCK.finditer(pt):
            t = m.group(1)
            if b'\xe3\x80\x8c' in t:
                continue
            if re.search(rb'[A-Za-z]{3,}\s+[A-Za-z]{3,}\s+[A-Za-z]{3,}', t):
                plain_blocks += 1
                plain_text += len(t)
    with open(OUT_STATS, 'w', encoding='utf-8') as fh:
        fh.write('dialogos: %d\n' % n)
        fh.write('bloques [[...]] con texto natural pero sin comillas: %d (%d bytes)\n' % (plain_blocks, plain_text))
    print('dialogos', n, '| bloques naturales sin comillas', plain_blocks, plain_text)


if __name__ == '__main__':
    main()
