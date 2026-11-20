# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

# Map of translated CPK -> original backup
pairs = [
 ("outputs/SysText_es.cpk", "backup/SysText_antes_es.cpk"),
 ("outputs/LT00_EN_es2.cpk", "backup/LT00_EN_antes_es2.cpk") if os.path.exists("backup/LT00_EN_antes_es2.cpk") else ("outputs/LT00_EN_es2.cpk","backup/LT00_EN_instalado_antes.cpk"),
 ("outputs/B_LT00_EN_es.cpk", "backup/B_LT00_EN_original.cpk"),
 ("outputs/MtZkn_Pt_es_acc2.cpk", "backup/MtZkn_Pt_original.cpk"),
 ("outputs/MtZkn_Rt_es_acc2.cpk", "backup/MtZkn_Rt_original.cpk"),
 ("outputs/MtZkn_Nm_es_acc.cpk", "backup/MtZkn_Nm_original.cpk"),
 ("outputs/rpw_jstr_es.cpk", "backup/rpw_jstr_original.cpk"),
 ("outputs/lega_zkn_es.cpk", "backup/lega_zkn_original.cpk"),
 ("outputs/OP_CK_es.cpk", "backup/OP_CK_original.cpk"),
 ("outputs/CMN00_CPK_final_es7.cpk", "backup/CMN00_CPK_original.cpk"),
 ("outputs/STGEST_EN_es.cpk", "backup/STGEST_EN_original.cpk"),
 ("outputs/KPACK_P4_LN_EN_full_stable2.cpk", "backup/KPACK_P4_LN_EN_original.cpk"),
 ("outputs/KPACK_P4_RG_EN_es.cpk", "backup/KPACK_P4_RG_EN_original.cpk"),
 ("outputs/Prologue_es.cpk", "backup/Prologue_EN_original.cpk"),
]

for trans, orig in pairs:
 if not os.path.exists(trans) or not os.path.exists(orig):
  print(trans, "MISSING"); continue
 cf_t = load(trans)
 cf_o = load(orig)
 pt_t = b"".join(cf_t.plain(r) for r in cf_t.rows)
 pt_o = b"".join(cf_o.plain(r) for r in cf_o.rows)
 # Find strings in original that are longer in translation
 # Simple approach: find all NUL-terminated strings in both
 def strings(data):
  out=[];start=0
  for i in range(len(data)):
   if data[i]==0:
    if i-start>=4:
     try: out.append((start,data[start:i]))
     except:pass
    start=i+1
  return out
 st=strings(pt_o)
 # match by position is hard; just check total byte counts and find longer strings
 # Instead, compare each original string's length to any matching translated string
 longer=0
 for ioff,so in st:
  # try to find same string in translation at same offset
  if ioff < len(pt_t):
   # find NUL end in translation
   j=ioff
   while j<len(pt_t) and pt_t[j]!=0:j+=1
   new=pt_t[ioff:j]
   if new!=so and len(new)>len(so):
    longer+=1
    if longer<=10:
     print("  LONGER: %r (%d) -> %r (%d)"%(so[:40],len(so),new[:40],len(new)))
 print("%-40s: %d strings longer"% (trans.split('/')[-1], longer))
