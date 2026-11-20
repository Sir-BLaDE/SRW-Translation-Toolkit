param([Parameter(Mandatory=$true)][ValidateSet('original','actual')]$Set, [int]$Runs = 0, [int]$WaitSeconds = 15)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = 'C:/Dev/Default Project/srwv/outputs'
$bak = 'C:/Dev/Default Project/srwv/backup'
$snap = 'C:/Dev/Default Project/srwv/backup/instalado_actual'

$items = @(
  @{ Dest='Data/AIDDATA/EN/SysText.cpk';           Orig=(Join-Path $bak 'SysText_antes_es.cpk');        Now=(Join-Path $out 'SysText_es.cpk') },
  @{ Dest='Data/AIDDATA/EN/Prologue.cpk';          Orig=(Join-Path $bak 'Prologue_EN_original.cpk');     Now=(Join-Path $out 'Prologue_es.cpk') },
  @{ Dest='Data/BTLC/EN0/CMN00.CPK';               Orig=(Join-Path $bak 'CMN00_CPK_original.cpk');      Now=(Join-Path $out 'CMN00_CPK_final_es7.cpk') },
  @{ Dest='CommonData/MtData/EN/MtZkn_Pt.cpk';     Orig=(Join-Path $bak 'MtZkn_Pt_original.cpk');       Now=(Join-Path $out 'MtZkn_Pt_es_acc2.cpk') },
  @{ Dest='CommonData/MtData/EN/MtZkn_Rt.cpk';     Orig=(Join-Path $bak 'MtZkn_Rt_original.cpk');       Now=(Join-Path $out 'MtZkn_Rt_es_acc2.cpk') },
  @{ Dest='CommonData/MtData/EN/MtZkn_Nm.cpk';     Orig=(Join-Path $bak 'MtZkn_Nm_original.cpk');       Now=(Join-Path $out 'MtZkn_Nm_es_acc.cpk') },
  @{ Dest='Data/KURODATA/EN/KPACK_P4_LN_EN.CPK';   Orig=(Join-Path $bak 'KPACK_P4_LN_EN_original.cpk'); Now=(Join-Path $out 'KPACK_P4_LN_EN_full_stable2.cpk') },
  @{ Dest='Data/STAGE/STGEST_EN.CPK';              Orig=(Join-Path $bak 'STGEST_EN_original.cpk');      Now=(Join-Path $out 'STGEST_EN_es.cpk') },
  @{ Dest='CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk';  Orig=(Join-Path $bak 'LT00_EN_antes_es2.cpk');     Now=(Join-Path $out 'LT00_EN_es2.cpk') },
  @{ Dest='CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk'; Orig=(Join-Path $bak 'B_LT00_EN_original.cpk');     Now=(Join-Path $out 'B_LT00_EN_es.cpk') },
  @{ Dest='CommonData/MtData/EN/rpw_jstr.cpk';      Orig=(Join-Path $bak 'rpw_jstr_original.cpk');       Now=(Join-Path $out 'rpw_jstr_es.cpk') },
  @{ Dest='Data/BTLC/EN0/OP.CPK';                  Orig=(Join-Path $bak 'OP_CK_original.cpk');          Now=(Join-Path $out 'OP_CK_es.cpk') },
  @{ Dest='Data/BTLC/EN0/1_CMN00.CPK';             Orig=(Join-Path $bak 'CMN00_CPK_original.cpk');      Now=(Join-Path $out 'CMN00_CPK_final_es7.cpk') },
  @{ Dest='Data/AIDDATA/EN/SysText - copia.cpk';   Orig=(Join-Path $bak 'SysText_antes_es.cpk');        Now=(Join-Path $out 'SysText_es.cpk') },
  @{ Dest='CommonData/MtData/EN/lega_zkn.cpk';     Orig=(Join-Path $bak 'lega_zkn_original.cpk');       Now=(Join-Path $out 'lega_zkn_es.cpk') },
  @{ Dest='Data/KURODATA/EN/1_KPACK_P4_RG_EN.CPK'; Orig=(Join-Path $bak 'KPACK_P4_RG_EN_original.cpk'); Now=(Join-Path $out 'KPACK_P4_RG_EN_es.cpk') },
  @{ Dest='Data/AIDDATA/EN/LayoutData.cpk';        Orig=(Join-Path $bak 'LayoutData_original.cpk');      Now=(Join-Path $out 'LayoutData_es.cpk') },
  @{ Dest='Data/AIDDATA/EN/LayoutImage.cpk';       Orig=(Join-Path $bak 'LayoutImage_original.cpk');     Now=(Join-Path $out 'LayoutImage_es.cpk') }
)

# DLC descargables (30 CPK en Data/DLCDIRE/EN)
Get-ChildItem (Join-Path $bak 'dlc_en') -Filter 'dlc*.cpk' | ForEach-Object {
  $items += @{
    Dest = "Data/DLCDIRE/EN/$($_.Name)"
    Orig = $_.FullName
    Now  = (Join-Path $out "dlc_es/$($_.Name)")
  }
}

if ($Set -eq 'actual' -and -not (Test-Path $snap)) {
  New-Item -ItemType Directory -Force -Path $snap | Out-Null
  foreach ($it in $items) {
    $dst = Join-Path $game $it.Dest
    $name = Split-Path $dst -Leaf
    Copy-Item -Force $dst (Join-Path $snap $name)
  }
}

foreach ($it in $items) {
  $dst = Join-Path $game $it.Dest
  $src = if ($Set -eq 'original') { $it.Orig } else { $it.Now }
  Copy-Item -Force $src $dst
}

if ($Runs -gt 0) {
  & (Join-Path $PSScriptRoot 'verify_boot_stability.ps1') -Runs $Runs -WaitSeconds $WaitSeconds
}
