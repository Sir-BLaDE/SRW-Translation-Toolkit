import io
ls = io.open(r'C:/Dev/Default Project/srwv/datos/kpack_rg_groups.txt', encoding='utf-8').read().splitlines()
cur = ''
for l in ls:
    if l.startswith('### '):
        cur = l
    elif l.split('\t')[0] in ('497', '498', '499', '500', '501', '502', '503'):
        print(cur, '|', l)
