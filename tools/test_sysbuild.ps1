param([Parameter(Mandatory=$true)][string]$Cpk, [int]$WaitSeconds = 30)

$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$dst = Join-Path $game 'Data/AIDDATA/EN/SysText.cpk'
Copy-Item -Force $Cpk $dst
Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game | Out-Null
$ok = $false
for ($i=0; $i -lt $WaitSeconds; $i++) {
  Start-Sleep -Seconds 1
  $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
  if ($p) { $ok = $true; 'ventana a los {0}s' -f ($i+1); break }
}
Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
'boot={0} cpk={1}' -f $ok, $Cpk
exit ([int](-not $ok))
