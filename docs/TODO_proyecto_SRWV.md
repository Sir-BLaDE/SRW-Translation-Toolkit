# TODO — Traducción SRW V (español de España)

## Prioridad actual: estabilidad + historia

- [x] **CRASH DE NUEVA PARTIDA RESUELTO**
  - Causa real: `CommonData/MtData/EN/MtZkn_Pt.cpk` (y potencialmente otros `MtZkn_*`)
    cambiaba el tamaño de sus filas al traducirlo. El juego tiene offsets fijos y
    crasheaba al crear partida nueva (al cargar una partida guardada no pasaba).
  - `Prologue.cpk` y `LayoutImage.cpk` eran señuelos: restaurados al original.
  - Solución: `tools/mtzkn_pt_fixedlen.py` reescribe nombres dentro del hueco
    exacto original (misma longitud de fila y de campo). Validado en juego:
    **partida nueva → selección de personaje, sin crash**.
  - Regla: cualquier CPK con índices internos debe traducirse **in-situ**,
    sin cambiar tamaños de fila.

- [ ] **Traducir la historia (`Prologue.cpk`) — CRASH AÚN NO RESUELTO**
  - IMPORTANTE: todas las pruebas de `Prologue` anteriores al arreglo de
    `MtZkn_Pt` eran inválidas (crasheaban por ese archivo, no por `Prologue`).
  - Pruebas limpias ya realizadas (con `MtZkn_Pt` estable):
    - `Prologue_es_exact.cpk` (31 filas) → CRASH.
    - `Prologue_exact_row0.cpk` (solo fila 0) → CRASH.
    - `Prologue_slot_test.cpk` (solo slot 0 de la fila 0) → CRASH.
    - `Prologue_rebuild_identical.cpk` (datos idénticos, contenedor reconstruido) → **NO crashea**.
    - Slot 0 con texto corto `1 nov 2199` → **NO crashea**.
    - Slot 0 con `1 nov 2199, NCC, espacio aereo de Pluton` (40 bytes) → CRASH.
    - Slot 0 con `oviembre 11, 2199 NCC, espacio aereo` (36 bytes) → usuario
      reporta que **la fecha sigue apareciendo en inglés** (confirmar si crasheó).
  - Hipótesis actual: (a) superar ~36 bytes en ese slot dispara el crash, y
    (b) el texto visible de la intro quizá NO viene de `Prologue.cpk` sino de
    otro CPK, porque sigue en inglés tras modificar el slot 0.
  - Acción en curso: `tools/find_date_real.py` busca `November 11`, `ovember 11`,
    `Pluto Airspace` y `2199 NCC` en TODOS los CPK del juego (se quedó en
    background al resumir; leer su resultado).
  - Correcciones que SÍ hay que aplicar al reconstruir: respetar metadata de
    22 bytes al final de cada slot y bytes estructurales (el `N` inicial del
    slot 5 de la fila 0); no cambiar longitudes de fila.

- [ ] **Traducir `STGEST_EN.CPK`** (diálogos de escenarios/historia).
  - Candidato validado: `outputs/STGEST_EN_es.cpk` (`magic=CPK `, 765 filas, `ExtractSize` OK).
  - Instalar y probar de uno en uno, creando partida nueva.

- [ ] **traducir los menús gráficos** (`LayoutImage.cpk`, `LT00_EN.cpk`, `B_LT00_EN.cpk`
  y cualquier otro menú dibujado en imágenes).
  - `outputs/LayoutImage_es.cpk` cambia tamaños de fila → crashea al elegir personaje.
  - Reconstruir in-situ, sin cambiar tamaños de fila / offsets, como en `MtZkn_Pt`.
  - Incluye la pantalla de título (`"Press any button"`), que no aparece como
    texto ASCII en los CPK habituales (probablemente en glifos/imagen).

- [ ] Corregir el texto residual en inglés de `LayoutData_es.cpk` (no sirve: es idéntico al original en los términos del menú).

## Menores / cosméticos

