param([int]$Seconds = 70, [int]$Interval = 6, [string]$Tag = 'prologue_es2')
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
$out = "C:/Dev/Default Project/srwv/tools/_intro_$Tag"
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-ChildItem $out -Filter *.png | Remove-Item -Force -ErrorAction SilentlyContinue
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Keys3 {
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint flags, UIntPtr extra);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  public static void Tap(byte vk){ keybd_event(vk,0,0,UIntPtr.Zero); System.Threading.Thread.Sleep(60); keybd_event(vk,0,2,UIntPtr.Zero); }
}
'@
function Get-GameWindow {
  $ps = Get-Process -Name SRWV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne '' }
  if ($ps) { return $ps | Select-Object -First 1 }
  return $null
}
$w = Get-GameWindow
if (-not $w) { Write-Output 'sin ventana'; exit 1 }
Write-Output ("ventana: '{0}' pid={1}" -f $w.MainWindowTitle,$w.Id)
[Keys3]::SetForegroundWindow($w.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 400
[Keys3]::Tap(0x0D)
Write-Output 'Enter enviado'
$t=0
while($t -lt $Seconds){
  Start-Sleep -Seconds $Interval
  $t+=$Interval
  $w=Get-GameWindow
  if(-not $w){ Write-Output ("t={0}s sin ventana" -f $t); continue }
  $bounds=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bmp=New-Object System.Drawing.Bitmap $bounds.Width,$bounds.Height
  $g=[System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($bounds.Location,[System.Drawing.Point]::Empty,$bounds.Size)
  $bmp.Save((Join-Path $out ("f{0:d3}.png" -f $t)))
  $g.Dispose(); $bmp.Dispose()
  Write-Output ("t={0,3}s -> f{0:d3}.png" -f $t)
}
