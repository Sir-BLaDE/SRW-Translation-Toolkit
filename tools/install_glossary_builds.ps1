$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = 'C:/Dev/Default Project/srwv/outputs'

$items = @(
  @{ From = 'SysText_es.cpk';            To = 'Data/AIDDATA/EN/SysText.cpk' },
  @{ From = 'Prologue_es.cpk';           To = 'Data/AIDDATA/EN/Prologue.cpk' },
  @{ From = 'CMN00_CPK_final_es6.cpk';   To = 'Data/BTLC/EN0/CMN00.CPK' },
  @{ From = 'MtZkn_Pt_es_acc.cpk';       To = 'CommonData/MtData/EN/MtZkn_Pt.cpk' },
  @{ From = 'MtZkn_Rt_es_acc.cpk';       To = 'CommonData/MtData/EN/MtZkn_Rt.cpk' },
  @{ From = 'KPACK_P4_LN_EN_es.cpk';     To = 'Data/KURODATA/EN/KPACK_P4_LN_EN.CPK' },
  @{ From = 'STGEST_EN_es.cpk';          To = 'Data/STAGE/STGEST_EN.CPK' }
)

foreach ($it in $items) {
  $src = Join-Path $out $it.From
  $dst = Join-Path $game $it.To
  Copy-Item -Force $src $dst
  $h = (Get-FileHash -Algorithm SHA256 $dst).Hash
  '{0,-32} {1}' -f $it.From, $h
}
