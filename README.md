# SRW Translation Toolkit

Herramientas (Python 3) creadas para traducir **Super Robot Wars V (Steam/PC)** al español de España y
reutilizables para otros *Super Robot Wars* de PC que usan el mismo motor (paquetes CRI `.cpk`
cifrados con Blowfish + compresión CRILAYLA, scripts Lua de escenarios, texturas DDS en CPK).

> No contiene ningún recurso del juego. Todas las herramientas leen los ficheros de **tu** copia legal.
> Proyecto de aficionados, sin relación con Bandai Namco ni B.B. Studio.

## Núcleo (empieza por aquí)
| Fichero | Para qué sirve |
|---|---|
| `tools/cpk_util.py` | `load(ruta)` abre un `.cpk`; cada fila tiene `plain(r)` (descifra y descomprime) y `cipher(r,datos)` (cifra de vuelta). |
| `tools/srwv_cpkbuild2.py` | `build_ordered(origen,{id:(cifrado,len)})` reconstruye un CPK con ITOC sustituyendo filas. |
| `tools/tex_build_toc2.py` | Método *append* para CPK con TOC clásico (LayoutImage, TPACKWIN, CMN00_PC, OP_PC, effwin): añade datos nuevos al final y parchea `FileOffset`/`FileSize`. |
| `tools/blowfish_tables.py` | Lee las tablas Blowfish estándar del propio `SRWV.EXE` (**edita la constante `EXE`** a tu ruta). |
| `tools/release_build.py`, `release/instalar_parche.py` | Generan/aplican parches binarios (zstd `--patch-from`) para distribuir sin redistribuir ficheros del juego. |

## Flujo de trabajo típico
1. `cpk_util.load()` → volcar texto/Lua/imágenes de cada CPK.
2. Traducir (glosario en `docs/` y `tools/nombres_ataques.py`, `glosario_nombres3.py`).
3. Reconstruir con `build_ordered` (CPK con ITOC) o con el método append (CPK con TOC).
4. **Verificar siempre**: `ex == len(plain(row))` para todas las filas y hacer *round-trip*.
5. Instalar con copia de seguridad; probar **partida nueva** (es donde aparecen los crashes).

## Lecciones aprendidas (resumen; detalle en `docs/`)
- Los CPK de datos con índices internos (`MtZkn_*`, `rpw_jstr`, `LayoutData`…) **no toleran cambiar el tamaño de las filas**: editar *in situ* (acortar y rellenar con NUL / espacios, nunca alargar).
- Los diálogos de escenario son Lua (`STGEST_*.CPK`, `DLC*.cpk`): bloques `[[Hablante\r\n「texto」]]`; las ramas `MHERO_scenario_flag` separan protagonista masculino/femenino (útil para concordancia de género).
- Texturas: DDS 32 bpp BGRA con cabecera de 128 bytes; los CPK de imágenes se reconstruyen con el método *append*.
- Nunca des por buena una prueba si no se ha creado una partida nueva y se ha llegado a combate.
- Cada instalación nueva: copia previa a `backup/`, comparar con `cmp` tras copiar.

## Requisitos
Python 3.10+, Pillow y NumPy para las herramientas de texturas; `zstd` (CLI) para `release_build.py`.

## Estado
Extraído de un proyecto real (≈730 scripts). Muchos son de un solo uso y están sin pulir; `tools/sesion_scripts/`
contiene los scripts de la última sesión de trabajo tal cual. Pull requests y adaptaciones a otros SRW bienvenidos.

Licencia del código: MIT.
