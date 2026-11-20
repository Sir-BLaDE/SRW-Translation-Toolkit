#!/usr/bin/env python3
"""Examine Prologue.cpk and SysText.cpk structures"""

from srwv_cpk import Cpk
import os

pro = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDADATA/EN/Prologue.cpk'
sys = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDADATA/EN/SysText.cpk'
font = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDADATA/EN/FontInfo.cpk'

for path in [pro, sys, font]:
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
