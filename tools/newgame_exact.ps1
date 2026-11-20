param([string]$Tag = 'ng_exact', [int]$WaitTitle = 10, [int]$WaitMenu = 8)
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class NXWin32 {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
"@
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = "C:/Dev/Default Project/srwv/tools/_intro_$Tag"
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-ChildItem $out -Filter *.png | Remove-Item -Force -ErrorAction SilentlyContinue
function Get-GameWindow {
  Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
}
function Focus {
  $w = Get-GameWindow
  if (-not $w) { return $null }
  [NXWin32]::ShowWindow($w.MainWindowHandle, 9) | Out-Null
  [NXWin32]::SetForegroundWindow($w.MainWindowHandle) | Out-Null
  Start-Sleep -Milliseconds 400
  $fg = [NXWin32]::GetForegroundWindow()
  if ($fg -ne $w.MainWindowHandle) { Write-Output "  AVISO: foco no es SRWV" }
  return $w
}
function Shot([int]$n, [string]$label) {
  $w = Focus
  if (-not $w) { Write-Output "f$n sin ventana"; return }
  $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
  $bmp.Save((Join-Path $out ("f{0:d3}_{1}.png" -f $n, $label)))
  $g.Dispose(); $bmp.Dispose()
  Write-Output "f$n $label"
}
function Key([string]$k, [int]$n, [string]$label) {
  $w = Focus
  if (-not $w) { Write-Output "sin ventana antes de $k"; return }
  [System.Windows.Forms.SendKeys]::SendWait($k)
  Write-Output "key $k @f$n $label"
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
Shot 1 title
Key "{ENTER}" 2 enter_title
Start-Sleep -Seconds $WaitMenu
Shot 3 menu
# menu horizontal: 3 x LEFT para ir de Continue a Start
Key "{LEFT}" 4 left1
Start-Sleep -Milliseconds 500
Key "{LEFT}" 5 left2
Start-Sleep -Milliseconds 500
Key "{LEFT}" 6 left3
Start-Sleep -Milliseconds 700
Shot 7 start_selected
Key "{ENTER}" 8 enter_start
Start-Sleep -Seconds 3
Shot 9 guidance
Key "{ENTER}" 10 enter_guidance
Start-Sleep -Seconds 3
Shot 11 charselect
for ($i = 12; $i -le 30; $i++) {
  Start-Sleep -Seconds 1
  Shot $i wait
  if ($p.HasExited) { Write-Output ("PROCESO TERMINADO exit=0x{0:X8}" -f $p.ExitCode); break }
}
if (-not $p.HasExited) { Write-Output 'final: VIVO' }
Write-Output ("capturas: {0}" -f (Get-ChildItem $out -Filter *.png).Count)
