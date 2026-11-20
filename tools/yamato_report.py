"""yamato_report.py - lista TODAS las apariciones de 'Yamato' en archivos del
juego (raw y XOR 0x5E), con los 8 bytes siguientes."""
import os, re
G = r'D:/Juegos/-SPARROW-/Super Robot Wars V'
XOR=0x5E
pat=re.compile(b'Yamato')
count=0
for root,dirs,files in os.walk(G):
    for f in files:
        p=os.path.join(root,f)
        try: data=open(p,'rb').read()
        except Exception: continue
        for mode,dd in [('raw',data)] + ([('xor',bytes(b^XOR for b in data))] if 'mtzkn' in f.lower() else []):
            for m in pat.finditer(dd):
                count+=1
                tail=dd[m.end():m.end()+10]
                print('%-55s %-4s @%-8d %-30s %s'%(
                    os.path.relpath(p,G)[:55], mode, m.start(),
                    tail.hex(' '),
                    ''.join(chr(x) if 32<=x<127 else '.' for x in tail)))
print('TOTAL:',count)
