"""verify_es6.py - verifica el binario es6: lineas Yamato y barras dobles."""
import sys
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from srwv_bltu import load
t=load(open(r'C:/Dev/Default Project/srwv/outputs/cmn_f1_es6.bin','rb').read())
allv=[x[3] for x in t.all_strings()]
print('doble-barra (\\\\) restante:',sum(1 for s in allv if '\\\\' in s))
n=0
for s in allv:
    if 'Yamato' in s:
        print(repr(s[:95])); n+=1
        if n>=8: break