- [ ] Nombres de pilotos con acentos en `OP.CPK`: UTF-8 no cabe en el hueco fijo y Latin-1 los corta. Dejar estables sin acentos.
- [ ] Nombres en `MtZkn_Pt_es_fixedlen.cpk` recortados al hueco original (279 de 351): revisar si se pueden acortar mejor sin perder sentido.
- [ ] Quedan 3 marcadores de inglés en la versión segura de `Prologue.cpk` (localizar y corregir sin cambiar tamaños).
- [ ] Revisar la línea de batalla en inglés detectada en `f054` de `_intro_nav_base`:
  `"Yeah, this is my kind of machine! Knowing a weapon like this is in our arsenal could keep..."`

## Estado instalado actual (estable, partida nueva OK)

| Archivo | Estado |
|---|---|
| `Data/BTLC/EN0/OP.CPK` | Válido, traducido (roles), sin acentos en nombres |
| `Data/BTLC/EN0/CMN00.CPK` | Traducido (diálogos de batalla en español) |
| `Data/AIDDATA/EN/LayoutImage.cpk` | **Original** (el traducido crashea) |
| `Data/AIDDATA/EN/Prologue.cpk` | **Slot 0 de la fila 0 modificado** (`oviembre 11, 2199 NCC, espacio aereo`, 36 bytes). Si crashea o no está confirmado, restaurar desde `backup/Prologue_original_20261118.cpk` |
| `Data/STAGE/STGEST_EN.CPK` | Original |
| `Data/AIDDATA/EN/SysText.cpk` | Traducido |
| `CommonData/.../LT00_EN.cpk`, `B_LT00_EN.cpk` | Traducidos |
| `CommonData/MtData/EN/MtZkn_Pt.cpk` | **Traducido in-situ (fixedlen), estable** |
| `CommonData/MtData/EN/MtZkn_Rt.cpk` | Traducido (pendiente de verificar in-situ) |
| `CommonData/MtData/EN/MtZkn_Nm.cpk` | Original/por verificar |

## Reglas que no se deben romper

- Todo CPK instalado debe cumplir `magic == b'CPK '` y `ExtractSize == len(plain)` por fila.
- **Traducir siempre in-situ**: no cambiar longitudes de fila en CPK con índices internos (MtZkn_*, LayoutImage, Prologue, etc.).
- No instalar nada desde `C:/Dev/Default Project/srwv/output/` (datos crudos sin cabecera).
- Siempre backup en `C:/Dev/Default Project/srwv/backup/` antes de reemplazar.
- Probar **creando partida nueva**, no cargando una partida guardada.
- KPACK_PC_CMN instalado v1 (Mapa de Escenarios, Aceptar/Rechazar, Mover). Pendiente: mapa SOLAR SYSTEM (no esta en TPACKWIN/LayoutImage/KPACK/PrologueImage; revisar MapDataEst/PieceEst/bgdata), LayoutData, auditoria global.
- LayoutData v4 instalado (outputs/LayoutData_es_v4.cpk, a07e28dcc87b): 302 etiquetas + 134 bloques multilinea traducidos in-situ. Backup: backup/LayoutData_es_v2_installed.cpk.
- rpw_jstr_es.cpk instalado en CommonData/MtData/EN (tamano distinto al original, offsets i2i verificados). Backup original: backup/rpw_jstr_original.cpk. Si el juego falla al arrancar: restaurar.
- TPACKWIN v4 instalado: filas 15 (Tablón), 215/216 (callouts). Backup v3.
- defaultSS_E instalado (captions de lugar inferiores, ~65 cadenas). Backup: backup/defaultSS_E_original.cpk.
- effwin v1 instalado (d0cf7306f3e4): 20 mapas (SISTEMA SOLAR / MAPA ESPACIAL / MAPA MUNDIAL + planetas, Vía Láctea, Gran Nube de Magallanes, Tierra, Luna) via tools/efm.py, efb.py, efi.py. Backup: backup/effwin_original.cpk.
- STGEST v5 instalado (a01ef42191d7): ~55 rótulos de lugar que seguían en inglés traducidos y 10 rótulos largos acortados (script tools/stcap.py). Backup: backup/STGEST_EN_es_v4_installed.cpk.
- AUDITORIA 19-nov: la biblioteca (MtZkn_Pt/Rt/Nm) solo tiene traducidos los NOMBRES (CHFN/CHNN/PRDC, in-situ). Las fichas largas (campo DSCR, ~390 filas Pt + 273 Rt + 19 Nm, ~700 KB de ingles) siguen en INGLES. Los acc2 con DSCR traducido cambian el tamano de fila (crash conocido) y su mapa dsc2 parte de textos truncados: no usar. Hace falta traduccion nueva que quepa en el mismo numero de bytes por fila (o descubrir por que crashea el cambio de tamano).

