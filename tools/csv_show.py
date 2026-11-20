import sys, csv
p=sys.argv[1]; ids=set(sys.argv[2:])
for r in csv.DictReader(open(p,encoding='utf-8-sig',newline='')):
    if r['id'] in ids:
        print('ID',r['id']); print(' EN',repr(r['en'])); print(' ES',repr(r['es']))
