param([int]$WaitSeconds = 45)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = 'C:/Dev/Default Project/srwv/outputs'
$bak = 'C:/Dev/Default Project/srwv/backup'

function Test-Boot {
  param([int]$Seconds)
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game | Out-Null
  $ok = $false
  for ($i=0; $i -lt $Seconds; $i++) {
    Start-Sleep -Seconds 1
    $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
    if ($p) { $ok = $true; '  -> ventana a los {0}s' -f ($i+1); break }
  }
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  return $ok
}

$cases = @(
  @{ Name='CMN00_original'; Dest='Data/BTLC/EN0/CMN00.CPK'; New=(Join-Path $out 'CMN00_CPK_final_es6.cpk'); Good=(Join-Path $bak 'CMN00_CPK_original.cpk') },
  @{ Name='CMN00_es5';      Dest='Data/BTLC/EN0/CMN00.CPK'; New=(Join-Path $out 'CMN00_CPK_final_es6.cpk'); Good=(Join-Path $bak 'CMN00_replaced_es5.cpk') },
  @{ Name='STGEST_original';Dest='Data/STAGE/STGEST_EN.CPK'; New=(Join-Path $out 'STGEST_EN_es.cpk'); Good=(Join-Path $bak 'STGEST_EN_original.cpk') },
  @{ Name='KPACKLN_es5';    Dest='Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'; New=(Join-Path $out 'KPACK_P4_LN_EN_es.cpk'); Good=(Join-Path $out 'KPACK_P4_LN_EN_es5.cpk') },
  @{ Name='MtZknPt_es';     Dest='CommonData/MtData/EN/MtZkn_Pt.cpk'; New=(Join-Path $out 'MtZkn_Pt_es_acc.cpk'); Good=(Join-Path $out 'MtZkn_Pt_es.cpk') },
  @{ Name='MtZknRt_es';     Dest='CommonData/MtData/EN/MtZkn_Rt.cpk'; New=(Join-Path $out 'MtZkn_Rt_es_acc.cpk'); Good=(Join-Path $out 'MtZkn_Rt_es.cpk') }
)

foreach ($c in $cases) {
  $dst = Join-Path $game $c.Dest
  Copy-Item -Force $c.Good $dst
  $ok = Test-Boot -Seconds $WaitSeconds
  Copy-Item -Force $c.New $dst
  '{0,-18} boot={1}' -f $c.Name, $ok
}
