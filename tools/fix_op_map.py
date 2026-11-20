# -*- coding: utf-8 -*-
p = r"C:/Dev/Default Project/srwv/tools/op_build.py"
data = open(p, "rb").read()

# Replace the specific MAP entries
replacements = [
    (b'"Wolfgang Subordinate": "Subalterno de Wolfgang"', b'"Wolfgang Subordinate": "Subalterno Wolfgang"'),
    (b'"Gamillas Captain": "Capit\xc3\xa1n Gamillas"', b'"Gamillas Captain": "Cap. Gamillas"'),
    (b'"Tenth Angel": "D\xc3\xa9cimo \xc3\x81ngel"', b'"Tenth Angel": "10. Angel"'),
    (b'"Metal Beast": "Bestia Mec\xc3\xa1nica"', b'"Metal Beast": "Bestia Mec"'),
]

for old, new in replacements:
    if old in data:
        data = data.replace(old, new)
        print("replaced:", old[:40])
    else:
        print("NOT FOUND:", old[:40])

open(p, "wb").write(data)
print("done")
