import sys, csv
ids=set(sys.argv[1:])
with open(r'C:/Dev/Default Project/srwv/datos/lineas_batalla.csv',encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        if r['id'] in ids:
            print('ID',r['id'])
            print(' EN',repr(r['en']))
            print(' ES',repr(r['es']))
