# Flujo de traducción SRW X (historia, STGEST002)

Carpeta de trabajo con `orig/`, `stg/` (ficheros Lua descifrados), `datos/story_dialogues.jsonl` y `datos/es_batches/*.json`.

1. `story_extract_x.py` → `stg/` + `story_dialogues.jsonl` (campos `pid` y `route`).
2. `route.py`: ruta de cada línea — `M`/`F` por `Cmd_BranchProtagonist_Begin 0/1`, por tabla `t_NNN` o por entrada; `N` = compartida (texto neutro en género).
3. `show.py A B` muestra solo lo que falta (memoria de traducción + duplicados) y deja en `/tmp/auto.json` lo reaprovechable.
4. Lote `bNNN_A_B.json`; `fill_dups.fill()` copia las variantes repetidas.
5. `rewrap.py` (≤50 caracteres visibles por línea), `check.py` (tokens `$n $F $l $f $kwb/$kwe`), `fixroute.py` (amo/ama según ruta; avisa de líneas neutras).
6. `story_build_x.py SALIDA.cpk` reconstruye y verifica todas las filas.
