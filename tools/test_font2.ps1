param(
  [Parameter(Mandatory = $true)][string]$Cpk,
  [int]$Seconds = 45
)
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$dst = Join-Path $game 'Data/AIDDATA/EN/FontInfo.cpk'

Write-Output ("=== {0} ({1} bytes) ===" -f (Split-Path $Cpk -Leaf), (Get-Item $Cpk).Length)
Copy-Item $Cpk $dst -Force
Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$d0 = (Get-ChildItem $game -Filter *.dmp | Measure-Object).Count

$p = Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game -PassThru
if ($p.WaitForExit($Seconds * 1000)) {
  Write-Output ("salio a los pocos segundos. ExitCode = 0x{0:X8} ({0})" -f $p.ExitCode)
} else {
  $alive = -not $p.HasExited
  Write-Output ("sigue viva a los {0}s: {1}" -f $Seconds, $alive)
  if ($alive) { Stop-Process -Id $p.Id -Force }
}
$d1 = (Get-ChildItem $game -Filter *.dmp | Measure-Object).Count
Write-Output ("dumps: {0} -> {1}" -f $d0, $d1)