## Biblioteca (fichas) — 2026-11-19
- [x] MtZkn_Pt v2 (621/621) instalado; backup/MtZkn_Pt_es_fixedlen_installed.cpk
- [x] MtZkn_Nm instalado
- [x] MtZkn_Rt v1 (263/263 fichas + nombres) instalado (sha 54a05d197f46); tamaño de fila = original. Original en backup/MtZkn_Rt_original.cpk
- Fuentes editables: datos/lib/{pt,rt,nm}_*_es.txt (rt_99/pt_99 = overrides acortados). Reconstruir: python3 tools/lib_build.py Rt outputs/MtZkn_Rt_names_fixed.cpk outputs/X.cpk
- 2026-11-19 (revisión glosario España): Rt v2 + Pt v3 instalados. Nombres con variantes (datos/mtzkn_names_es.json admite listas, elige la que cabe), sin recortes. Mazinger: Puños Fuera / Fuego de Pecho / Huracán Corrosivo / Barón Ashler / Conde Broken; gamilas; Sable de Haz. SysText: 7 nombres EN corregidos. Backups: backup/MtZkn_{Rt_es_v1,Pt_es_v2}_installed.cpk, backup/lib_es_antes_glosario/

## 2026-11-19 — CMN00 es9 (puntuación ¿/¡ y nombres de ataques)
- Instalado outputs/CMN00_CPK_final_es9.cpk (backup: backup/CMN00_installed_antes_es9.cpk). Generado con tools/cmn_rebuild_desde_instalado.py (parte del CPK instalado, no del CSV es6, que está desfasado) usando tools/fix_puntuacion.py y tools/nombres_ataques.py.
- Corregidos ~800 ¿/¡ faltantes o mal abiertos y ~110 nombres de ataque (Puños fuera, Fuego de pecho, Huracán corrosivo, Cañón de Alta Mega, Abanico Daitarn…).
- es10 instalado (etiquetas de estado: Movilidad reducida, Puntería reducida, Blindaje reducido…); es9 queda como backup en outputs/.
- es11 instalado: Funnels→Cañones satélite, Fin Funnels→Aletas satélite, Lambda Driver→Motor Lambda, Full Frontal→Frontal Total, Tri Bomber→Triple Bombardero, Battle Bomber→Bombardero de Combate, Great Mightgaine→Gran Mightgaine (solo CMN00).

