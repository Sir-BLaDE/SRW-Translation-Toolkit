param([int]$Seconds = 30)
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
$game = 'D:/Juegos/-SPARROW-/Super Robot Wars V'
$out = 'C:/Dev/Default Project/srwv/tools/_font_render/shots'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-ChildItem $out -Filter *.png | Remove-Item -Force -ErrorAction SilentlyContinue

Stop-Process -Name SRWV -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$p = Start-Process -FilePath (Join-Path $game 'SRWV.EXE') -WorkingDirectory $game -PassThru

$t = 0
while ($t -lt $Seconds) {
  Start-Sleep -Seconds 2
  $t += 2
  $alive = -not $p.HasExited
  $w = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
  $title = if ($w) { $w.MainWindowTitle } else { '' }
  $hwnd = if ($w) { $w.MainWindowHandle } else { 0 }
  Write-Output ("t={0,2}s vivo={1} hwnd={2} titulo='{3}'" -f $t, $alive, $hwnd, $title)
  if ($alive) {
    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bmp.Save((Join-Path $out ("t{0:d2}.png" -f $t)))
    $g.Dispose(); $bmp.Dispose()
  } else {
    Write-Output ("  salio. ExitCode=0x{0:X8}" -f $p.ExitCode)
    break
  }
}
if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force }
