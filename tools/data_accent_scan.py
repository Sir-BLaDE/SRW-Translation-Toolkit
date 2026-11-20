import pathlib, re, os
root=pathlib.Path(r'C:/Dev/Default Project/srwv/datos')
pat=re.compile(r'[áéíóúñÁÉÍÓÚü¿¡]')
for p in sorted(root.rglob('*')):
    if p.is_file() and p.suffix.lower() in ('.json','.csv','.txt','.md'):
        try: s=p.read_text(encoding='utf-8-sig')
        except Exception: continue
        n=len(pat.findall(s))
        if n>=0:
            print('%-55s %8d acc=%6d'%(str(p.relative_to(root)),p.stat().st_size,n))
