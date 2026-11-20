param([int]$WaitSeconds = 25)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = 'C:/Dev/Default Project/srwv/outputs'
$bak = 'C:/Dev/Default Project/srwv/backup'

$cases = @(
  @{ Name='STGEST';  Dest='Data/STAGE/STGEST_EN.CPK';              New=(Join-Path $out 'STGEST_EN_es.cpk');           Good=(Join-Path $bak 'STGEST_EN_original.cpk') },
  @{ Name='KPACKLN'; Dest='Data/KURODATA/EN/KPACK_P4_LN_EN.CPK';   New=(Join-Path $out 'KPACK_P4_LN_EN_es.cpk');       Good=(Join-Path $out 'KPACK_P4_LN_EN_es5.cpk') },
  @{ Name='CMN00';   Dest='Data/BTLC/EN0/CMN00.CPK';               New=(Join-Path $out 'CMN00_CPK_final_es6.cpk');     Good=(Join-Path $bak 'CMN00_replaced_es5.cpk') },
  @{ Name='SysText'; Dest='Data/AIDDATA/EN/SysText.cpk';           New=(Join-Path $out 'SysText_es.cpk');              Good=(Join-Path $bak 'SysText_antes_es.cpk') },
  @{ Name='Prologue';Dest='Data/AIDDATA/EN/Prologue.cpk';          New=(Join-Path $out 'Prologue_es.cpk');             Good=(Join-Path $bak 'Prologue_EN_original.cpk') },
  @{ Name='MtZknPt'; Dest='CommonData/MtData/EN/MtZkn_Pt.cpk';     New=(Join-Path $out 'MtZkn_Pt_es_acc.cpk');         Good=(Join-Path $out 'MtZkn_Pt_es.cpk') },
  @{ Name='MtZknRt'; Dest='CommonData/MtData/EN/MtZkn_Rt.cpk';     New=(Join-Path $out 'MtZkn_Rt_es_acc.cpk');         Good=(Join-Path $out 'MtZkn_Rt_es.cpk') }
)

function Test-Boot {
  param([string]$Exe, [string]$WorkDir, [int]$Seconds)
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  Start-Sleep -Milliseconds 500
  Start-Process -FilePath $Exe -WorkingDirectory $WorkDir | Out-Null
  for ($i=0; $i -lt $Seconds; $i++) {
    Start-Sleep -Seconds 1
    $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
    if ($p) {
      Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
      return $true
    }
  }
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  return $false
}

foreach ($c in $cases) {
  $dst = Join-Path $game $c.Dest
  Copy-Item -Force $c.Good $dst
  $ok = Test-Boot -Exe (Join-Path $game 'SRWV.EXE') -WorkDir $game -Seconds $WaitSeconds
  Copy-Item -Force $c.New $dst
  '{0,-10} good={1}' -f $c.Name, $ok
}
