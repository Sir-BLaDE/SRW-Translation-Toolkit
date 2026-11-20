param([string]$Tag = 'newgame_probe', [int]$WaitTitle = 10)
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class NGWin32 {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = "C:/Dev/Default Project/srwv/tools/_intro_$Tag"
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-ChildItem $out -Filter *.png | Remove-Item -Force -ErrorAction SilentlyContinue
function Get-GameWindow {
  $ps = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
  if ($ps) { return $ps | Select-Object -First 1 }
  return $null
}
function Shot([int]$n) {
  $w = Get-GameWindow
  if (-not $w) { return }
  [NGWin32]::ShowWindow($w.MainWindowHandle, 9) | Out-Null
  [NGWin32]::SetForegroundWindow($w.MainWindowHandle) | Out-Null
  Start-Sleep -Milliseconds 200
  $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
  $bmp.Save((Join-Path $out ("f{0:d3}.png" -f $n)))
  $g.Dispose(); $bmp.Dispose()
}
function Key([string]$k, [int]$n) {
  $w = Get-GameWindow
  if (-not $w) { Write-Output "sin ventana antes de $k"; return }
  [NGWin32]::ShowWindow($w.MainWindowHandle, 9) | Out-Null
  [NGWin32]::SetForegroundWindow($w.MainWindowHandle) | Out-Null
  Start-Sleep -Milliseconds 200
  [System.Windows.Forms.SendKeys]::SendWait($k)
  Write-Output "key $k @f$n"
}

Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$p = Start-Process -FilePath "$game/SRWV.EXE" -WorkingDirectory $game -PassThru
Write-Output "lanzado pid=$($p.Id)"
$w = $null
for ($i = 0; $i -lt 60; $i++) {
  Start-Sleep -Seconds 1
  $w = Get-GameWindow
  if ($w) { Write-Output "ventana a los $($i+1)s"; break }
}
if (-not $w) { Write-Output 'sin ventana'; exit 1 }
Start-Sleep -Seconds $WaitTitle
Shot 1
Key "{ENTER}" 2
Start-Sleep -Seconds 2
Shot 3
# el menu es horizontal: LEFT x3 para seleccionar Start en lugar de Continue
Key "{LEFT}{LEFT}{LEFT}" 4
Start-Sleep -Milliseconds 500
Shot 5
Key "{ENTER}" 6
Start-Sleep -Seconds 2
Shot 7
Key "{ENTER}" 8
Start-Sleep -Seconds 2
Shot 9
for ($i = 10; $i -le 25; $i++) {
  Start-Sleep -Seconds 1
  Shot $i
  if ($p.HasExited) { Write-Output ("PROCESO TERMINADO exit=0x{0:X8}" -f $p.ExitCode); break }
}
if (-not $p.HasExited) { Write-Output 'final: VIVO' }
Write-Output ("capturas: {0}" -f (Get-ChildItem $out -Filter *.png).Count)
