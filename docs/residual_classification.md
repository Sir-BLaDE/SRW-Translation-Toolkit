# Clasificación de residuales de la auditoría (tras integrar la pasada de corchetes)

Fecha: 2026-11-18. Auditoría: `tools/audit_comprehensive.py` → `datos/audit_untranslated.txt`.

La auditoría divide cada bloque descomprimido por bytes de control `0x00-0x08,0x0b,0x0c,0x0e-0x1f`
(NO por CR/LF), de modo que un «residuo» suele ser un segmento grande que contiene
código Lua, etiquetas binarias y texto ya traducido. Por eso los recuentos no cambian
necesariamente cuando se traduce un subconjunto de texto dentro de esos segmentos.

## STGEST — 180 EN / 331 MIXTO
Comentarios Lua de compilación (`--[[ ... \SRDEV_T\z3of2\... ]]`,
`\Tentative\z3of2\PS4\...`) y comentarios `@note` en japonés sobre la conversión
`CsCppToCsLua`. No se muestran en pantalla. **Falso positivo intencionado.**

Verificado: los 1.809 bloques `[[...]]` traducidos están presentes en el CPK instalado;
0 claves inglesas de `stgest_bracket_es.json` sobreviven; el número de delimitadores
`[[` se conserva (71.204).

## SYSTEXT — 21 EN / 15 MIXTO
- 10 cadenas en fila 2 (`Terrain Handling Up: *`, `Emperor of Darkness`,
  `Great General of Darkness`, `Aestivalis Custom Hikaru Unit`,
  `Calidus Multi-phase Beam Cannon`, `High Energy Long-range Beam Cannon`,
  `High-Mobility Unit Black Selena`, `Kurogane Five Certain Death Attack`):
  están fuera de las tablas activas TAB1 (0x1440) / TAB2 (0x1640); ninguna entrada
  de esas tablas apunta a sus desplazamientos. **Huérfanas, no referenciadas.**
  Las traducciones existen en `datos/systext_trans.json` por si se necesitan.
- 11 cadenas en fila 3 (`ass to ass`, `qq more`, `screw you`, `the yeti`, …):
  lista de palabras/profanidades, no texto de interfaz. **No se muestran.**
- MIXTO: texto ya traducido que contiene `START`, `SELECT` o títulos de canciones.

## PROLOGUE — 11 EN / 4 MIXTO
Nombres de empresas y cargos de los créditos (`ALPHA UNIT Co.,Ltd`,
`Pole To Win Co., Ltd.`, `Senior VP Of Asia Pacific`, `Heart of Nashville,TN`),
un título (`THE EXCEEDER`), un crédito de voz (`Ple Two … \t1Chieko Honda`) y
fragmentos recortados por la división por bytes de control (`their`, `gate on`,
`naan in order`, `came to be protected by Celestial Being…`). **Créditos/nombres
propios y fragmentos, no texto jugable.**

## MTZKN (Pt 177 EN / Rt 41 EN / Nm 2 EN)
- Marcadores binarios `^^DATA`, `^^DATA!`, etc. y secuencias cifradas residuales.
- Etiquetas `PRDC` con títulos oficiales de las obras (Gundam, Evangelion, Cross Ange,
  Full Metal Panic!, Nadesico…). Se conservan los títulos originales.
- Campos `RBTN` / `RBN2` / `CHFN` / `CHNN` con nombres de unidad/piloto. Los nombres
  principales ya están traducidos en `CMN00.CPK` y `KPACK_P4_LN_EN.CPK`
  (p. ej. `Emperador de la Oscuridad`, `Gran General de la Oscuridad`); modificar
  estos campos binarios sin evidencia de que se muestren podría corromper los
  registros. **Pendiente de confirmación visual; no se toca.**
- MIXTO: descripciones ya traducidas con etiquetas `^^`, `KANA`, `DSC2`. Falso positivo.

## CMN00 — 4 EN (todos falsos positivos)
- `Campo AT`: el clasificador detecta la palabra inglesa `at` dentro del término
  de glosario `Campo AT` (24 apariciones). Es español.
