# -*- coding: utf-8 -*-
"""Auditar qué archivos del juego difieren de sus backups originales."""
import os, hashlib

GAME = r'D:/Juegos/-SPARROW-/Super Robot Wars V'
BAK = r'C:/Dev/Default Project/srwv/backup'

pairs = [
 ('OP.CPK', 'OP_CK_original.cpk'),
 ('CMN00.CPK', 'CMN00_original_20261118.cpk'),
 ('LayoutImage.cpk', 'LayoutImage_original_20261118.cpk'),
 ('LayoutData.cpk', 'LayoutData_original.cpk'),
 ('Prologue.cpk', 'Prologue_original_20261118.cpk'),
 ('SysText.cpk', 'SysText_original.cpk'),
 ('FontInfo.cpk', 'FontInfo_original.cpk'),
 ('STGEST_EN.CPK', 'STGEST_EN_original.cpk'),
 ('MtZkn_Pt.cpk', 'MtZkn_Pt_original.cpk'),
 ('MtZkn_Rt.cpk', 'MtZkn_Rt_original.cpk'),
 ('MtZkn_Nm.cpk', 'MtZkn_Nm_original.cpk'),
 ('lega_zkn.cpk', 'lega_zkn_original.cpk'),
 ('rpw_jstr.cpk', 'rpw_jstr_original.cpk'),
 ('B_LT00_EN.cpk', 'B_LT00_EN_original.cpk'),
 ('LT00_EN.cpk', 'LT00_EN_original.cpk'),
]

def h(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest() if os.path.exists(p) else None

for name, bak in pairs:
    # buscar el archivo en el arbol del juego
    matches=[]
    for root, dirs, files in os.walk(os.path.join(GAME,'Data')):
        if name in files:
            matches.append(os.path.join(root,name))
    for root, dirs, files in os.walk(os.path.join(GAME,'CommonData')):
        if name in files:
            matches.append(os.path.join(root,name))
    bp = os.path.join(BAK,bak)
    if not matches:
        print('%-20s NO ENCONTRADO' % name); continue
    bh = h(bp)
    for m in matches:
        mh = h(m)
        estado = 'ORIGINAL' if mh==bh else 'MODIFICADO'
        print('%-20s %-10s %s' % (name, estado, m.replace(GAME+os.sep,'')))
