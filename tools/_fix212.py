# -*- coding: utf-8 -*-
"""Acorta traducciones de b034/b035 para que la entrada 212 (tabla L, u16)
vuelva a quedar por debajo de 65.535 bytes de texto plano."""
import json

S = {
    'C:/Dev/Default Project/srwv/datos/es_batches/b035_13300_13699.json': {
        "13300": "Si pudiéramos volver a casa, volvería a hacer lo que hay que hacer.\r\n　Pero no es el caso.",
        "13318": "Malas noticias. Nos avisan del Nadesico que hay criminales en movimiento en Kansai.",
        "13350": "Si Banjo se hiciera público, hasta mi fama de tipo bueno estaría en riesgo.",
        "13424": "Si Banjo se hiciera público, hasta mi fama de tipo bueno estaría en riesgo.",
        "13348": "Si el maestro Banjo publicara sus bienes, la fama del maestro Maito\r\n　como el más rico del mundo peligraría.",
        "13422": "Si el maestro Banjo publicara sus bienes, la fama del maestro Maito\r\n　como el más rico del mundo peligraría.",
        "13362": "Un mayordomo y secretarias guapas. Solo estas dos monadas\r\n　ya le dan ventaja sobre Maito.",
        "13436": "Un mayordomo y secretarias guapas. Solo estas dos monadas\r\n　ya le dan ventaja sobre Maito.",
        "13394": "¿Qu-quién es este? ¿Un demonio? ¿Un demonio con piel humana?",
        "13468": "¿Qu-quién es este? ¿Un demonio? ¿Un demonio con piel humana?",
    },
    'C:/Dev/Default Project/srwv/datos/es_batches/b034_12900_13299.json': {
        "13291": "Ahora que sabe quién causó el accidente de sus padres, considera su próximo paso.",
    },
}

for p, patch in S.items():
    d = json.load(open(p, encoding='utf-8'))
    for k, v in patch.items():
        if k in d:
            d[k] = v
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('aplicado')

# comprobar
import story_build as sb
from story import find_dialogs, rebuild_block
from cpk_util import load
trans = sb.load_translations()
tm = sb.load_tm()
by_entry = sb.load_dialogues()
recs = by_entry['_rec']
per_entry = {}
for i, dd in recs.items():
    per_entry.setdefault(dd['entry'], []).append(dd)
GAME = 'C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk'
cf = load(GAME)
f = [r for r in cf.rows if r['id'] == 212][0]
pt = cf.plain(f)
dialogs = find_dialogs(212, pt)
by_start = {x.start: x for x in dialogs}
ds = per_entry.get(212, [])
out = bytearray(); last = 0
for dd in ds:
    if dd['start'] not in by_start: continue
    es = trans.get(dd['id'])
    if es is None: es = tm.get(dd['text'])
    if es is None: continue
    dlg = by_start[dd['start']]
    out += pt[last:dlg.start]
    out += rebuild_block(dlg.speaker, es)
    last = dlg.end
out += pt[last:]
print('entrada 212 plano:', len(out), '(limite 65535)')