- `He fallado.`, `He luchado contra monstruos antes.`, `He recibido golpes antes.`:
  `he` es el auxiliar del pretérito perfecto español, pero también palabra
  inglesa; el clasificador lo marca como EN. Son diálogos ya traducidos.

## LT00 / B_LT00 — 1 EN cada uno
`Mejora HIT`: `HIT` se usa como abreviatura estadística en todo el juego traducido
(`CQB`, `RNG`, `SKL`, `DEF`, `EVD`). Coherente con el resto. **Falso positivo.**

## KPACK_LN — 1 EN / 2 MIXTO (antes 90 EN)
Los 90 residuales EN **no eran huérfanos**: eran títulos y descripciones de
escenarios/DLC y cadenas de habilidad mostradas al jugador (verificado por
`tools/ln_residual_extract.py` y la sonda de referencias de `SRWV.EXE`).

Se han traducido los 112 residuales detectados (fila 1: 3, fila 2: 30,
fila 3: 7, fila 4: 72) en `datos/ln_residual_es_list.json` y se han aplicado
con `tools/ln_build_full_stable2.py`, que:
- reconstruye filas 0/1/3 desde el original con sus mapas ampliados;
- parchea filas 2/4 **en su hueco exacto** (alineado a 4 en id2; u32 en
  `pos-4` en id4), sin cambiar longitudes ni cabeceras.

Verificación: `ex_mismatch=0`, 0 textos EN sobreviven, 0 traducciones faltan,
misma secuencia de registros id4 (119 registros, offsets/claves/longitudes
idénticos), 145 registros id3, MD5 instalado = salida.
Tras la instalación la auditoría pasa de `EN=90 MIXTO=1 ES=296` a
`EN=1 MIXTO=2 ES=373`.

El único EN restante es `Campo AT`: falso positivo del clasificador, que detecta
la palabra inglesa `at` dentro de nuestro término de glosario `Campo AT`
(24 apariciones en CMN00). No es texto sin traducir.

## rpw_jstr — 820 residuales aceptados (nombres propios)
`CommonData/MtData/EN/rpw_jstr.cpk` es el contenedor de cadenas compartidas
(`j-string` + tabla `jstr-i2i` de 14.802 entradas). Se han traducido 1.460 claves
(1.551 apariciones en el pool); quedan 820 cadenas sin tocar, que son:

- nombres oficiales de mechas, naves y personajes (`AAM-4 Murasame`,
  `ARX-7 Arbalest`, `Destiny Gundam`, `Unicorn Gundam`, `Great Mazinger`,
  `Asuka Misurugi`, `Rohm Halharris`…), conservados por el glosario;
- variantes japonesas y cadenas `rid_*`/`pid_*` internas;
- 55 entradas del mapa son idénticas al original a propósito (títulos oficiales
  de las obras: `Mobile Suit Gundam Unicorn`, `EVANGELION 1.0 YOU ARE (NOT) ALONE.`,
  `Space Battleship Yamato`…).

Reconstrucción: `tools/rpw_jstr_build.py` regenera pool, tabla `jstr-i2i` y los
chunks con `next = len + 72`; el modo sin mapa reproduce el CPK original byte a byte
(`ExtractSize = 245.052`). El CPK traducido tiene `ExtractSize = 255.413` y los
14.802 offsets de `jstr-i2i` son válidos.

## CMN00 — corrección estructural del BLTU (importante)
El constructor anterior (`tools/srwv_buildbltu.py`) reconstruía los 6 bloques del
BLTU pero **no remapeaba la cabecera**. La cabecera real es:

```
u32[0..5] = {6, 0x10, 0x30, 0, 0, 0x20}
u32[6..9] = offset_del_bloque_2..5 - 0x30      (offsets relativos al área de bloques)
u32[10]   = longitud_total - 0x30
```

