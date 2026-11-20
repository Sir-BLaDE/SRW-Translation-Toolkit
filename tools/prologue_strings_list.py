"""prologue_strings_list.py - lista cadenas unicas de narracion con longitud."""
import sys, json, collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full.json', encoding='utf-8'))
seen = collections.OrderedDict()
for rid in [0,1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]:
    rd = d[str(rid)]
    for row in rd['rows']:
        for s in row['parts']:
            s = s.strip()
            if len(s) < 4: continue
            if s not in seen:
                seen[s] = []
            if rid not in seen[s]:
                seen[s].append(rid)
print('unicas (no creditos):', len(seen))
for s, rows in seen.items():
    print('%3d filas=%-14s | %s' % (len(s), ','.join(map(str,rows))[:14], s))
