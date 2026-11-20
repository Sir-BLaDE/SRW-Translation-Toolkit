#!/bin/bash
# uso: bisect.sh orig|inst NOMBRE...   (instala la version traducida o restaura el original)
B="$HOME/mnt/srwv/backup"; D="$B/estado_roto_nombres3"; R="$HOME/mnt/Super Robot Wars V"
declare -A DST=( [font]="Data/AIDDATA/EN/FontInfo.cpk" [op]="Data/BTLC/EN0/OP.CPK" [nm]="CommonData/MtData/EN/MtZkn_Nm.cpk" [pt]="CommonData/MtData/EN/MtZkn_Pt.cpk" [rt]="CommonData/MtData/EN/MtZkn_Rt.cpk" [systext]="Data/AIDDATA/EN/SysText.cpk" [cmn00]="Data/BTLC/EN0/CMN00.CPK" [layoutdata]="Data/AIDDATA/EN/LayoutData.cpk" [rpw]="CommonData/MtData/EN/rpw_jstr.cpk" [defaultss]="CommonData/hiyama/defaultSS_E.cpk" [blt]="CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk" [kpackcmn]="Data/KURODATA/CMN/KPACK_PC_CMN.cpk" [tpack]="Data/TABATA/EN/TPACKWIN_EN.cpk" [stgest]="Data/STAGE/STGEST_EN.CPK" [effwin]="Data/ANIME/effwin.cpk" [prologue]="Data/AIDDATA/EN/Prologue.cpk" [ln]="Data/KURODATA/EN/KPACK_P4_LN_EN.CPK" [exe]="SRWV.EXE" )
declare -A ORIG=( [font]=FontInfo_original.cpk [op]=OP_CK_original.cpk [nm]=MtZkn_Nm_original.cpk [pt]=MtZkn_Pt_original.cpk [rt]=MtZkn_Rt_original.cpk [systext]=SysText_original.cpk [cmn00]=CMN00_CPK_original.cpk [layoutdata]=LayoutData_original.cpk [rpw]=rpw_jstr_original.cpk [defaultss]=defaultSS_E_original.cpk [blt]=B_LT00_EN_original.cpk [kpackcmn]=KPACK_PC_CMN_original.cpk [tpack]=TPACKWIN_EN_original.cpk [stgest]=STGEST_EN_original.cpk [effwin]=effwin_original.cpk [prologue]=Prologue_original_20261118.cpk [ln]=KPACK_P4_LN_EN_original.cpk [exe]=SRWV_original.EXE )
declare -A INST=( [font]=FontInfo.cpk.inst [op]=OP.CPK.inst [nm]=MtZkn_Nm.cpk.inst [pt]=MtZkn_Pt.cpk.inst [rt]=MtZkn_Rt.cpk.inst [systext]=SysText.cpk.inst [cmn00]=CMN00.CPK.inst [layoutdata]=LayoutData.cpk.inst [rpw]=rpw_jstr.cpk.inst [defaultss]=defaultSS_E.cpk.inst [blt]=B_LT00_EN.cpk.inst [kpackcmn]=KPACK_PC_CMN.cpk.inst [tpack]=TPACKWIN_EN.cpk.inst [stgest]=STGEST_EN.CPK.inst [effwin]=effwin.cpk.inst [prologue]=Prologue_instalado.cpk [ln]=../KPACK_P4_LN_EN_stable3_installed.cpk [exe]=SRWV_parcheado.EXE )
mode=$1; shift
for n in "$@"; do
  if [ "$mode" = orig ]; then src="$B/${ORIG[$n]}"; else src="$D/${INST[$n]}"; fi
  [ -f "$src" ] || { echo "falta $src"; continue; }
  cp "$src" "$R/${DST[$n]}" && echo "$mode $n"
done
