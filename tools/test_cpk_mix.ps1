param(
  [Parameter(Mandatory=$true)][string]$On,
  [int]$Runs = 3,
  [int]$WaitSeconds = 15
)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = 'C:/Dev/Default Project/srwv/outputs'
$bak = 'C:/Dev/Default Project/srwv/backup'
$on = @($On -split ',' | ForEach-Object { $_.Trim() })

$items = @(
  @{ Name='SysText';  Dest='Data/AIDDATA/EN/SysText.cpk';         Orig=(Join-Path $bak 'SysText_antes_es.cpk');        Now=(Join-Path $out 'SysText_es.cpk') },
  @{ Name='Prologue'; Dest='Data/AIDDATA/EN/Prologue.cpk';        Orig=(Join-Path $bak 'Prologue_EN_original.cpk');     Now=(Join-Path $out 'Prologue_es.cpk') },
  @{ Name='CMN00';    Dest='Data/BTLC/EN0/CMN00.CPK';             Orig=(Join-Path $bak 'CMN00_CPK_original.cpk');      Now=(Join-Path $out 'CMN00_CPK_final_es6.cpk') },
  @{ Name='MtZknPt';  Dest='CommonData/MtData/EN/MtZkn_Pt.cpk';   Orig=(Join-Path $bak 'MtZkn_Pt_original.cpk');       Now=(Join-Path $out 'MtZkn_Pt_es_acc.cpk') },
  @{ Name='MtZknRt';  Dest='CommonData/MtData/EN/MtZkn_Rt.cpk';   Orig=(Join-Path $bak 'MtZkn_Rt_original.cpk');       Now=(Join-Path $out 'MtZkn_Rt_es_acc.cpk') },
  @{ Name='KPACKLN';  Dest='Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'; Orig=(Join-Path $bak 'KPACK_P4_LN_EN_original.cpk'); Now=(Join-Path $out 'KPACK_P4_LN_EN_es.cpk') },
  @{ Name='STGEST';   Dest='Data/STAGE/STGEST_EN.CPK';            Orig=(Join-Path $bak 'STGEST_EN_original.cpk');      Now=(Join-Path $out 'STGEST_EN_es.cpk') }
)

foreach ($it in $items) {
  $dst = Join-Path $game $it.Dest
  $src = if ($on -contains $it.Name) { $it.Now } else { $it.Orig }
  Copy-Item -Force $src $dst
}

$exe = Join-Path $game 'SRWV.EXE'
$okCount = 0
for ($n = 1; $n -le $Runs; $n++) {
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  Start-Process -FilePath $exe -WorkingDirectory $game | Out-Null
  $booted = $false
  for ($i = 0; $i -lt $WaitSeconds; $i++) {
    Start-Sleep -Seconds 1
    $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
    if ($p) { $booted = $true; break }
  }
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  if ($booted) { $okCount++ }
}
'ON={0} boot={1}/{2}' -f ($on -join '+'), $okCount, $Runs