## 2026-11-19 (tarde) — nombres aplicados a todo
- Pt v5 / Rt v4 instalados (ataques y armas traducidas en fichas; backups backup/MtZkn_*_antes_ataques.cpk). LT00_EN y B_LT00_EN con tabla tools/glosario_nombres3.py. Nm sin cambios.
- KPACK_P4_LN_EN instalado full_stable3 (sinopsis/títulos/barreras traducidos; parcheo in-situ, misma estructura que stable2). Restaurar con backup/KPACK_P4_LN_EN_original.cpk si el juego no arranca. NO probado en juego (el test 4/5 de es3 fue en una versión anterior).
- SysText fila 2: 0 restos en inglés. LT00/B_LT00: puntuación ¿/¡ correcta.
- Estado de instalación real arriba en esta sección prevalece sobre la tabla antigua.
- KPACK_P4_LN restaurado al original (stable3 sospechoso de no arrancar).
- BISECT: tools/bisect.sh orig|inst NOMBRE...  (nombres: font op nm pt rt systext cmn00 layoutdata rpw defaultss blt kpackcmn tpack stgest effwin prologue ln exe)
- bisect ronda2: instalados solo rpw defaultss kpackcmn ln
- ronda2 OK (abre con rpw defaultss kpackcmn ln). ronda3: + effwin
- ronda3 OK (effwin bien). ronda4: + tpack stgest
- ronda4 OK (tpack stgest bien). ronda5: + prologue
- ronda5 OK (prologue bien). ronda6: + exe parcheado
- ronda6 OK (grupo1 completo abre; el fallo anterior pudo ser intermitente/proceso colgado). ronda7: grupo2 completo (versiones previas a hoy)
- ronda7 FALLA (grupo2). ronda8: instalados solo font op systext layoutdata (+grupo1); nm pt rt cmn00 blt en original
- ronda8 FALLA. ronda9: instalados font op; layoutdata systext original
- ronda9 OK (font op bien). ronda10: + systext
- ronda10 FALLA: SysText names2 culpable. ronda11: SysText_installed_before_names2 (110040 bytes, pre-names2)
- ronda11 OK (SysText pre-names2 abre). Causa del fallo: names2 guardaba la fila 2 SIN cifrar/comprimir (BLTU en claro). Rehecho como SysText_es_names3 (cifrado+CRILAYLA, mismo tamaño). ronda12: names3 + layoutdata nm pt rt cmn00 blt (versiones previas a hoy)
- ronda12 OK. ronda13: instalados Pt v5, Rt v4, CMN00 es11, LT00/B_LT00 nombres3

## 2026-11-19 (noche) — ESTADO INSTALADO VERIFICADO (arranca)
Instalado y arrancando: rpw_jstr, defaultSS_E, KPACK_PC_CMN, KPACK_P4_LN (stable3), effwin, TPACKWIN, STGEST, Prologue v8, SRWV.EXE parcheado, FontInfo, OP, LayoutData, Nm, SysText names3, Pt v5, Rt v4, CMN00 es11, LT00/B_LT00 con nombres3.
Pendiente: KPACK_P4_RG (rompió antes), lega_zkn, DLC no instalados, LayoutImage (crashea), PrologueImage (texto en textura), TPACKWIN fila 13 y "Voom!" fila 208, revisión de sentido en OP/Prologue, línea de Banagher (falta que Luis indique cuál), fecha "noviembre 11" (aparcada), es_batches de LT00 con Tri Bomber (aplicar tabla si se instalan).
Lección: las filas de SysText deben guardarse cifradas+CRILAYLA (cf.cipher), nunca en claro.
- PUNTO ESTABLE guardado: backup/punto_estable_2026-11-19_arranca (19 ficheros, arranca). Volver aqui si algo falla.
- STGEST v6 instalado (b9dfc0a5b928): 458 nombres/ataques traducidos en 75 filas (tabla nombres3+ataques). Para volver: backup/punto_estable_2026-11-19_arranca/Data__STAGE__STGEST_EN.CPK
- CMN00 es12 instalado: 14 líneas con Banagher corregidas (calcos). Anterior: backup/CMN00_installed_es11.cpk

## Texturas (2026-11-19) — inspección, sin cambios instalados
- PrologueImage.cpk (10 filas DDS BGRA 32 bpp): solo fondos del prólogo, SIN texto. Nada que traducir.
- TPACKWIN_EN fila 0-4: logos/créditos © (dejar). Fila 5: números. Fila 13: "ExC. n" (Ex-Count).
- "PRESS START"/"Press any button" NO está en ninguna textura revisada: se dibuja con fuente (texto), no es imagen.
- LayoutImage EN (8 atlas 1024x1024 BGRA, filas 0-7; 4-7 son copias espejadas/volteadas de 0): etiquetas en inglés
  (Main Sub, Combo, Free Fix, Command/Tension/Tag, Critical!, V-UP!, Lv Up!, Weapon Caution!, Key/Help, Pilot/Robot,
  Support Defend/Attack, Second Attack, Training/Patrol/Simulation/Money, Combo Attack, Ammo, EN Cost, Cmb-Atk).
  Editable solo redibujando en el MISMO rectángulo y con el MISMO tamaño de fila (4194432 bytes).
