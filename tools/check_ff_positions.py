# -*- coding: utf-8 -*-
"""Comparar posiciones de FF FF (centinelas) en original vs traducidos."""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

FILES = {
 'ORIG': r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk',
 'v7'  : r'C:/Dev/Default Project/srwv/outputs/Prologue_es_inplace_v7.cpk',
 'ascii': r'C:/Dev/Default Project/srwv/outputs/Prologue_es_inplace_ascii.cpk',
}
cs = {k: load(v) for k, v in FILES.items()}

for r in cs['ORIG'].rows:
    fid = r['id']
    base = cs['ORIG'].plain(r)
    poses = [i for i in range(len(base)-1) if base[i:i+2] == b'\xff\xff']
    if not poses:
        continue
    print('fila %d: %d centinelas en orig @ %s' % (fid, len(poses), poses[:12]))
    for name in ('v7','ascii'):
        p = cs[name].plain(next(q for q in cs[name].rows if q['id']==fid))
        pp = [i for i in range(len(p)-1) if p[i:i+2] == b'\xff\xff']
        same = pp == poses
        print('   %-6s %d centinelas @ %s  %s' % (name, len(pp), pp[:12], 'IGUAL' if same else 'DIFERENTE'))
