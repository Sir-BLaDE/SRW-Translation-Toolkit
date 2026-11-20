# Listar todos los strings ASCII en OP.CPK instalado - Versión simplificada
$opcpk = "D:\Juegos\-SPARROW\-Super Robot Wars V\Data\BTLC\EN0\OP.CPK"

if (Test-Path $opcpk) {
    Write-Host "=== OP.CPK INSTALADO ACTUAL ===" -ForegroundColor Cyan
    $fileSize = (Get-Item $opcpk).Length
    Write-Host "Tamaño archivo: $([Math]::Round($fileSize/1MB, 2)) MB ($($fileSize.toLocaleString()) bytes)"
    
    # Leer archivo como bytes
    $bytes = [System.IO.File]::ReadAllBytes($opcpk)
    $size = $bytes.Length
    
    Write-Host "`nVerificando strings tradujdos:" -ForegroundColor Yellow
    
    # Verificar si "Analizador" está presente (string traducido en los ultimos bytes)
    $analPos = $bytes.IndexOf([byte[]]@('A','n','a','l','i','z','a','d','o','r'))
    if ($analPos -ge 0) {
        Write-Host "  ✅ 'Analizador' encontrado en offset $(Get-Hex $analPos)" -ForegroundColor Green
        $nextText = [string]$([System.Text.Encoding]::ASCII.GetString($bytes[$analPos..$analPos+15]))
        Write-Host "    Contexto: '$nextText'"
    } else {
        Write-Host "  ❌ 'Analizador' NO encontrado" -ForegroundColor Red
    }
    
    # Verificar string de personaje clave: Setsuna  
    $setsPos = $bytes.IndexOf([byte[]]@('S','e','t','s','u'))
    if ($setsPos -ge 0) {
        Write-Host "  ✅ 'Setsuna' encontrado en offset $(Get-Hex $setsPos)" -ForegroundColor Green
        $setName = [string]$([System.Text.Encoding]::ASCII.GetString($bytes[$setsPos..$setsPos+12]))
        Write-Host "    Nombre: '$setName'"
    } else {
        Write-Host "  ❌ 'Setsuna' NO encontrado" -ForegroundColor Red
    }
    
    # Listar todos los bloques ASCII legibles (null-terminated strings, max 40 chars)
    Write-Host "`n=== Top 50 strings ASCII encontrados ===" -ForegroundColor Cyan
    
    $strings = @()
    for ($i = 0; $i -lt $size -and $strings.Count -lt 50; $i++) {
        if ($bytes[$i] -ge 32 -and $bytes[$i] -le 126) {
            $start = $i
            $j = $i + 1
            while ($j -lt [Math]::Min($size, $start + 50)) {
                if ($bytes[$j] -eq 0 -or $bytes[$j] -ge 32 -and $bytes[$j] -le 126) {
                    $j++
                } else {
                    break
                }
            }
            
            # Convertir bytes a string ASCII
            $text = [string]$([System.Text.Encoding]::ASCII.GetString($bytes[$start..$($j-1)]))
            $text = $text.TrimEnd(" ", "`t", "`n")
            
            # Solo strings con al menos 8 caracteres de texto (no solo espacios)
            $trimmedText = ($text -split ' ') | Where-Object { $_.Length -ge 3 } | ForEach-Object { $_ }
            
            if ([string]::IsNullOrWhiteSpace($text) -eq $false -and $text.Length -ge 8 -and $text.Length -le 45) {
                # Solo agregar si es un string válido (no duplicar exactamente el mismo texto repetidamente)
                $isDuplicate = $strings | Where-Object { $_.Text -eq $text }
                if (-not $isDuplicate) {
                    $strings += [PSCustomObject]@{
                        Offset = "0x$(Get-Hex $start)"
                        Text = $text
                    }
                }
            }
        }
    }
    
    # Mostrar strings más largos primero (top strings ordenados por longitud)
    $strings | Sort-Object { $_.Text.Length } -Descending | ForEach-Object {
        Write-Host "  Offset `$_(Offset): '$($_.Text)"
    }
    
    Write-Host "`nTotal bloques ASCII únicos encontrados: $($strings.Count)" -ForegroundColor Gray
    
} else {
    Write-Host "OP.CPK NO ENCONTRADO en: $opcpk" -ForegroundColor Red
}
