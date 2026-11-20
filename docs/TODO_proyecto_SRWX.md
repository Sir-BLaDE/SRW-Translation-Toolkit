# TODO — Traducción SRW X (español de España)

Base: Sir-BLaDE/SRW-Translation-Toolkit (mismo motor que SRWV). Variables: `SRW_GAME=X` (clave Blowfish "SRVX Steam Game"),
`SRW_EXE=<ruta a SRWX.EXE>`. Ficheros con sufijo EST002 en vez de EST001.

## Alcance medido (texto en inglés)
| Archivo | Volumen |
|---|---|
| Data/STAGE/STGEST002_EN.CPK (historia, Lua) | 47.992 líneas de diálogo, 2,68 M caracteres, 330 entradas |
| Data/BTLC/EN0/CMN00.CPK (frases de combate) | ~26.400 cadenas, ~1 MB |
| DLC (Data/DLCDIRE/EN, 30 paquetes) | ~12 KB por paquete |
| SysText, LT00_EN, LayoutData, Prologue, rpw_jstr, KPACK_P4_LN/RG | ~240 KB en total |
| MtZkn_Pt/Rt/Nm/KW (biblioteca, ofuscado) | por medir |

## Hecho (2026-11-20)
- [x] Toolkit adaptado: clave por `SRW_GAME`, S-box localizada en cualquier EXE, `font_patch.py` con rutas por entorno y modo X.
- [x] Extracción de diálogos con campo `pid` (pid_XMHERO* = Iori/masc., pid_XFHERO* = protagonista fem.) -> `datos/story_dialogues.jsonl`.
- [x] Fuente: la EN de X tiene é É ü ¡ ¿ « » como cuadrados de relleno y no tiene á í ó ú ñ Á Í Ó Ú Ñ.
      `FontInfo_EN_es1.cpk`: 15 glifos sintetizados reutilizando registros de à è ù â ê ë ï î ô û (mismo tamaño de filas).
- [x] Piloto: escenario 1 (líneas 1-129, entradas 3 y 4) traducido -> `STGEST002_EN_es_piloto.cpk`.
- [x] INSTALADOS piloto + fuente. Originales en `_traduccion_es/backup_original/`.

## Prueba pendiente (Luis)
Partida nueva -> ruta masculina (Iori) -> escenario 1: comprobar arranque, acentos/ñ/¿¡ y textos $kwb traducidos
(Dr. Infierno, Bestias Mecánicas, Cuerpo Express Valiente). Si los acentos fallan: instalar `STGEST002_EN_es_piloto_ascii.cpk`.
Si no arranca: restaurar los dos ficheros desde backup_original.

## Progreso historia (STGEST002)
- 2026-11-20: 5.576 / 47.268 líneas (11,8 %), entradas 2-87: escenarios 1-9 aprox., ambas rutas (Iori/Amari). Instalado.
- Glosario fijado: Guardianes del Orden, Autobrujo, Dogma, Od, forastero (Otherworlder), Tierra del Maná / Tierra de las Bestias,
  hombres bestia, Norma, Para-Mail, Dragones, Piedra Azul (Nadia), Neo Atlántida, la Superficie (Dunbine), Ejército de la Capital,
  Amería, Siglo Reguild, Alianza del Pacto Libre, Gran República de Zogilia, acoplamiento (Valiancer), Gólems Rúnicos, X-Cross ($c).
- Spero llama «amo»/«ama» según la ruta; en líneas compartidas (ruta N) se evita el género.

## Siguiente
- [x] Piloto probado: arranca (2026-11-20).
- [ ] Traducir el resto de STGEST por lotes de 200 líneas (`datos/es_batches/bNNN_inicio_fin.json`, formato de ES_GUIDE).
- [ ] CMN00 (combate), SysText, LT00, LayoutData, Prologue, rpw_jstr, KPACK, DLC, biblioteca.
- [ ] Glosario de series nuevas de X (Wataru, Nadia, Cross Ange, Code Geass, Gurren Lagann, Majestic Prince, G-Reco, Valvrave...).
