param(
  [int]$Runs = 5,
  [int]$Seconds = 30,
  [int]$Cores = 0,
  [string]$Compat = '',
  [switch]$Admin,
  [string]$Tag = ''
)
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$log = "C:/Dev/Default Project/srwv/tools/_stability_$Tag.log"
"=== Tag=$Tag Cores=$Cores Compat=$Compat Admin=$Admin Runs=$Runs Seconds=$Seconds $(Get-Date -Format s) ===" | Set-Content $log

function Get-CrashInfo {
  param($since)
  $ev = Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='Application Error'; StartTime=$since} -ErrorAction SilentlyContinue
  if (-not $ev) { return '' }
  $m = ($ev | Select-Object -First 1).Message -split "`r?`n"
  $mod = ($m | Where-Object { $_ -match 'Nombre del m.dulo con errores' })
  $code = ($m | Where-Object { $_ -match 'C.digo de excepci' })
  $off = ($m | Where-Object { $_ -match 'Desplazamiento con errores' })
  $mod = ($mod -replace '.*: ', '') ; $code = ($code -replace '.*: ', '') ; $off = ($off -replace '.*: ', '')
  return "$mod $code off=$off"
}

$ok = 0
for ($i = 1; $i -le $Runs; $i++) {
  Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  $t0 = Get-Date
  $p = Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game -PassThru
  if ($Cores -gt 0) { try { $mask = [int64]([math]::Pow(2, $Cores) - 1); $p.ProcessorAffinity = [IntPtr]$mask } catch { "afinidad fallo: $_" | Add-Content $log } }
  if ($Compat -ne '') {
    $key = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers'
    if (-not (Test-Path $key)) { New-Item -Path $key -Force | Out-Null }
    $flags = if ($Admin) { "$Compat RUNASADMIN" } else { $Compat }
    Set-ItemProperty -Path $key -Name (Join-Path $game 'SRWV.EXE') -Value $flags
  }
  $deadline = (Get-Date).AddSeconds($Seconds)
  while ((Get-Date) -lt $deadline -and -not $p.HasExited) { Start-Sleep -Milliseconds 500 }
  if ($p.HasExited) {
    $code = '0x{0:X8}' -f $p.ExitCode
    $crash = Get-CrashInfo $t0
    "intento $i : FALLO  exit=$code  $crash" | Add-Content $log
  } else {
    $proc = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
    $hwnd = if ($proc) { $proc.MainWindowHandle } else { 0 }
    $title = if ($proc) { $proc.MainWindowTitle } else { '' }
    "intento $i : VIVO a $Seconds s  hwnd=$hwnd titulo='$title'" | Add-Content $log
    $ok++
    Stop-Process -Id $p.Id -Force
  }
  Start-Sleep -Seconds 3
}
"RESULTADO: $ok / $Runs vivos" | Add-Content $log
Get-Content $log
