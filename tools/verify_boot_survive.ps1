param([int]$Runs = 3, [int]$WaitWindow = 30, [int]$SurviveSeconds = 30, [int]$Cooldown = 4)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$exe = Join-Path $game 'SRWV.EXE'

for ($n = 1; $n -le $Runs; $n++) {
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds $Cooldown
  Start-Process -FilePath $exe -WorkingDirectory $game | Out-Null
  $win = $false
  for ($i = 0; $i -lt $WaitWindow; $i++) {
    Start-Sleep -Seconds 1
    $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
    if ($p) { $win = $true; break }
  }
  if (-not $win) {
    'run {0}: SIN VENTANA' -f $n
    Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
    continue
  }
  $alive = $true
  for ($s = 0; $s -lt $SurviveSeconds; $s++) {
    Start-Sleep -Seconds 1
    $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue
    if (-not $p) { $alive = $false; break }
  }
  if ($alive) { 'run {0}: VENTANA + {1}s VIVO' -f $n, $SurviveSeconds }
  else { 'run {0}: CRASH a los {1}s tras ventana' -f $n, ($s + 1) }
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
}