- INSTALADO LayoutImage_EN_es_tex1.cpk (sha c19e23c4121e; original en backup/LayoutImage_original_20261118.cpk): etiquetas Critical!→¡Crítico!, Main Sub→Princ. Sub (x4 tamaños), Lv Up→¡Sube Nv.!, Weapon Caution→¡Cuidado, arma!, Pilot→Piloto; tools/tex_layout.py + tex_cipher_step.py + tex_build_toc.py. Tamaño de fila almacenado cambia (el anterior LayoutImage_es crasheó al elegir personaje): si crashea, restaurar el original.

## Auditoría 2026-11-19 (tarde) — instalado
- Gamilas: rpw_jstr, OP, KPACK_P4_LN_EN (gamillano/a→gamila), Prologue (fragmento inglés "ambled on a last stand…" vaciado). tools/fix_gamila_all.py, fix_gamila_ln.py. Backups en backup/antes_auditoria_20261119/.
- STGEST v7 (sha 12c0aeee433b): 1513 nombres de hablante y 93 rótulos "-Lugar-" traducidos. tools/stgest_audit1.py.
- LayoutData v5 (sha 84d5363f9c67): ~1100 etiquetas más (Acquired Money, SR Points, Enemies List, Spirit Cmds…) in-situ. tools/layout_audit1.py.
- Pendiente: texturas (LayoutImage: Attack/Return Attack/Counter/Ammo/EN Cost/Air Grd…; TPACKWIN ExC.), otros textos (LT00/B_LT00 'Lista de Escuadrone.' desborda).

## effwin v2 (2026-11-19) — instalado
- tools/effw.py, tools/effwin_v2.py: fases (94/96 FASE ALIADA/ENEMIGA), Game Over→DERROTA (98), etiquetas combate (6) y estados (7), Selección de sonido / Mensaje de interrupción (215/218), rótulos Episodio (621..743). Backup: backup/effwin_instalado_antes_v2.cpk. Sin probar en juego.
- Pendiente: HUD de batalla "Return Attack/Attack/Counter" (no está en effwin; buscar en otros CPK de texturas), más etiquetas LayoutImage, TPACKWIN fila 13 "ExC.".
- LayoutImage tex2 instalado (tools/tex_layout2.py + tex_build_toc2.py): Song/MAP/ALL/Assist/SCORE/Boosted/UP/HIT&AWAY/NEW/Unit/COMMAND/SIZE/Key/Help/OPTIONS/Lv/Ace, Support Defend/Attack/Second Attack, START, HIT MISS, Free Fix, Tag/Tension/Command, CHARACTERS-REFERENCE/ROBOTS-SPEC. Backup: backup/LayoutImage_instalado_tex1.cpk. Sin probar en juego.
- KPACK_P4_LN audit2 instalado (tools/ln_audit2.py): ~50 títulos de escenario en inglés, nombres de habilidades (fila 3), 6 resúmenes, 3 descripciones Destroy Mode. Backup: backup/KPACK_P4_LN_instalado_antes_audit2.cpk. SysText "Escuadrones" (backup/SysText_instalado_antes_lista.cpk).
- LayoutData v6 instalado (Save/Suspend/Squad/Force/Slide/Ally). Pendiente: KPACK_P4_RG (mensajes DLC/tienda en inglés, PNG filas 1-3), gráficos de batalla sin localizar.

