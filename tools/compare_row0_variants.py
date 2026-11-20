# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

files = {
 'ORIG': r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk',
 'old': r'C:/Dev/Default Project/srwv/outputs/Prologue_half_single.cpk',
 'exact': r'C:/Dev/Default Project/srwv/outputs/Prologue_exact_row0.cpk',
}
cs={k:load(v) for k,v in files.items()}
x=cs['ORIG'].plain(next(r for r in cs['ORIG'].rows if r['id']==0))
for name in ('old','exact'):
    y=cs[name].plain(next(r for r in cs[name].rows if r['id']==0))
    # comparar ultimos 22 bytes de cada slot (meta)
    print('\n===',name,'===')
    for si in range(24):
        base=24+si*70
        mx=x[base+48:base+70]
        my=y[base+48:base+70]
        if mx!=my:
            print(' slot %2d META DIFERENTE:'%si)
            print('   orig',mx.hex(' '))
            print('   var ',my.hex(' '))
    # comparar primeros 24 bytes globales
    if x[:24]!=y[:24]:
        print(' CABECERA 24 DISTINTA:',x[:24].hex(' '),'->',y[:24].hex(' '))
