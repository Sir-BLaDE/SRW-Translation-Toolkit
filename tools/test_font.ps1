param(
  [Parameter(Mandatory = $true)][string]$Cpk,
  [int]$Seconds = 60
)
# Instala un FontInfo.cpk y prueba si el juego arranca y se mantiene vivo.
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$dst = Join-Path $game 'Data/AIDDATA/EN/FontInfo.cpk'

Write-Output ("=== probando {0} ===" -f (Split-Path $Cpk -Leaf))
Copy-Item $Cpk $dst -Force
Get-Item $dst | ForEach-Object { Write-Output ("instalado: {0} bytes  {1}" -f $_.Length, $_.LastWriteTime) }

Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$d0 = (Get-ChildItem $game -Filter *.dmp | Measure-Object).Count
Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game

$aliveAt = 0
for ($i = 1; $i -le [math]::Ceiling($Seconds / 3); $i++) {
  Start-Sleep -Seconds 3
  $p = Get-Process -Name SRWV -ErrorAction SilentlyContinue
  if ($p) {
    $aliveAt = $i * 3
  } else {
    Write-Output ("t={0}s  MUERTA" -f ($i * 3))
    break
  }
}
if ($aliveAt -ge $Seconds) { Write-Output ("t={0}s  VIVA" -f $aliveAt) }

$d1 = (Get-ChildItem $game -Filter *.dmp | Measure-Object).Count
Write-Output ("dumps: antes={0} despues={1}  -> {2}" -f $d0, $d1, $(if ($d1 -eq $d0) { 'SIN CRASH' } else { 'CRASH' }))