Al crecer los bloques, `u32[6..9]` quedaban apuntando a posiciones antiguas (dentro
del blob de otro bloque) y el juego leía basura al cargar las tablas pequeñas; el
síntoma era un **cuelgue/crash determinista a los ~25 s** (modo demostración del
título, en `ucrtbase.dll`). `u32[10]` además se escribía como `len(out)` en vez de
`len(out) - 0x30`.

Corregido en `tools/cmn_build_v2.py`, que:
- con traducciones vacías reproduce **byte a byte** el BLTU original;
- escribe `u32[6..9]` y `u32[10]` con la base `- 0x30`;
- genera `outputs/CMN00_CPK_final_es7.cpk` (`ExtractSize = 1.487.184`).

Verificación tras instalar el conjunto completo: arranque 15/15 y permanencia
4/4 durante 60 s (antes: crash a los 25 s en las 3 pruebas).

## DLC (30 CPK en `Data/DLCDIRE/EN`) — reconstrucción
Los CPK de DLC se reconstruyen **siempre** desde `backup/dlc_en` con
`tools/dlc_build.py`. El modo sin mapas reproduce los 30 originales byte a byte,
así que el riesgo estructural es nulo. El verificador comprueba
`ExtractSize == len(plain)`, el número de delimitadores `[[` y que ningún bloque
u objetivo con traducción conserva su texto inglés.

Contenido traducible por fila:
- fila 1: script Lua; solo `str_tbl` (objetivos, 26 únicos). Se reutiliza la
  redacción de STGEST. El resto del script (código, comentarios) no se toca.
- filas 3/4: tablas de evento convertidas con diálogo en bloques `[[...]]`.
  5 CPK (322, 323, 326, 328, 329) solo tienen texto en la fila 3.
- fila 2: bloques de comentarios Lua con texto japonés embebido. **No se traduce.**
- filas 0/5/6: binarias.

Inventario autoritativo: `datos/dlc_work/blocks_en.json` (5.389 bloques únicos,
6.389 apariciones), repartidos en 27 lotes de 200 (`datos/dlc_work/batches/`).
`datos/dlc_work/labels_es.json` fija 53 etiquetas de lugar y rótulos que se
aplican antes que los lotes. `BFL_EN.CPK` es el manifiesto (ID + rutas) y se
deja en inglés.

Herramientas: `tools/dlc_work_extract.py` (inventario), `tools/dlc_labels.py`,
`tools/dlc_batch_check.py` (validador estructural por lote),
`tools/dlc_check_all.py` (todos los lotes), `tools/dlc_coverage.py` (progreso),
`tools/dlc_glossary_scan.py` y `tools/dlc_warnings.py` (coherencia) y
`tools/dlc_build.py` (reconstrucción + verificación).

**Estado final:** 27/27 lotes válidos, 5.334/5.389 bloques traducidos (55 idénticos
por ser neutros, p. ej. `No.`, `Lottie—`, `Oh...`). Los 30 CPK reconstruidos pasan
verificación: 80 filas modificadas, 7.494 delimitadores `[[` (idénticos a los
originales), `ex_mismatch=[]`. El glosario obligatorio no aparece en inglés en
ningún lote y no hay restos de inglés detectable.

La auditoría `audit_comprehensive.py` solo ve ~15 cadenas por DLC (una por fila,
porque divide por bytes de control y el diálogo completo queda dentro de una sola
cadena Lua). El único residual EN por CPK es la cabecera de comentario
`--[[ ... \Tentative\z3of2\PS4\CommonData\KuroData ... ]]`, el mismo falso
positivo de compilación que STGEST. **No es texto jugable.**

Tras instalar el conjunto completo: arranque 15/15, permanencia 3/3 a 60 s.

## PrologueImage — texto incrustado
`PRESS START` / `Press any button` parecen estar horneados en las texturas DDS
(`Data/AIDDATA/COMMON/PrologueImage.cpk`). No hay cadena ASCII localizable en los
datos descomprimidos, el OCR de Windows no encontró texto legible y este modelo no
puede inspeccionar imágenes. **Sin resolver; requiere edición visual de texturas.**
