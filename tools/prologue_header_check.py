# -*- coding: utf-8 -*-
import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
paths = {
 'EN':r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk',
 'ES':r'C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk',
 'JP':r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/JP/Prologue.cpk',
}
for rid in [1,2,5,6]:
    print('\n=== fila %d ==='%rid)
    for lang,p in paths.items():
        c=load(p); r=[x for x in c.rows if x['id']==rid][0]; pt=c.plain(r)
        cnt=struct.unpack_from('<H',pt,0)[0]
        slot=(len(pt)-24)//cnt
        head=pt[:24]
        print(' %-3s len=%-7d cnt=%-4d slot=%-4d head=%s'%(lang,len(pt),cnt,slot,head.hex(' ')))