## 2026-11-19 KPACK_P4_RG_EN es1 (tienda DLC / escenarios extra)
- tools/rg_dlc1.py (diccionario) + tools/rg_audit.py -> outputs/KPACK_P4_RG_EN_es1.cpk (sha cb78da365b22), INSTALADO en Data/KURODATA/EN/KPACK_P4_RG_EN.CPK.
- 305 cadenas traducidas in-situ (fila 0, desde 0x1abb), mismo tamaño, sin NOCABE. Claves KBT_ y tablas binarias intactas.
- Pendiente: prueba de arranque por Luis. Si falla: copiar backup/KPACK_P4_RG_EN_original.cpk sobre el instalado.
- Pendiente: HUD de combate (Counter/Return Attack) aún sin localizar.
- es1 PROBADO: NO ARRANCA. Restaurado original (df740978788b). Hipótesis: row 0 contiene tablas/offsets (longitudes de cadena) o el motor valida el contenido.
- 2026-11-19 tras 'no arranca' (RG original ya restaurado): revertidos LN audit2, LayoutData v6 y SysText Escuadrones a versiones previas. Siguiente sospechoso si falla: LayoutImage tex2, effwin v2.
- 'arranca' tras revertir. Bisect: reinstalados SysText Escuadrones + LayoutData v6 (prueba). Falta LN audit2 (outputs/KPACK_P4_LN_EN_audit2.cpk), RG es1 sospechoso.
- SysText+LayoutData v6 OK (arranca). Instalado LN audit2 (prueba).
- LN audit2 completo NO arranca; revertido. Bisect por filas: A01 (filas 0,1) instalado en prueba; luego B3 (fila 3), C4 (fila 4) en outputs/LN_bis_*.cpk
- A01 OK. Instalado A01+B3 (fila 3) en prueba.
- A01+B3 OK => fila 4 rompe. Instalado A01+B3+C4titulos (prueba); luego C4largos (sinopsis/Destroy).
- Fila 4 de KPACK_P4_LN (títulos de escenarios DLC, 59) rompe el arranque (incluso solo la 1ª mitad). Dejar en inglés junto con KPACK_P4_RG (DLC). Instalado final: LN A01+B3 (outputs/LN_bis_A01B3.cpk), LayoutData v6, SysText lista2. Estado esperado: arranca.
- Búsqueda gráficos 2026-11-19: descartados por contenido: SRVC5 (datos), DB00 (placeholders Now Printing), HIYAMA/default (arte personajes), XP00 (datos), PCI00_PC (texturas modelos piloto), PieceEst001Win (piezas mapa), RG00 (status images). Etiquetas HUD combate ya en effwin filas 6/7 (v2). Pendiente: pedir capturas de lo que aún se vea en inglés.
- Revisión final gráficos: FF00 (iconos 240x280 de unidades/pilotos), FB00 (imágenes de robots + COOR), MapDataEst001Win (datos de mapa): sin texto de UI. No queda más localizable sin captura. Estado instalado final estable: LN A01+B3, LayoutData v6, SysText lista2, LayoutImage tex2, effwin v2; DLC (RG y LN fila 4) en inglés por romper arranque.
- TPACKWIN row 13: ExC.->CE. instalado (outputs/TPACKWIN_EN_exc.cpk; backup/TPACKWIN_EN_instalado_antes_exc.cpk). Pendiente prueba arranque.
- LayoutImage tex3 instalado (outputs/LayoutImage_EN_es_tex3.cpk, backup/LayoutImage_instalado_tex2.cpk): X:Piloto, ¡MÁX!, CE., Cta. Extra, RANGO. Junto con TPACKWIN exc (CE.). Pendiente prueba arranque de ambos.
- CAUSA del fallo de fila 4 LN: cada título DLC tiene campo capacidad u32 LE justo antes (20,16,12...); audit2 lo superaba y pisaba campos. tools/ln_row4_fix.py respeta len<cap. Instalado outputs/KPACK_P4_LN_EN_row4fix.cpk (prueba). Si arranca, aplicar misma lógica a RG (KPACK_P4_RG row0: buscar campos longitud/capacidad).
- LN row4fix OK (arranca). RG bisect: instalado bis_0_150 (primeras 150 cadenas de 305, orden por offset). Estructura RG row0: BLTU, pool cadenas desde 0x30 (claves KBT_ luego mensajes), tabla offsets u32 en 0x4138 (530 entradas), registros 32B en 0x4980.
- RG bis_0_150 OK. Instalado bis_0_228.
- RG bis_0_228 OK. Instalado bis_0_267 (culpable en 267..304 si arranca / 228..266 si no).
- RG bis_0_267 OK. Instalado bis_0_286.
- RG bis_0_286 OK. Instalado bis_0_296 (indices 286..295 añadidos).
- RG bis_0_296 OK. Instalado bis_0_303 (solo faltan HP Regen y None).
- RG FINAL: 303 de 305 cadenas traducidas, arranca (outputs/KPACK_P4_RG_EN_es2_final.cpk). Fallaban solo 'HP Regen' y 'None' (final del pool, junto a la tabla): se dejan en inglés. LN row4fix OK. Estado: DLC traducido. Sin pendientes conocidos salvo HIT/START vertical y lo que Luis vea en pantalla.

