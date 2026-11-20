import csv, re
p=r'C:/Dev/Default Project/srwv/datos/lineas_batalla.csv'
a=b=c=d=0
samples=[]
for r in csv.DictReader(open(p,encoding='utf-8-sig',newline='')):
    en,es=r['en'],r['es']
    if not es: continue
    if '\\n' in en:
        a+=1
        if '\\n' not in es:
            b+=1
            if len(samples)<10: samples.append((r['id'],en,es))
    if ', ¡' in es or '¡¡' in es or '! ¡' in es: c+=1
    if re.search(r'\b(brace|the|a|and)\b',es) and re.search(r'\b(brace)\b',es): d+=1
print('EN con \\n:',a,'ES sin \\n:',b,'ES con ¡ redundante:',c,'con brace:',d)
for x in samples: print(x[0],repr(x[1][:90]),'->',repr(x[2][:90]))
