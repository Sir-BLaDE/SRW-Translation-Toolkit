"""verify_88.py - confirma que las lineas con doble backslash tenian \n simple
en el original ingles."""
import csv
SRC=r'C:/Dev/Default Project/srwv/datos/lineas_batalla_final.csv'
n=0; mostradas=0
with open(SRC,encoding='utf-8-sig',newline='') as f:
    for row in csv.DictReader(f):
        es=row['es']; en=row['en']
        if '\\\\' in es:
            n+=1
            if mostradas<12:
                print('EN:',repr(en[:80]))
                print('ES:',repr(es[:80]))
                print()
                mostradas+=1
print('total con doble barra en CSV anterior:',n)
