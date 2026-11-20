param([int]$WaitSeconds = 45)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = 'C:/Dev/Default Project/srwv/outputs'
$bak = 'C:/Dev/Default Project/srwv/backup'

function Test-Boot {
  param([int]$Seconds)
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game | Out-Null
  $t = 0
  while ($t -lt $Seconds) {
    Start-Sleep -Seconds 1
    $t++
    $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
    if ($p) {
      '  -> ventana a los {0}s' -f $t
      Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
      return $true
    }
  }
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  return $false
}

$sysDst = Join-Path $game 'Data/AIDDATA/EN/SysText.cpk'
$proDst = Join-Path $game 'Data/AIDDATA/EN/Prologue.cpk'
$sysNew = Join-Path $out 'SysText_es.cpk'
$proNew = Join-Path $out 'Prologue_es.cpk'
$sysGood = Join-Path $bak 'SysText_antes_es.cpk'
$proGood = Join-Path $bak 'Prologue_EN_original.cpk'

'BASELINE (todos los nuevos)'
$baseline = Test-Boot -Seconds $WaitSeconds
'baseline={0}' -f $baseline

'SOLO SysText original'
Copy-Item -Force $sysGood $sysDst
$a = Test-Boot -Seconds $WaitSeconds
Copy-Item -Force $sysNew $sysDst
'systext_original={0}' -f $a

'SOLO Prologue original'
Copy-Item -Force $proGood $proDst
$b = Test-Boot -Seconds $WaitSeconds
Copy-Item -Force $proNew $proDst
'prologue_original={0}' -f $b
