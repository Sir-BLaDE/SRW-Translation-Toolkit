param([int]$WaitWindow = 90, [int]$Seconds = 45, [int]$Interval = 1, [string]$Tag = 'fromlaunch_v6')
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32Foreground {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@
$game='D:/Juegos/-SPARROW-/Super Robot Wars V'
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
Start-Process -FilePath "$game/SRWV.EXE" -WorkingDirectory $game | Out-Null
Write-Output 'lanzado, esperando ventana...'
$w=$null
for($i=0;$i -lt $WaitWindow;$i++){
  Start-Sleep -Seconds 1
  $w=Get-GameWindow
  if($w){ Write-Output ("ventana a los {0}s pid={1}" -f ($i+1),$w.Id); break }
}
if(-not $w){ Write-Output 'sin ventana'; exit 1 }
$sw=[System.Diagnostics.Stopwatch]::StartNew()
$t=0
while($t -lt $Seconds){
  Start-Sleep -Seconds $Interval
  $t+=$Interval
  $w=Get-GameWindow
  if(-not $w){ Write-Output ("t={0}s sin ventana" -f $t); continue }
  [Win32Foreground]::ShowWindow($w.MainWindowHandle, 9) | Out-Null
  [Win32Foreground]::SetForegroundWindow($w.MainWindowHandle) | Out-Null
  Start-Sleep -Milliseconds 350
  $bounds=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bmp=New-Object System.Drawing.Bitmap $bounds.Width,$bounds.Height
  $g=[System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($bounds.Location,[System.Drawing.Point]::Empty,$bounds.Size)
  $bmp.Save((Join-Path $out ("f{0:d3}.png" -f $t)))
  $g.Dispose(); $bmp.Dispose()
}
Write-Output ("capturas: {0}" -f (Get-ChildItem $out -Filter *.png).Count)
