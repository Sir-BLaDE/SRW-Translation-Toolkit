# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")

checks = [
    ("OP.CPK", "Data/BTLC/EN0/OP.CPK", "backup/OP_CK_original.cpk", "outputs/OP_CK_es.cpk"),
    ("CMN00.CPK", "Data/BTLC/EN0/CMN00.CPK", "backup/CMN00_CPK_original.cpk", "outputs/CMN00_CPK_final_es7.cpk"),
    ("1_CMN00.CPK", "Data/BTLC/EN0/1_CMN00.CPK", "backup/CMN00_CPK_original.cpk", "outputs/CMN00_CPK_final_es7.cpk"),
    ("SysText.cpk", "Data/AIDDATA/EN/SysText.cpk", "backup/SysText_antes_es.cpk", "outputs/SysText_es.cpk"),
    ("SysText - copia.cpk", "Data/AIDDATA/EN/SysText - copia.cpk", "backup/SysText_antes_es.cpk", "outputs/SysText_es.cpk"),
    ("FontInfo.cpk", "Data/AIDDATA/EN/FontInfo.cpk", "backup/FontInfo_EN_original.cpk", "outputs/FontInfo_es7.cpk"),
    ("LT00_EN.cpk", "CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk", "backup/LT00_EN_antes_es2.cpk", "outputs/LT00_EN_es2.cpk"),
    ("B_LT00_EN.cpk", "CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk", "backup/B_LT00_EN_original.cpk", "outputs/B_LT00_EN_es.cpk"),
    ("Prologue.cpk", "Data/AIDDATA/EN/Prologue.cpk", "backup/Prologue_EN_original.cpk", "outputs/Prologue_es.cpk"),
    ("lega_zkn.cpk", "CommonData/MtData/EN/lega_zkn.cpk", "backup/lega_zkn_original.cpk", "outputs/lega_zkn_es.cpk"),
    ("rpw_jstr.cpk", "CommonData/MtData/EN/rpw_jstr.cpk", "backup/rpw_jstr_original.cpk", "outputs/rpw_jstr_es.cpk"),
    ("MtZkn_Pt.cpk", "CommonData/MtData/EN/MtZkn_Pt.cpk", "backup/MtZkn_Pt_original.cpk", "outputs/MtZkn_Pt_es_acc2.cpk"),
    ("MtZkn_Rt.cpk", "CommonData/MtData/EN/MtZkn_Rt.cpk", "backup/MtZkn_Rt_original.cpk", "outputs/MtZkn_Rt_es_acc2.cpk"),
    ("MtZkn_Nm.cpk", "CommonData/MtData/EN/MtZkn_Nm.cpk", "backup/MtZkn_Nm_original.cpk", "outputs/MtZkn_Nm_es_acc.cpk"),
    ("KPACK_P4_LN_EN.CPK", "Data/KURODATA/EN/KPACK_P4_LN_EN.CPK", "backup/KPACK_P4_LN_EN_original.cpk", "outputs/KPACK_P4_LN_EN_full_stable2.cpk"),
    ("KPACK_P4_RG_EN.CPK", "Data/KURODATA/EN/KPACK_P4_RG_EN.CPK", "backup/KPACK_P4_RG_EN_original.cpk", "outputs/KPACK_P4_RG_EN_es.cpk"),
    ("1_KPACK_P4_RG_EN.CPK", "Data/KURODATA/EN/1_KPACK_P4_RG_EN.CPK", "backup/KPACK_P4_RG_EN_original.cpk", "outputs/KPACK_P4_RG_EN_es.cpk"),
    ("STGEST_EN.CPK", "Data/STAGE/STGEST_EN.CPK", "backup/STGEST_EN_original.cpk", "outputs/STGEST_EN_es.cpk"),
]

G = "D:/Juegos/-SPARROW-/Super Robot Wars V"
for name, rel, orig, out in checks:
    inst = os.path.join(G, rel)
    if not os.path.exists(inst):
        print("%-25s NOT INSTALLED" % name); continue
    b = open(inst, "rb").read()
    o = open(orig, "rb").read()
    u = open(out, "rb").read()
    status = "ORIG" if b == o else ("MODIFIED" if b == u else "UNKNOWN")
    print("%-25s %s" % (name, status))
