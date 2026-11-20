"""yamato_allcpk.py - escanea TODOS los CPK instalados buscando 'Yamato'
seguido de un byte que el motor pintaria como yen (0x5C o C2 A5 o FF E5).
Incluye decodificacion XOR 0x5E de los CPK MtZkn.
"""
import os, re
G = r'D:/Juegos/-SPARROW-/Super Robot Wars V'
XOR = 0x5E

pat = re.compile(b'Yamato')
yen = (b'\x5c', b'\xc2\xa5', b'\xef\xbf\xa5', b'\xe5\x86\x86')  # \, ¥, Ｙ? no: U+FFE5

def scan(label, data):
    out=[]
    for m in pat.finditer(data):
        tail=data[m.end():m.end()+16]
        ctx=data[max(0,m.start()-10):m.end()+20]
        out.append((m.start(), tail[:6].hex(' '),
                    ''.join(chr(x) if 32<=x<127 else '.' for x in tail[:6]),
                    ''.join(chr(x) if 32<=x<127 else '.' for x in ctx)))
    return out

found=False
for root,dirs,files in os.walk(G):
    for f in files:
        p=os.path.join(root,f)
        low=f.lower()
        if not (low.endswith('.cpk') or low.endswith('.bin')):
            continue
        try:
            data=open(p,'rb').read()
        except Exception:
            continue
        hits=scan('raw',data)
        if not hits and ('mtzkn' in low.lower()):
            hits=scan('xor',bytes(b^XOR for b in data))
        if hits:
            # solo mostrar los que tienen yen justo detras
            suspicious=[h for h in hits if any(h[1].replace(' ','').startswith(y.hex()) for y in yen)]
            if suspicious:
                found=True
                rel=os.path.relpath(p,G)
                print('=== %s'%rel)
                for off,hx,asc,ctx in suspicious[:10]:
                    print('  @%-8d %-18s %-10s ctx=%s'%(off,hx,asc,ctx))
if not found:
    print('NINGUN Yamato seguido de 0x5C/¥ en todos los CPK instalados')