## 2026-11-20
- Instalado `BTLC/EN0/CMN00_PC.CPK` = outputs/BTLC_EN0_CMN00_PC_es1.cpk (HUD de batalla; arranque pendiente de confirmar).
- Instalado LayoutImage tex4 (PUNTOS sin ":" y más estrecho, "ExC.", "Ex-Cuenta" pequeño). Backup: backup/LayoutImage_instalado_antes_tex4.cpk.
- TPACKWIN revertido a la versión previa a "CE." (ExC. original) para coherencia con el glosario.
- Pendiente: SP→PE en LayoutData (regiones de 4 bytes), "Day", más gráficos en inglés en batalla.
- Escenarios especiales (DLC) EN INSTALADOS: outputs/dlc_es/*.cpk -> Data/DLCDIRE/EN/ (30 paquetes; originales en backup/dlc_en). Para volver: copiar backup/dlc_en/*.cpk a Data/DLCDIRE/EN/. Pendiente confirmar arranque/escenario.
- DLC glosario posterior aplicado (tools: /tmp/b/_dlcfix.py -> copiado a tools/dlc_glosario_post.py): gamilas (no gamillanos), R/R3 de ataques y unidades, nombres de hablante (Operador, Jefe, Buzo guardián...). Instalado outputs/dlc_es2/* en Data/DLCDIRE/EN.
- LayoutData v7 instalado (SP->PE, Cost.PE, Day->Dia). Backup backup/LayoutData_instalado_antes_SPPE.cpk
- BTLC/EN0/OP_PC.CPK es1 instalado (14 títulos de serie en español; los oficiales en inglés se mantienen). Backup backup/BTLC_EN0_OP_PC_original.cpk. Pendiente confirmar arranque.

- rpw_jstr espiritus (Puntería, Muro, Certero, Brio, Ardor, Pena, Ilusión) instalado. LayoutData v8 (Salvar/Cargar) instalado. Pendiente prueba de arranque.
- EN CURSO: revisión de concordancia género/número en textos con plantillas.
- STGEST conc1 instalado (Galleon). Revisión concordancia: SysText/KPACK/Prologue/rpw_jstr limpios.
- DLC es3 (pilotoo->piloto, el bronca, una capitana) instalado; backup/dlc_es2_instalado
- STGEST gen2 instalado: concordancia de género del protagonista (pid_FHERO fem / MHERO masc) y personajes femeninos en 1ª persona. tools/genero_personajes.py. DLC es3 con Capitana Katsuragi/Hoshino.
- STGEST gen4 instalado: género dirigido al protagonista por ramas MHERO/FHERO (tools/genero_dirigido*.py) + Chitose/Misaki etc. Backups: STGEST_EN_instalado_antes_dirigido/genero
- Mobile Suit fix instalado (traje móvil→Mobile Suit; robot en frases de máquina). Backup backup/pre_mobilesuit. SysText/rpw_jstr títulos 'Traje móvil Gundam…' sin cambiar (sin holgura).
