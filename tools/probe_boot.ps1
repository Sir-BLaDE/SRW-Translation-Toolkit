param([Parameter(Mandatory=$true)][string[]]$Cpks, [int]$WaitSeconds = 15)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$dst = Join-Path $game 'Data/AIDDATA/EN/SysText.cpk'
$exe = Join-Path $game 'SRWV.EXE'

foreach ($cpk in $Cpks) {
  Copy-Item -Force $cpk $dst
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
  '{0} boot={1}' -f (Split-Path $cpk -Leaf), $booted
}
