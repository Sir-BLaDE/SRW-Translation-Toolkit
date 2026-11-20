# Lista todos los strings ASCII en OP.CPK
$opcpk = "D:\Juegos\-SPARROW\-Super Robot Wars V\Data\BTLC\EN0\OP.CPK"

if (Test-Path $opcpk) {
    Write-Host "Analizando $opcpk..."
    
    # Leer archivo como bytes
    $bytes = [System.IO.File]::ReadAllBytes($opcpk)
    $size = $bytes.Length
    Write-Host "Tamaño: $([Math]::Round($size/1MB, 2)) MB"
    
    # Extraer strings ASCII (max 30 chars, entre null terminators)
    $strings = @()
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        if ($bytes[$i] -ge 32 -and $bytes[$i] -le 126) {
            $start = $i
            $j = $i + 1
            while ($j -lt [Math]::Min($bytes.Length, $start + 50)) {
                if ($bytes[$j] -eq 0 -or $bytes[$j] -ge 32 -and $bytes[$j] -le 126) {
                    $j++
                } else {
                    break
                }
            }
            
            $text = -join $bytes[$start..$($j-1)] -replace '[^a-zA-Z0-9\s]', ''
            if ($text.Length -ge 8) {
                $strings += [PSCustomObject]@{
                    Offset = "0x{(Get-Hex $start)}"
                    Text = $text
                }
            }
        }
    }
    
    Write-Host "`nTotal strings encontrados: $($strings.Count)"
    Write-Host "`nTop 30 strings:"
    $strings | Sort-Object { $_.Text.Length } -Descending | Select-Object -First 30 | ForEach-Object {
        Write-Host "  Offset `$_(Offset): '$($_.Text)"
    }
} else {
    Write-Host "OP.CPK no encontrado en: $opcpk"
}
