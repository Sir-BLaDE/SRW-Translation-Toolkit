# -*- coding: utf-8 -*-
"""Comparar tamanos de fila de MtZkn instalado vs original."""
import os, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

G = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN'
B = r'C:/Dev/Default Project/srwv/backup'
pairs = [
 ('MtZkn_Pt.cpk','MtZkn_Pt_original.cpk'),
 ('MtZkn_Rt.cpk','MtZkn_Rt_original.cpk'),
 ('MtZkn_Nm.cpk','MtZkn_Nm_original.cpk'),
 ('MtZkn_Rt.cpk','MtZkn_Rt_original.cpk'),
]
for name, bak in pairs:
    cur = os.path.join(G, name)
    orig = os.path.join(B, bak)
    if not os.path.exists(cur) or not os.path.exists(orig):
        print(name, 'FALTA'); continue
    a, b = load(orig), load(cur)
    da = {r['id']: len(a.plain(r)) for r in a.rows}
    db = {r['id']: len(b.plain(r)) for r in b.rows}
    diffs = [(i, da.get(i), db.get(i)) for i in sorted(set(da)|set(db)) if da.get(i)!=db.get(i)]
    print('%-16s filas %d/%d  longitudes distintas: %d' % (name, len(a.rows), len(b.rows), len(diffs)))
    if diffs[:5]: print('  ejemplos', diffs[:5])
