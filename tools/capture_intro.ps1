param([int]$Seconds = 90, [int]$Interval = 3, [string]$Tag = 'intro')
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = "C:/Dev/Default Project/srwv/tools/_intro_$Tag"
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-ChildItem $out -Filter *.png | Remove-Item -Force -ErrorAction SilentlyContinue

Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$p = Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game -PassThru
Start-Sleep -Seconds 6

# enviar Enter/espacios para avanzar titulos hacia la intro
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Keys {
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint flags, UIntPtr extra);
  public static void Tap(byte vk){ keybd_event(vk,0,0,UIntPtr.Zero); System.Threading.Thread.Sleep(60); keybd_event(vk,0,2,UIntPtr.Zero); }
}
'@

$w = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
if ($w -and $w.MainWindowHandle -ne 0) {
  [Keys]::Tap(0x0D)  # Enter
  Write-Output 'Enter enviado'
}

$t = 0
while ($t -lt $Seconds) {
  Start-Sleep -Seconds $Interval
  $t += $Interval
  $alive = -not $p.HasExited
  $w = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
  $title = if ($w) { $w.MainWindowTitle } else { '' }
  if ($alive) {
    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bmp.Save((Join-Path $out ("f{0:d3}.png" -f $t)))
    $g.Dispose(); $bmp.Dispose()
    Write-Output ("t={0,3}s vivo={1} titulo='{2}' -> f{0:d3}.png" -f $t, $alive, $title)
  } else {
    Write-Output ("t={0}s salio 0x{1:X8}" -f $t, $p.ExitCode)
    break
  }
}
if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force }
