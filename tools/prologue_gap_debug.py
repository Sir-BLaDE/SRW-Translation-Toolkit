# -*- coding: utf-8 -*-
import sys, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full.json', encoding='utf-8'))
rd=d['1']; si=3
s=rd['rows'][si]
print('slot',si,'meta',s['meta'],'parts:',s['parts'])
print('longitudes:',[(len(p.encode()),p[:40]) for p in s['parts']])
