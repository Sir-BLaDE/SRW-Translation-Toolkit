param([int]$Runs = 3, [int]$WaitSeconds = 40, [int]$Cooldown = 2)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$exe = Join-Path $game 'SRWV.EXE'

for ($n = 1; $n -le $Runs; $n++) {
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds $Cooldown
  Start-Process -FilePath $exe -WorkingDirectory $game | Out-Null
  $booted = $false
  $secs = 0
  for ($i = 0; $i -lt $WaitSeconds; $i++) {
    Start-Sleep -Seconds 1
    $secs++
    $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
    if ($p) { $booted = $true; break }
  }
  if ($booted) { 'run {0}: BOOT ok ({1}s)' -f $n, $secs }
  else { 'run {0}: BOOT FAIL ({1}s)' -f $n, $secs }
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
}
