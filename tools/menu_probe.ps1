param([string]$Tag = 'menu_probe', [int]$Wait = 12, [int]$Frames = 25, [switch]$NoEnter)
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class MPWin32 {
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
Start-Sleep -Seconds $Wait
[MPWin32]::ShowWindow($w.MainWindowHandle, 9) | Out-Null
[MPWin32]::SetForegroundWindow($w.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 300
if (-not $NoEnter) {
  [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
  Write-Output 'ENTER enviado'
} else {
  Write-Output 'sin ENTER'
}
for ($i = 1; $i -le $Frames; $i++) {
  Start-Sleep -Seconds 1
  $w = Get-GameWindow
  if (-not $w) { Write-Output "t=$i sin ventana"; break }
  $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
  $bmp.Save((Join-Path $out ("f{0:d3}.png" -f $i)))
  $g.Dispose(); $bmp.Dispose()
}
Write-Output ("capturas: {0}" -f (Get-ChildItem $out -Filter *.png).Count)
