"""
merge.py - Integra un lote de traducciones en lineas_batalla.csv.
Formato del lote: una linea por entrada, "id|traduccion".
Avisa si no coinciden los \\n entre el ingles y la traduccion.
Uso: python merge.py lote.txt
"""
import sys, csv, os

CSV = r"C:\Dev\Default Project\srwv\datos\lineas_batalla.csv"

def main():
    if len(sys.argv) < 2:
        print("uso: python merge.py lote.txt")
        sys.exit(1)
    lote = sys.argv[1]
    # leer el lote
    updates = {}
    with open(lote, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if "|" not in line:
                print("linea sin |, ignorada:", line)
                continue
            idi, tr = line.split("|", 1)
            updates[int(idi)] = tr

    # leer el CSV
    rows = []
    with open(CSV, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        header = next(r)
        rows = list(r)

    # indexar por id
    by_id = {int(row[0]): row for row in rows}
    ok = 0
    warn = 0
    missing = 0
    for idi, tr in updates.items():
        if idi not in by_id:
            print("id no encontrado:", idi)
            missing += 1
            continue
        en = by_id[idi][1]
        # comprobar \n
        if en.count("\n") != tr.count("\n"):
            print(f"AVISO id {idi}: ingles tiene {en.count(chr(10))} \\n, "
                  f"traduccion tiene {tr.count(chr(10))} \\n")
            warn += 1
        by_id[idi][2] = tr
        ok += 1

    # escribir el CSV
    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for row in rows:
            w.writerow(row)

    print(f"integradas: {ok}, avisos de \\n: {warn}, no encontradas: {missing}")

if __name__ == "__main__":
    main()
