"""prologue_dump.py - volca todas las cadenas legibles de Prologue.cpk EN."""
import sys,re
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c=load(p)
for r in c.rows:
    pt=c.plain(r)
    # dividir por nulos y quedarse con cadenas imprimibles razonables
    parts=pt.split(b'\x00')
    ss=[]
    for x in parts:
        try: s=x.decode('utf-8')
        except Exception: continue
        s=''.join(ch if (ch.isprintable() or ch in '\n\r\t　') else '.' for ch in s)
        s=s.strip(' \t\r\n.　')
        if len(s)>=4: ss.append(s)
    if ss:
        print('\n===== FILA %d (%d cadenas) ====='%(r['id'],len(ss)))
        for s in ss:
            print('  |'+s)
