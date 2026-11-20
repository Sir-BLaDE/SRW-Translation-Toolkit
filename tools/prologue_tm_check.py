import json,re
en=json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_en.json',encoding='utf-8'))
tm=json.load(open(r'C:/Dev/Default Project/srwv/datos/es_tm.json',encoding='utf-8'))
print('tm size',len(tm))
hit=[s for s in en if s in tm]
print('exact hits',len(hit),'of',len(en))
for s in hit[:15]: print(' ',repr(s[:70]),'->',repr(tm[s][:70]))
