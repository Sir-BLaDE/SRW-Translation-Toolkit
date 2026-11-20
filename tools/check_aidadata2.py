#!/usr/bin/env python3
"""Examine Prologue.cpk and SysText.cpk structures with correct paths"""

from srwv_cpk import Cpk

paths = [
    'D:/Juegos/-SPARROW-/Super Robot Wars V/Data\\AIDDATA/EN/Prologue.cpk',
    'D:/Juegos/-SPARROW-/Super Robot Wars V/Data\\AIDDATA/EN/SysText.cpk',
    'D:/Juegos/-SPARROW-/Super Robot Wars V/Data\\AIDDATA/EN/FontInfo.cpk',
    'D:/Juegos/-SPARROW-/Super Robot Wars V/Data\\AIDDATA/COMMON/PrologueImage.cpk',
    'D:/Juegos/-SPARROW-/Super Robot Wars V/Data\\AIDDATA/COMMON/ButtonHintsSTEAM.cpk',
]

for path in paths:
    print(f'=== {path} ===')
    try:
        c = Cpk(path)
        print('  version:', c.version)
        print('  files:', c.files_count)
        for f in c.file_list():
            print('  ', f)
    except Exception as e:
        print('  ERROR:', e)
    print()
