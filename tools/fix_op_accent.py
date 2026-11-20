# -*- coding: utf-8 -*-
p = r"C:/Dev/Default Project/srwv/tools/op_build.py"
data = open(p, "rb").read()
data = data.replace(b"Soldado de J\xc3\xbapiter", b"Soldado de Jupiter")
open(p, "wb").write(data)
print("done" if b"Soldado de Jupiter" in data else "FAIL")
# verify
for line in data.split(b'\n'):
    if b'Jupiter Empire' in line:
        print(line.decode('utf-8','replace'))
