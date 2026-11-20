param([Parameter(Mandatory=$true)][string[]]$Cpks, [int]$Runs = 6, [int]$WaitSeconds = 15)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$dst = Join-Path $game 'Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
$exe = Join-Path $game 'SRWV.EXE'

foreach ($c in $Cpks) {
  Copy-Item -Force $c $dst
  $ok = 0
  for ($n = 0; $n -lt $Runs; $n++) {
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
    if ($booted) { $ok++ }
  }
  '{0} boot={1}/{2}' -f (Split-Path $c -Leaf), $ok, $Runs
}
