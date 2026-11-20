#!/usr/bin/env python3
"""Find exact paths for AIDADATA files"""

import os

base = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
candidates = [
    'AIDDATA/EN/Prologue.cpk',
    'AIDDATA/EN/SysText.cpk',
    'AIDDATA/EN/FontInfo.cpk',
    'AIDDATA/COMMON/PrologueImage.cpk',
    'AIDDATA/COMMON/SysText - copia.cpk',
    'AIDDATA/COMMON/ButtonHintsSTEAM.cpk',
]

for c in candidates:
    fp = os.path.join(base, c)
    if os.path.exists(fp):
        print('EXISTS:', fp)
    else:
        print('NOT FOUND:', fp)

print()
print('Listing AIDADATA directories:')
for root, dirs, files in os.walk(base + '/AIDATA'):
    for d in dirs:
        print('DIR:', os.path.join(root, d))
    for fn in files:
        if fn.endswith('.cpk'):
            print('FILE:', os.path.join(root, fn))
