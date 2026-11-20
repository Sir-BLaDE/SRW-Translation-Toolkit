"""fix_double_backslash.py - corrige \\n -> \n (barra doble -> simple) en la
traduccion de batalla. Una barra doble hace que el motor pinte un '¥' (0x5C
se dibuja como yen en la fuente japonesa) antes del salto de linea.
"""
import csv, re, os
SRC=r'C:/Dev/Default Project/srwv/datos/lineas_batalla_final.csv'
DST=r'C:/Dev/Default Project/srwv/datos/lineas_batalla_final_es6.csv'

def fix(s):
    # en el CSV los saltos estan escritos como dos caracteres backslash + n
    # sustituirsecuencias duplicadas por una sola
    n=0
    def rep(m):
        nonlocal n
        n+=1
        return m.group(0)[:len(m.group(0))//2]
    s2=re.sub(r'(?:\\\\){2,}',rep,s)
    s2=s2.replace('\\\\','\\')
    return s2,n

rows=[]
changed=0
with open(SRC,encoding='utf-8-sig',newline='') as f:
    r=csv.reader(f)
    hdr=next(r)
    for row in r:
        if len(row)>=3:
            new,c=fix(row[2])
            if c: changed+=1
            row[2]=new
        rows.append(row)
with open(DST,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(hdr); w.writerows(rows)
print('filas cambiadas:',changed)
# mostrar algunas
for row in rows:
    if 'Yamato' in row[2] and ('\\\\' in row[2] or '\\' in row[2]):
        print(repr(row[2][:100])); break
