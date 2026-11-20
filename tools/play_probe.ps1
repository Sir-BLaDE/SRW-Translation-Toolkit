param([int]$Seconds = 90, [string]$Tag = 'probe')
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
}
"@
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = "C:/Dev/Default Project/srwv/tools/_font_render/$Tag"
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-ChildItem $out -Filter *.png -ErrorAction SilentlyContinue | Remove-Item -Force

Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$p = Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game -PassThru

function Shot($n) {
  $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
  $bmp.Save((Join-Path $out ("{0:d3}.png" -f $n)))
  $g.Dispose(); $bmp.Dispose()
}
function Press($vk, $scan) {
  [W]::keybd_event($vk, $scan, 0, [UIntPtr]::Zero)
  Start-Sleep -Milliseconds 80
  [W]::keybd_event($vk, $scan, 2, [UIntPtr]::Zero)
}

$t = 0
$n = 0
while ($t -lt $Seconds) {
  Start-Sleep -Seconds 2
  $t += 2
  if ($p.HasExited) { Write-Output ("salio a los $t s, ExitCode=0x{0:X8}" -f $p.ExitCode); break }
  $proc = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
  if ($proc -and $proc.MainWindowHandle -ne 0 -and $t % 4 -eq 0) {
    [W]::ShowWindow($proc.MainWindowHandle, 3) | Out-Null
    [W]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
  }
  if ($t -ge 12 -and $t % 4 -eq 0) { Press 0x0D 0x1C }   # ENTER
  if ($t -ge 14 -and $t % 6 -eq 0) { Press 0x20 0x39 }   # SPACE
  $n++
  Shot $n
  Write-Output ("t={0,3}s hwnd={1} shot={2}" -f $t, $(if ($proc) { $proc.MainWindowHandle } else { 0 }), $n)
}
if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force }
Write-Output "capturas en $out"
